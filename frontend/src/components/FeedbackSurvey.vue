<template>
  <popup-survey :style="{ width: '35%' }" :survey="survey" :isExpanded="true" />
</template>
<script>
import Vue from "vue";
import { Model, StylesManager } from "survey-vue";
import "survey-vue/defaultV2.min.css";

import { json } from "@/js/survey.js";

StylesManager.applyTheme("defaultV2");

export default Vue.component("survey-component", {
  name: "survey-component",
  data() {
    const survey = new Model(json);
    survey.onComplete.add(this.alertResults);

    return {
      survey: survey,
    };
  },
  methods: {
    alertResults(sender) {
      const results = JSON.stringify(sender.data);
      this.$emit("feedback-result", results);
    },
  },
});
</script>
