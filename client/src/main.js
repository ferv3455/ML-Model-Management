import { createApp } from 'vue';
import VueCookies from 'vue-cookies';
import App from './App.vue';
import router from './router';
import './style/main.css';
import './style/theme/default.css';
import './style/theme/monotone.css';
import './style/theme/cyberpunk.css';
import './style/theme/goldDigger.css';
import './style/theme/mountain.css';
import './style/setcolor.css';

const app = createApp(App);

app.config.globalProperties.$cookies = VueCookies;

app.use(router).mount('#app');
