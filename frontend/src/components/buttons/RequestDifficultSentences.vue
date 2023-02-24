<template>
  <v-btn
    color="secondary"
    class="button"
    id="btn"
    rounded
    @click="highlightText"
    >Show difficult sentences</v-btn
  >
</template>

<script>
import process from "process";
const _axios = require("axios").default;
const axiosRetry = require("axios-retry");
const axios = _axios.create();

export default {
  computed: {
    // eslint-disable-next-line prettier/prettier
    regex: () => /(<([^>]+)>)/gi,
  },
  data: () => {
    return {
      originalTextReadOnly: "",
    };
  },
  methods: {
    highlightSentence(selectedText) {
      let indexOfText = this.text.replace(this.regex, "").indexOf(selectedText);
      if (indexOfText >= 0)
        this.editor.formatText(
          indexOfText,
          selectedText.length,
          "background",
          "RGB(255, 0, 0)"
        );
    },
    async highlightText() {
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
          process.env.VUE_APP_READABILITY_COMPLICATED_SENTENCES,
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          text: this.text.replace(this.regex, ""),
          options: {
            metric_name: this.selectedDS,
          },
        },
      };

      await axios
        .request(config)
        .then((response) => {
          const difficultSentences = response.data.difficult_sentences;
          window.console.log(difficultSentences);
          this.$emit("saveDiffSentencesModel", difficultSentences);
          for (let sentence of difficultSentences)
            this.highlightSentence(sentence);
        })
        .catch((error) => {
          console.log(error);
          alert(error.response.detail);
        });
      this.$loading(false);
    },
  },
  props: ["text", "editor", "selectedDS"],
};
</script>
