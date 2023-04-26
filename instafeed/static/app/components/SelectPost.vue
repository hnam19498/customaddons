<template>
    <div v-if="posts" style="background: white; margin-top: 15px; margin-bottom: 15px">
        <div>
            <div class="setting-btn">
                <button class="btn-setting" id="btn-cancel" @click="cancelSelectPost">Cancel</button>
                <button class="btn-setting" id="btn-next" @click="nextToFeedSettings">NEXT</button>
            </div>
            <div id="setting_widget">
                <label id="enable_widget">Enable Widget</label>
                <a-switch v-model:checked="enable_widget" checked-children="ON" un-checked-children="OFF"/>
            </div>
        </div>
        <div style="position: relative; width: 100%">
            <div>
                <div id="choose-post">
                    <font-awesome-icon icon="fa-solid fa-circle-question" style="color: #5C5F62"/>
                    <span>Choose post(s)</span>
                </div>
                <div class="selected_posts" v-if="this.selected_posts.length > 0">
                    <div :key="post.id"
                         v-for="post in this.selected_posts"
                         class="selected_post">
                        <div style="height: 17px; margin-left: 10px; margin-bottom: 5px; margin-top: 5px">
                            {{ post.caption }}
                        </div>
                        <font-awesome-icon icon="fa-solid fa-circle-xmark"
                                           @click="deleteChoosePost(post.id)"
                                           style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"
                                           size="sm"/>
                    </div>
                </div>
                <div class="table">
                    <table>
                        <tr class="table-col-name">
                            <td><input type="checkbox" @change="SelectAllPosts" v-model="tickAllPosts"></td>
                            <td>Media</td>
                            <td>Like</td>
                            <td>Caption</td>
                        </tr>
                        <tr class="table-row" v-for="post in posts" :key="post.id" @click="select_post(post)">
                            <td>
                                <input :checked="selected_posts.filter(e => e.id == post.id).length > 0"
                                       type="checkbox">
                            </td>
                            <td v-if="post.media_type=='VIDEO'">
                                <video controls width="200" height="200" style="object-fit: cover">
                                    <source :src="post.media_url">
                                </video>
                            </td>
                            <td v-if="post.media_type=='IMAGE'">
                                <img :alt="post.caption" :src="post.media_url"
                                     style="width: 200px; height: 200px; object-fit: cover">
                            </td>
                            <td>{{ post.like_count }}</td>
                            <td>{{ post.caption }}</td>
                        </tr>
                    </table>
                </div>
            </div>
            <div v-if="!enable_widget" class="blur"/>
        </div>
    </div>
</template>
<script>
import {h} from 'vue'
import {notification} from 'ant-design-vue'
import {CloseCircleFilled} from "@ant-design/icons-vue"

export default {
    data() {
        return {
            enable_widget: false,
            selected_posts: [],
            tickAllPosts: false
        }
    },
    mounted() {
        if (window.selected_posts) {
            this.enable_widget = true
            this.selected_posts = window.selected_posts
        }
    },
    props: {
        posts: {type: Array, default: []}
    },
    emits: ['SelectPostToFeedSettings'],
    methods: {
        show_toast: function (type, message, duration) {
            notification[type]({
                message: message,
                duration: duration,
                class: 'error_popup',
                closeIcon: e => {
                    return (<CloseCircleFilled/>)
                }
            })
        },
        cancelSelectPost() {
            this.selected_posts = []
            this.tickAllPosts = false
        },
        nextToFeedSettings() {
            if (this.selected_posts.length == 0) {
                this.show_toast(
                    'open',
                    'Please select at least 1 post from the list to continue.',
                    3
                )
            } else {
                window.selected_posts = this.selected_posts
                this.$emit('SelectPostToFeedSettings', 'FeedSettings', this.selected_posts)
            }
        },
        SelectAllPosts() {
            this.selected_posts = []
            if (this.tickAllPosts == true) {
                for (let post of this.posts) {
                    let data = {
                        hover_status: post.hover_status,
                        id: post.id,
                        media_url: post.media_url,
                        comments: post.comments,
                        post_id: post.post_id,
                        like_count: post.like_count,
                        link_to_post: post.link_to_post,
                        caption: post.caption,
                        media_type: post.media_type,
                        thumbnail_url: post.thumbnail_url
                    }
                    this.selected_posts.push(data)
                }
            } else {
                this.selected_posts = []
            }
        },
        select_post(post) {
            let self = this
            let count = 0
            let post_index
            let post_data = {
                id: post.id,
                media_url: post.media_url,
                comments: post.comments,
                post_id: post.post_id,
                like_count: post.like_count,
                caption: post.caption,
                media_type: post.media_type,
                thumbnail_url: post.thumbnail_url,
                link_to_post: post.link_to_post,
                hover_status: post.hover_status
            }
            for (let i = 0; i < self.selected_posts.length; i++) {
                if (post_data.id == self.selected_posts[i].id) {
                    count += 1
                    post_index = i
                }
            }
            if (count == 0) {
                self.selected_posts.push(post_data)
            } else {
                self.selected_posts.splice(post_index, 1)
            }
            this.tickAllPosts = this.selected_posts.length == this.posts.length
        },
        deleteChoosePost(post_id) {
            for (let i = 0; i < this.selected_posts.length; i++) {
                if (post_id == this.selected_posts[i].id) {
                    this.selected_posts.splice(i, 1)
                }
            }
            this.tickAllPosts = this.selected_posts.length == this.posts.length
        }
    }
}
</script>
<style scoped>
.setting-btn {
    text-align: right;
    margin-top: 11px;
    margin-right: 30px;
}

#btn-next {
    align-items: center;
    padding: 4px 12px;
    gap: 4px;
    width: 62px;
    height: 32px;
    color: white;
    font-style: normal;
    font-weight: 700;
    border: #1D1E21;
    cursor: pointer;
    font-size: 14px;
    line-height: 24px;
    background: #1D1E21;
    border-radius: 5px;
}

#btn-cancel {
    align-items: center;
    padding: 4px 12px;
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    border: #E2E2E2;
    line-height: 24px;
    color: #000000;
    flex: none;
    order: 1;
    flex-grow: 0;
    cursor: pointer;
    gap: 4px;
    width: 71px;
    height: 32px;
    background: #E2E2E2;
    border-radius: 5px;
    margin-right: 25px;
}

#setting_widget {
    display: flex;
    margin-left: 34px;
    margin-top: 3px;
    align-items: center;
}

#enable_widget {
    width: 127px !important;
    height: 22px !important;
    font-style: normal;
    font-weight: 600;
    font-size: 18px;
    line-height: 22px;
    color: black;
}

.ant-switch {
    margin-left: 28px;
    width: 56px;
}

.blur {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 99;
    opacity: 0.5;
    background-color: white;
    justify-content: center;
}

#choose-post {
    display: flex;
    align-items: center;
}

#choose-post span {
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    margin-left: 10px;
    line-height: 28px;
    display: flex;
    align-items: center;
    color: #202223;
    flex: none;
    order: 1;
    flex-grow: 1;
}

#choose-post svg {
    margin-left: 40px;
    margin-bottom: 1.5px;
    width: 12px;
    height: 12px;
}

.table {
    width: 95%;
    height: 50%;
    margin-left: 1rem;
    margin-top: 1rem;
}

table {
    width: 100%;
    font-size: 14px;
    height: 100%;
    margin-bottom: 15px;
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

.selected_posts {
    margin-left: 21px;
    width: 100%;
    height: max-content;
    margin-top: 13px;
}

.selected_post {
    height: 24px;
    font-style: normal;
    font-weight: 400;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    font-size: 14px;
    background: white;
    margin-right: 15px;
    float: left;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    line-height: 17px;
    color: black;
}

.selected_post svg {
    cursor: pointer;
    margin-left: 5px;
}
</style>