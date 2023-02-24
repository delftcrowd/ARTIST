<template>
  <div>
    <v-btn
      color="secondary"
      class="button"
      :loading="isSelecting"
      @click="handleFileUpload"
      rounded
    >
      Upload File
    </v-btn>

    <!-- Create a File Input that will be hidden but triggered with JavaScript -->
    <input ref="uploader" class="d-none" type="file" @input="onFileChanged" />
  </div>
</template>

<script>
import process from "process";
const _axios = require("axios").default;
const axiosRetry = require("axios-retry");
const axios = _axios.create();

export default {
  computed: {
    console: () => window.console,
  },
  methods: {
    /**
     * Method used for triggering the file upload dialog.
     * Add an event that checks if the file uploader has been triggered.
     * If so, use javascript to click on the invisible file uploader through the button.
     */
    handleFileUpload() {
      this.isSelecting = true;

      // After obtaining the focus when closing the upload dialog, return the button state to normal
      window.addEventListener(
        "focus",
        () => {
          this.isSelecting = false;
        },
        { once: true }
      );

      // Trigger click on the FileInput
      this.$refs.uploader.click();
    },
    /**
     * Takes the contents of an uploaded file and turns the data into the Original Text.
     * @note Been made asynchronous, because the method should wait for the file to finish being read.
     */
    async onFileChanged() {
      this.$loading(true);
      let selectedFile = this.$refs.uploader.files[0];
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

      let data = new FormData();
      data.append("file", selectedFile);
      data.append(
        "json",
        JSON.stringify({
          options: {
            model_name: "T5",
            model_options: {
              max_length_sum: 0.9,
              min_length_sum: 0.1,
              max_length_original: 512,
            },
          },
        })
      );

      let config = {
        url:
          process.env.VUE_APP_BASE_API_URL +
          process.env.VUE_APP_SIMPLIFICATION_FILE,
        method: "post",
        headers: {
          "Content-Type": "multipart/form-data",
        },
        data,
      };

      await axios
        .request(config)
        .then((response) => {
          this.$emit("input", response.data.original_text);
        })
        .catch((error) => {
          console.log(error);
          alert(error.response.data.detail);
        });
      this.$loading(false);
    },
  },
  data: () => {
    return {
      isSelecting: false,
    };
  },
};
</script>
