<template>
    <div id="preview">
        <div style="margin-right: 10px; border-bottom: 1px groove #dcdcdc; font-weight: 700; margin-left: 10px; margin-top: 5px">
            PREVIEW
        </div>
        <h2 style="text-align: center; margin-top: 20px; margin-bottom: 15px">{{ feed_title }}</h2>
        <div style="display: grid; text-align: center"
             :style="{gridTemplateColumns: `repeat(${number_column}, 1fr)`}"
             class="posts">
            <div :key="post.id"
                 @mouseenter="post.hover_status = true"
                 @mouseleave="post.hover_status = false"
                 v-for="post in selected_posts"
                 style="position: relative; margin-bottom: 15px"
                 class="post">
                <img v-if="post.media_type == 'IMAGE'"
                     :alt="post.caption"
                     style="height: 150px; width: 150px; object-fit: cover"
                     :src="post.media_url">
                <img v-if="post.media_type == 'VIDEO'"
                     :alt="post.caption"
                     style="height: 150px; width: 150px; object-fit: cover"
                     :src="post.thumbnail_url">
                <div v-if="post.hover_status"
                     class="post_hover"
                     @click='openPost(post)'>
                    <font-awesome-icon icon="fa-brands fa-instagram"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type=='IMAGE'"/>
                    <font-awesome-icon icon="fa-solid fa-play"
                                       style="color: white; height: 30px; width: 30px"
                                       v-if="post.media_type=='VIDEO'"/>
                </div>
            </div>
        </div>
        <div style="color: #707070"><i><b>Tip:</b> Click on a post to start tagging products</i></div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Shopify",
    data() {
        return {}
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/instafeed/get_feed',{
            
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
</style>