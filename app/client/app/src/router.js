import Vue from 'vue'
import Router from 'vue-router'

import Navbar from './components/Navbar'
import SubNavbar from './components/SubNavbar'

import Dashboard from './views/Dashboard'
import About from './views/About'
import Error from './views/Error'
import PageTwo from './views/PageTwo'

/*
 Integrating the Vue Router into a Vue application, where we are already composing our application with components,
 allows us to map the pre-existing components to routes.
 */

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/dashboard' 
    },
    {
      path: '/dashboard',
      components: {
        navbar: Navbar,
        subnavbar: SubNavbar,
        main: Dashboard
      }
    },
    {
      path: '/about',
      components: {
        navbar: Navbar,
        subnavbar: SubNavbar,
        main: About
      }
    },
    /*
     https://github.com/vuejs/vue-router/issues/866
     Any invalid route, i.e. routes not specified above, will be redirected to the root path.
    */

    /*
     TODO: create and redirect to error page.
    */
    {
      path: '/*',
      components: {
        navbar: Navbar,
        subnavbar: SubNavbar,
        main: Error
      } 
    }
  ]
})
