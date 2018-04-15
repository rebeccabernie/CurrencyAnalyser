import Vue from 'vue'
import Vuex from 'vuex'
import router from './router.js'
import store from './store'
import VTooltip from 'v-tooltip'

import './filters.js'
// import Mixins from './mixins.js'
// Vue.mixin(Mixins)

Vue.use(VTooltip)

import App from './App.vue'

// Set up global handlers and scope of the application.
var vue = new Vue({
  // el: '#vue-app',
  render: h => h(App),
  router,
  store,
  template: '<App/>',
  // mixins: [Mixins],
  components: { App }
}).$mount('#vue-app')

