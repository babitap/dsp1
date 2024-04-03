<template>
  <div class="header">
    <h1>{{ title }}</h1>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
  },
};
</script>

<style scoped>
.header {
  flex: 1;
  color: black;
  padding-left: 1rem;
  padding-top: 1rem;
}
</style>
