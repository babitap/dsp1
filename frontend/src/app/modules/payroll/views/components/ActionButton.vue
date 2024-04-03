<template>
  <div>
    <va-button large @click="handleButtonClick">{{ label }}  </va-button>
  </div>
</template>

<script>
export default {
  props: {
    label: String,
  },
   methods: {
    handleButtonClick() {     
      this.$emit('button-clicked');
    },
    handleFinalButtonClick() {    
      this.$emit('button-clicked');
    },
  },
};
</script>

<style scoped>
.action-button {
  margin-top: 5rem;
}
</style>
