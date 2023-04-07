<template>
    <layout>
        <layout-header>
            <button id="instagram-connection">
                <font-awesome-icon icon="fa-brands fa-instagram"/>
                Connect with Instagram
            </button>
            <div id="published-status-success">
                <span>
                    Connected to <span>Username</span> with Instagram
                </span>
            </div>
        </layout-header>
        <layout-content>
            <a-row type="flex" justify="center" align="top">
                <a-col :span="6">
                    <h2>FEED TITLE</h2>
                </a-col>
                <a-col :span="6">
                    <h2>Preview</h2>
                </a-col>
            </a-row>
        </layout-content>
    </layout>
</template>

<script>
import axios from 'axios'
import {Layout, LayoutHeader, LayoutContent} from "ant-design-vue"
export default {
    name: "App",
    data() {
        return {}
    },
    components:{
        Layout, LayoutHeader, LayoutContent
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
}

#published-status-success {
    font-size: 13px;
}
</style>