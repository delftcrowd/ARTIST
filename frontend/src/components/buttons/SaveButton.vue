<template>
  <v-btn color="secondary" class="button" @click="save" rounded>
    Store to database
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
    async save() {
      this.$confirm({
        message:
          "Your work is about to be stored in the database. This could be used for research purposes. " +
          "Would you like to continue?",
        button: {
          no: "Cancel",
          yes: "Confirm",
        },
        callback: async (confirm) => {
          if (confirm) {
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
                process.env.VUE_APP_SAVE_TO_DATABASE,
              method: "post",
              headers: {
                "Content-Type": "application/json",
              },
              data: {
                unsimplified_text: this.unsimplifiedText.replace(regex, ""),
                simplified_by_model: this.simplified_by_model,
                simplified_by_user: this.simplified_by_user.replace(regex, ""),
                rating_simplification: this.simplificationRating | 0,
                comments: this.feedbackComments,
                model_info: {
                  model_name: this.selectedMLM,
                  options: [
                    {
                      option_name: "max_length_sum",
                      option_type: "float",
                      option_value: this.max_length_sum.toString(),
                    },
                    {
                      option_name: "min_length_sum",
                      option_type: "float",
                      option_value: this.min_length_sum.toString(),
                    },
                    {
                      option_name: "max_length_original",
                      option_type: "float",
                      option_value: this.max_length_original.toString(),
                    },
                  ],
                },
                difficult_sentences_original: this.difficultSentencesModel,
                difficult_sentences_revised: this.complicatedSentencesUser,
                rating_sentences: this.difficultSentencesRating | 0,
                metric_options: {
                  metric_name: this.selectedDS,
                },
              },
            };

            await axios
              .request(config)
              .then((response) => {
                console.log(this.isSaved);
                this.$emit("input", true);
                console.log(this.isSaved);

                console.log(response);
              })
              .catch((error) => {
                console.log(error);
                alert(error.response.data);
              });

            this.$loading(false);
          }
        },
      });
    },
  },
  props: {
    unsimplifiedText: String,
    simplified_by_model: String,
    simplified_by_user: String,
    selectedMLM: String,
    selectedDS: String,
    max_length_original: Number,
    max_length_sum: Number,
    min_length_sum: Number,
    simplificationRating: Number,
    feedbackComments: String,
    difficultSentencesRating: Number,
    complicatedSentencesUser: Array,
    difficultSentencesModel: Array,
  },
};
</script>
