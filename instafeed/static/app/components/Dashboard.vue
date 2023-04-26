<template>
    <div id="welcome">WELCOME, {{ shop_owner }}!</div>
    <div id="table-product">
        <table>
            <tr class="table-col-name">
                <td>#</td>
                <td>Feed title</td>
                <td>List post</td>
                <td class="status">Status</td>
            </tr>
            <tr class="table-row" v-if="list_feed" v-for="feed in list_feed">
                <td>{{ feed.id }}</td>
                <td>{{ feed.feed_title }}</td>
                <td>
                    <div style="display: flex">
                        <div style="margin-left: 5px" v-for="post in feed.selected_posts">
                            <img v-if="post.media_type == 'IMAGE'"
                                 :src="post.media_url"
                                 style="height: 50px; width: 50px; object-fit: cover"
                                 :alt="post.caption">
                            <img v-if="post.media_type == 'VIDEO'"
                                 :src="post.thumbnail_url"
                                 style="height: 50px; width: 50px; object-fit: cover"
                                 :alt="post.caption">
                        </div>
                    </div>
                </td>
                <td class="status">
                    <a-switch @change="changeFeedStatus(feed.id, feed.enable_status)"
                              v-model:checked="feed.enable_status"
                              checked-children="ON"
                              un-checked-children="OFF"/>
                </td>
            </tr>
        </table>
    </div>
</template>
<script>
import axios from "axios"

export default {
    name: "Dashboard",
    data() {
        return {
            shop_owner: '',
            list_feed: []
        }
    },
    methods: {
        changeFeedStatus(feed_id, status) {
            let self = this
            axios.post("https://odoo.website/instafeed/change_status_feed", {
                jsonrpc: "2.0",
                params: {
                    feed_id: feed_id,
                    status: status
                }
            }).then(res => {
                if (res.data.result.change_status_feed) {
                    alert(res.data.result.change_status_feed)
                }
                if (res.data.result.error_enable_feed) {
                    alert(res.data.result.error_enable_feed)
                }
            }).catch(error => {
                console.log(error)
            })
        }
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/instafeed/get_feed', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            self.shop_owner = res.data.result.shop_owner
            self.list_feed = res.data.result.list_feed
        }).catch(error => {
            console.log(error)
        })
    }
}
</script>
<style scoped>
#welcome {
    color: black;
    height: 24px;
    font-style: normal;
    font-weight: 600;
    font-size: 27px;
    margin-left: 57px;
    margin-top: 51px;
    line-height: 24px;
}

#table-product {
    width: 90%;
    height: 50%;
    margin-left: 60px;
    margin-top: 1rem;
    margin-right: 100px;
}

table {
    width: 100%;
    margin-top: 81px;
    font-size: 14px;
}

.table-row {
    height: 3rem;
    border-bottom: 1px groove #EFEFEF;
    font-size: 14px;
}

.table-col-name {
    height: 3rem;
    border-bottom: 1px groove #EFEFEF;
    border-top: 1px groove #EFEFEF;
    color: rgba(0, 0, 0);
    font-weight: 700;
    font-size: 14px;
}

.status {
    width: 70px;
}

.ant-switch {
    width: 56px
}
</style>