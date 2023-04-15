<template>
    <layout>
        <layout-header>
            <feed-header/>
        </layout-header>
        <layout-content>
            <select-post
                :posts="posts"
                v-if="currentTab=='SelectPost'"
                @SelectPostToFeedSettings="SelectPostToFeedSettings"/>
            <feed-settings
                :selected_posts="selected_posts"
                v-if="currentTab=='FeedSettings'"/>
        </layout-content>
    </layout>
</template>
<script>
import axios from 'axios'
import {Layout, LayoutHeader, LayoutContent} from "ant-design-vue"
import FeedSettings from "./components/FeedSettings.vue"
import FeedHeader from "./components/FeedHeader.vue"
import Loading from './components/Loading.vue'
import SelectPost from "./components/SelectPost.vue"

export default {
    name: "App",
    data() {
        return {
            posts: [],
            tabs: ['SelectPost', 'FeedSettings'],
            currentTab: "SelectPost",
            selected_posts: []
        }
    },
    components: {
        Layout,
        LayoutHeader,
        LayoutContent,
        FeedSettings,
        FeedHeader,
        Loading,
        SelectPost
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/instagram/get_posts', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            self.posts = res.data.result.post_data
        }).catch(error => {
            console.log(error)
        })
    },
    methods:{
        SelectPostToFeedSettings(tab, selected_posts){
            this.selected_posts = selected_posts
            this.currentTab = tab
        }
    }
}
</script>
<style scoped>
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