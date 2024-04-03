import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export const powerbiExportState = {
  namespaced: true,
  state: {
    availableExports:[],
    documentContent: null,
    availableFilters: []
  },
  mutations: {

  setAvailableExports(state, data) {
      state.availableExports = data;
  },    

  clearDocumentContent(state){
    state.documentContent = null; 
    },   

  setDocumentContent(state, data){
      state.documentContent = data; 
  }, 

  setAvailableFilters(state, data){
    state.availableFilters = data; 
    }  

    
  },
  actions: {
    
    async getExportList(context, entityId){
        const url = `/powerbiExport/ExportPageList/${entityId}`
        //loadingService.showLoading(true);
  
        return await httpClient.get(url)
          .then(res => {
              const data = res.data;
              let result = {'success': true, 'errorMessage': ''};
  
              if(!data.message){
                  context.commit('setAvailableExports', data.export_list)

              }
              else{
                  result.success = false;
                  result.errorMessage = 'Error retrieve export list';
              }
              return result;
          })
          .catch(err => {       
              console.log(err);    
              throw err; // reject
          })
          .finally(() =>{
              //loadingService.showLoading(false);
          })
      },    

      async clearDocumentContent(context, params){
        context.commit('clearDocumentContent')
      },

      async getDocumentContent(context, params){
        const url = `/powerbiExport/ExportContent/${params.entityId}/${params.exportId}?subject=${params.subject}&year=${params.year}&year_level=${params.year_level}&class_name=${params.class_name}&term=${params.term}`

        return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(data){
                context.commit('setDocumentContent', data)
            }
            else{
                result.success = false;
                result.errorMessage = 'Error retrieve document content';
            }
            return result;
        })
        .catch(err => {       
            console.log(err);    
            throw err; // reject
        })
        .finally(() =>{
            //loadingService.showLoading(false);
        })
    },
//entityId, export_id
    async getFilters(context, params){

        console.log('go to filter')

        const url = `powerbiExport/GetFilters/${params.entityId}/${params.export_id}`
        //loadingService.showLoading(true);

        return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};
            
            if(data){
                // console.log("user here");
                // console.log(data);

                context.commit('setAvailableFilters', data)
            }
            else{
                result.success = false;
                result.errorMessage = 'Error retrieve export list';
            }
            return result;
        })
        .catch(err => {       
            console.log(err);    
            throw err; // reject
        })
        .finally(() =>{
            //loadingService.showLoading(false);
        })
    },  

      
    
  },

}
