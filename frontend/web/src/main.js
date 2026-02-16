import { createApp } from 'vue'
import VueAxios from 'vue-axios'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from './axios'
import base from './components/Base'
import footer from './components/Footer'

// 创建Vue对象
const app = createApp(App)
// 注册组件
app.component('base-page', base)
app.component('footer-page', footer)
// 将路由对象绑定到Vue对象
app.use(router)
app.use(store)
// 将vue-axios与axios关联并绑定到Vue对象
app.use(VueAxios, axios)
// 挂载使用Vue对象
app.mount('#app')
