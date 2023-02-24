<template>
  <v-app-bar app height="90">
    <v-img
      class="ms-5 mt-2"
      src="../assets/TU-Delft-logo.webp"
      max-width="150"
    ></v-img>
    <v-img class="ms-7" src="../assets/KB_logo.png" max-width="200"></v-img>
    <v-spacer></v-spacer>
    <Settings
      :max_length_original="max_length_original_prop"
      :max_length_sum="max_length_sum_prop"
      :min_length_sum="min_length_sum_prop"
      @savedOptions="saveOptions"
    ></Settings>
    <Popup></Popup>
  </v-app-bar>
</template>

<script>
import Popup from "./PopupTutorial";
import Settings from "./SettingsDialog";

export default {
  components: {
    Popup,
    Settings,
  },
  methods: {
    saveOptions(options) {
      this.$emit("savedOptions", options);
    },
  },
  props: {
    max_length_original_prop: Number,
    max_length_sum_prop: Number,
    min_length_sum_prop: Number,
  },
};
</script>
