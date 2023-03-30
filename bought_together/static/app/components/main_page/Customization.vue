<template>
    <div class="setting-btn">
        <button class="btn-setting" id="btn-cancel" @click="cancelCustomization">Cancel</button>
        <button class="btn-setting" id="btn-save" @click="saveCustomization">SAVE</button>
    </div>
    <div id="setting_customization">
        <label id="settings">Settings</label>
        <font-awesome-icon :icon="['fass', 'circle-question']" style="color: #5C5F62"/>
    </div>
    <div style="display: flex; flex-direction: row; margin-top: 30px">
        <div style="display:flex; flex-direction: column">
            <div class="configuration">
                <font-awesome-icon :icon="['fass', 'circle-question']" style="color: #5C5F62"/>
                <span>General Configuration</span>
            </div>
            <div class="widget">Widget Title</div>
            <input type="text" class="input-widget" v-model="widget_title">
            <div style="display: flex; flex-direction: row; margin-top: 18px; align-items: center">
                <div style="display: flex; flex-direction: column">
                    <div class="color">
                        Title Color
                    </div>
                    <div style="display: flex; margin-top: 20px; align-items: center; flex-direction: row">
                        <div class="input-color">
                            <input type="color" v-model="title_color">
                        </div>
                        <input v-model="title_color" type="text" class="text-color">
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; margin-left: 50px" class="select-font">
                    <div class="font-size">Font Size</div>
                    <select v-model="title_font_size">
                        <option disabled value="">Please select one</option>
                        <option value="10px">Extra Small</option>
                        <option value="15px">Small</option>
                        <option value="20px">Medium</option>
                        <option value="25px">Large</option>
                        <option value="30px">Extra Large</option>
                    </select>
                </div>
            </div>
            <div class="widget">Widget Description</div>
            <input type="text" class="input-widget" v-model="widget_description">
            <div style="display: flex; flex-direction: row; margin-top: 18px; align-items: center">
                <div style="display: flex; flex-direction: column">
                    <div class="color">Description Color</div>
                    <div style="display: flex; margin-top: 20px; align-items: center; flex-direction: row">
                        <div class="input-color">
                            <input type="color" v-model="description_color">
                        </div>
                        <input type="text" class="text-color" v-model="description_color">
                    </div>
                </div>
                <div style="display: flex; margin-left: 50px; flex-direction: column" class="select-font">
                    <div class="font-size">Font Size</div>
                    <select v-model="description_font_size">
                        <option disabled value="">Please select one</option>
                        <option value="10px">Extra Small</option>
                        <option value="15px">Small</option>
                        <option value="20px">Medium</option>
                        <option value="25px">Large</option>
                        <option value="30px">Extra Large</option>
                    </select>
                </div>
            </div>
            <div style="display: flex; flex-direction: row; margin-top: 30px">
                <div style="display: flex; flex-direction: column">
                    <div class="layout-style">Layout Style</div>
                    <div style="display:flex; flex-direction: row" class="layout-select">
                        <input type="radio" id="layout-style">
                        <label for="layout-style">List</label>
                    </div>
                </div>
                <div class="number-products" style="display: flex; flex-direction: column">
                    <div>Number of products to show</div>
                    <input type="number" min="1" max="5" value="3">
                </div>
            </div>
            <div class="configuration" style="margin-top: 25px">
                <font-awesome-icon :icon="['fass', 'circle-question']" style="color: #5C5F62"/>
                <span>Button Configuration</span>
            </div>
            <div class="widget">Button Text</div>
            <input type="text" class="input-widget" v-model="btn_text">
            <div class="color" style="margin-top: 30px">Text Color</div>
            <div style="display: flex; flex-direction: row; margin-top: 20px">
                <div class="input-color">
                    <input type="color" v-model="text_color">
                </div>
                <input type="text" v-model="text_color" class="text-color">
            </div>
            <div style="display: flex; flex-direction: row; margin-top: 10px">
                <div style="display: flex; flex-direction: column">
                    <div class="color">Background Color</div>
                    <div style="display: flex; flex-direction: row; margin-top: 20px">
                        <div class="input-color">
                            <input type="color" v-model="background_color">
                        </div>
                        <input type="text" v-model="background_color" class="text-color">
                    </div>
                </div>
                <div style="display: flex; flex-direction: column">
                    <div id="border-color">Border Color</div>
                    <div style="display: flex; margin-top: 20px; flex-direction: row">
                        <div class="input-color">
                            <input type="color" v-model="border_color">
                        </div>
                        <input type="text" class="text-color" v-model="border_color">
                    </div>
                </div>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; width: 100%">
            <div class="configuration" style="margin-left: -50px">
                <font-awesome-icon :icon="['fass', 'circle-question']" style="color: #5C5F62"/>
                <span>Preview</span>
            </div>
            <div id="preview">
                <div :style="{ color: title_color, fontSize: title_font_size }"
                     style="margin-top:32px; height: 24px; font-style: normal; font-weight: 700; line-height: 22px">
                    {{ this.widget_title }}
                </div>
                <div :style="{ color: description_color, fontSize: description_font_size }"
                     style="margin-top: 14px; height: 25px; font-style: normal; font-weight: 400; line-height: 22px">
                    {{ this.widget_description }}
                </div>
                <div style="display: flex; flex-direction: row">
                    <div
                        style="display: flex; flex-direction: row; margin-top: 50px; width: 100%; justify-content: center">
                        <div :key="product.id"
                             v-for="product in this.list_recommendation"
                             style="display: flex; align-items: center">
                            <img :src="product.img"
                                 style="border: 1px solid #E2E2E2; border-radius: 5px; width: 65px; height: 65px">
                            <div style="margin: 5px; font-weight: 600; font-size: 16px"
                                 v-if="this.list_ids[this.list_ids.length - 1] != product.id">+
                            </div>
                        </div>
                    </div>
                    <div
                        style="display: flex; flex-direction: column; align-items: center; width: 50%; margin-left: auto">
                        <div
                            style="display: flex; flex-direction: row; margin-top: 60px; height: 18px; font-style: normal; font-weight: 600; font-size: 16px; line-height: 22px">
                            <div style="color: black">Total:</div>
                            <div style="color: red; margin-left: 3px">${{ this.total_price }}</div>
                        </div>
                        <button :style="{ background: background_color, borderColor: border_color, color: text_color }"
                                style="min-width: 70px; border-radius: 5px; height: 24px; margin-top: 10px">
                            {{ this.btn_text }}
                        </button>
                    </div>
                </div>
                <div style="margin-top: 18px; margin-bottom: 17px">
                    <div style="display: flex; flex-direction: row"
                         class="item"
                         v-for="product in this.list_recommendation"
                         :key="product.id">
                        <input type="checkbox"
                               :value="product.id"
                               disabled
                               :checked="this.list_ids.includes(product.id)">
                        <div>{{ product.name }}</div>
                        <span style="color: red">${{ product.price }}</span>
                    </div>
                    <span id="total_compare_at_price">${{ this.total_compare_at_price }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios"

export default {
    methods: {
        cancelCustomization() {
            this.widget_description = 'Good deals only for you!'
            this.title_color = '#000000'
            this.description_color = '#000000'
            this.border_color = '#000000'
            this.title_font_size = ''
            this.text_color = '#000000'
            this.background_color = '#000000'
            this.description_font_size = ''
            this.btn_text = ''
            this.widget_title = "YOU MAY ALSO LIKE..."
        },
        saveCustomization() {
            let self = this
            axios.post('https://odoo.website/bought_together/save_widget', {
                jsonrpc: "2.0",
                params: {
                    recommendation_products: self.list_recommendation,
                    widget_description: self.widget_description,
                    title_color: self.title_color,
                    description_color: self.description_color,
                    border_color: self.border_color,
                    title_font_size: self.title_font_size,
                    text_color: self.text_color,
                    background_color: self.background_color,
                    description_font_size: self.description_font_size,
                    btn_text: self.btn_text,
                    widget_title: self.widget_title,
                    total_price: self.total_price,
                    excluded_products: self.list_excluded,
                    total_compare_at_price: self.total_compare_at_price
                }
            }).then(function (res) {
                self.$emit('changeTab', 'Installation')
            }).catch(error => {
                console.log(error)
            })
        }
    },
    data() {
        return {
            widget_description: 'Good deals only for you!',
            title_color: '#000000',
            description_color: '#000000',
            border_color: '#000000',
            title_font_size: '',
            text_color: '#000000',
            background_color: '#000000',
            description_font_size: '',
            btn_text: '',
            widget_title: "YOU MAY ALSO LIKE...",
            list_ids: [],
            total_price: 0,
            total_compare_at_price: 0
        }
    },
    props: {
        list_recommendation: Array,
        list_excluded: {
            type: Array,
            default: []
        }
    },
    emits: ['changeTab'],
    mounted() {
        for (let product of this.list_recommendation) {
            this.list_ids.push(product.id)
            this.total_price += product.price
            this.total_compare_at_price += product.compare_at_price
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

#btn-save {
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
    color: black;
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

#setting_customization {
    display: flex;
    margin-left: 35px;
    margin-top: 28px;
    align-items: center;
}

#settings {
    width: 81px;
    height: 22px;
    font-style: normal;
    font-weight: 600;
    font-size: 20px;
    line-height: 22px;
    color: black;
}

.configuration {
    display: flex;
    align-items: center;
}

#setting_customization svg {
    margin-left: 70px;
    height: 12px;
    width: 12px;
}

.configuration svg {
    margin-left: 30px;
    height: 12px;
    width: 12px;
}

.configuration span {
    margin-left: 10px;
    color: #202223;
    height: 28px;
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 28px;
}

.widget {
    height: 22px;
    margin-top: 25px;
    margin-left: 55px;
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 22px;
    color: black
}

.input-widget {
    background: white;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    height: 40px;
    margin-left: 55px;
    margin-top: 10px;
    width: 421px;
}

.color {
    margin-left: 61px;
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    color: black;
    height: 22px;
    line-height: 22px
}

.text-color {
    margin-left: 12px;
    background: white;
    height: 36px;
    border: 1px solid #C9CCCF;
    gap: 10px;
    color: #202223;
    border-radius: 5px;
    width: 190px;
}

.font-size {
    color: black;
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 22px;
    height: 22px;
}

.select-font select {
    background: white;
    border: 1px solid #C9CCCF;
    border-radius: 5px;
    height: 36px;
    margin-top: 20px;
    width: 190px;
}

.input-color {
    width: 30px;
    overflow: hidden;
    height: 30px;
    border-radius: 50%;
    margin-left: 55px;
}

.input-color input {
    width: 200%;
    height: 200%;
    cursor: pointer;
    margin-top: -15px;
    margin-left: -15px
}

.layout-style {
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 22px;
    height: 22px;
    color: black;
    margin-left: 60px;
}

.layout-select {
    margin-left: 77px;
    display: flex;
    margin-top: 24px;
    align-items: center;
}

#layout-style {
    background: black;
}

.layout-select label {
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    color: black;
    height: 22px;
    line-height: 22px;
    margin-left: 10px;
}

.number-products {
    margin-left: 150px;
}

.number-products div {
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 22px;
    color: black;
    height: 22px;
}

.number-products input {
    background: white;
    border: 1px solid #C8C8C8;
    height: 36px;
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 16px;
    color: black;
    border-radius: 5px;
    width: 140px;
    margin-top: 17px;
}

#border-color {
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    color: black;
    height: 22px;
    line-height: 22px;
}

#preview {
    display: flex;
    flex-direction: column;
    background: white;
    border: 1px solid #BFBFBF;
    border-radius: 5px;
    text-align: center;
    margin-top: 25px;
    margin-right: 42px;
}

.item {
    height: 16px;
    align-items: center;
    margin-top: 12px;
}

.item input {
    width: 16px;
    background: white;
    border-radius: 2px;
    margin-left: 30px;
}

.item div {
    color: black;
    font-style: normal;
    font-weight: 400;
    margin-left: 14px;
    font-size: 14px;
    line-height: 17px;
}

.item span {
    color: red;
    font-style: normal;
    font-weight: 600;
    font-size: 12px;
    line-height: 22px;
    margin-right: 84px;
    margin-left: auto;
}

#total_compare_at_price {
    margin-top: -19px;
    margin-right: 16px;
    float: right;
    font-style: normal;
    text-decoration-line: line-through;
    height: 19px;
    font-weight: 600;
    font-size: 12px;
    line-height: 22px;
    color: #848484;
}
</style>