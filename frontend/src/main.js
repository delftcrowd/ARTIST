import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import VueConfirmDialog from "vue-confirm-dialog";
import VueLoading from "vuejs-loading-plugin";
import VueQuill from "vue-quill";

Vue.config.productionTip = false;
Vue.use(VueConfirmDialog);
Vue.component("vue-confirm-dialog", VueConfirmDialog.default);
Vue.use(VueLoading);
Vue.use(VueQuill);

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
