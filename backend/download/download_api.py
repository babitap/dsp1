from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *

import json,os,urllib,itertools
import urllib.parse

from django.conf import settings
from azure.storage.blob import BlobClient
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.storage.blob import BlobServiceClient 
import base64
from access_control.dbviews import helpers

class downloadList(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, *args, **kwargs):
        # this get request is to provide all download links in the left navigation bar

        try:
            # get download list for the login user and the selected entity
            user_id = self.user.id
            download_list = DownloadPermission.objects.get_download_list( user_id, entity_id )

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

        return JsonResponse(data={'download_list':download_list})



class documentList(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, download_id, *args, **kwargs):
        # this GET request is to provide all documents list in the selection bar
        
        # step 1, check the permissiona and get the mapped folder for this download
        try:
            user_id = self.user.id 
            mapped_folder = DownloadPermission.objects.get_mapped_folder( user_id, entity_id, download_id )
        except Exception as e:
            return JsonResponse(data={'message':repr(e)})

        if len(mapped_folder) == 0: 
            return JsonResponse(data={'Error':'No permission'})
        else: 
            mapped_folder = mapped_folder[0]

        # step 2, get the container information 
        connection_string = settings.STORAGE_CONNECTION_STRING
        blob_service_client =  BlobServiceClient.from_connection_string(connection_string)
        my_container = blob_service_client.get_container_client(settings.DOWNLOAD_CONTAINER_NAME)
        
        # step 3, list all the available files, desc sorted by date 
        my_blobs = my_container.list_blobs(name_starts_with=mapped_folder+'/')
        list_of_files = []
        for blob in my_blobs:
            # print("\t" + blob.name + ' ' + blob.blob_type + ' ' + str(blob.creation_time)  )
            list_of_files.append( {
                'file_path_name': blob.name, 
                'file_name'     : blob.name.split('/',1)[1], # get the file name 
                'creation_time' : blob.creation_time
            } )
        list_of_files_sorted = sorted( list_of_files, key=lambda i: i['creation_time'], reverse=True )
        
        # step 4, return the result 
        return JsonResponse(data={'document_list':list_of_files_sorted})


class documentContent(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, download_id ,*args, **kwargs):

        # get the content of the document
        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        
        if helpers.checkRequiredParams(params,['document_path']):
            return JsonResponse(data={'Error':'Error with inputs'})

        download_document_path = params['document_path'][0]

        # step 1, check the permissiona and get the mapped folder for this download
        try:
            user_id = self.user.id 
            mapped_folder = DownloadPermission.objects.get_mapped_folder( user_id, entity_id, download_id )
        except Exception as e:
            return JsonResponse(data={'message':repr(e)})

        if len(mapped_folder) == 0: 
            return JsonResponse(data={'Error':'No permission'})
        else: 
            mapped_folder = mapped_folder[0]

        # step 2, get the container information 
        connection_string = settings.STORAGE_CONNECTION_STRING
        blob_service_client =  BlobServiceClient.from_connection_string(connection_string)
        my_container = blob_service_client.get_container_client(settings.DOWNLOAD_CONTAINER_NAME)
        
        # step 3, check the folder is in 
        
        blob = my_container.get_blob_client(download_document_path)

        raw_bytes = blob.download_blob().readall()  
        b64encoded_bytes = base64.b64encode(raw_bytes)
        decoded_bytes = b64encoded_bytes.decode('ascii') 
        return JsonResponse(data={'document_content':decoded_bytes})             
        #else: 
        #    return JsonResponse(data={'Error':'Could not find blob with the given name'})

"""
class downloadDocument(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):
        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()
    
    def get(self, request, *args, **kwargs):
        # this get request is to download the document hosted in blob storage
        # step 1, Get the paramter download_id  

        # step 2, Check whether user has the permission which required by the download_id

        # step 3, If allowed, proceed with fetching content from blob storage
        connection_string = settings.STORAGE_CONNECTION_STRING
        blob_service_client =  BlobServiceClient.from_connection_string(connection_string)
        my_container = blob_service_client.get_container_client(settings.DOWNLOAD_CONTAINER_NAME)

        my_blobs = my_container.list_blobs()
        blob_url_dict = {}
        blob_url_dict_list={}
        for blob in my_blobs:
            print("blob.name")    
            bytes = my_container.get_blob_client(blob).download_blob().readall()      
            encoded = base64.b64encode(bytes)
            blob_url_dict[blob.name] = encoded.decode('ascii')       
        return JsonResponse(data={'blob_url':blob_url_dict})
"""


