<template>
  <div class="lawyer-tabs">   
    <div class="flex xs12">
      <va-tabs v-model="selectedTab">
        <va-tab v-for="(tab, index) in tabNames" :key="index">
          {{ tab }}
        </va-tab>
      </va-tabs>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabNames: Array,
    value: Number,
  },
  computed: {
    selectedTab: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit('input', value);
      },
    },
  },
};
</script>

<style scoped>
.lawyer-tabs {
  overflow-x: auto;
  background-color: #eeeeee;
  color: black;
}
</style>