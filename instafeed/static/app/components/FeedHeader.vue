<template>
    <div id="header">
        <div id="auth" style="display: flex">
            <button @click="auth_instagram" type="button" id="instagram-connection">
                <font-awesome-icon icon="fa-brands fa-instagram" style="margin-right: 5px; color: white"/>
                Connect with Instagram
            </button>
            <button @click="login_facebook" type="button" id="facebook-connection">
                <font-awesome-icon icon="fa-brands fa-facebook-f"
                                   style="margin-right: 10px; margin-left: 10px; color: white"/>
                Connect with Facebook
            </button>
            <button @click="fetch_product_shopify" id="fetch_product_shopify">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" style="width: 25px; margin-right: 10px">
                    <path d="M388.32,104.1a4.66,4.66,0,0,0-4.4-4c-2,0-37.23-.8-37.23-.8s-21.61-20.82-29.62-28.83V503.2L442.76,472S388.72,106.5,388.32,104.1ZM288.65,70.47a116.67,116.67,0,0,0-7.21-17.61C271,32.85,255.42,22,237,22a15,15,0,0,0-4,.4c-.4-.8-1.2-1.2-1.6-2C223.4,11.63,213,7.63,200.58,8c-24,.8-48,18-67.25,48.83-13.61,21.62-24,48.84-26.82,70.06-27.62,8.4-46.83,14.41-47.23,14.81-14,4.4-14.41,4.8-16,18-1.2,10-38,291.82-38,291.82L307.86,504V65.67a41.66,41.66,0,0,0-4.4.4S297.86,67.67,288.65,70.47ZM233.41,87.69c-16,4.8-33.63,10.4-50.84,15.61,4.8-18.82,14.41-37.63,25.62-50,4.4-4.4,10.41-9.61,17.21-12.81C232.21,54.86,233.81,74.48,233.41,87.69ZM200.58,24.44A27.49,27.49,0,0,1,215,28c-6.4,3.2-12.81,8.41-18.81,14.41-15.21,16.42-26.82,42-31.62,66.45-14.42,4.41-28.83,8.81-42,12.81C131.33,83.28,163.75,25.24,200.58,24.44ZM154.15,244.61c1.6,25.61,69.25,31.22,73.25,91.66,2.8,47.64-25.22,80.06-65.65,82.47-48.83,3.2-75.65-25.62-75.65-25.62l10.4-44s26.82,20.42,48.44,18.82c14-.8,19.22-12.41,18.81-20.42-2-33.62-57.24-31.62-60.84-86.86-3.2-46.44,27.22-93.27,94.47-97.68,26-1.6,39.23,4.81,39.23,4.81L221.4,225.39s-17.21-8-37.63-6.4C154.15,221,153.75,239.8,154.15,244.61ZM249.42,82.88c0-12-1.6-29.22-7.21-43.63,18.42,3.6,27.22,24,31.23,36.43Q262.63,78.68,249.42,82.88Z"/>
                </svg>
                Fetch product shopify
            </button>
            <button @click="fetch_post_instagram" v-if="instagram_username" id="fetch_post_instagram">
                <font-awesome-icon icon="fa-brands fa-instagram" style="margin-right: 5px; color: white; width: 25px"/>
                Fetch post instagram
            </button>
            <div style="margin-left: auto">
                <a-dropdown block="true">
                    <template #overlay>
                        <a-menu @click="handleMenuClick">
                            <a-menu-item value="SelectPost">SelectPost</a-menu-item>
                            <a-menu-item value="FeedSettings">FeedSettings</a-menu-item>
                            <a-menu-item value="Dashboard">Dashboard</a-menu-item>
                        </a-menu>
                    </template>
                    <a-button>
                        MENU
                        <DownOutlined/>
                    </a-button>
                </a-dropdown>
            </div>
        </div>
        <div class="published-status-success" v-if="instagram_username">
            <span>Connected to <span>{{ instagram_username }}</span> with Instagram | <span
                    style="color: #1890ff; cursor: pointer" @click="changeInstagram">Change account</span></span>
        </div>
        <div class="login-facebook-success" v-if="facebook_username">
            <span>Connected to <span>{{ facebook_username }}</span> with Facebook</span>
        </div>
    </div>
</template>
<script>
import axios from "axios"
import {Modal} from "ant-design-vue"
import {DownOutlined} from "@ant-design/icons-vue"

window.fbAsyncInit = () => {
    FB.init({
        appId: '300578203867324',
        channelURL: '',
        status: true,
        cookie: true,
        oauth: true,
        xfbml: false
    })
}
export default {
    name: "FeedHeader",
    components: {Modal, DownOutlined},
    methods: {
        handleMenuClick(e) {
            this.$emit('changeTab', e.item.value)
        },
        fetch_post_instagram() {
            let self = this
            self.$emit('fetch_post_loading', true)
            axios.post('https://odoo.website/instafeed/fetch_post', {
                jsonrpc: "2.0",
                params: {instagram_username: self.instagram_username}
            }).then(res => {
                if (res.data.result.fetch_post_instagram_success) {
                    alert(res.data.result.fetch_post_instagram_success)
                }
                if (res.data.result.fetch_post_instagram_error) {
                    alert(res.data.result.fetch_post_instagram_error)
                }
                self.$emit('fetch_post_loading', false)
            }).catch(error => {
                console.log(error)
            })
        },
        auth_instagram() {
            window.open('https://odoo.website/instafeed/auth', '_blank')
        },
        async login_facebook() {
            await window.open('https://odoo.website/facebook/auth', "_blank")
            FB.getLoginStatus(() => {
                FB.login(() => {
                }, {scope: 'pages_show_list, instagram_basic, pages_manage_engagement'})
            })
        },
        changeInstagram() {
            this.$emit('changeInstagramAccount', true)
        },
        fetch_product_shopify() {
            axios.post('https://odoo.website/shopify/fetch_product', {
                jsonrpc: "2.0",
                params: {}
            }).then(res => {
                if (res.data.result.fetch_product_shopify_success) {
                    alert(res.data.result.fetch_product_shopify_success)
                }
                if (res.data.result.fetch_product_shopify_error) {
                    alert(res.data.result.fetch_product_shopify_error)
                }
            }).catch(error => {
                console.log(error)
            })
        }
    },
    emits: ['changeInstagramAccount', "fetch_post_loading", "changeTab"],
    mounted() {
        let e = document.createElement('script');
        e.async = true
        e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js'
        document.getElementById('auth').appendChild(e)
        if (window.instafeed.users.instagram_username) {
            this.instagram_username = window.instafeed.users.instagram_username
        } else {
            this.instagram_username = ''
        }
        if (window.instafeed.users.facebook_username) {
            this.facebook_username = window.instafeed.users.facebook_username
        } else {
            this.facebook_username = ''
        }
    },
    data() {
        return {
            instagram_username: '',
            facebook_username: ''
        }
    }
}
</script>
<style scoped>
#instagram-connection {
    background: rgb(0 128 96);
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: white;
    cursor: pointer;
    height: 40px;
    width: fit-content;
    display: flex;
    align-items: center;
    margin-right: 10px;
}

#facebook-connection {
    background: #1c67e9;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: white;
    width: 200px;
    cursor: pointer;
    height: 40px;
    display: flex;
    align-items: center;
}

#instagram-connection:hover {
    background: rgb(1, 119, 89);
    border: .1rem solid #5400bb;
}

#fetch_product_shopify {
    background: #62ec33;
    margin-left: 10px;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: black;
    cursor: pointer;
    height: 40px;
    width: fit-content;
    display: flex;
    align-items: center;
    margin-right: 10px;
}

#fetch_post_instagram {
    background: violet;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: white;
    cursor: pointer;
    height: 40px;
    width: fit-content;
    display: flex;
    align-items: center;
    margin-right: 10px;
}

#facebook-connection:hover {
    background: #115ad7;
    border: .1rem solid #5400bb;
}

.published-status-success {
    font-size: 14px;
    color: #007B5C;
    margin-left: 10px;
    font-weight: bold;
}

.login-facebook-success {
    font-size: 14px;
    color: #1c67e9;
    margin-top: 10px;
    font-weight: bold;
    margin-bottom: 5px;
    margin-left: 10px;
}

#header {
    margin-right: 10px;
    margin-left: 10px;
    margin-top: 10px;
    display: grid;
    border-radius: 5px;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
    background: white;
}

#auth {
    margin: 10px
}

#dashboard {
    background: #E2E2E2;
    margin-left: auto;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    border-radius: 5px;
    font-weight: 400;
    color: black;
    cursor: pointer;
    height: 40px;
    width: fit-content;
    display: flex;
    align-items: center;
    margin-right: 20px;
}
</style>