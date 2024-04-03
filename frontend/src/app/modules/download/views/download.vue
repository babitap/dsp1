<template>
<div class="download">
    <div class="row row-equal outer-container">
        
        <div class="flex xs12 dropdown-container">
            <label >{{download_name}}</label>
            <div class="flex xs12 row" >
                <div class="flex xs9 ">
                    
                    <multiselect
                        :value="selectedOption"
                        :options="availableDocuments"
                        :custom-label="onlyName"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectOption"
                    ></multiselect>

                </div>

                <div class="flex xs3 ">
                    
                    <va-button class="btn" @click="click_download">Download</va-button>   
                </div>
                
            </div>
        </div>
    </div> 

    <div  class="flex xs12 dropdown-container">
      
    </div>    

</div>    
</template>

<script>

import { mapState, mapActions } from "vuex";
import { loadingService } from '@/app/shared/services/loading-service'
//import DocumentPreview from '../../shared/DocumentPreview'
import Multiselect from "vue-multiselect";
import { httpClient } from '@/app/shared/services/http-client'
import axios from "axios"
//import pdf from 'vue-pdf'

export default {
    name: "download",
    components:{
        Multiselect,
        //DocumentPreview,
        //pdf,
    },
    props: { 
        download_id: String, 
        download_name: String,
    }, 
    data () {
        return {
            selectedOption: {} , 
            downloadName : '',
  
        }
    },
    computed:{
        ...mapState({
            selectedEntity:     state => state.user.selectedEntity,           
            availableDocuments: state => state.download.availableDocuments, 
            documentContent:    state => state.download.documentContent,
        }), 

    },
    watch:{

        download_id(newValue){
            this.clearDocumentList();
            if( newValue && this.selectedEntity.id  ){                
                this.getDocumentList( { entityId : this.selectedEntity.id , 
                                        downloadId: newValue
                                    } );
            }
            
        },
        selectedEntity(newValue){
            console.log("document::watch::selectedEntity")
            if( newValue && newValue.id ){                
                this.getDocumentList( { entityId : newValue.id, 
                                        downloadId: this.download_id
                                    } );
            }
            
        },
        availableDocuments(newValue){
            if( newValue.length > 0 ){
                this.selectedOption = newValue[0];
            }
            else{
                this.selectedOption = {}; 
            }
        },
        documentContent(newValue){
            if(newValue!==null){

                var byteArraryBuffer = this.base64ToArrayBuffer(this.documentContent);  
                this.saveByteArray2Browser(this.selectedOption.file_name, byteArraryBuffer);
            }
        }
    },
    async created(){
        console.log("document::created")
        if( this.selectedEntity.id && this.download_id){
            this.getDocumentList( { entityId : this.selectedEntity.id, 
                                    downloadId: this.download_id
                                } );
        }
    },

    async created1(){
        // 1, send the GET request to get all available blob urls
        const url = '/download/'+ '48004' +'/'+this.reportName
        
        await httpClient.get(url)
            .then(res => {
                const data = res.data;
                //debugger;
                var list_availableFiles = []
                // print the dictionary 
                for( var document_name in data.blob_url ){
                    var document_sas_url = data.blob_url[document_name]
                    //console.log(document_name+'  :  ' + document_sas_url)
                    list_availableFiles.push( document_name ) 
                }

                // 1, get all available blob urls
                this.availableBlobUrls = data.blob_url

                // 2, get the list of available files
                this.availableFiles = list_availableFiles

                // 3, default selected file
                this.selectedFile = this.availableFiles[ this.availableFiles.length-1]

                // 4, default selected file url 
                this.selectedFileUrl = this.availableBlobUrls[this.selectedFile]
            })
            .catch(err => {       
                console.log(err);    
                throw err; // reject
            })

    },
    methods: {
        ...mapActions(
            {
                clearDocumentList:      "download/clearDocumentList",
                getDocumentList:        "download/getDocumentList",
                
                clearDocumentContent:   "download/clearDocumentContent",
                getDocumentContent:     "download/getDocumentContent",
                
            }
        ),
        onlyName( item ){
            return item.file_name
        },

        click_download(e){
            this.clearDocumentContent();
            this.getDocumentContent({ entityId : this.selectedEntity.id, 
                                    downloadId: this.download_id,
                                    documentPath: this.selectedOption.file_path_name,
                                }); 

        },
        base64ToArrayBuffer(base64) {
            var binaryString = window.atob(base64);
            var binaryLen = binaryString.length;
            var bytes = new Uint8Array(binaryLen);
            for (var i = 0; i < binaryLen; i++) {
            var ascii = binaryString.charCodeAt(i);
            bytes[i] = ascii;
            }
            return bytes;
        },

        getMIMEType(ext){
            const MIME_Dict = {
                ".doc":"application/msword", 
                ".dot":"application/msword", 
                ".docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                ".dotx":"application/vnd.openxmlformats-officedocument.wordprocessingml.template", 
                ".docm":"application/vnd.ms-word.document.macroEnabled.12", 
                ".dotm":"application/vnd.ms-word.template.macroEnabled.12", 
                ".xls":"application/vnd.ms-excel", 
                ".xlt":"application/vnd.ms-excel", 
                ".xla":"application/vnd.ms-excel", 
                ".xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                ".xltx":"application/vnd.openxmlformats-officedocument.spreadsheetml.template", 
                ".xlsm":"application/vnd.ms-excel.sheet.macroEnabled.12", 
                ".xltm":"application/vnd.ms-excel.template.macroEnabled.12", 
                ".xlam":"application/vnd.ms-excel.addin.macroEnabled.12", 
                ".xlsb":"application/vnd.ms-excel.sheet.binary.macroEnabled.12", 
                ".ppt":"application/vnd.ms-powerpoint", 
                ".pot":"application/vnd.ms-powerpoint", 
                ".pps":"application/vnd.ms-powerpoint", 
                ".ppa":"application/vnd.ms-powerpoint", 
                ".pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation", 
                ".potx":"application/vnd.openxmlformats-officedocument.presentationml.template", 
                ".ppsx":"application/vnd.openxmlformats-officedocument.presentationml.slideshow", 
                ".ppam":"application/vnd.ms-powerpoint.addin.macroEnabled.12", 
                ".pptm":"application/vnd.ms-powerpoint.presentation.macroEnabled.12", 
                ".potm":"application/vnd.ms-powerpoint.template.macroEnabled.12", 
                ".ppsm":"application/vnd.ms-powerpoint.slideshow.macroEnabled.12", 
                ".mdb":"application/vnd.ms-access", 
            }
            if(ext in MIME_Dict){
                return MIME_Dict[ext]
            }
            else{
                return 'text/plain'
            }

        },
        saveByteArray2Browser(reportName, byte) {
            var ext = '.' + reportName.split('.').pop(); 
            var MIME_type = this.getMIMEType( ext );

            var blob = new Blob([byte], {type: MIME_type});
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            var fileName = reportName;
            //this.pdffileName = link.href;
            link.download = fileName;
            link.click();
        },

        selectOption( option ){
            this.selectedOption = option; 
        },

        
    }
}
</script>
<style scoped>
.dropdown-container {
  display: flex;
  flex-wrap: wrap;
  border: none;
  border-radius: 0.375rem;
  background: white;
}

.dropdown {
  margin: 5px;
}

.outer-container {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.row.row-equal.outer-container + .row.row-equal.outer-container {
  margin-top: 15px;
}

.group-title {
  float: left;
  font-weight: 600;
  padding: 0 !important;
}
</style>
