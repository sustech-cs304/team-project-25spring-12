import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
import './assets/css/icon.css'
import V3waterfall from 'v3-waterfall'
import 'v3-waterfall/dist/style.css'


const app = createApp(App)
app.use(createPinia())
app.use(ElementPlus)
app.use(router)
app.use(V3waterfall)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.mount('#app')
