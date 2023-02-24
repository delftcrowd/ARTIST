<template>
  <v-app>
    <vue-confirm-dialog></vue-confirm-dialog>
    <PageBanner
      :max_length_original_prop="max_length_original"
      :max_length_sum_prop="max_length_sum"
      :min_length_sum_prop="min_length_sum"
      @savedOptions="saveOptions"
    ></PageBanner>

    <v-main>
      <v-container grid-list-md text-xs-center>
        <v-row>
          <TextEditorComponent
            class="mt-5"
            label="Original"
            v-model="originalText"
            :onSimplified="onSimplified"
            :selectedRMprop="selectedRM"
            :selectedDSprop="selectedDS"
            @addToSentences="(item) => (complicatedSentencesUser = item)"
            @saveDiffSentencesModel="(item) => (difficultSentencesModel = item)"
            @ishighlightedModel="(item) => (isHighlightedModel = item)"
            @ishighlightedUser="(item) => (isHighlightedUser = item)"
          />
          <TextEditorComponent
            class="mt-5"
            label="Simplified"
            v-model="simplifiedText"
            :onSimplified="onSimplified"
            :selectedRMprop="selectedRM"
            :selectedDSprop="selectedDS"
          />
        </v-row>
        <v-row class="mt-10">
          <v-col>
            <div class="mt-10 d-flex">
              <UploadButton
                class="ml-5"
                v-model="originalText"
                v-if="!this.onSimplified"
              />
              <SimplifyButton
                class="ml-5"
                v-if="!this.onSimplified"
                :text="originalText"
                :selectedMLM="selectedMLM"
                :max_length_original="max_length_original"
                :max_length_sum="max_length_sum"
                :min_length_sum="min_length_sum"
                @simplified="getSimplified"
              />
              <v-btn
                @click="reset"
                rounded
                color="secondary"
                class="ml-5 button"
                >Reset</v-btn
              >
            </div>
          </v-col>
          <v-col>
            <div class="mt-10 d-flex">
              <ClipboardButton class="ml-5" :text="simplifiedText" />
              <DownloadButton class="ml-5" :text="simplifiedText" />
              <SaveButton
                class="ml-5"
                v-if="this.onSimplified"
                :unsimplifiedText="originalText"
                :simplified_by_model="simplifiedTextModel"
                :simplified_by_user="simplifiedText"
                :selectedMLM="selectedMLM"
                :selectedDS="selectedDS"
                :max_length_original="max_length_original"
                :max_length_sum="max_length_sum"
                :min_length_sum="min_length_sum"
                :simplificationRating="simplificationRating"
                :feedbackComments="feedbackComments"
                :difficultSentencesRating="difficultSentencesRating"
                :complicatedSentencesUser="complicatedSentencesUser"
                :difficultSentencesModel="difficultSentencesModel"
                v-model="isSaved"
              />
            </div>
          </v-col>
        </v-row>
        <FeedbackSurvey
          v-if="showFeedbackSurvey"
          @feedback-result="saveResults"
        ></FeedbackSurvey>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import * as util from "@/js/util.js";

import ClipboardButton from "./components/buttons/CopyClipboardButton.vue";
import DownloadButton from "./components/buttons/DownloadButton.vue";
import SimplifyButton from "./components/buttons/SimplifyButton.vue";
import UploadButton from "./components/buttons/UploadButton.vue";
import PageBanner from "./components/PageBanner.vue";
import FeedbackSurvey from "./components/FeedbackSurvey.vue";
import SaveButton from "./components/buttons/SaveButton.vue";
import TextEditorComponent from "./components/TextEditorComponent.vue";

export default {
  components: {
    ClipboardButton,
    DownloadButton,
    SimplifyButton,
    UploadButton,
    PageBanner,
    FeedbackSurvey,
    SaveButton,
    TextEditorComponent,
  },
  computed: {
    console: () => window.console,
  },
  methods: {
    getSimplified(newValue) {
      if (this.simplifiedText.trim()) {
        this.$confirm({
          message:
            "Your text currenlty in your Simplified texteditor will be overwritten " +
            "Are you sure you want to continue?",
          button: {
            no: "Cancel",
            yes: "Confirm",
          },
          callback: (confirm) => {
            if (confirm) {
              this.simplifiedText = newValue;
              this.simplificationRating = null;
              this.feedbackComments = "";
              this.difficultSentencesRating = null;
              this.showFeedbackSurvey = true;
              this.simplifiedTextModel = newValue;
              this.onSimplified = true;
            }
          },
        });
      } else {
        this.simplificationRating = null;
        this.feedbackComments = "";
        this.difficultSentencesRating = null;
        this.showFeedbackSurvey = true;
        this.simplifiedText = newValue;
        this.simplifiedTextModel = newValue;
        this.onSimplified = true;
      }
    },
    reset() {
      this.$confirm({
        message: "Would you like to start over?",
        button: {
          no: "Cancel",
          yes: "Confirm",
        },
        callback: (confirm) => {
          if (confirm) {
            if (!this.isSaved) {
              this.$confirm({
                message:
                  "Your work and feedback has not been saved to the database yet." +
                  "This can be done using the 'Store to database' button. Do you want to continue without doing so? ",
                button: {
                  no: "Cancel",
                  yes: "Confirm",
                },
                callback: (confirm) => {
                  if (confirm) this.resetForm();
                },
              });
            } else this.resetForm();
          }
        },
      });
    },
    resetForm() {
      this.simplifiedText = "";
      this.simplifiedTextModel = "";
      this.originalText = "";
      this.originalTextReadOnly = "";
      this.complicatedSentencesUser = [];
      this.onSimplified = false;
      this.showFeedbackSurvey = false;
      this.isSaved = false;
      this.isHighlightedModel = false;
      this.isHighlightedUser = false;
    },
    saveResults(newValue) {
      var jsonVal = JSON.parse(newValue);
      this.simplificationRating = jsonVal.simplificationRating;
      if (jsonVal.feedbackComments !== undefined) {
        this.feedbackComments = jsonVal.feedbackComments;
      }
      if (jsonVal.difficultSentencesRating !== undefined) {
        this.difficultSentencesRating = jsonVal.difficultSentencesRating;
      }
      this.showFeedbackSurvey = false;
    },
    saveOptions(options) {
      if (options.model_name !== undefined) {
        this.selectedMLM = options.model_name;
      }
      if (options.measure_metric_name !== undefined) {
        this.selectedRM = options.measure_metric_name;
      }
      if (options.sentence_metric_name !== undefined) {
        this.selectedDS = options.sentence_metric_name;
      }

      var advOptions = options.model_options;

      if (advOptions.max_length_original >= 100) {
        this.max_length_original = advOptions.max_length_original;
      }
      if (advOptions.max_length_sum <= 1) {
        this.max_length_sum = advOptions.max_length_sum;
      }
      if (advOptions.min_length_sum <= 1) {
        this.min_length_sum = advOptions.min_length_sum;
      }
    },
  },
  data: () => {
    return {
      originalText: "",
      originalTextReadOnly: "",
      onSimplified: false,
      simplifiedText: "",
      simplificationRating: null,
      feedbackComments: "",
      difficultSentencesRating: null,
      showFeedbackSurvey: false,
      selectedMLM: "T5",
      max_length_original: 512,
      max_length_sum: 0.9,
      min_length_sum: 0.1,
      selectedRM: "FleschDouma",
      selectedDS: "Spache",
      simplifiedTextModel: "",
      complicatedSentencesUser: [],
      difficultSentencesModel: [],
      isSaved: false,
      isHighlightedModel: false,
      isHighlightedUser: false,
    };
  },
  created() {
    if (localStorage.originalText) {
      this.originalText = localStorage.originalText;
    }
    if (localStorage.simplifiedText) {
      this.simplifiedText = localStorage.simplifiedText;
    }
    if (localStorage.selectedMLM) {
      this.selectedMLM = localStorage.selectedMLM;
    }
    if (localStorage.selectedRM) {
      this.selectedRM = localStorage.selectedRM;
    }
    if (localStorage.selectedDS) {
      this.selectedDS = localStorage.selectedDS;
    }
    if (localStorage.simplifiedTextModel) {
      this.simplifiedTextModel = localStorage.simplifiedTextModel;
    }
    if (localStorage.complicatedSentencesUser) {
      this.complicatedSentencesUser = JSON.parse(
        localStorage.getItem("sentences")
      );
    }
    if (localStorage.isHighlightedUser) {
      this.ishighlightedUser = localStorage.isHighlightedUser;
    }
    if (localStorage.isHighlightedModel) {
      this.ishighlightedModel = localStorage.isHighlightedModel;
    }
  },
  watch: {
    originalText: util.debounce(function (newOriginalText) {
      localStorage.originalText = newOriginalText;
      this.originalText = newOriginalText;
    }, 500),
    simplifiedText: util.debounce(function (newSimplifiedText) {
      localStorage.simplifiedText = newSimplifiedText;
      this.simplifiedText = newSimplifiedText;
    }, 500),
    selectedMLM: util.debounce(function (newMLM) {
      localStorage.selectedMLM = newMLM;
      this.selectedMLM = newMLM;
    }, 500),
    selectedRM: util.debounce(function (newRM) {
      localStorage.selectedRM = newRM;
      this.selectedRM = newRM;
    }, 500),
    selectedDS: util.debounce(function (newDS) {
      localStorage.selectedDS = newDS;
      this.selectedDS = newDS;
    }, 500),
    simplifiedTextModel: util.debounce(function (newSimplifiedText) {
      localStorage.simplifiedTextModel = newSimplifiedText;
      this.simplifiedTextModel = newSimplifiedText;
    }, 500),
    complicatedSentencesUser: util.debounce(function (sentences) {
      localStorage.setItem("sentences", JSON.stringify(sentences));
      this.complicatedSentencesUser = sentences;
    }, 500),
    isSaved: function (newValue) {
      this.isSaved = newValue;
    },
    isHighlightedUser: function (newValue) {
      localStorage.isHighlightedUser = newValue;
      this.isHighlightedUser = newValue;
    },
    isHighlightedModel: function (newValue) {
      localStorage.isHighlightedModel = newValue;
      this.isHighlightedModel = newValue;
    },
  },
};
</script>

<style lang="scss" src="@/assets/buttons.scss"></style>

<style>
#app {
  background-color: #7bb9ae;
}

.originalText-readonly {
  background-color: white;
}
</style>
