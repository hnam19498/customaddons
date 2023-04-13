<template>
    <div style="display: flex">
        <div id="setting_feed">
            <div style="background: white">
                <div style="margin-top: 5px; display: flex; flex-direction: column; margin-left: 5px; margin-right: 5px">
                    <span class="label">FEED TITLE</span>
                    <input type="text" style="border-radius: 5px; border: 1px solid #E2E2E2; height: 30px">
                    <div style="display: flex; justify-content: space-between; margin-top: 15px">
                        <div class="feed_setting" style="width: 30%; margin-right: 10px">
                            <span class="label">POST SPACING</span>
                            <select>
                                <option value="no spacing">No spacing</option>
                                <option value="small">Small</option>
                                <option value="medium">Medium</option>
                                <option value="large">Large</option>
                            </select>
                        </div>
                        <div class="feed_setting" style="width: 70%">
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
                                <option value="grid_squares">AUTO</option>
                                <option value="grid_tiles">Manual</option>
                            </select>
                        </div>
                    </div>
                    <div style="display: flex; margin-top: 15px">
                        <div class="feed_setting" style="width: 50%; margin-right: 10px">
                            <span class="label">ROWS</span>
                            <input type="number">
                        </div>
                        <div class="feed_setting" style="width: 50%">
                            <span class="label">COLUMNS</span>
                            <input type="number">
                        </div>
                    </div>
                    <button id="btn_save" style="margin-top: 15px">Save feed</button>
                </div>
            </div>
        </div>
        <div id="preview">

        </div>
    </div>
</template>

<script>
import {LeftCircleOutlined, RightCircleOutlined} from '@ant-design/icons-vue';

export default {
    name: "FeedSettings",
    components: {
        LeftCircleOutlined,
        RightCircleOutlined
    }
}
</script>

<style scoped>
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
</style>