import Vue from 'vue'
import Vuex from 'vuex'
import router from './router.js'
import VTooltip from 'v-tooltip'

import './filters.js'

Vue.use(VTooltip)

import App from './App.vue'

// Set up global handlers and scope of the application.
var vue = new Vue({
  // el: '#vue-app',
  render: h => h(App),
  router,
  template: '<App/>',
  components: { App }
}).$mount('#vue-app')

