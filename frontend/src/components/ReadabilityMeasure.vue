<template>
  <div class="d-flex">
    <span class="d-flex message-counter">{{
      "Characters: " + text.replace(regex, "").length
    }}</span>
    <span v-if="!noText" class="d-flex readability-measure-score"
      >Readability measure: {{ readabilityMeasure }}</span
    >
    <v-tooltip top v-if="!noText" max-width="400" color="black">
      <template v-slot:activator="{ on, attrs }">
        <v-icon size="20" class="ml-5" v-bind="attrs" v-on="on"
          >mdi-information</v-icon
        >
      </template>
      <span
        ><div>
          <b>{{ this.metricName }}</b>
        </div>
        <div>{{ this.metricDescription }}</div></span
      >
    </v-tooltip>
  </div>
</template>

<script>
import * as util from "@/js/util.js";
import process from "process";
const _axios = require("axios").default;
const axiosRetry = require("axios-retry");
const axios = _axios.create();

export default {
  // eslint-disable-next-line prettier/prettier
  computed: { console: () => window.console, regex: () => /(<([^>]+)>)/gi },
  data: () => {
    return {
      readabilityMeasure: 0,
      metricName: "",
      metricDescription: "",
      noText: false,
    };
  },
  methods: {
    async readabilityAPI() {
      if (!this.text.replace(this.regex, "").trim()) {
        this.noText = true;
        return;
      }
      this.noText = false;
      const retryDelay = (retryNumber = 0) => {
        const seconds = Math.pow(2, retryNumber) * 1000;
        const randomMs = 1000 * Math.random();
        return seconds + randomMs;
      };

      axiosRetry(axios, {
        retries: 2,
        retryDelay,
        // retry on Network Error & 5xx responses
        retryCondition: axiosRetry.isRetryableError,
      });

      let config = {
        url:
          process.env.VUE_APP_BASE_API_URL +
          process.env.VUE_APP_READABILITY_MEASURE,
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          text: this.text.replace(this.regex, ""),
          options: {
            metric_name: this.selectedRM,
          },
        },
      };

      await axios
        .request(config)
        .then((response) => {
          console.log(response);
          (this.readabilityMeasure = response.data.min_age) &&
            (this.metricName = response.data.metric_name) &&
            (this.metricDescription = response.data.description);
        })
        .catch((error) => {
          console.log(error);
          alert(error.response.data.detail);
        });
    },
  },
  mounted() {
    this.readabilityAPI();
  },
  watch: {
    text: util.debounce(function () {
      this.readabilityAPI();
    }, 500),
    selectedRM: function (newMetric) {
      this.metricName = newMetric;
      this.readabilityAPI();
    },
  },
  props: ["text", "selectedRM"],
};
</script>

<style lang="scss" src="@/assets/readability.scss"></style>
