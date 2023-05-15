<template>
    <div>
        <h2 style="text-align: center; margin-top: 20px; margin-bottom: 20px">{{ feed.feed_title }}</h2>
        <Carousel v-bind="{itemsToShow: feed.number_column, snapAlign: 'start', itemsToScroll: feed.number_column}"
                  style="margin-left: 10px; margin-right: 10px; margin-bottom: 10px"
                  v-if="feed.feed_layout == 'slider_squares' && screen_width > 600"
                  :wrap-around="true"
                  :transition="1000"
                  :autoplay="5000">
            <Slide @mouseleave="post.hover_status = false"
                   @mouseenter="post.hover_status = true"
                   v-for="post in feed.selected_posts"
                   :key="post.id">
                <div :style="{padding: feed.post_spacing}"
                     class="carousel__item"
                     style="width: 100%">
                    <img style="width: 100%; object-fit: cover"
                         v-if="post.media_type == 'IMAGE'"
                         :src="post.media_url"
                         :alt="post.caption">
                    <img style="width: 100%; object-fit: cover"
                         v-if="post.media_type == 'VIDEO'"
                         :src="post.thumbnail_url"
                         :alt="post.caption">
                </div>
                <div style="height: 100%; width: 100%"
                     @click="openPost(feed, post)"
                     v-if="post.hover_status"
                     class="post_hover">
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"
                                       icon="fa-brands fa-instagram"/>
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"
                                       icon="fa-solid fa-play"/>
                </div>
            </Slide>
            <template #addons>
                <Navigation/>
            </template>
        </Carousel>
        <Carousel v-bind="{itemsToShow: feed.number_column, snapAlign: 'start', itemsToScroll: feed.number_column}"
                  style="margin-left: 10px; margin-right: 10px; margin-bottom: 10px"
                  v-if="feed.feed_layout == 'slider_tiles' && screen_width > 600"
                  :wrap-around="true"
                  :transition="1000"
                  :autoplay="5000">
            <Slide @mouseleave="post.hover_status = false"
                   @mouseenter="post.hover_status = true"
                   v-for="post in feed.selected_posts"
                   :key="post.id">
                <div class="carousel__item" style="width: 100%" :style="{padding: feed.post_spacing}">
                    <img style="width: 100%; object-fit: cover; height: 500px"
                         v-if="post.media_type == 'IMAGE'"
                         :src="post.media_url"
                         :alt="post.caption">
                    <img style="width: 100%; object-fit: cover; height: 500px"
                         v-if="post.media_type == 'VIDEO'"
                         :src="post.thumbnail_url"
                         :alt="post.caption">
                </div>
                <div style="height: 100%; width: 100%"
                     @click='openPost(feed, post)'
                     v-if="post.hover_status"
                     class="post_hover">
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"
                                       icon="fa-brands fa-instagram"/>
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"
                                       icon="fa-solid fa-play"/>
                </div>
            </Slide>
            <template #addons>
                <Navigation/>
            </template>
        </Carousel>
        <Carousel v-bind="{itemsToShow: feed.number_column, snapAlign: 'start', itemsToScroll: feed.number_column}"
                  style="margin-left: 10px; margin-right: 10px; margin-bottom: 10px"
                  v-if="feed.feed_layout == 'slider_tiles' && screen_width <= 600"
                  :wrap-around="true"
                  :transition="1000"
                  :autoplay="5000">
            <Slide v-for="post in feed.selected_posts"
                   @click="openPost(feed, post)"
                   :key="post.id">
                <div :style="{padding: feed.post_spacing}"
                     class="carousel__item"
                     style="width: 100%">
                    <img style="width: 100%; object-fit: cover; height: 200px"
                         v-if="post.media_type == 'IMAGE'"
                         :src="post.media_url"
                         :alt="post.caption">
                    <img style="width: 100%; object-fit: cover; height: 200px"
                         v-if="post.media_type == 'VIDEO'"
                         :src="post.thumbnail_url"
                         :alt="post.caption">
                </div>
            </Slide>
            <template #addons>
                <Navigation/>
            </template>
        </Carousel>
        <Carousel v-bind="{itemsToShow: feed.number_column, snapAlign: 'start', itemsToScroll: feed.number_column}"
                  v-if="feed.feed_layout == 'slider_squares' && screen_width <= 600"
                  style="margin-left: 10px; margin-right: 10px; margin-bottom: 10px"
                  :wrap-around="true"
                  :transition="1000"
                  :autoplay="5000">
            <Slide v-for="post in feed.selected_posts"
                   @click='openPost(feed, post)'
                   :key="post.id">
                <div :style="{padding: feed.post_spacing}"
                     class="carousel__item"
                     style="width: 100%">
                    <img style="width: 100%; object-fit: cover"
                         v-if="post.media_type == 'IMAGE'"
                         :src="post.media_url"
                         :alt="post.caption">
                    <img style="width: 100%; object-fit: cover"
                         v-if="post.media_type == 'VIDEO'"
                         :src="post.thumbnail_url"
                         :alt="post.caption">
                </div>
            </Slide>
            <template #addons>
                <Navigation/>
            </template>
        </Carousel>
        <div :style="{gridTemplateColumns: `repeat(${feed.number_column}, 1fr)`, gap: feed.post_spacing}"
             style="display: grid; text-align: center; width: 100%; margin-bottom: 10px"
             v-if="feed.feed_layout == 'grid_squares'">
            <div style="position: relative; margin-bottom: 15px"
                 @mouseleave="post.hover_status = false"
                 @mouseenter="post.hover_status = true"
                 v-for="post in feed.selected_posts"
                 :key="post.id"
                 class="post">
                <img v-if="post.media_type == 'IMAGE' && feed.feed_layout == 'grid_squares'"
                     style="width: 100%; object-fit: cover"
                     :src="post.media_url"
                     :alt="post.caption">
                <img v-if="post.media_type == 'VIDEO' && feed.feed_layout == 'grid_squares'"
                     style="width: 100%; object-fit: cover"
                     :src="post.thumbnail_url"
                     :alt="post.caption">
                <div v-if="post.hover_status && feed.feed_layout == 'grid_squares'"
                     style="width: 100%; height: 100%"
                     @click='openPost(feed, post)'
                     class="post_hover">
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"
                                       icon="fa-brands fa-instagram"/>
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"
                                       icon="fa-solid fa-play"/>
                </div>
            </div>
        </div>
        <div :style="{gridTemplateColumns: `repeat(${feed.number_column}, 1fr)`, gap: feed.post_spacing}"
             style="display: grid; text-align: center; width: 100%; margin-bottom: 10px"
             v-if="feed.feed_layout == 'grid_tiles' && screen_width > 600">
            <div style="position: relative; width: 100%; height: 500px"
                 @mouseleave="post.hover_status = false"
                 @mouseenter="post.hover_status = true"
                 v-for="post in feed.selected_posts"
                 :key="post.id"
                 class="post">
                <img style="width: 100%; object-fit: cover; height: 100%"
                     v-if="post.media_type == 'IMAGE'"
                     :src="post.media_url"
                     :alt="post.caption">
                <img style="width: 100%; object-fit: cover; height: 100%"
                     v-if="post.media_type == 'VIDEO'"
                     :src="post.thumbnail_url"
                     :alt="post.caption">
                <div style="width: 100%; height: 100%"
                     @click='openPost(feed, post)'
                     v-if="post.hover_status"
                     class="post_hover">
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"
                                       icon="fa-brands fa-instagram"/>
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"
                                       icon="fa-solid fa-play"/>
                </div>
            </div>
        </div>
        <div :style="{gridTemplateColumns: `repeat(${feed.number_column}, 1fr)`, gap: feed.post_spacing}"
             style="display: grid; text-align: center; width: 100%; margin-bottom: 10px"
             v-if="feed.feed_layout == 'grid_tiles' && screen_width <= 600">
            <div style="position: relative; width: 100%; height: 200px"
                 @mouseleave="post.hover_status = false"
                 @mouseenter="post.hover_status = true"
                 v-for="post in feed.selected_posts"
                 :key="post.id"
                 class="post">
                <img style="width: 100%; object-fit: cover; height: 100%"
                     v-if="post.media_type == 'IMAGE'"
                     :src="post.media_url"
                     :alt="post.caption">
                <img style="width: 100%; object-fit: cover; height: 100%"
                     v-if="post.media_type == 'VIDEO'"
                     :src="post.thumbnail_url"
                     :alt="post.caption">
                <div style="width: 100%; height: 100%"
                     @click='openPost(feed, post)'
                     v-if="post.hover_status"
                     class="post_hover">
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'IMAGE'"
                                       icon="fa-brands fa-instagram"/>
                    <font-awesome-icon style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type == 'VIDEO'"
                                       icon="fa-solid fa-play"/>
                </div>
            </div>
        </div>
        <Modal @cancel="selected_post = {}; selected_feed = {}"
               v-model:visible="post_modal"
               v-if="screen_width > 600"
               :maskClosable="false"
               style="width: 750px"
               :footer="null">
            <div style="display: flex">
                <img v-if="selected_post.media_type == 'IMAGE'"
                     style="width: 50%; height: 50%"
                     :src="selected_post.media_url"
                     :alt="selected_post.caption">
                <video v-if="selected_post.media_type == 'VIDEO'"
                       height="400"
                       autoplay>
                    <source :src="selected_post.media_url">
                </video>
                <div style="width: 100%; display: flex; flex-direction: column">
                    <div style="margin-left: 20px; display: flex; background-color: white; align-items: center">
                        <div style="display: flex; justify-content: center; align-items: center; border: 1px solid #E2E2E2; border-radius: 50%; height: 40px; width: 40px">
                            <img style="height: 40px; width: 40px; object-fit: cover"
                                 :src="instagram_avatar"
                                 :alt="instagram_user">
                        </div>
                        <div style="cursor: pointer; color: black; font-weight: 600; line-height: 23px; font-size: 17px; margin-left: 15px"
                             @click="redirectToInstagramUser">
                            {{ instagram_user }}
                        </div>
                    </div>
                    <div style="display: flex">
                        <button @click="previous_post(selected_post.id)"
                                style="margin-left: 20px"
                                class="btn_post">
                            <font-awesome-icon style="color: black; font-size: 30px"
                                               icon="fa-solid fa-caret-left"/>
                        </button>
                        <button @click="next_post(selected_post.id)"
                                style="right: 0; margin-left: auto"
                                class="btn_post">
                            <font-awesome-icon style="color: black; font-size: 30px"
                                               icon="fa-solid fa-caret-right"/>
                        </button>
                    </div>
                    <div style="margin-left: 10px">
                        <div>{{ selected_post.caption }}</div>
                        <div style="border-bottom: 1px solid #dcdcdc">{{ selected_post.like_count }}
                            <font-awesome-icon icon="fa-regular fa-heart"
                                               style="color: black"/>
                        </div>
                        <div v-if="selected_feed.on_post_click == 'open'">
                            <div v-for="line in JSON.parse(selected_feed.list_tag)"
                                 style="justify-content: center; display: flex; flex-direction: column">
                                <div v-if="line.post_id == selected_post.id">

                                </div>
                                <button v-if="line.post_id == selected_post.id"
                                        @click="openProduct(line.product_id)"
                                        class="shop_now">
                                    Shop now
                                </button>
                            </div>
                        </div>
                        <div v-if="comments">
                            <div :key="comment.id" v-for="comment in comments">
                                <div>{{ comment['username'] }}: {{ comment['text'] }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
        <Modal @cancel="selected_post = {}; selected_feed = {}"
               style="margin-left: 10%; width: 50%"
               v-model:visible="post_modal"
               v-if="screen_width <= 600"
               :maskClosable="false"
               :footer="null">
            <div style="display: flex; flex-direction: column">
                <img v-if="selected_post.media_type == 'IMAGE'"
                     :src="selected_post.media_url"
                     :alt="selected_post.caption"
                     style="width: 100%">
                <video v-if="selected_post.media_type == 'VIDEO'"
                       height="400"
                       autoplay>
                    <source :src="selected_post.media_url">
                </video>
                <div style="width: 100%; display: flex; flex-direction: column">
                    <div style="margin-left: 20px; display: flex; background-color: white; align-items: center">
                        <div style="display: flex; justify-content: center; align-items: center; border: 1px solid #E2E2E2; border-radius: 50%; height: 40px; width: 40px">
                            <img style="height: 40px; width: 40px; object-fit: cover"
                                 :src="instagram_avatar"
                                 :alt="instagram_user">
                        </div>
                        <div style="cursor: pointer; color: black; font-weight: 600; line-height: 23px; font-size: 17px; margin-left: 15px"
                             @click="redirectToInstagramUser">
                            {{ instagram_user }}
                        </div>
                    </div>
                    <div style="margin-left: 10px">
                        <div>{{ selected_post.caption }}</div>
                        <div style="border-bottom: 1px solid #dcdcdc">{{ selected_post.like_count }}
                            <font-awesome-icon icon="fa-regular fa-heart"
                                               style="color: black"/>
                        </div>
                        <div v-if="selected_feed.on_post_click == 'open'">
                            <div v-for="line in JSON.parse(selected_feed.list_tag)"
                                 style="display: flex; justify-content: center">
                                <button v-if="line.post_id == selected_post.id"
                                        @click="openProduct(line.product_id)"
                                        class="shop_now">
                                    Shop now
                                </button>
                            </div>
                        </div>
                        <div v-if="comments">
                            <div :key="comment.id" v-for="comment in comments">
                                <div>{{ comment['username'] }}: {{ comment['text'] }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
    </div>
</template>
<script>
import {Carousel, Navigation, Slide} from "vue3-carousel"
import 'vue3-carousel/dist/carousel.css'
import {Modal} from "ant-design-vue"
import axios from 'axios'

export default {
    name: "Shopify",
    components: {Carousel, Modal, Navigation, Slide},
    data() {
        return {
            feed: {},
            selected_post: {},
            post_modal: false,
            comments: [],
            instagram_user: '',
            selected_feed: {},
            screen_width: 0,
            instagram_avatar: ''
        }
    },
    methods: {
        previous_post(current_post_id) {
            let self = this
            for (let i = 0; i < self.feed.selected_posts.length; i++) {
                if (current_post_id == self.feed.selected_posts[i].id) {
                    if (i == 0) {
                        self.selected_post = self.feed.selected_posts[self.feed.selected_posts.length - 1]
                    } else {
                        self.selected_post = self.feed.selected_posts[i - 1]
                    }
                    if (self.selected_post.comments) {
                        self.comments = JSON.parse(self.selected_post.comments)
                    } else {
                        self.comments = []
                    }
                }
            }
        },
        next_post(current_post_id) {
            let self = this
            for (let i = 0; i < self.feed.selected_posts.length; i++) {
                if (current_post_id == self.feed.selected_posts[i].id) {
                    if (i == self.feed.selected_posts.length - 1) {
                        self.selected_post = self.feed.selected_posts[0]
                    } else {
                        self.selected_post = self.feed.selected_posts[i + 1]
                    }
                    if (self.selected_post.comments) {
                        self.comments = JSON.parse(self.selected_post.comments)
                    } else {
                        self.comments = []
                    }
                }
            }
        },
        openProduct(product_id) {
            axios.post('/apps/lmao/shopify/get_product', {
                jsonrpc: "2.0",
                params: {
                    product_id: product_id,
                    shop_url: window.location.origin
                }
            }).then(res => {
                window.location.href = res.data.result.kw_product.url
            }).catch(error => {
                console.log(error)
            })
        },
        redirectToInstagramUser() {
            window.open("https://www.instagram.com/" + this.instagram_user, '_blank')
        },
        openPost(feed, post) {
            let self = this
            if (feed.on_post_click == 'open') {
                self.selected_post = JSON.parse(JSON.stringify(post))
                self.selected_feed = JSON.parse(JSON.stringify(feed))
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
        }
    },
    mounted() {
        let self = this
        axios.post('/apps/lmao/instafeed/get_feed', {
            jsonrpc: '2.0',
            params: {
                feed_id: self.$.attrs.data.feed_id,
                shop_url: window.location.origin
            }
        }).then(res => {
            if (res.data.result.list_feed) {
                self.feed = res.data.result.list_feed[0]
            }
            if (res.data.result.instagram_user) {
                self.instagram_user = res.data.result.instagram_user
                self.instagram_avatar = res.data.result.instagram_avatar
            }
        }).catch(error => {
            console.log(error)
        })
        self.screen_width = screen.width
    }
}
</script>
<style scoped>
#preview {
    margin-left: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #e2e2e2;
    width: 100%;
    margin-right: 10px;
}

.shop_now {
    background: #51baf7;
    color: white;
    line-height: 30px;
    font-weight: 700;
    border-radius: 3px;
    margin-top: 10px;
    border: 0;
    text-align: center;
    width: 150px;
    text-transform: uppercase;
    cursor: pointer;
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
    background: #151515;
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
.carousel__prev, .carousel__next {
    border: 1px solid #efefef;
    height: 25px;
    width: 25px;
    background: #efefef;
    border-radius: 50%;
}

.btn_post {
    cursor: pointer;
    border: 0;
    background: white;
}

.ant-modal-close-x {
    height: 16px !important;
    width: 16px !important;
    line-height: 16px !important;
}

.ant-modal-close {
    margin-top: 5px;
    margin-right: 5px;
}
</style>