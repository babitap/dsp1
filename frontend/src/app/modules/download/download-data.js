import { httpClient } from '@/app/shared/services/http-client'
import { loadingService } from '@/app/shared/services/loading-service'

export const downloadState = {
  namespaced: true,
  state: {
    availableDownloads:[],
    availableDocuments:[],
    documentContent: null,
  },
  mutations: {

    clearAvailableDocuments(state){
        state.availableDocuments = []
    },
    setAvailableDownloads(state, data) {
        state.availableDownloads = data;
    }, 

    setAvailableDocuments(state, data) {
        state.availableDocuments = data;
    },   
    
    clearDocumentContent(state){
        state.documentContent = null; 
    },    
    setDocumentContent(state, data){
        state.documentContent = data; 
    }  
    
  },
  actions: {
    
    async getDownloadList(context, entityId){
        const url = `/download/downloadList/${entityId}`
        //loadingService.showLoading(true);
  
        return await httpClient.get(url)
          .then(res => {
              const data = res.data;
              let result = {'success': true, 'errorMessage': ''};
  
              if(!data.message){
                  context.commit('setAvailableDownloads', data.download_list)
              }
              else{
                  result.success = false;
                  result.errorMessage = 'Error retrieve download list';
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

      async clearDocumentList(context, params){
        context.commit('clearAvailableDocuments')
      },

    async getDocumentList(context, params){

      const url = `/download/documentList/${params.entityId}/${params.downloadId}`
      //loadingService.showLoading(true);

      return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(!data.message){
                context.commit('setAvailableDocuments', data.document_list)
            }
            else{
                result.success = false;
                result.errorMessage = 'Error retrieve document list';
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
        const url = `/download/documentContent/${params.entityId}/${params.downloadId}?document_path=${params.documentPath}`

        return await httpClient.get(url)
        .then(res => {
            const data = res.data;
            let result = {'success': true, 'errorMessage': ''};

            if(!data.message){
                context.commit('setDocumentContent', data.document_content)
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
    }
    
  },

}
