<template>
  <v-btn @click="exportToTxt" color="secondary" class="button" rounded>
    Download
  </v-btn>
</template>

<script>
import saveAs from "file-saver";

export default {
  computed: { regex: () => /(<([^>]+)>)/gi },
  methods: {
    /**
     * Takes the Original text and transforms it into a .txt file to be downloaded.
     */
    exportToTxt() {
      var blob = new Blob([this.text.replace(this.regex, "")], {
        type: "text/plain;charset=utf-8",
      });
      saveAs(blob, "simplified.txt");
    },
  },
  props: ["text"],
};
</script>
