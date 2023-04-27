import {createApp, h} from 'vue/dist/vue.esm-bundler'
import Shopify from './Shopify.vue'
import 'ant-design-vue/dist/antd.css'
import Antd from 'ant-design-vue'
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome"
import {fas} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'
import {far} from '@fortawesome/free-regular-svg-icons'
import {faInstagram, faFacebookF} from '@fortawesome/free-brands-svg-icons'

library.add(fas, far, faFacebookF, faInstagram)
let test_apps = document.getElementsByClassName('test_app')
for (let test_app of test_apps) {
    let feed_id = test_app.getAttribute('data-feed-id')
    let feed_app = createApp({
        name: 'Feed_' + feed_id,
        render: () => h(Shopify, {data: {feed_id: feed_id}})
    })
    feed_app.component("font-awesome-icon", FontAwesomeIcon).use(Antd).mount(test_app)
}