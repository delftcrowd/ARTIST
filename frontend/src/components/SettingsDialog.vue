<template>
  <div>
    <v-btn
      class="me-5"
      style="background-color: #7bb9ae"
      @click="getOptions"
      @options="dialog = true"
    >
      Settings
    </v-btn>

    <v-dialog
      v-model="dialog"
      width="70vw"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-items>
          <v-toolbar dark color="#7bb9ae">
            <v-btn icon dark @click="dialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>Settings</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
              <v-btn dark text @click="saveOptions"> Save </v-btn>
            </v-toolbar-items>
          </v-toolbar>

          <v-list three-line>
            <h4 class="ml-3">
              Choose the readability measures to be used for analysing the
              difficulty of the texts.
            </h4>

            <v-list-item-group v-model="selectedRM" single>
              <template>
                <v-list-item
                  v-for="(item, i) in readabilityMeasuresOptions"
                  :key="`item.metric_name-${i}`"
                  :value="item.metric_name"
                  active-class="text--accent-4"
                >
                  <template v-slot:default="{ active }">
                    <v-list-item-content>
                      <v-list-item-title
                        v-text="item.metric_name"
                      ></v-list-item-title>
                      <v-list-item-subtitle>
                        {{ item.description }}
                      </v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                      <v-checkbox
                        :input-value="active"
                        color="#7bb9ae"
                        off-icon="mdi-radiobox-blank"
                        on-icon="mdi-radiobox-marked"
                      ></v-checkbox>
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>

          <v-divider></v-divider>

          <v-list three-line>
            <h4 class="ml-3">
              Choose the readability measures to be used for finding the
              difficult sentences in the original text.
            </h4>

            <v-list-item-group v-model="selectedDS" single>
              <template>
                <v-list-item
                  v-for="(item, i) in diffSentencesOptions"
                  :key="`item.metric_name-${i}`"
                  :value="item.metric_name"
                  active-class="text--accent-4"
                >
                  <template v-slot:default="{ active }">
                    <v-list-item-content>
                      <v-list-item-title
                        v-text="item.metric_name"
                      ></v-list-item-title>
                      <v-list-item-subtitle>
                        {{ item.description }}
                      </v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                      <v-checkbox
                        :input-value="active"
                        color="#7bb9ae"
                      ></v-checkbox>
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>

          <v-divider></v-divider>
          <v-list three-line>
            <h4 class="ml-3">
              Choose the machine learning models to be used for the
              simplification.
            </h4>

            <v-list-item-group v-model="selectedMLM" single>
              <template>
                <v-list-item
                  v-for="(item, i) in modelOptions"
                  :key="`item.model_name-${i}`"
                  :value="item.model_name"
                  active-class="text--accent-4"
                >
                  <template v-slot:default="{ active }">
                    <v-list-item-content>
                      <v-list-item-title
                        v-text="item.model_name"
                      ></v-list-item-title>

                      <v-list-item-group>
                        <template>
                          <v-list-item
                            v-for="(option, i2) in item.options"
                            :key="`option.option_name-${i2}`"
                            :value="option.option_name"
                          >
                            <template>
                              <v-list-item-content>
                                <v-list-item-title
                                  v-text="option.option_name"
                                ></v-list-item-title>
                                <v-list-item-subtitle>
                                  {{ option.option_description }}
                                </v-list-item-subtitle>
                              </v-list-item-content>

                              <v-list-item-action>
                                <v-text-field
                                  v-model.number="
                                    newSpecificModelValues[option.option_name]
                                  "
                                  step="0.1"
                                  min="0"
                                />
                              </v-list-item-action>
                            </template>
                          </v-list-item>
                        </template>
                      </v-list-item-group>
                    </v-list-item-content>

                    <v-list-item-action>
                      <v-checkbox
                        :input-value="active"
                        color="#7bb9ae"
                      ></v-checkbox>
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
          </v-list>
        </v-card-items>

        <v-divider></v-divider>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
const _axios = require("axios").default;
const axiosRetry = require("axios-retry");
const axios = _axios.create();

export default {
  data() {
    return {
      dialog: false,
      selectedRM: "FleschDouma",
      selectedDS: "Spache",
      selectedMLM: "T5",
      modelOptions: [],
      modelOptionsCopy: [],
      diffSentencesOptions: [],
      readabilityMeasuresOptions: [],
      newSpecificModelValues: {
        max_length_original: this.max_length_original,
        max_length_sum: this.max_length_sum,
        min_length_sum: this.min_length_sum,
      },
    };
  },
  methods: {
    async getOptions() {
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

      await axios
        .get(
          process.env.VUE_APP_BASE_API_URL +
            process.env.VUE_APP_SIMPLIFICATION_SIMPLIFY +
            "options/?format=json"
        )
        .then(
          (response) =>
            (this.modelOptions = response.data.simplification_options[0])
        )

        .catch((error) => {
          alert(error);
          //alert("API error, please check the console");
        });

      await axios
        .get(
          process.env.VUE_APP_BASE_API_URL +
            process.env.VUE_APP_READABILITY +
            "options/?format=json"
        )
        .then(
          (response) =>
            (this.diffSentencesOptions =
              response.data.metric_options.difficult_sentences) &&
            (this.readabilityMeasuresOptions =
              response.data.metric_options.readability_measures) &&
            (this.dialog = true)
        )

        .catch((error) => {
          alert(error);
          //alert("API error, please check the console");
        });
      this.$loading(false);
    },
    saveOptions() {
      let result = {
        model_name: this.selectedMLM,
        model_options: this.newSpecificModelValues,
        sentence_metric_name: this.selectedDS,
        measure_metric_name: this.selectedRM,
      };
      this.$emit("savedOptions", result);
      this.dialog = false;
    },
  },
  props: {
    max_length_original: Number,
    max_length_sum: Number,
    min_length_sum: Number,
  },
};
</script>
