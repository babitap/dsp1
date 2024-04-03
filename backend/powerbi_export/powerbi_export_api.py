from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *
from access_control.dbviews import helpers
from powerbi.helpers  import *

import json,os,urllib,itertools
import urllib.parse

from django.db import connections
from django.conf import settings
import pandas as pd
import base64
import time
from datetime import datetime

class ExportPageList(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, *args, **kwargs):
        # this get request is to provide all export links in the left navigation bar

        try:
            # get export list for the login user and the selected entity
            user_id = self.user.id
            export_list = ExportPermission.objects.get_export_pages_list( user_id, entity_id )

        except Exception as e: 
            print('error: ', repr(e))
            return JsonResponse(data={'message':'Internal Errors'})

        return JsonResponse(data={'export_list':export_list})


# This class is designed only for exporting student report from Powerbi, 
# Return: collection of filters options that users (teacher) can selects based on their roles: year, year level, subject, class, term
class GetFilters(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, export_id, *args, **kwargs):
        # this get request returns all filters options for a specific login users

        try:
            user_name = self.user.username
            user_id = self.user.id
            
            # get export list for the login user and the selected entity
            export_list = ExportPermission.objects.get_export_pages_list( user_id, entity_id )

            if len(export_list) > 0:
                sql = '''
                    select   year, term, [Year Level] as yearLevel, TRIM([Subject Desc]) as subjectDesc, trim(class) as class
                    from 
                    [Findex].[sp2_view_studresults_perterm_noJS] t  join [findex].teacher_roles r on t.[Teacher Code] = r.[Teacher Code]
                    where [Year Level] in (7,8,9) and [school Email] = %s and year >= YEAR(GETDATE()) -1
                    group by year, term, [Year Level], [Subject Desc], class
                '''

                df = pd.read_sql(sql=sql, con = connections['present'], params=(user_name,))
            else:
                return JsonResponse(data={'message': "Error while retrieving fields for user"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

        return JsonResponse(data =  df.to_dict('records'), safe = False)


class ExportContent(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, export_id, *args, **kwargs):
        """
        Purpose: export many powerbi pdf reports as zip and email it out
        """
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print('Selected filters:')
        print(params)

        ## check all filters are populated
        if helpers.checkRequiredParams(params,['year_level','subject','class_name','year','term']):
            return JsonResponse(data={'message':'Error with inputs'})

        ## Ensure export_id exists
        if export_id == '' :
            return JsonResponse(data={'message':'Export ID is required'})

        try:
            #Check user permission for the report
            report = ExportPermission.objects.get(id=export_id)
            errorMsg = ''
            if report is not None:
                if self.user.has_perm(perm=report.permission_codename, entityId=report.entity_id):
                    # yes, the user has the access to view the report
                    # send the request to logic app to trigger the export-to-zip
                    PBI_EXPORT_TO_ZIP_WITH_RLS_HTTP_ENDPOINT = settings.PBI_EXPORT_TO_ZIP_WITH_RLS_HTTP_ENDPOINT
                    PBI_EXPORT_TO_FILE_HTTP_APIKEY   = settings.PBI_EXPORT_TO_FILE_HTTP_APIKEY

                    # relevant_student_list = self.get_relevant_students(username = self.user.username, params=params)

                    username = self.user.username
                    year_level = params['year_level'][0]
                    subject = params['subject'][0]
                    class_name = params['class_name'][0]
                    year = params['year'][0]
                    term = params['term'][0]

                    values_for_query = (year_level,year,term,subject,class_name,username)

                    try:
                        # # get all relevant students for the login user and the selected entity according to filters
                        studentcodes_query = '''
                                                SELECT DISTINCT [Student Code], t.[Teacher Code], [Year Level], class, Year, Term, [Subject Desc] 
                                                from [Findex].[sp2_view_studresults_perterm_noJS] t  join [findex].teacher_roles r on t.[Teacher Code] = r.[Teacher Code]
                                                where [Year Level] = %s and [Year] = %s and [Term] = %s and 
                                                    [Subject Desc] = %s and [class] = %s and [school Email] = %s
                                            '''

                        student_codes = pd.read_sql(studentcodes_query, connections['present'], params = values_for_query)
                        student_codes_list = list(student_codes['Student Code'].unique())
                        student_codes_list = [x.strip(' ') for x in student_codes_list]
                        print("--- " + str(len(student_codes_list)) + " students to be downloaded. ---")

                        # ensure student list is not empty
                        if len(student_codes_list) > 0:
                            # generate report dictionary
                            report_list = []
                            term_year = year + " Term " + term

                            filter_str1 = "student_resuls_summarised_fixed/Student_Code eq '"
                            filter_str2 = "' and term_for_filter/Term_Year eq '" + term_year + "'"

                            for x,student_x in enumerate(student_codes_list):
                                report_dict = {"filter":filter_str1 + student_x + filter_str2,
                                                "uniquename": student_x + '_' + year + "_Term " + term}
                                report_list.append(report_dict)
                        else:
                            report_list = None
                    except:
                        report_list = None


                    if isinstance(report_list, list):
                        body = {
                            "reports": report_list,
                            "workspaceId":report.workspace_id,
                            "reportId":report.report_id,
                            "reportName":report.report_name,
                            "emailAddress":self.user.username,  # username is the email address, which might be changed in the future
                            "APIKey": PBI_EXPORT_TO_FILE_HTTP_APIKEY                        
                        }

                        # RLS is expected - may need to change in future
                        endpoint = PBI_EXPORT_TO_ZIP_WITH_RLS_HTTP_ENDPOINT
                        body['userName'] = self.user.username

                        # roles 
                        all_user_groups = self.user.get_all_user_group(report.entity_id)
                        role_list = []
                        for user_group in all_user_groups:
                            role_list.append(user_group['name'])
                        if self.user.is_superuser:
                            role_list.append('SUPERUSER')
                        i=1
                        for role in role_list:
                            body["role"+str(i)]=role 
                            i = i + 1

                        # dateset
                        #  need send 
                        accesstoken = getaccesstoken()
                        dataset = getembeddataset(accesstoken, report.workspace_id, report.report_id)    
                        body['dataset'] = dataset          

                        try:                   
                            apiresponse = requests.post(endpoint, json=body )
                            status_code = apiresponse.status_code
                            print(apiresponse.headers)
                            print(status_code)

                            if (status_code != 202) & (status_code != 200):
                                if status_code == 429:
                                    errorMsg = 'Error: Too many requests. Please try again in an hour.\n'

                                else:
                                    errorMsg = 'Error: Error while sending request to EXPORT-TO-ZIP endpoint.\n'                                

                        except Exception as ex:
                            raise Exception('Error: Error while sending request to EXPORT-TO-ZIP endpoint.\n')

                    else: errorMsg = "Error: Error while retrieving students."
                else:
                    errorMsg = "Error: No permission to view report."
            else:
                errorMsg = 'Error: Report not found.'

            if errorMsg == '':
                return JsonResponse(data={'message':''})
            else:
                return JsonResponse(data={'message': errorMsg})

        except User.DoesNotExist:
            return JsonResponse(data={'message':"Error: User does not exist."})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})