import Vue from 'vue';
import $ from 'jquery';
import App from './App.vue';
import VueRouter from 'vue-router';
import VueMaterial from 'vue-material';
import store from './store'

import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

import Statistics from "./components/pages/Statistics";

window.$ = $; // Import jQuery to $.
Vue.use(VueRouter); // Use VueRouter to navigate.
Vue.use(VueMaterial); // Use VueMaterial as design framework.
Vue.config.productionTip = false; // Determine whether you want to be bothered by "tips."

window.hashCode = function(e) { // Function to hash strings.
    var hash = 0;
    for (var i = 0; i < e.length; i++) {
      var character = e.charCodeAt(i);
      hash = ((hash<<5)-hash)+character;
      hash = hash & hash; // Convert to 32bit integer
    }

    return hash;
};

export default {
  name: 'app',
  components: {}
}

const routes = [ // Determine the possible routes in this application.
  {
    path: '/',
    name: 'Statistics',
    component: Statistics,
    props: {}
  }
];

const router = new VueRouter({ // Initialize the router.
  routes
});

new Vue({ // Initialize Vue itself.
  name: 'Home',
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
}).$mount('#app');