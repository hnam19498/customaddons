<template>
    <div :key="feed.id" id="preview" v-for="feed in list_feed">
        <h2 style="text-align: center; margin-top: 20px; margin-bottom: 15px">{{ feed.feed_title }}</h2>
        <Carousel style="margin-left: 10px; margin-right: 10px"
                  :items-to-show="feed.number_column"
                  v-if="feed.feed_layout.includes('slider')"
                  :wrap-around="true">
            <Slide v-for="post in feed.selected_posts" :key="post.id">
                <div class="carousel__item" @click='openPost(feed, post)'>
                    <img v-if="post.media_type == 'IMAGE' && feed.feed_layout == 'slider_squares'"
                         :alt="post.caption"
                         style="height: 150px; width: 150px; object-fit: cover"
                         :src="post.media_url">
                    <img v-if="post.media_type == 'VIDEO' && feed.feed_layout == 'slider_squares'"
                         :alt="post.caption"
                         style="height: 150px; width: 150px; object-fit: cover"
                         :src="post.thumbnail_url">
                    <img v-if="post.media_type == 'IMAGE' && feed.feed_layout == 'slider_tiles'"
                         :alt="post.caption"
                         style="height: 250px; width: 150px; object-fit: cover"
                         :src="post.media_url">
                    <img v-if="post.media_type == 'VIDEO' && feed.feed_layout == 'slider_tiles'"
                         :alt="post.caption"
                         style="height: 250px; width: 150px; object-fit: cover"
                         :src="post.thumbnail_url">
                </div>
            </Slide>
            <template #addons>
                <Navigation/>
            </template>
        </Carousel>
        <div style="display: grid; text-align: center"
             v-if="feed.feed_layout.includes('grid')"
             :style="{gridTemplateColumns: `repeat(${feed.number_column}, 1fr)`}">
            <div :key="post.id"
                 @mouseenter="post.hover_status = true"
                 @mouseleave="post.hover_status = false"
                 v-for="post in feed.selected_posts"
                 style="position: relative; margin-bottom: 15px"
                 class="post">
                <img v-if="post.media_type == 'IMAGE' && feed.feed_layout == 'grid_squares'"
                     :alt="post.caption"
                     style="height: 150px; width: 150px; object-fit: cover"
                     :src="post.media_url">
                <img v-if="post.media_type == 'VIDEO' && feed.feed_layout == 'grid_squares'"
                     :alt="post.caption"
                     style="height: 150px; width: 150px; object-fit: cover"
                     :src="post.thumbnail_url">
                <img v-if="post.media_type == 'IMAGE' && feed.feed_layout == 'grid_tiles'"
                     :alt="post.caption"
                     style="height: 250px; width: 150px; object-fit: cover"
                     :src="post.media_url">
                <img v-if="post.media_type == 'VIDEO' && feed.feed_layout == 'grid_tiles'"
                     :alt="post.caption"
                     style="height: 250px; width: 150px; object-fit: cover"
                     :src="post.thumbnail_url">
                <div v-if="post.hover_status && feed.feed_layout == 'grid_squares'"
                     class="post_hover"
                     style="height: 150px; width: 150px"
                     @click='openPost(feed, post)'>
                    <font-awesome-icon icon="fa-brands fa-instagram"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"/>
                    <font-awesome-icon icon="fa-solid fa-play"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"/>
                </div>
                <div v-if="post.hover_status && feed.feed_layout == 'grid_tiles'"
                     class="post_hover"
                     style="height: 250px; width: 150px"
                     @click='openPost(feed, post)'>
                    <font-awesome-icon icon="fa-brands fa-instagram"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"/>
                    <font-awesome-icon icon="fa-solid fa-play"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"/>
                </div>
            </div>
        </div>
    </div>
    <Modal :footer="null"
           v-model:visible="post_modal"
           :maskClosable="false"
           @cancel="selected_post={}">
        <div style="display: flex">
            <img v-if="selected_post.media_type=='IMAGE'"
                 :src="selected_post.media_url"
                 :alt="selected_post.caption"
                 style="width: 50%; height: 50%">
            <video height="400" autoplay v-if="selected_post.media_type=='VIDEO'">
                <source :src="selected_post.media_url">
            </video>
            <div style="width: 100%; display: flex; flex-direction: column">
                <div style="margin-left:20px; display: flex; background-color: white; align-items: center">
                    <div style="display: flex; justify-content: center; align-items: center;border: 1px solid #E2E2E2; border-radius: 50%; height: 40px; width: 40px">
                        <font-awesome-icon icon="fa-brands fa-instagram"
                                           style="height:30px; width: 30px; color: black"/>
                    </div>
                    <div @click="redirectToInstagramUser"
                         style="cursor: pointer; color: #000; font-weight: 600; line-height: 23px; font-size: 17px; margin-left: 15px">
                        {{ instagram_user }}
                    </div>
                </div>
                <div style="margin-left: 10px">
                    <div>{{ selected_post.caption }}</div>
                    <div style="border-bottom: 1px solid #dcdcdc">{{ selected_post.like_count }} ❤️</div>
                    <div v-if="comments" v-for="comment in comments">
                        <div>{{ comment['username'] }}: {{ comment['text'] }}</div>
                    </div>
                </div>
            </div>
        </div>
    </Modal>
</template>

<script>
import axios from 'axios'
import {Carousel, Navigation, Slide} from "vue3-carousel"
import {Modal} from "ant-design-vue"
import 'vue3-carousel/dist/carousel.css'

export default {
    name: "Shopify",
    components: {
        Carousel,
        Modal,
        Navigation,
        Slide
    },
    data() {
        return {
            list_feed: [],
            selected_post: {},
            post_modal: false,
            comments: [],
            instagram_user: ''
        }
    },
    methods: {
        redirectToInstagramUser() {
            window.open("https://www.instagram.com/" + this.instagram_user, '_blank')
        },
        openPost(feed, post) {
            let self = this
            if (feed.on_post_click == 'open') {
                self.selected_post = post
                self.post_modal = true
                if (self.selected_post.comments) {
                    self.comments = JSON.parse(self.selected_post.comments)
                } else {
                    self.comments = []
                }
            }
            if (feed.on_post_click == 'instagram') {
                window.open(post.link_to_post, '_blank')
            }
        },
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/instafeed/get_feed', {
            jsonrpc: "2.0",
            params: {
                shop_url: window.location.origin
            }
        }).then(res => {
            if (res.data.result.list_feed) {
                self.list_feed = res.data.result.list_feed
            }
            if (res.data.result.instagram_user) {
                self.instagram_user = res.data.result.instagram_user
            }
            console.log(self.list_feed)
        }).catch(error => {
            console.log(error)
        })
    }
}
</script>

<style scoped>
#preview {
    margin-left: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #E2E2E2;
    width: 100%;
    margin-right: 10px;
}

.post_hover {
    cursor: pointer;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 20;
    position: absolute;
    opacity: 0.5;
    background: #151515
}

.post {
    position: relative;
}

.post img:hover {
    opacity: 0.5;
    cursor: pointer;
}

.carousel__item {
    min-height: 150px;
    width: 100%;
    background-color: white;
    display: flex;
    cursor: pointer;
    justify-content: center;
    align-items: center;
}
</style>
<style>
.carousel__prev {
    border: 1px solid #EFEFEF;
    height: 25px;
    width: 25px;
    background: #EFEFEF;
    border-radius: 50%;
}

.carousel__next {
    border: 1px solid #EFEFEF;
    background: #EFEFEF;
    height: 25px;
    width: 25px;
    border-radius: 50%;
}
</style>