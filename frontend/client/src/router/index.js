import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/poi', component: 'POI' },
  { path: '/poi/add', component: 'AddPOI' },
  { path: '/poi/update', component: 'UpdatePOI' },
  { path: '/camera', component: 'Camera' },
  { path: '/camera/add', component: 'AddCamera' },
  { path: '/prediction/add', component: 'AddPrediction' },
  { path: '/prediction', component: 'Prediction' },
  { path: '/map', component: 'Map' },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
