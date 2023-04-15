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
                            <select>
                                <option value="open">Open popup / show product</option>
                                <option value="instagram">Go to Instagram</option>
                                <option value="nothing">Do nothing</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px">
                        <div class="feed_setting" style="width: 50%; margin-right: 10px">
                            <span class="label">LAYOUT</span>
                            <select>
                                <option value="grid_squares">Grid - Squares</option>
                                <option value="grid_tiles">Grid - Tiles</option>
                                <option value="slider_squares">Slider - Squares</option>
                                <option value="slider_tiles">Slider - Tiles</option>
                            </select>
                        </div>
                        <div class="feed_setting" style="width: 50%">
                            <span class="label">CONFIGURATION</span>
                            <select>
                                <option value="auto">AUTO</option>
                                <option value="manual">Manual</option>
                            </select>
                        </div>
                    </div>
                    <div class="feed_setting" style="width: 100%">
                        <span class="label">COLUMNS</span>
                        <input type="number">
                    </div>
                    <button id="btn_save" style="margin-top: 15px">Save feed</button>
                </div>
            </div>
        </div>
        <div id="preview">
            <div style="margin-right: 10px; border-bottom: 1px groove #dcdcdc; font-weight: 700; margin-left: 10px; margin-top: 5px">
                PREVIEW
            </div>
            <h2 style="text-align: center; margin-top: 20px; margin-bottom: 15px">{{ feed_title }}</h2>
            <div class="posts" style="display: grid; text-align: center; grid-template-columns: repeat(3, 1fr)">
                <div :key="post.id"
                     @mouseenter="post.hover_status = true"
                     @mouseleave="post.hover_status = false"
                     v-for="post in selected_posts"
                     style="position: relative; margin-bottom: 15px"
                     class="post">
                    <img v-if="post.media_type == 'IMAGE'"
                         :alt="post.caption"
                         style="height: 200px; width: 200px; object-fit: cover"
                         :src="post.media_url">
                    <img v-if="post.media_type == 'VIDEO'"
                         :alt="post.caption"
                         style="height: 200px; width: 200px; object-fit: cover"
                         :src="post.thumbnail_url">
                    <div v-if="post.hover_status"
                         style="justify-content: center; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 20; width: 200px; height: 200px; position: absolute; opacity: 0.5; background: red"
                         @click='openTagProduct(post.id)'/>
                </div>
            </div>
            <div style="color: #707070"><i><b>Tip:</b> Click on a post to start tagging products</i></div>
        </div>
    </div>
</template>
<script>
export default {
    name: "FeedSettings",
    props: {
        selected_posts: {
            type: Array,
            default: []
        }
    },
    data() {
        return {
            feed_title: '',

        }
    },
    methods: {
        openTagProduct(post_id) {
            console.log(post_id);
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
    width: 100%;
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
    height: 30px;
    border-radius: 5px;
    border: .1rem solid transparent;
    box-shadow: inset 0 1px 0 0 transparent, 0 1px 0 0 rgb(22 29 37/5%), 0 0 0 0 transparent;
    margin-bottom: 10px;
}

.ant-carousel :deep(.slick-slide) {
    text-align: center;
    height: 160px;
    line-height: 160px;
    background: #364d79;
    overflow: hidden;
}

.ant-carousel :deep(.slick-arrow.custom-slick-arrow) {
    width: 25px;
    height: 25px;
    font-size: 25px;
    color: #fff;
    background-color: rgba(31, 45, 61, 0.11);
    opacity: 0.3;
    z-index: 1;
}

.ant-carousel :deep(.custom-slick-arrow:before) {
    display: none;
}

.ant-carousel :deep(.custom-slick-arrow:hover) {
    opacity: 0.5;
}

.ant-carousel :deep(.slick-slide h3) {
    color: #fff;
}

.post {
    position: relative;
}

.post img:hover {
    opacity: 0.5;
    cursor: pointer;
}
</style>