<template>
    <layout>
        <layout-header>
            <feed-header/>
        </layout-header>
        <layout-content>
            <feed-settings/>
        </layout-content>
    </layout>
</template>
<script>
import axios from 'axios'
import {Layout, LayoutHeader, LayoutContent} from "ant-design-vue"
import FeedSettings from "./components/FeedSettings.vue"
import FeedHeader from "./components/FeedHeader.vue"

export default {
    name: "App",
    data() {
        return {}
    },
    components: {
        Layout,
        LayoutHeader,
        LayoutContent,
        FeedSettings,
        FeedHeader
    },
    mounted() {
        axios.post('https://odoo.website/instagram/get_posts', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })
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
</style>