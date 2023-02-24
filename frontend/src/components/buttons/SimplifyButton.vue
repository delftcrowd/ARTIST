<template>
  <v-btn color="secondary" class="button" @click="simplify" rounded>
    Simplify
  </v-btn>
</template>

<script>
import process from "process";
const _axios = require("axios").default;
const axiosRetry = require("axios-retry");
const axios = _axios.create();

// eslint-disable-next-line prettier/prettier
var regex = /(<([^>]+)>)/gi;

export default {
  methods: {
    async simplify() {
      if (!this.text.replace(regex, "").trim()) {
        alert("There is no text to simplify.");
        return;
      }
      this.$loading(true);
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
          process.env.VUE_APP_SIMPLIFICATION_SIMPLIFY,
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          text: this.text.replace(regex, ""),
          options: {
            model_name: this.selectedMLM,
            model_options: {
              max_length_sum: parseFloat(this.max_length_sum),
              min_length_sum: parseFloat(this.min_length_sum),
              max_length_original: parseFloat(this.max_length_original),
            },
          },
        },
      };

      await axios
        .request(config)
        .then((response) =>
          this.$emit(
            "simplified",
            "<p>" + response.data.simplified_text + "</p>"
          )
        )
        .catch((error) => {
          console.log(error);
          alert(error.response.data.detail);
        });
      this.$loading(false);
    },
  },
  props: {
    text: String,
    selectedMLM: String,
    max_length_original: Number,
    max_length_sum: Number,
    min_length_sum: Number,
  },
};
</script>
