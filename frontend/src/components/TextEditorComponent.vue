<template>
  <v-row>
    <v-col class="d-flex justify-content-center">
      <v-card width="34em">
        <v-card-title>{{ label }}</v-card-title>
        <v-card-text>
          <quill
            output="html"
            v-model="content"
            :ref="label + 'Text'"
            :key="key"
            :config="editorOption"
            @selection-change="highlightSentences"
          />
        </v-card-text>
        <Readability
          class="pb-5"
          :selectedRM="selectedRMprop"
          :text="content"
        />
        <v-card-actions
          v-if="content.trim()"
          class="row row-flex overflow-y-auto pb-5"
        >
          <v-btn
            :key="label + '-highlight'"
            v-if="label == 'Original' && !isHighlightedModel"
            color="secondary"
            class="ml-5 my-2 button"
            id="btn"
            rounded
            @click="storeHighlights"
            >Classify sentence as difficult</v-btn
          >
          <RequestDifficultSentences
            v-if="label == 'Original' && !isHighlightedModel"
            class="ml-3 my-2 button"
            @saveDiffSentencesModel="saveDiffSentencesModel"
            :text="content"
            :editor="editor"
            :selectedDS="selectedDSprop"
          />
          <v-btn
            v-if="
              label == 'Original' && (isHighlightedModel || isHighlightedUser)
            "
            color="secondary"
            class="ml-3 my-2 button"
            id="btn"
            rounded
            @click="resetBackground"
            >Remove highlights</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-col>
    <v-col v-if="label == 'Simplified'"
      ><div class="tools">
        <div class="my-2">
          <v-btn @click="undo" fab x-small dark>
            <v-icon>mdi-undo</v-icon>
          </v-btn>
        </div>
        <div class="my-2">
          <v-btn @click="redo" fab x-small dark>
            <v-icon>mdi-redo</v-icon>
          </v-btn>
        </div>
      </div></v-col
    >
  </v-row>
</template>

<script>
import Readability from "../components/ReadabilityMeasure.vue";
import RequestDifficultSentences from "./buttons/RequestDifficultSentences.vue";

import "quill/dist/quill.snow.css";

export default {
  components: {
    Readability,
    RequestDifficultSentences,
  },
  computed: {
    content: {
      get() {
        return this.value;
      },
      set(newValue) {
        this.$emit("input", newValue);
      },
    },
  },
  data: () => {
    return {
      editor: null,
      editorOption: {
        modules: {
          toolbar: [
            [{ header: [1, 2, false] }],
            [{ script: "sub" }, { script: "super" }],
            ["bold", "italic", "underline"],
            ["blockquote", "code-block"],
            [{ color: [] }, { background: [] }],
            [{ align: [] }],
          ],
        },
      },
      key: 0,
      range: {},
      sentences: [],
      selectedSentence: "",
    };
  },
  mounted() {
    if (!this.editor) this.editor = localStorage.editor;

    this.$nextTick(() => {
      this.key = this.key + this.label;
    });
  },
  methods: {
    highlightSentences(quillEditor, range) {
      {
        this.editor = quillEditor;

        if (range !== null && range.length > 1) {
          this.selectedSentence = quillEditor.getText(
            range.index,
            range.length
          );
          var format = quillEditor.getFormat(range.index, range.length);

          if (!format.background) {
            this.range = range;
          }
        }
      }
    },
    resetBackground() {
      this.editor.removeFormat(0, this.editor.getText().length);
      this.$emit("isHighlightedModel", false);
      this.$emit("isHighlightedUser", false);
    },
    storeHighlights() {
      if (this.editor) {
        const isHighlighted = this.editor.getFormat(
          this.range.index,
          this.range.length
        ).background;
        var form1 = this.editor.getFormat(this.range.index, 1).background;
        var form2 = this.editor.getFormat(this.range.length, 1).background;
        if (isHighlighted || form1 || form2)
          alert("This sentence has already been highlighted");
        else if (this.range.length > 1) {
          this.editor.formatText(
            this.range.index,
            this.range.length,
            "background",
            "RGB(255, 255, 0)"
          );
          this.sentences.push(this.selectedSentence);
          this.$emit("addToSentences", this.sentences);
          this.$emit("isHighlightedUser", true);
        } else alert("Please highlight something first.");
      } else alert("This sentence has already been highlighted");
    },
    saveDiffSentencesModel(difficultSentences) {
      this.$emit("saveDiffSentencesModel", difficultSentences);
      this.$emit("isHighlightedModel", true);
    },
    undo() {
      this.editor.history.undo();
    },
    redo() {
      this.editor.history.redo();
    },
  },

  props: {
    value: String,
    onSimplified: Boolean,
    label: String,
    selectedRMprop: String,
    selectedDSprop: String,
    isHighlightedModel: Boolean,
    isHighlightedUser: Boolean,
  },
  watch: {
    value: function (newValue) {
      if ((newValue && !newValue.includes("<p>")) || !newValue)
        this.$nextTick(() => {
          this.key += 1;
        });
    },
    onSimplified: function () {
      this.$nextTick(() => {
        this.key += 1;
      });
    },
    editor: function (newEditor) {
      this.editor = newEditor;
      localStorage.editor = newEditor;
    },
  },
};
</script>

<style>
.ql-editor {
  height: 300px;
}

#btn > span {
  font-size: 50%;
  font-weight: bold;
}
</style>
