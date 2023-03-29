import {createApp} from 'vue/dist/vue.esm-bundler'
import shopify from "./shopify.vue"
import 'ant-design-vue/dist/antd.css'
import Antd from 'ant-design-vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome"
import {fas} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'
import {far} from '@fortawesome/free-regular-svg-icons'

library.add(fas, far)
if (window.location.href.indexOf('products') > -1) {
    createApp(shopify).component("font-awesome-icon", FontAwesomeIcon).use(Antd).mount('#test_app_1')
}