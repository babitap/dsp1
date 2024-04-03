<template>
  <va-card class="container" style="overflow-x: auto; overflow-y: visible;">
    <p class="display-5" style="color: #5f6e78;">{{title}}</p>

    <div class="body">
      <va-input
        v-model="rule_description"
        label="New Rule Description"
        rows="2"
        outlined
        type="textarea"
      />
      <va-input
        v-model="rule_memo"
        label="Rule Comment"
        rows="2"
        outlined
        type="textarea"
      ></va-input>
      <va-button class="btn alignleft" @click="cancel">CANCEL</va-button>
      <va-button
        class="btn alignright"
        @click="save"
      >SAVE</va-button>
    </div>
  </va-card>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "EditRuleModal",
  props: {
    title: String,
    propsCategory: "",
    propsComment: "",
    propsNumber: ""
  },
  data() {
    return {
      rule_description: "",
      rule_memo: "",
      rule_number: 99,

    };
  },
  mounted() {
    this.rule_description = this.propsCategory
    this.rule_memo = this.propsComment
    this.rule_number = this.propsNumber
  },
  methods: {
    cancel() {
      this.$emit("close");
    },
    save() {
      this.$emit("editdata", {
        'number': this.rule_number,
        'description' : this.rule_description,
        'memo' : this.rule_memo
      })
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
.container {
  box-shadow: none !important;
}

.body {
  margin-top: 1rem;
}

.alignright {
  float: right;
}

.alignleft {
  float: left;
}
</style>