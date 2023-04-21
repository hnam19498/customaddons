<template>
    <layout style="position: relative">
        <div class="loading" v-if="fetch_status">
            <a-spin size="large"/>
        </div>
        <layout-header>
            <feed-header @changeInstagramAccount="changeInstagramAccount"
                         @fetch_post_loading="fetch_post_loading"/>
        </layout-header>
        <layout-content>
            <select-post @SelectPostToFeedSettings="SelectPostToFeedSettings"
                         :posts="posts"
                         v-if="currentTab == 'SelectPost'"/>
            <feed-settings @changeTab="changeTab"
                           :selected_posts="selected_posts"
                           v-if="currentTab == 'FeedSettings'"/>
            <Modal style="width: 70%"
                   title="CHANGE THE INSTAGRAM ACCOUNT CONNECTED"
                   :footer="null"
                   @cancel="this.changeInstagram=false"
                   v-model:visible="changeInstagram"
                   :maskClosable="false">
                <div>Follow the steps below on your computer and not mobile.</div>
                <div>1 - Go to www.instagram.com in your desktop browser and log out.</div>
                <div>2 - Important: Login to www.instagram.com with the Instagram username you want to show in your
                    feed. This is not your personal or shared username, you need to log in using the username (account
                    name) of the account that you want to show. If you don't have the password for that username use the
                    recover password option
                </div>
                <div>Go back to Instafeed and connect your Instagram account again.</div>
            </Modal>
        </layout-content>
    </layout>
</template>
<script>
import axios from 'axios'
import {Layout, LayoutHeader, LayoutContent, Modal} from "ant-design-vue"
import FeedSettings from "./components/FeedSettings.vue"
import FeedHeader from "./components/FeedHeader.vue"
import SelectPost from "./components/SelectPost.vue"
import {SearchOutlined} from "@ant-design/icons-vue"

export default {
    name: "App",
    data() {
        return {
            posts: [],
            tabs: ['SelectPost', 'FeedSettings'],
            currentTab: "SelectPost",
            selected_posts: [],
            changeInstagram: false,
            fetch_status: false
        }
    },
    components: {
        SearchOutlined, Modal,
        Layout,
        LayoutHeader,
        LayoutContent,
        FeedSettings,
        FeedHeader,
        SelectPost
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/instagram/get_posts', {
            jsonrpc: "2.0",
            params: {instagram_username: window.instafeed.users.instagram_username}
        }).then(res => {
            self.posts = res.data.result.post_data
        }).catch(error => {
            console.log(error)
        })
    },
    methods: {
        fetch_post_loading(status) {
            this.fetch_status = status
        },
        changeInstagramAccount(changeStatus) {
            console.log(changeStatus)
            this.changeInstagram = changeStatus
        },
        SelectPostToFeedSettings(tab, selected_posts) {
            this.selected_posts = selected_posts
            this.currentTab = tab
        },
        changeTab(tab) {
            console.log(tab)
            this.currentTab = tab
        }
    }
}
</script>
<style scoped>
.loading {
    justify-content: center;
    display: flex;
    width: 100%;
    opacity: 0.5;
    height: 500px;
    align-items: center;
    background-color: white;
    position: absolute;
}

.ant-layout-header {
    background: inherit !important;
    padding: 0 0 !important;
    height: fit-content !important;
    line-height: normal !important;
}

main {
    background: white;
    margin-top: 20px;
    border-radius: 5px;
    margin-right: 10px;
    margin-left: 10px;
    box-shadow: 0 0 0 1px rgba(63, 63, 68, .05), 0 1px 3px 0 rgba(63, 63, 68, .15);
}
</style>
<style>
body {
    background-color: #f0f2f5 !important;
}
</style>