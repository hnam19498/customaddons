<template>
    <div style="display: flex; margin-bottom: 10px">
        <div id="setting_feed">
            <div style="background: white">
                <div style="margin-top: 5px; display: flex; flex-direction: column; margin-left: 5px; margin-right: 5px">
                    <span class="label">FEED TITLE</span>
                    <input v-model="feed_title" type="text"
                           style="border-radius: 5px; border: 1px solid #E2E2E2; height: 30px">
                    <div style="display: flex; justify-content: space-between; margin-top: 15px">
                        <div class="feed_setting" style="width: 40%; margin-right: 10px">
                            <span class="label">POST SPACING</span>
                            <select>
                                <option value="no spacing">No spacing</option>
                                <option value="small">Small</option>
                                <option value="medium">Medium</option>
                                <option value="large">Large</option>
                            </select>
                        </div>
                        <div class="feed_setting" style="width: 60%">
                            <span class="label">ON POST CLICK</span>
                            <select v-model="on_post_click">
                                <option value="open">Open popup / show product</option>
                                <option value="instagram">Go to Instagram</option>
                                <option value="nothing">Do nothing</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px">
                        <div class="feed_setting" style="width: 50%; margin-right: 10px">
                            <span class="label">LAYOUT</span>
                            <select v-model="feed_layout">
                                <option value="grid_squares">Grid - Squares</option>
                                <option value="grid_tiles">Grid - Tiles</option>
                                <option value="slider_squares">Slider - Squares</option>
                                <option value="slider_tiles">Slider - Tiles</option>
                            </select>
                        </div>
                        <div class="feed_setting" style="width: 50%">
                            <span class="label">CONFIGURATION</span>
                            <select v-model="configuration_select">
                                <option value="auto">AUTO</option>
                                <option value="manual">Manual</option>
                            </select>
                        </div>
                    </div>
                    <div class="feed_setting" style="width: 100%; margin-top: 15px">
                        <span class="label">COLUMNS</span>
                        <input v-model="number_column"
                               min="1" max="6"
                               v-if="configuration_select=='manual'"
                               type="number">
                        <input value="AUTO"
                               v-if="configuration_select=='auto'"
                               disabled>
                    </div>
                    <button @click="save_feed" id="btn_save">Save feed</button>
                    <div style="display: flex">
                        <div style="width: 50%">
                            <button style="width: 100%" id="btn_back" @click="backToSelectPost">
                                <font-awesome-icon icon="fa-solid fa-arrow-left" style="color: white"/>
                            </button>
                        </div>
                        <div style="width: 50%; margin-left: 10px">
                            <button id="btn_cancel" @click="cancelFeed" style="width: 100%">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="preview">
            <div style="margin-right: 10px; border-bottom: 1px groove #dcdcdc; font-weight: 700; margin-left: 10px; margin-top: 5px">
                PREVIEW
            </div>
            <h2 style="text-align: center; margin-top: 20px; margin-bottom: 15px">{{ feed_title }}</h2>
            <Carousel style="margin-left: 10px; margin-right: 10px"
                      :items-to-show="number_column"
                      :wrap-around="true"
                      v-if="feed_layout.includes('slider')">
                <Slide v-for="post in selected_posts" :key="post.id">
                    <div class="carousel__item" @click='openPost(post)'>
                        <img v-if="post.media_type == 'IMAGE' && feed_layout == 'slider_squares'"
                             :alt="post.caption"
                             style="height: 150px; width: 150px; object-fit: cover"
                             :src="post.media_url">
                        <img v-if="post.media_type == 'VIDEO' && feed_layout == 'slider_squares'"
                             :alt="post.caption"
                             style="height: 150px; width: 150px; object-fit: cover"
                             :src="post.thumbnail_url">
                        <img v-if="post.media_type == 'IMAGE' && feed_layout == 'slider_tiles'"
                             :alt="post.caption"
                             style="height: 250px; width: 150px; object-fit: cover"
                             :src="post.media_url">
                        <img v-if="post.media_type == 'VIDEO' && feed_layout == 'slider_tiles'"
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
                 v-if="feed_layout.includes('grid')"
                 :style="{gridTemplateColumns: `repeat(${number_column}, 1fr)`}">
                <div :key="post.id"
                     @mouseenter="post.hover_status = true"
                     @mouseleave="post.hover_status = false"
                     v-for="post in selected_posts"
                     style="position: relative; margin-bottom: 15px"
                     class="post">
                    <img v-if="post.media_type == 'IMAGE' && feed_layout == 'grid_squares'"
                         :alt="post.caption"
                         style="height: 150px; width: 150px; object-fit: cover"
                         :src="post.media_url">
                    <img v-if="post.media_type == 'VIDEO' && feed_layout == 'grid_squares'"
                         :alt="post.caption"
                         style="height: 150px; width: 150px; object-fit: cover"
                         :src="post.thumbnail_url">
                    <img v-if="post.media_type == 'IMAGE' && feed_layout == 'grid_tiles'"
                         :alt="post.caption"
                         style="height: 250px; width: 150px; object-fit: cover"
                         :src="post.media_url">
                    <img v-if="post.media_type == 'VIDEO' && feed_layout == 'grid_tiles'"
                         :alt="post.caption"
                         style="height: 250px; width: 150px; object-fit: cover"
                         :src="post.thumbnail_url">
                    <div v-if="post.hover_status && feed_layout == 'grid_squares'"
                         class="post_hover"
                         style="height: 150px; width: 150px"
                         @click='openPost(post)'>
                        <font-awesome-icon icon="fa-brands fa-instagram"
                                           style="color: white; height: 30px; width: 30px"
                                           v-if="post.media_type == 'IMAGE'"/>
                        <font-awesome-icon icon="fa-solid fa-play"
                                           style="color: white; height: 30px; width: 30px"
                                           v-if="post.media_type == 'VIDEO'"/>
                    </div>
                    <div v-if="post.hover_status && feed_layout == 'grid_tiles'"
                         class="post_hover"
                         style="height: 250px; width: 150px"
                         @click='openPost(post)'>
                        <font-awesome-icon icon="fa-brands fa-instagram"
                                           style="color: white; height: 30px; width: 30px"
                                           v-if="post.media_type == 'IMAGE'"/>
                        <font-awesome-icon icon="fa-solid fa-play"
                                           style="color: white; height: 30px; width: 30px"
                                           v-if="post.media_type == 'VIDEO'"/>
                    </div>
                </div>
            </div>
            <div style="color: #707070; margin-left: 10px">
                <i><b>Tip:</b> Click on a post to start tagging products</i>
            </div>
        </div>
        <Modal style="width: 70%"
               :footer="null"
               v-model:visible="post_modal"
               :maskClosable="false"
               @cancel="selected_post={}">
            <div style="display: flex">
                <img v-if="selected_post.media_type == 'IMAGE'"
                     :src="selected_post.media_url"
                     :alt="selected_post.caption"
                     style="width: 50%; height: 50%">
                <video height="400" autoplay v-if="selected_post.media_type == 'VIDEO'">
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
                    <div style="display: flex; justify-content: center; text-align: center">
                        <button @click="tag_modal = true" class="tag_product">Tag product</button>
                    </div>
                    <div style="margin-left: 10px">
                        <div>{{ selected_post.caption }}</div>
                        <div style="border-bottom: 1px solid #dcdcdc">
                            {{ selected_post.like_count }}
                            <font-awesome-icon icon="fa-regular fa-heart" beat style="color: black" />
                        </div>
                        <div v-if="comments" v-for="comment in comments">
                            <div>{{ comment['username'] }}: {{ comment['text'] }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </Modal>
        <Modal style="width: 70%"
               title="Thêm sản phẩm"
               @cancel="cancelTab"
               v-model:visible="tag_modal"
               @ok="submitTab(this.current_list_tag)"
               :maskClosable="false">
            <a-input v-model:value="search" placeholder="Basic usage">
                <template #prefix>
                    <SearchOutlined/>
                </template>
            </a-input>
            <table>
                <tr v-for="product in list_product_filter"
                    :key="product.id"
                    class="table-row"
                    @click="tagProduct(selected_post, product)"
                    style="width: 100%">
                    <td>
                        <input type="checkbox"
                               :checked="list_tag.filter(e => e.product_id == product.id).length > 0 || current_list_tag.filter(e => e.product_id == product.id).length > 0"
                               :disabled="list_tag.filter(e => e.product_id == product.id).length > 0"
                               style="margin-left: 10px">
                    </td>
                    <td><img style="width: 50px; margin-left: 20px" :src="product.url_img" :alt="product.name"></td>
                    <td style="width: 100%">
                        <div style="margin-left: 20px">{{ product.name }}</div>
                    </td>
                </tr>
            </table>
        </Modal>
    </div>
</template>
<script>
import {Modal, notification} from 'ant-design-vue'
import {Carousel, Navigation, Slide} from 'vue3-carousel'
import 'vue3-carousel/dist/carousel.css'
import {SearchOutlined} from "@ant-design/icons-vue"
import axios from "axios"
import {h} from 'vue'
import {LeftCircleOutlined, RightCircleOutlined, CloseCircleFilled} from '@ant-design/icons-vue'

export default {
    name: "FeedSettings",
    components: {
        CloseCircleFilled,
        Modal,
        Carousel,
        Navigation,
        Slide,
        SearchOutlined,
        LeftCircleOutlined,
        RightCircleOutlined
    },
    props: {
        selected_posts: {
            type: Array,
            default: []
        }
    },
    data() {
        return {
            list_tag: [],
            on_post_click: "open",
            search: '',
            feed_layout: 'grid_squares',
            feed_title: 'EDIT FEED TITLE',
            post_modal: false,
            selected_post: {},
            instagram_user: '',
            tag_modal: false,
            comments: [],
            list_product: [],
            number_column: 3,
            current_list_tag: [],
            configuration_select: 'auto'
        }
    },
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
        save_feed() {
            let self = this
            if (self.selected_posts.length == 0) {
                console.log(self.selected_posts)
                this.show_toast(
                    'open',
                    'Please select at least 1 post at SelectPost before continue.',
                    3
                )
            } else {
                if (self.configuration_select == 'auto') {
                    self.number_column = 3
                }
                axios.post('https://odoo.website/instafeed/save_feed', {
                    jsonrpc: "2.0",
                    params: {
                        list_tag: self.list_tag,
                        feed_title: self.feed_title,
                        number_column: self.number_column,
                        on_post_click: self.on_post_click,
                        feed_layout: self.feed_layout,
                        selected_posts: self.selected_posts
                    }
                }).then(res => {
                    if (res.data.result.success) {
                        alert("Saved!")
                    } else {
                        alert(res.data.result.error)
                    }
                }).catch(error => {
                    console.log(error)
                })
            }
        },
        cancelFeed() {
            this.number_column = 3
            this.feed_title = ''
            this.search = ''
            this.post_modal = false
            this.selected_post = {}
            this.instagram_user = ''
            this.current_list_tag = []
            this.list_tag = []
            this.tag_modal = false
            this.list_product = []
        },
        cancelTab() {
            let self = this
            self.current_list_tag = []
            self.tag_modal = false
            self.search = ''
        },
        submitTab(current_list_tag) {
            let self = this
            self.list_tag.push(...current_list_tag)
            self.current_list_tag = []
            self.tag_modal = false
            self.search = ""
            self.post_modal = false
        },
        tagProduct(selected_post, product) {
            let self = this
            let count = 0
            for (let line of self.current_list_tag) {
                if (line.post_id == selected_post.id && line.product_id == product.id) {
                    count += 1
                }
            }
            if (count == 0) {
                self.current_list_tag.push({post_id: selected_post.id, product_id: product.id})
            }
        },
        backToSelectPost() {
            this.feed_title = ''
            this.post_modal = false
            this.selected_post = {}
            this.instagram_user = ''
            this.number_column = 3
            this.current_list_tag = []
            this.list_tag = []
            this.search = ""
            this.tag_modal = false
            this.list_product = []
            this.$emit('changeTab', 'SelectPost')
        },
        openPost(post) {
            let self = this
            if (self.on_post_click == 'open') {
                self.selected_post = post
                self.search = ''
                self.post_modal = true
                if (self.selected_post.comments) {
                    self.comments = JSON.parse(self.selected_post.comments)
                } else {
                    self.comments = []
                }
            }
            if (self.on_post_click == 'instagram') {
                window.open(post.link_to_post, '_blank')
            }

        },
        redirectToInstagramUser() {
            window.open('https://www.instagram.com/' + this.instagram_user, '_blank')
        }
    },
    emits: ['changeTab'],
    mounted() {
        let self = this
        self.instagram_user = window.instafeed.users.instagram_username
        axios.post('https://odoo.website/shopify/get_product', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            self.list_product = res.data.result.list_product
        }).catch(error => {
            console.log(error)
        })
    },
    computed: {
        list_product_filter() {
            let self = this
            return self.list_product.filter(product => product.name.toLowerCase().includes(self.search.toLowerCase())
            )
        }
    }
}
</script>
<style scoped>
#preview {
    margin-left: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #E2E2E2;
    width: 73%;
    margin-right: 10px;
}

#setting_feed {
    display: flex;
    margin-left: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #E2E2E2;
}

.label {
    font-weight: 700;
    color: #212b35;
}

.feed_setting {
    display: flex;
    flex-direction: column;
}

.feed_setting select {
    height: 30px;
    border-radius: 5px;
    background: white;
    border: 1px solid #E2E2E2;
}

.feed_setting input {
    border-radius: 5px;
    border: 1px solid #E2E2E2;
    height: 30px;
}

#btn_save {
    background: rgb(0 128 96);
    color: white;
    font-weight: 400;
    margin-top: 15px;
    cursor: pointer;
    height: 30px;
    border-radius: 5px;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    margin-bottom: 10px;
}

#btn_back {
    background: rgb(59, 59, 59);
    color: white;
    font-weight: 400;
    height: 30px;
    cursor: pointer;
    border-radius: 5px;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    margin-bottom: 10px;
}

#btn_cancel {
    background: red;
    color: white;
    font-weight: 400;
    height: 30px;
    cursor: pointer;
    border-radius: 5px;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    margin-bottom: 10px;
}

.post {
    position: relative;
}

.post img:hover {
    opacity: 0.5;
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
    background: #151515
}

.tag_product {
    color: white;
    min-height: 35px;
    min-width: 100px;
    border-radius: 4px;
    background: rgb(0 128 96);
    cursor: pointer;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    font-weight: 400;
}

.ant-input-affix-wrapper {
    border-radius: 5px;
}

.table-row {
    height: 3rem;
    border-bottom: 1px groove #EFEFEF;
    font-size: 14px;
}

tr {
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