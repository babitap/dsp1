<template>
    <div class="report">
        <!-- <div class="option">
        <label>Availble Report:</label>
        <multiselect
          :value="selected"
          :options="availableReports"
          :multiple="false"
          :allow-empty="false"
          :showLabels="false"
          trackBy="id"
          label="name"
          :searchable="false"
          @input="valueSelected"
          placeholder="Select report">
        </multiselect>
      </div> -->
      <div class="flex xs12 " align="right"> 
      <div class="container">
        <va-button  @click="clickDownloadAsPDF()">Email as PDF</va-button>
      </div>
        </div> 
        <div class="container">
        <div id="container" class="container"></div>
        </div>
    </div>
</template>

<script>
import * as pbi from 'powerbi-client';
import Multiselect from "vue-multiselect";
import { mapState, mapActions } from "vuex";
import { httpClient } from '@/app/shared/services/http-client'

export default {
    name: "report",
    components: {
        Multiselect
    },
    props:{
        codename:String
    },
  data() {
    return {
        config: {
          type: 'report',
          tokenType:  pbi.models.TokenType.Embed,
          accessToken: '',
          embedUrl: '',
          permissions: pbi.models.Permissions.All,
          settings: {
              filterPaneEnabled: false,
              navContentPaneEnabled: true
          }
      },
      selected: null,
      powerbi: null,
      reportContainer: null,
      selectEntityId: 0
    }
  },
  computed: {
      ...mapState({
      availableReports: state => state.report.availableReports ? state.report.availableReports : [],
      reportInfo: state => state.report.reportInfo
    }),
  },
  watch:{
      reportInfo(newValue){
          if(newValue){
              this.config.accessToken = newValue.accessToken;
              this.config.embedUrl = newValue.embedUrl

              var report = this.powerbi.embed(this.reportContainer, this.config);

              if(report){
                report.on("loaded", function () {
                console.log("Report load successful")
              });
                report.off("loaded");


                report.off("rendered");

                report.on("error", function () {
                    report.off("error");
                });

              }
          }
      },
      codename(newValue, oldValue){
          if(newValue && newValue !== oldValue){
              if(this.codename) this.getReportEmbedInfo({codename:this.codename})
          }
      }
  },
  methods: {
      ...mapActions({
            getReportEmbedInfo: "report/getReportEmbedInfo",
            exportReportAndEmail: "report/exportReportAndEmail",
        }),
    valueSelected(value){
        this.selected = value;
        const {workspace_id, report_id} = value;
        //this.getReportEmbedInfo({workspaceId:workspace_id, reportId:report_id})
    }, 
    clickDownloadAsPDF(){

      var r = window.confirm('Do you want the report be exported as a pdf document and send to your email box?');
      if(r==true){
        console.log('proceed with the action of export to file and email')
        this.exportReportAndEmail({codename:this.codename})
      }
      else{
        console.log('cancel the action of export to file and email')
      } 
      
    }
  },
  mounted (){
      
      this.powerbi = new pbi.service.Service(pbi.factories.hpmFactory, pbi.factories.wpmpFactory, pbi.factories.routerFactory);
      this.reportContainer = document.getElementById('container');
      if(this.codename){
          this.getReportEmbedInfo({codename:this.codename})
      }
  }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss" scoped>
.report {
  width: 100%;
  height: 100%;
}

.container {
  width: 100%;
  height: 100%;
}

.option {
  margin-bottom: 1rem;

  & .multiselect {
    margin-top: 10px;
  }
}

</style>

