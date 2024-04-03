<template>
<div class="download">
    <div class="row row-equal outer-container">
        
        <div class="flex xs12 dropdown-container">
            <label >{{export_name}}</label>
            
            <div class="flex xs12 row" >
                <label><b>Ensure all fields are populated before proceeding.</b> Request will be sent once confirmation window pops up.</label>
            </div>

            <div class="flex xs12 row" >
                <div class="flex xs2 ">
                    <label>Year:</label>
                    <multiselect
                        :value="selectedYear"
                        :options="yearOptions"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectYear"
                    ></multiselect>
                </div>

                <div class="flex xs2 ">
                    <label>Term:</label>
                    <multiselect
                        :value="selectedTerm"
                        :options="termOptions"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectTerm"
                    ></multiselect>
                </div>

                <div class="flex xs2 ">
                    <label>Year Level:</label>
                    <multiselect
                        :value="selectedYearLevel"
                        :options="yearLevelOptions"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectYearLevel"
                    ></multiselect>
                </div>

                <div class="flex xs3 ">
                    <label>Subject:</label>
                    <multiselect
                        :value="selectedSubject"
                        :options="subjectOptions"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectSubject"
                    ></multiselect>
                </div>
                <div class="flex xs3 ">
                    <label>Class:</label>
                    <multiselect
                        :value="selectedClass"
                        :options="classOptions"
                        :multiple="false"
                        :taggable="true"
                        :allow-empty="false"
                        :showLabels="false"
                        
                        @input="selectClass"
                    ></multiselect>
                </div>

                 <div class="flex xs3 ">
                    <va-button  @click="clickDownloadAsZIP()">Email as ZIP</va-button>
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
    name: "powerbi-export",
    components:{
        Multiselect,
        //DocumentPreview,
        //pdf,
    },
    props: { 
        export_id: String, 
        export_name: String,
    }, 
    data () {
        return {
            selectedOption: '', 
            filters: {},
            
            selectedYear: '',
            yearOptions: [],
            
            selectedTerm: '',
            termOptions: [],            
            
            selectedYearLevel: '',
            yearLevelOptions: [],   

            selectedSubject: '',
            subjectOptions: [],            
            
            selectedClass: '',
            classOptions: [],         
        }
    },
    computed:{
        ...mapState({
            selectedEntity:     state => state.user.selectedEntity,
            documentContent:    state => state.powerbiExport.documentContent,
            availableFilters: state => state.powerbiExport.availableFilters,
        }), 

    },
    watch:{
        export_id(newValue){
            console.log("export::watch::export_id")
            if( newValue && this.selectedEntity.id  ){
                this.getFilters( { entityId : this.selectedEntity.id, 
                 export_id : newValue});
            }
            
        },
        selectedEntity(newValue){
            console.log("export::watch::selectedEntity")
            if( newValue && newValue.id ){
                this.getFilters( { entityId : newValue.id, 
                 export_id : this.export_id});
            }
            
        },
        
        documentContent(newValue){
            if(newValue !== null){
                var error_response = this.documentContent.message;

                if(error_response == ''){
                    var sent = window.confirm('Zip folder generation in progress. An email will be sent once completed. Please allow 5 to 10 minutes.');     
                    }

                else{
                    var didnotsend = window.confirm(error_response);
                }   
                
            }
        },

            availableFilters(newValue){
                if( newValue.length > 0 ){
                    // this.selectedOption = newValue[0];

                    this.getYearOptions();
                    if(this.yearOptions.length > 0){
                        this.selectedYear = this.yearOptions[0];
                        
                    }

                    this.getTermOptions();
                    if(this.termOptions.length > 0){
                        this.selectedTerm = this.termOptions[0];
                    }

                    else{
                        this.selectedTerm = ''
                    } 

                    this.getYearLevelOptions();
                    if(this.yearLevelOptions.length > 0){
                        this.selectedYearLevel = this.yearLevelOptions[0];
                    }

                    else{
                        this.selectedYearLevel = ''
                    } 

                    this.getSubjectOptions();
                    if(this.subjectOptions.length > 0){
                        this.selectedSubject = this.subjectOptions[0];
                    }

                    else{
                        this.selectedSubject = ''
                    } 

                    this.getClassOptions();
                    if(this.subjectOptions.length > 0){
                        this.selectedClass = this.classOptions[0];
                    }
                    
                    else{
                        this.selectedClass = ''
                    } 
                
                }
                else{
                    this.selectedOption = {}; 
                }
        },
  
        selectedYear(newValue){
            if(this.selectedYear){
                this.getTermOptions();
                if(this.termOptions.length > 0){
                    this.selectedTerm = this.termOptions[0];
                }
                else{
                    this.selectedTerm = ''
                } 
            }

        },
        selectedTerm(newValue){
            if(this.selectedYear && this.selectedTerm){
                this.getYearLevelOptions();
                if(this.yearLevelOptions.length > 0){
                    this.selectedYearLevel = this.yearLevelOptions[0];
                }
                else{
                    this.selectedYearLevel = ''
                } 
            }

        },

        selectedYearLevel(newValue){
            if(this.selectedYear && this.selectedTerm && this.selectedTerm){
                this.getSubjectOptions();
                console.log("selectedSubject")
                if(this.subjectOptions.length > 0){
                    this.selectedSubject = this.subjectOptions[0];
                }
                else{
                    this.selectedSubject = ''
                } 
            }

        },

        selectedSubject(newValue){
            if(this.selectedYear && this.selectedTerm && this.selectedYearLevel && this.selectedSubject){
                this.getClassOptions();
                console.log("selectedClass")
                if(this.classOptions.length > 0){
                    this.selectedClass = this.classOptions[0];
                }
                else{
                    this.selectedClass = ''
                } 
            }

        },
       
    },
    async created(){
        //debugger;
            console.log("export::created", this.selectedEntity.id, this.export_id);           
        
        if( this.selectedEntity.id && this.export_id){
           // console.log("Created------------------------");           
            this.getFilters( {entityId : this.selectedEntity.id, export_id : this.export_id});

        }
    },

    
    methods: {
        ...mapActions(
            {
                // clearDocumentList:      "powerbiExport/clearDocumentList",
                // getDocumentList:        "powerbiExport/getDocumentList",
                
                clearDocumentContent:   "powerbiExport/clearDocumentContent",
                getDocumentContent:     "powerbiExport/getDocumentContent",
                getFilters:             "powerbiExport/getFilters"
                
            }
        ),

        // async getFilters(entityId, export_id){

        //     console.log('go to filter')
        //     console.log(entityId)

        //     const url = `powerbiExport/GetFilters/${entityId}/${export_id}`
        //     //loadingService.showLoading(true);
    
        //     return await httpClient.get(url)
        //     .then(res => {
        //         const data = res.data;
        //         let result = {'success': true, 'errorMessage': ''};
                
        //         if(data){
        //             console.log("user here");
        //             console.log(data);

        //             this.availableDocuments = data;
        //         }
        //         else{
        //             result.success = false;
        //             result.errorMessage = 'Error retrieve export list';
        //         }
        //         return result;
        //     })
        //     .catch(err => {       
        //         console.log(err);    
        //         throw err; // reject
        //     })
        //     .finally(() =>{
        //         //loadingService.showLoading(false);
        //     })
        // },  

        onlyName( item ){
            return item.file_name
        },

        clickDownloadAsZIP(e){
            var selectedOptions = [...new Set([this.selectedSubject,this.selectedYear,this.selectedTerm,this.selectedYearLevel,this.selectedClass])];

            
            if(selectedOptions.includes('')==true){
                var cantproceed = window.confirm('Unable to proceed. Please ensure that all fields are populated.');
            }
            
            if(selectedOptions.includes('')==false){
                console.log('proceed with the action of export to file and email')
                this.clearDocumentContent();
                this.getDocumentContent({ entityId : this.selectedEntity.id, 
                        exportId: this.export_id,
                        subject: this.selectedSubject,
                        year: this.selectedYear,
                        term: this.selectedTerm,
                        year_level: this.selectedYearLevel,
                        class_name: this.selectedClass});
            }
            else{
                console.log('Cancel the action of export to file and email')
            } 
        },

        selectYear(option){
            this.selectedYear = option;
        },

        getYearOptions(){
            var items = this.availableFilters.map(item => {return item.year})

            this.yearOptions = [...new Set(items)].sort().reverse();
        },

        selectTerm(option){
            this.selectedTerm = option;
        },

        getTermOptions(){
            if ( this.selectedYear ){
                console.log('getTermOptions')
                // console.log(this.selectedYear)
                var selectedYearVar = this.selectedYear
                var availableTerms = this.availableFilters.filter(function (e) {
                        return e.year == selectedYearVar;
                    });
                var items = availableTerms.map(item => {return item.term})
                // console.log(items)
                this.termOptions = [...new Set(items)].sort().reverse();
                this.termOptions.unshift('');
            }
            else{
                this.termOptions = []
            }
            

        },

        selectYearLevel(option){
            this.selectedYearLevel = option;
        },

        getYearLevelOptions(){
            if ( this.selectedYear && this.selectedTerm ){
                console.log('getYearLevelOptions')
                console.log(this.selectedTerm)
                var selectedYearVar = this.selectedYear
                var selectedTermVar = this.selectedTerm
                var availableYearLevels = this.availableFilters.filter(function (e) {
                        return e.year == selectedYearVar && e.term == selectedTermVar;
                    });
                var items = availableYearLevels.map(item => {return item.yearLevel})
                console.log(items)
                this.yearLevelOptions = [...new Set(items)].sort();
                this.yearLevelOptions.unshift('');
            }
            else{
                this.yearLevelOptions = []
            }
            

        },

        selectSubject(option){
            this.selectedSubject = option;
        },

        getSubjectOptions(){
            if ( this.selectedYear && this.selectedTerm  && this.selectedYearLevel ){
                console.log('getSubjectOptions')
                // console.log(this.selectedTerm)
                var selectedYearVar = this.selectedYear;
                var selectedTermVar = this.selectedTerm;
                var selectedYearLevelVar = this.selectedYearLevel;
                var availableSubjects = this.availableFilters.filter(function (e) {
                        return e.year == selectedYearVar && e.term == selectedTermVar && e.yearLevel == selectedYearLevelVar;
                    });
                var items = availableSubjects.map(item => {return item.subjectDesc})
                // console.log(items)
                this.subjectOptions = [...new Set(items)].sort().reverse();
                this.subjectOptions.unshift('');
            }
            else{
                this.subjectOptions = []
            }
        
        },

        selectClass(option){
            this.selectedClass = option;
        },

        getClassOptions(){
            if ( this.selectedYear && this.selectedTerm  && this.selectedYearLevel   && this.selectedSubject){
                console.log('getClassOptions')
                console.log(this.selectedSubject)
                var selectedYearVar = this.selectedYear;
                var selectedTermVar = this.selectedTerm;
                var selectedYearLevelVar = this.selectedYearLevel;
                var selectedSubjectVar = this.selectedSubject;
                var availableClasses = this.availableFilters.filter(function (e) {
                        return e.year == selectedYearVar && e.term == selectedTermVar && e.yearLevel == selectedYearLevelVar && e.subjectDesc == selectedSubjectVar;
                    });
                var items = availableClasses.map(item => {return item.class})
                // console.log(items)
                this.classOptions = [...new Set(items)].sort().reverse();
                this.classOptions.unshift('');
            }
            else{
                this.classOptions = []
            }
            

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
