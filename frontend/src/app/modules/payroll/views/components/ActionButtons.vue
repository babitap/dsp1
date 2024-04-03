<template>
  <div class="action-buttons">    
    <va-button medium>Delete Rule(s)</va-button>
    <va-button medium>Add a New Rule</va-button>  
    <va-button medium @click="handleFinalButtonClick">Final Review & Sign off</va-button>
   
  </div>
</template>

<script>
import Vue from 'vue';
import VModal from 'vue-js-modal/dist/ssr.index';

Vue.use(VModal);

export default {
  methods: {
     handleFinalButtonClick() {
      this.$emit('button-clicked');
    },
    clickFinalReview() { 
      const alertMessage = 'Uploaded document is reviewed & Sign off!';
      alert(alertMessage);          
    }
  }
};
</script>

<style scoped>
.action-buttons {
  display: flex;
  justify-content: center;
}
</style>
