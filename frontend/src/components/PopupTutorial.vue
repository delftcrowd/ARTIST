<template>
  <div>
    <v-btn
      class="me-10"
      style="background-color: #7bb9ae"
      @click="dialog = true"
    >
      Tutorial
    </v-btn>

    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-window v-model="onboarding">
          <v-window-item v-for="index in length" :key="`card-${index}`">
            <v-card>
              <v-row class="white">
                <v-card-title
                  background-color="white"
                  style="word-break: break-word"
                >
                  <h3 v-if="index === 1" class="text-center">
                    Type text in the 'Original' textbox. Or use the 'Upload'
                    button to select .txt, .pdf, .epub or .docx files from your
                    computer that you wish to simplify.
                  </h3>
                  <h3 v-if="index === 2" class="text-center">
                    You can use the 'Classify sentence as difficult' button to
                    mark difficult sentences in the original text. Or use the
                    'Show difficult sentences' button the show the sentences
                    identified as difficult by the model. Click 'Undo' to remove
                    the highlighting.
                  </h3>
                  <h3 v-if="index === 3" class="text-center">
                    When the text is ready click the 'Simplify' button to
                    request a simplification. When ready, the result will appear
                    in the 'Simplified' textbox.
                  </h3>
                  <h3 v-if="index === 4" class="text-center">
                    You can manually alter the simplification until you are
                    satisfied with the result. The undo and redo buttons can be
                    used to reverse pervious changes made on the text.
                  </h3>
                  <h3 v-if="index === 5" class="text-center">
                    The readability measure score is calculated for the text in
                    both textboxes and can be found in the right lower corner.
                    Hovering the info icon shows extra information regarding the
                    measure used.
                  </h3>
                  <h3 v-if="index === 6" class="text-center">
                    When the simplification is ready you can either use the
                    'Copy to clipboard' or 'Download' button to export the
                    result for further use.
                  </h3>
                  <h3 v-if="index === 7" class="text-center">
                    After your simplification is done, you can press the 'Store
                    to database' button to save the original and simplified text
                    to a database, which can be used to further train the
                    machine learning model. Along with the text possible input
                    for difficult sentences and feedback survey will be sent
                    aswell.
                  </h3>
                  <h3 v-if="index === 8" class="text-center">
                    If you want to start another simplification you can click
                    the 'Reset' button to reset the textboxes.
                  </h3>
                  <h3 v-if="index === 9" class="text-center">
                    The 'Settings' button on the top right of the page can be
                    used to choose advanced settings like the readability
                    measure or machine learning model to be used.
                  </h3>
                </v-card-title>
                <v-divider />
              </v-row>
              <v-row style="background-color: #7bb9ae" class="justify-center">
                <v-card-actions>
                  <v-btn
                    v-if="index === 1"
                    class="my-15"
                    color="secondary"
                    rounded
                  >
                    Upload File
                  </v-btn>
                  <v-img
                    v-if="index === 2"
                    width="600px"
                    src="../assets/difficult_sentences.png"
                  ></v-img>
                  <v-btn
                    v-if="index === 3"
                    class="my-15"
                    color="secondary"
                    rounded
                  >
                    Simplify
                  </v-btn>
                  <div v-if="index === 4" class="my-10">
                    <div class="my-2">
                      <v-btn fab x-small dark>
                        <v-icon>mdi-undo</v-icon>
                      </v-btn>
                    </div>
                    <div class="my-2">
                      <v-btn fab x-small dark>
                        <v-icon>mdi-redo</v-icon>
                      </v-btn>
                    </div>
                  </div>
                  <v-img
                    v-if="index === 5"
                    class="my-15"
                    width="200px"
                    src="../assets/readability_measure.png"
                  ></v-img>
                  <div v-if="index === 6">
                    <v-btn class="my-15" color="secondary" rounded>
                      Copy to clipboard
                    </v-btn>
                    <v-btn class="my-15 ml-5" color="secondary" rounded>
                      Download
                    </v-btn>
                  </div>
                  <v-btn
                    v-if="index === 7"
                    class="my-15"
                    color="secondary"
                    rounded
                  >
                    Store to database
                  </v-btn>
                  <v-btn
                    v-if="index === 8"
                    class="my-15"
                    color="secondary"
                    rounded
                  >
                    Reset
                  </v-btn>
                  <v-btn
                    v-if="index === 9"
                    class="my-15"
                    style="background-color: #7bb9ae"
                  >
                    Settings
                  </v-btn>
                </v-card-actions>
              </v-row>
            </v-card>
          </v-window-item>
        </v-window>

        <v-card-actions class="justify-space-between">
          <v-btn text @click="prev">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-item-group v-model="onboarding" class="text-center" mandatory>
            <v-item
              v-for="n in length"
              :key="`btn-${n}`"
              v-slot="{ active, toggle }"
            >
              <v-btn :input-value="active" icon @click="toggle">
                <v-icon>mdi-record</v-icon>
              </v-btn>
            </v-item>
          </v-item-group>
          <v-btn text @click="next">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      length: 9,
      onboarding: 0,
    };
  },
  methods: {
    next() {
      this.onboarding =
        this.onboarding + 1 === this.length ? 0 : this.onboarding + 1;
    },
    prev() {
      this.onboarding =
        this.onboarding - 1 < 0 ? this.length - 1 : this.onboarding - 1;
    },
  },
};
</script>
