from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *

import requests
import json
import os
import urllib
import itertools
import urllib.parse

from django.conf import settings
from azure.storage.blob import BlobClient
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.storage.blob import BlobServiceClient

import base64
from access_control.dbviews import helpers


class fileparse(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        # self.user = User.objects.get(username = 'user1@email.com')
        return self.validate()

    # def upload(params):
    #     return

    def post(self, request, *args, **kwargs):
        # print('Uploading the file to Azure Function')
        # print(request)
        try:
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()
            _, file_extension = os.path.splitext(uploaded_file.name)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in the request body'}, status=400)

        azure_function_url = "https://fna-payrollai-dev.azurewebsites.net/api/process_upload_azfunc?code=BnNI11Gp3AYTdpE3gwkRktMctMUBctVwDhndOYqLMFaMAzFug2Rg1w=="
        # print(azure_function_url)
        file_content_base64 = base64.b64encode(file_content).decode('utf-8')

        headers = {'Content-Type': 'application/json'}
        payload = {
            'fileContents': file_content_base64,
            'fileExtension': file_extension
        }

        try:
            # Make a POST request to the Azure Function
            # print('make a post request now')
            response = requests.post(
                azure_function_url, headers=headers, data=json.dumps(payload), timeout=1000)

            # Check the response status
            if response.status_code == 200:
                # If successful, return the response from the Azure Function
                return JsonResponse(response.json(), safe=False)
            else:
                mock_json_data = [
                    {
                        "Object": "Full Time Day Ordinary Hours",
                        "Category": "Shift",
                        "Rule": "For full time day employees, the span of weekdays is from 07:00 am to 7:00 pm. Maximum ordinary hours per day is 7.6 and per week is 38."
                    },
                    {
                        "Object": "Full Time Shift Ordinary Hours",
                        "Category": "Shift",
                        "Rule": "For full time shift employees, the span is outside shift. Maximum ordinary hours per day is 7.6 and per week is 38."
                    },
                    {
                        "Object": "Part Time Ordinary Hours",
                        "Category": "Shift",
                        "Rule": "For part time employees, the span is outside normal part time hours. Maximum ordinary hours is according to part time schedule and maximum per week is 38."
                    },
                    {
                        "Object": "Casual Day Ordinary Hours",
                        "Category": "Shift",
                        "Rule": "For casual day employees, the span of weekdays is from 7 am to 7 pm. Maximum ordinary hours per day is 10 and per week is 38."
                    },
                    {
                        "Object": "Casual Shift Ordinary Hours",
                        "Category": "Shift",
                        "Rule": "For casual shift employees, the span is outside shift. Maximum ordinary hours per day is 10 and per week is 38."
                    },
                    {
                        "Object": "Leave Loading Calculation Logic",
                        "Category": "Leave",
                        "Rule": "Leave loading is calculated as the maximum of 17.5% of base rate or the relevant penalty (night-shift). The base rate is the minimum hourly rate."
                    },
                    {
                        "Object": "Super Annuation on Annual Leave",
                        "Category": "Super",
                        "Rule": "Super annuation is paid on annual leave for all employment types."
                    },
                    {
                        "Object": "Super Annuation on Public Holiday Ordinary Hours",
                        "Category": "Super",
                        "Rule": "Super annuation is paid on public holiday ordinary hours for all employment types."
                    },
                    {
                        "Object": "Super Annuation on Public Holiday Overtime Hours",
                        "Category": "Super",
                        "Rule": "Super annuation is not paid on public holiday overtime hours for all employment types."
                    },
                    {
                        "Object": "Afternoon Shift Loading and Timing",
                        "Category": "Shift",
                        "Rule": "For all employment types, the afternoon shift loading is 15%. The shift must start after a specified time."
                    },
                    {
                        "Object": "Night Shift Loading and Timing",
                        "Category": "Shift",
                        "Rule": "For all employment types, the night shift loading is 30%. The shift must start after a specified time and finish before a specified time."
                    },
                    {
                        "Object": "Permanent Night Shift Loading and Timing",
                        "Category": "Shift",
                        "Rule": "For all employment types, the permanent night shift loading is 30%. The shift must start after a specified time."
                    },
                    {
                        "Object": "Day Work Shift Loading and Timing",
                        "Category": "Shift",
                        "Rule": "For all employment types, the day work shift loading is 0%. The shift must start after 7:00 AM."
                    },
                    {
                        "Object": "Full and Part Time Saturday Overtime",
                        "Category": "Overtime",
                        "Rule": "For full and part time employees, Saturday overtime is paid at 200%."
                    },
                    {
                        "Object": "Casual Saturday Overtime",
                        "Category": "Overtime",
                        "Rule": "For casual employees, Saturday overtime is paid at 225%."
                    },
                    {
                        "Object": "Full and Part Time Sunday Overtime",
                        "Category": "Overtime",
                        "Rule": "For full and part time employees, Sunday overtime is paid at 200%."
                    },
                    {
                        "Object": "Casual Sunday Overtime",
                        "Category": "Overtime",
                        "Rule": "For casual employees, Sunday overtime is paid at 225%."
                    },
                    {
                        "Object": "Full and Part Time Public Holiday Overtime",
                        "Category": "Overtime",
                        "Rule": "For full and part time employees, public holiday overtime is paid at 200%."
                    },
                    {
                        "Object": "Casual Public Holiday Overtime",
                        "Category": "Overtime",
                        "Rule": "For casual employees, public holiday overtime is paid at 225%."
                    },
                    {
                        "Object": "All Employment Types Christmas and Good Friday Overtime",
                        "Category": "Overtime",
                        "Rule": "On Christmas or Good Friday, overtime for all employees is paid at 250%."
                    },
                    {
                        "Object": "Full Time Laundry Allowance",
                        "Category": "Allowance",
                        "Rule": "For full time employees, the laundry allowance is $3.55 per week."
                    },
                    {
                        "Object": "Part Time and Casual Laundry Allowance",
                        "Category": "Allowance",
                        "Rule": "For part time and casual employees, the laundry allowance is $0.71 per day."
                    },
                    {
                        "Object": "All Employment Types Meal Allowance",
                        "Category": "Allowance",
                        "Rule": "For all employees, the meal allowance is $16.91 if overtime is greater than 1.5 hours and an additional $13.54 if overtime is greater than 4 hours."
                    },
                    {
                        "Object": "First Aid Allowance",
                        "Category": "Allowance",
                        "Rule": "For all employees with first aid duties, the first aid allowance is $14.11 weekly."
                    }
                ]
                return JsonResponse(mock_json_data, safe=False)
                # return JsonResponse({'error': f'Azure Function request failed with status code {response.status_code}'}, status=500)
        except requests.RequestException as e:

            mock_json_data = [
                {
                    "Object": "Full Time Day Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For full time day employees, the span of weekdays is from 07:00 am to 7:00 pm. Maximum ordinary hours per day is 7.6 and per week is 38."
                },
                {
                    "Object": "Full Time Shift Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For full time shift employees, the span is outside shift. Maximum ordinary hours per day is 7.6 and per week is 38."
                },
                {
                    "Object": "Part Time Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For part time employees, the span is outside normal part time hours. Maximum ordinary hours is according to part time schedule and maximum per week is 38."
                },
                {
                    "Object": "Casual Day Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For casual day employees, the span of weekdays is from 7 am to 7 pm. Maximum ordinary hours per day is 10 and per week is 38."
                },
                {
                    "Object": "Casual Shift Ordinary Hours",
                    "Category": "Shift",
                    "Rule": "For casual shift employees, the span is outside shift. Maximum ordinary hours per day is 10 and per week is 38."
                },
                {
                    "Object": "Leave Loading Calculation Logic",
                    "Category": "Leave",
                    "Rule": "Leave loading is calculated as the maximum of 17.5% of base rate or the relevant penalty (night-shift). The base rate is the minimum hourly rate."
                },
                {
                    "Object": "Super Annuation on Annual Leave",
                    "Category": "Super",
                    "Rule": "Super annuation is paid on annual leave for all employment types."
                },
                {
                    "Object": "Super Annuation on Public Holiday Ordinary Hours",
                    "Category": "Super",
                    "Rule": "Super annuation is paid on public holiday ordinary hours for all employment types."
                },
                {
                    "Object": "Super Annuation on Public Holiday Overtime Hours",
                    "Category": "Super",
                    "Rule": "Super annuation is not paid on public holiday overtime hours for all employment types."
                },
                {
                    "Object": "Afternoon Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the afternoon shift loading is 15%. The shift must start after a specified time."
                },
                {
                    "Object": "Night Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the night shift loading is 30%. The shift must start after a specified time and finish before a specified time."
                },
                {
                    "Object": "Permanent Night Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the permanent night shift loading is 30%. The shift must start after a specified time."
                },
                {
                    "Object": "Day Work Shift Loading and Timing",
                    "Category": "Shift",
                    "Rule": "For all employment types, the day work shift loading is 0%. The shift must start after 7:00 AM."
                },
                {
                    "Object": "Full and Part Time Saturday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, Saturday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Saturday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, Saturday overtime is paid at 225%."
                },
                {
                    "Object": "Full and Part Time Sunday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, Sunday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Sunday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, Sunday overtime is paid at 225%."
                },
                {
                    "Object": "Full and Part Time Public Holiday Overtime",
                    "Category": "Overtime",
                    "Rule": "For full and part time employees, public holiday overtime is paid at 200%."
                },
                {
                    "Object": "Casual Public Holiday Overtime",
                    "Category": "Overtime",
                    "Rule": "For casual employees, public holiday overtime is paid at 225%."
                },
                {
                    "Object": "All Employment Types Christmas and Good Friday Overtime",
                    "Category": "Overtime",
                    "Rule": "On Christmas or Good Friday, overtime for all employees is paid at 250%."
                },
                {
                    "Object": "Full Time Laundry Allowance",
                    "Category": "Allowance",
                    "Rule": "For full time employees, the laundry allowance is $3.55 per week."
                },
                {
                    "Object": "Part Time and Casual Laundry Allowance",
                    "Category": "Allowance",
                    "Rule": "For part time and casual employees, the laundry allowance is $0.71 per day."
                },
                {
                    "Object": "All Employment Types Meal Allowance",
                    "Category": "Allowance",
                    "Rule": "For all employees, the meal allowance is $16.91 if overtime is greater than 1.5 hours and an additional $13.54 if overtime is greater than 4 hours."
                },
                {
                    "Object": "First Aid Allowance",
                    "Category": "Allowance",
                    "Rule": "For all employees with first aid duties, the first aid allowance is $14.11 weekly."
                }
            ]
            return JsonResponse(mock_json_data, safe=False)
            # Handle request exception
            # return JsonResponse({'error': f'Request to Azure Function failed1: {str(e)}'}, status=500)
