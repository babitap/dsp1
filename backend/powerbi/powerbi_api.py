from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *
from .helpers  import *

import json,os,urllib,itertools
import urllib.parse
from django.conf import settings

class reportEmbedInfo(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):

        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get powerBI embed information for given codename
        """

        #Extract params from query
        codename = kwargs.get('codename', '')

        ##Ensure required params exist

        if codename == '' :
            return JsonResponse(data={'message':'codename is required'})

        try:
            #Check user permission for the report
            report = Report.objects.get(codename=codename)

            if report is not None:
                if self.user.has_perm(perm=report.permission.codename, entityId=report.entity_id):
                    # step 1, get all user groups which the login user has been assigned to; 
                    #       an special usergroup 'SUPERUSER' will be appended if the login user is a super user. 
                    all_user_groups = self.user.get_all_user_group(report.entity_id)
                    role_list = []
                    for user_group in all_user_groups:
                        role_list.append(user_group['name'])
                    if self.user.is_superuser:
                        role_list.append('SUPERUSER')

                    # step 2, get access token
                    accesstoken = getaccesstoken()

                    embedinfo = getembedparam(accesstoken, report.workspace_id, report.report_id, report.enable_RLS, 
                                                self.user.username, role_list )
                    errorMsg = embedinfo.get('errorMsg', '')
                else:
                    errorMsg = "No permission to view report"
            else:
                errorMsg = 'Report is not found'

            if errorMsg == '':
                return JsonResponse(embedinfo)
            else:
                return JsonResponse(data={'message': errorMsg})

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class reportList(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get list of report information for current request user
        """

        #Extract params from query
        entityId = kwargs.get('entityId', '')

        ##Ensure required params exist

        if entityId == '':
            return JsonResponse(data={'message': 'EntityId is required'})

        try:

            output = {
                'reports': {}
            }
            # Make sure current user has access to the entity
            entities = self.user.get_entities()

            # Check permission for given user
            permissions = self.user.get_all_permissions(entityId=entityId)
            permissionIds = list(map(lambda x: x['id'], permissions))

            matchedEntity = next((e for e in entities if e['id'] == entityId), None)

            if matchedEntity is not None:
                isActiveFiler = Q(is_active=True)
                entityFilter = Q(entity=entityId)
                permissionFilter = Q(permission__in=permissionIds)

                #Find report that satisfy the filter
                reports = list(Report.objects.filter(isActiveFiler & entityFilter & permissionFilter)
                    .select_related('category').values('category__name', 'name', 'codename'))
                
                for report in reports:
                    reportName = report['category__name']
                    if output['reports'].get(reportName) is None:
                        output['reports'][reportName] = []
                    output['reports'][reportName].append(report)

            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message': "User does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message': repr(e)})


class reportExportAndEmail(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: export powerbi report as pdf and email it out
        """
        
        #Extract params from query
        #Extract params from query
        codename = kwargs.get('codename', '')

        ##Ensure required params exist

        if codename == '' :
            return JsonResponse(data={'message':'codename is required'})

        try:
            #Check user permission for the report
            report = Report.objects.get(codename=codename)
            errorMsg = ''
            if report is not None:
                if self.user.has_perm(perm=report.permission.codename, entityId=report.entity_id):
                    # yes, the user has the access to view the report
                    # send the request to logic app to trigger the export-to-file
                    PBI_EXPORT_TO_FILE_HTTP_ENDPOINT = settings.PBI_EXPORT_TO_FILE_HTTP_ENDPOINT
                    PBI_EXPORT_TO_FILE_WITH_RLS_HTTP_ENDPOINT = settings.PBI_EXPORT_TO_FILE_WITH_RLS_HTTP_ENDPOINT
                    PBI_EXPORT_TO_FILE_HTTP_APIKEY   = settings.PBI_EXPORT_TO_FILE_HTTP_APIKEY

                    body = {
                        "workspaceId":report.workspace_id,
                        "reportId":report.report_id,
                        "reportName":report.name,
                        "emailAddress":self.user.username,  # username is the email address, which might be changed in the future
                        "APIKey": PBI_EXPORT_TO_FILE_HTTP_APIKEY                        
                    }

                    if report.enable_RLS: 
                        # if enable_RLS is set 
                        endpoint = PBI_EXPORT_TO_FILE_WITH_RLS_HTTP_ENDPOINT
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
                        body['dataset1'] = dataset           


                    else: 
                        endpoint = PBI_EXPORT_TO_FILE_HTTP_ENDPOINT

                    try:
                        print('body=')
                        print(body)                        
                        apiresponse = requests.post(endpoint, json=body )

                    except Exception as ex:
                        raise Exception('Error while sending request to EXPORT-TO-FILE endpoint\n')

                else:
                    errorMsg = "No permission to view report"
            else:
                errorMsg = 'Report is not found'

            if errorMsg == '':
                return JsonResponse(data={'message':''})
            else:
                return JsonResponse(data={'message': errorMsg})

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

                        