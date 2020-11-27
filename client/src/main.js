import Vue from 'vue'
import Vuetify from 'vuetify'
import ImageUploader from 'vue-image-upload-resize'
import 'vuetify/dist/vuetify.min.css'

import App from './App.vue'
import MainFooter from './Footer.vue'

Vue.use(Vuetify)
Vue.use(ImageUploader)

const opts = {}

new Vue({
  el: '#app',
  vuetify: new Vuetify(opts),
  render: h => h(App)
})

new Vue({
  el: '#main-footer',
  vuetify: new Vuetify(opts),
  render: h => h(MainFooter)
})
