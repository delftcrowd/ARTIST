<template>
  <v-btn
    @click="copyToClipboard(text)"
    class="button"
    color="secondary"
    rounded
  >
    Copy to clipboard
  </v-btn>
</template>

<script>
import * as buttonMethods from "@/js/buttons";

export default {
  computed: { regex: () => /(<([^>]+)>)/gi },
  methods: {
    /**
     * see @copyToClipboard in util.js
     */
    async copyToClipboard(text) {
      if (!text.trim()) {
        alert("There is no text to be copied");
      } else {
        buttonMethods.copyToClipboard(text.replace(this.regex, ""));
      }
    },
  },
  props: ["text"],
};
</script>
