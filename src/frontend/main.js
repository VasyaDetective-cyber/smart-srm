import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import './styles.css'
import './refinement.css'
import './customers.css'
import './language.css'
import './ui-polish.css'
import './customers-polish.css'
import './pagination.css'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
