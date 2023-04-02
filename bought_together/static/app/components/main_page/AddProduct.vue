<template>
    <div v-if="products">
        <div class="setting-btn">
            <button class="btn-setting" id="btn-cancel" @click="cancelAddProducts">Cancel</button>
            <button class="btn-setting" id="btn-save" @click="saveAddProducts"
                    :disabled="list_recommendation.length > 5 || list_recommendation.length == 0">SAVE
            </button>
        </div>
        <div id="setting_widget">
            <label id="enable_widget">Enable Widget</label>
            <a-switch v-model:checked="enable_widget" checked-children="ON" un-checked-children="OFF"/>
        </div>
        <div id="manual-recommendation">
            <span>Manual Recommendation</span>
            <font-awesome-icon style="color: #5C5F62" icon="fa-solid fa-circle-question"/>
        </div>
        <div style="position: relative; width: 100%">
            <div id="choose-recommendation-product">
                <div id="choose-recommendation">
                    <font-awesome-icon icon="fa-solid fa-circle-question" style="color: #5C5F62"/>
                    <span>Choose recommendation product(s)</span>
                </div>
                <div class="search">
                    <a-input v-model:value="search_recommendation"
                             placeholder="Search product by name"
                             :suffix="this.list_recommendation.length + ' selected'"/>
                </div>
                <div class="selected_products" v-if="this.list_recommendation.length > 0">
                    <div :key="recommendation_product.id"
                         v-for="recommendation_product in this.list_recommendation"
                         class="selected_product">
                        <div style="height: 17px; margin-left: 10px; margin-bottom: 5px; margin-top: 5px">
                            {{ recommendation_product.name }}
                        </div>
                        <font-awesome-icon icon="fa-solid fa-circle-xmark"
                                           @click="handleClickRecommendationProduct(recommendation_product.id)"
                                           style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"
                                           size="sm"/>
                    </div>
                </div>
                <div class="table-product">
                    <table>
                        <tr class="table-col-name">
                            <td>
                                <input type="checkbox"
                                       @change="SelectAllRecommendation"
                                       v-model="tickAllRecommendation">
                            </td>
                            <td>Image</td>
                            <td>Product name</td>
                            <td>Price</td>
                            <td>Compare at price</td>
                            <td>In Stock</td>
                        </tr>
                        <tr class="table-row"
                            v-for="product in filteredRecommendation"
                            :key="product.id">
                            <td>
                                <input :checked="list_recommendation.filter(e => e.id == product.id).length > 0"
                                       type="checkbox"
                                       :value="{
                                           id: product.id,
                                           name: product.name,
                                           price: product.price,
                                           img: product.url_img,
                                           compare_at_price: product.compare_at_price,
                                           quantity: product.qty}"
                                       :id="product.id"
                                       @change="select_recommendation">
                            </td>
                            <td><img :alt="product.name" :src="product.url_img" style="width: 30px; height: 30px"></td>
                            <td>{{ product.name }}</td>
                            <td>{{ product.price }}</td>
                            <td>{{ product.compare_at_price }}</td>
                            <td>{{ product.qty }}</td>
                        </tr>
                    </table>
                </div>
            </div>

            <div id="choose-excluded-product">
                <div id="choose-excluded">
                    <font-awesome-icon style="color: #5C5F62" icon="fa-solid fa-circle-question"/>
                    <span>Choose excluded product(s)</span>
                </div>
                <div class="search">
                    <a-input v-model:value="search_excluded"
                             :suffix="this.list_excluded.length + ' selected'"
                             placeholder="Search product by name"/>
                </div>
                <div class="selected_products" v-if="this.list_excluded.length > 0">
                    <div v-for="excluded_product in this.list_excluded"
                         class="selected_product"
                         :key="excluded_product.id">
                        <div style="height: 17px; margin-left: 10px; margin-bottom: 5px; margin-top: 5px">
                            {{ excluded_product.name }}
                        </div>
                        <font-awesome-icon icon="fa-solid fa-circle-xmark"
                                           size="sm"
                                           style="height: 15px; margin-right: 10px; color: red; margin-top: 5px; width: 15px; margin-bottom: 5px"
                                           @click="handleClickExcludedProduct(excluded_product.id)"/>
                    </div>
                </div>
                <div class="table-product">
                    <table>
                        <tr class="table-col-name">
                            <td>
                                <input type="checkbox"
                                       @change="SelectAllExcluded"
                                       v-model="tickAllExcluded">
                            </td>
                            <td>Image</td>
                            <td>Product Name</td>
                            <td>Price</td>
                            <td>Compare At Price</td>
                            <td>In Stock</td>
                        </tr>
                        <tr class="table-row" v-for="product in filteredExcluded" :key="product.id">
                            <td>
                                <input :checked="list_excluded.filter(e => e.id == product.id).length > 0"
                                       @change="select_excluded"
                                       :value="{
                                           id: product.id,
                                           name: product.name,
                                           img: product.url_img,
                                           price: product.price,
                                           compare_at_price: product.compare_at_price,
                                           quantity: product.qty}"
                                       type="checkbox">
                            </td>
                            <td><img :alt="product.name" :src='product.url_img' style="width: 30px; height: 30px"></td>
                            <td>{{ product.name }}</td>
                            <td>{{ product.price }}</td>
                            <td>{{ product.compare_at_price }}</td>
                            <td>{{ product.qty }}</td>
                        </tr>
                    </table>
                </div>
            </div>
            <div v-if="!enable_widget" class="blur"></div>
        </div>
    </div>
    <div v-else>
        <loading/>
    </div>
</template>
<script>
import {reactive, h, toRefs} from 'vue'
import Loading from "./Loading.vue"
import {notification} from 'ant-design-vue'
import {CloseCircleFilled} from "@ant-design/icons-vue"

export default {
    mounted() {
        let self = this
        if (window.list_recommendation) {
            self.list_recommendation = window.list_recommendation
            self.list_excluded = window.list_excluded
            self.enable_widget = window.enable_widget
        }
    },
    emits: ['addProductToCustomization'],
    props: {products: Array},
    components: {Loading, CloseCircleFilled},
    setup() {
        const state = reactive({enable_widget: false})
        return {...toRefs(state)}
    },
    watch: {
        list_recommendation: function () {
            this.tickAllRecommendation = this.list_recommendation.length == this.filteredRecommendation.length
        },
        list_excluded: function () {
            this.tickAllExcluded = this.list_excluded.length == this.filteredExcluded.length
        }
    },
    data() {
        return {
            tickAllRecommendation: false,
            tickAllExcluded: false,
            list_recommendation: [],
            list_excluded: [],
            search_excluded: '',
            search_recommendation: ''
        }
    },
    methods: {
        saveAddProducts() {
            this.$emit(
                'addProductToCustomization',
                "Customization",
                this.list_recommendation,
                this.list_excluded,
                this.enable_widget
            )
        },
        cancelAddProducts() {
            this.tickAllRecommendation = false
            this.tickAllExcluded = false
            this.list_recommendation = []
            this.list_excluded = []
            this.search_excluded = ''
            this.search_recommendation = ''
        },
        show_toast: function (type, message, description, duration) {
            notification[type]({
                description: description,
                message: message,
                duration: duration,
                class: 'error_popup',
                closeIcon: e => {
                    return (<CloseCircleFilled/>)
                }
            })
        },
        handleClickRecommendationProduct(product_id) {
            for (let i = 0; i < this.list_recommendation.length; i++) {
                if (product_id == this.list_recommendation[i].id) {
                    this.list_recommendation.splice(i, 1)
                }
            }
            this.tickAllRecommendation = this.list_recommendation.length == this.filteredRecommendation.length
            if (this.list_recommendation.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        },
        SelectAllRecommendation() {
            this.list_recommendation = []
            if (this.tickAllRecommendation == true) {
                for (let product of this.filteredRecommendation) {
                    let data = {
                        id: product.id,
                        img: product.url_img,
                        name: product.name,
                        price: product.price,
                        compare_at_price: product.compare_at_price,
                        quantity: product.qty
                    }
                    this.list_recommendation.push(data)
                }
            } else {
                this.list_recommendation = []
            }
            if (this.list_recommendation.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        },
        select_recommendation(ob) {
            if (!ob.target.checked) {
                this.list_recommendation = this.list_recommendation.filter(e => e.id != ob.target._value.id)
            } else {
                this.list_recommendation.push(ob.target._value)
                this.tickAllRecommendation = this.list_recommendation.length == this.filteredRecommendation.length
            }
            if (this.list_recommendation.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        },
        SelectAllExcluded() {
            this.list_excluded = []
            if (this.tickAllExcluded == true) {
                for (let product of this.filteredExcluded) {
                    let data = {
                        id: product.id,
                        img: product.url_img,
                        name: product.name,
                        price: product.price,
                        compare_at_price: product.compare_at_price,
                        quantity: product.qty
                    }
                    this.list_excluded.push(data)
                }
            } else {
                this.list_excluded = []
            }
            if (this.list_excluded.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        },
        select_excluded(ob) {
            if (!ob.target.checked) {
                this.list_excluded = this.list_excluded.filter(e => e.id != ob.target._value.id)
            } else {
                this.list_excluded.push(ob.target._value)
                this.tickAllExcluded = this.list_excluded.length == this.filteredExcluded.length
            }
            if (this.list_excluded.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        },
        handleClickExcludedProduct(product_id) {
            for (let i = 0; i < this.list_excluded.length; i++) {
                if (product_id == this.list_excluded[i].id) {
                    this.list_excluded.splice(i, 1)
                }
            }
            this.tickAllExcluded = this.list_excluded.length == this.filteredExcluded.length
            if (this.list_excluded.length > 5) {
                this.show_toast(
                    'open',
                    'You have reach the product limitation.',
                    'Please untick any products from the list to continue selecting.',
                    3
                )
            }
        }
    },
    computed: {
        filteredRecommendation() {
            let self = this
            return self.products.filter(function (product) {
                return product.name.toLowerCase().includes(self.search_recommendation.toLowerCase())
            })
        },
        filteredExcluded() {
            return this.products.filter(product =>
                product.name.toLowerCase().includes(this.search_excluded.toLowerCase()))
        }
    }
}
</script>
<style scoped>
svg {
    margin-left: 8px;
    margin-bottom: 1px;
}

.setting-btn {
    text-align: right;
    margin-top: 11px;
    margin-right: 30px;
}

#choose-recommendation-product {
    border: 1px solid #E2E2E2;
    background-color: white;
    margin-left: 20px;
    margin-right: 37px;
    border-radius: 5px;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

#choose-recommendation {
    display: flex;
    align-items: center;
}

#choose-recommendation span {
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

#choose-recommendation svg {
    margin-left: 8px;
    margin-bottom: 1.5px;
    width: 12px;
    height: 12px;
}

#choose-excluded-product {
    border: 1px solid #E2E2E2;
    background-color: white;
    margin-left: 20px;
    margin-right: 37px;
    border-radius: 5px;
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

#choose-excluded {
    display: flex;
    align-items: center;
}

#choose-excluded span {
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

#choose-excluded svg {
    margin-left: 8px;
    margin-bottom: 1.5px;
    width: 12px;
    height: 12px;
}

#manual-recommendation {
    margin-top: 16px;
    margin-left: 20px;
    display: flex;
    align-items: center;
}

#manual-recommendation span {
    font-size: 20px;
    line-height: 22px;
    font-weight: 600;
    font-style: normal;
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

.search {
    display: flex;
    width: 100%;
}

.search span {
    background: white;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    margin-left: 20px;
    margin-top: 4px;
    margin-right: 23px;
    height: 40px;
    width: 100%;
}

.table-product {
    width: 95%;
    height: 50%;
    margin-left: 1rem;
    margin-top: 1rem;
}

.table-product table {
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

.blur {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 99;
    opacity: 0.5;
    background-color: white
}

.selected_products {
    margin-left: 21px;
    width: 100%;
    height: max-content;
    margin-top: 13px;
}

.selected_product {
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

.selected_product svg {
    cursor: pointer;
}
</style>