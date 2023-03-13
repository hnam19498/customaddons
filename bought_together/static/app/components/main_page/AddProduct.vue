<template>
    <!--    <div v-if="data">-->
    <div class="setting-btn">
        <button class="btn-setting" id="btn-cancel">Cancel</button>
        <button class="btn-setting" id="btn-save">SAVE</button>
    </div>
    <div id="setting_widget">
        <label id="enable_widget">Enable Widget</label>
        <a-switch v-model:checked="checked1" checked-children="ON" un-checked-children="OFF"/>
    </div>
    <div id="manual-recommendation">
        <span>Manual Recommendation</span>
        <font-awesome-icon icon="fa-solid fa-circle-question"/>
    </div>
    <div style="position: relative; width: 100%">
        <div id="choose-recommendation-product">
            <div id="choose-recommendation">
                <font-awesome-icon icon="fa-solid fa-circle-question"/>
                <span>Choose recommendation product(s)</span>
            </div>
            <div id="search">
                <a-input placeholder="Search product by name" :suffix="this.list_recommendation.length + ' selected'"/>
            </div>
            <div style="display: flex" class="recommendation_products" v-if="this.list_recommendation.length>0">
                <div v-for="recommendation_product of this.list_recommendation" class="recommendation_product">
                    {{ recommendation_product.name }}
                </div>
            </div>
            <div id="table-product">
                <table>
                    <tr class="table-col-name">
                        <td>
                            <input
                                id="checkbox-table-recommendation-product"
                                type="checkbox"
                                @click="SelectAllRecommendation"
                                v-model="tickAllRecommendation"
                            >
                        </td>
                        <td>Image</td>
                        <td>Product name</td>
                        <td>Price</td>
                        <td>Compare at price</td>
                        <td>In Stock</td>
                    </tr>
                    <tr class="table-row" v-for="product in this.recommendation_products" :key="product.id">
                        <td>
                            <input
                                type="checkbox"
                                class="item-recommendation-checkbox"
                                :id="product.id"
                                v-model="list_recommendation"
                                @change="select_recommendation"
                                :value="{
                                    id:product.id,
                                    name:product.name,
                                    price:product.price,
                                    compare_at_price:product.compare_at_price,
                                    quantity:product.quantity}"
                                :checked="this.list_ids_recommendation.includes(product.id)"
                            >
                        </td>
                        <td><img :src="product.img" style="width: 30px; height: 30px"></td>
                        <td>{{ product.name }}</td>
                        <td>{{ product.price }}</td>
                        <td>{{ product.compare_at_price }}</td>
                        <td>{{ product.quantity }}</td>
                    </tr>
                </table>
            </div>
        </div>

        <div id="choose-excluded-product">
            <div id="choose-excluded">
                <font-awesome-icon icon="fa-solid fa-circle-question"/>
                <span>Choose excluded product(s)</span>
            </div>
            <div id="search" style="display: flex">
                <a-input placeholder="Search product by name" :suffix="this.list_excluded.length + ' selected'"/>
            </div>
            <div style="display: flex" class="excluded_products" v-if="this.list_excluded.length>0">
                <div v-for="excluded_product of this.list_excluded" class="excluded_product">
                    {{ excluded_product.name }}
                </div>
            </div>
            <div id="table-product">
                <table>
                    <tr class="table-col-name">
                        <td>
                            <input
                                id="checkbox-table-excluded-product"
                                type="checkbox"
                                @click="SelectAllExcluded"
                                v-model="tickAllExcluded"
                            >
                        </td>
                        <td>Image</td>
                        <td>Product Name</td>
                        <td>Price</td>
                        <td>Compare At Price</td>
                        <td>In Stock</td>
                    </tr>
                    <tr class="table-row" v-for="product in this.excluded_products" :key="product.id">
                        <td>
                            <input
                                type="checkbox"
                                v-model="list_excluded"
                                @change="select_excluded"
                                :value="{
                                    id:product.id,
                                    name:product.name,
                                    price:product.price,
                                    compare_at_price:product.compare_at_price,
                                    quantity:product.quantity}"
                            >
                        </td>
                        <td>
                            <img :src='product.img' style="width: 30px; height: 30px">
                        </td>
                        <td>{{ product.name }}</td>
                        <td>{{ product.price }}</td>
                        <td>{{ product.compare_at_price }}</td>
                        <td>{{ product.quantity }}</td>
                    </tr>
                </table>
            </div>
        </div>
        <div v-if="!checked1" class="blur"></div>
    </div>
    <!--    </div>-->
    <!--    <div v-else>-->
    <!--        <loading/>-->
    <!--    </div>-->
</template>
<script>
import {reactive, toRefs} from 'vue'
import Loading from "./Loading.vue"

export default {
    components: {Loading},
    setup() {
        const state = reactive({checked1: false})
        return {...toRefs(state)}
    },
    data() {
        return {

            tickAllRecommendation: false,
            list_ids_recommendation: [],
            tickAllExcluded: false,
            list_recommendation: [],
            list_excluded: [],
            list_ids_excluded: [],
            excluded_products: [
                {
                    id: 1,
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 1',
                    price: 'Price test 1',
                    compare_at_price: 'Test 1',
                    quantity: 1
                }, {
                    id: 2,
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 2',
                    price: 'Price test 2',
                    compare_at_price: 'Test 2',
                    quantity: 2
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 3',
                    price: 'Price test 3',
                    compare_at_price: 'Test 3',
                    id: 3,
                    quantity: 3
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 4',
                    id: 4,
                    price: 'Price test 4',
                    compare_at_price: 'Test 4',
                    quantity: 4
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 5',
                    price: 'Price test 5',
                    id: 5,
                    compare_at_price: 'Test 5',
                    quantity: 5
                }
            ], recommendation_products: [
                {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 1',
                    id: 1,
                    price: 'Price test 1',
                    compare_at_price: 'Test 1',
                    quantity: 1
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 2',
                    price: 'Price test 2',
                    compare_at_price: 'Test 2',
                    id: 2,
                    quantity: 2
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 3',
                    price: 'Price test 3',
                    id: 3,
                    compare_at_price: 'Test 3',
                    quantity: 3
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 4',
                    price: 'Price test 4',
                    compare_at_price: 'Test 4',
                    id: 4,
                    quantity: 4
                }, {
                    img: "/bought_together/static/app/img/LogoNestScale.png",
                    name: 'Name test 5',
                    price: 'Price test 5',
                    id: 5,
                    compare_at_price: 'Test 5',
                    quantity: 5
                }
            ]
        }
    },
    methods: {
        SelectAllRecommendation() {
            this.list_recommendation = []
            this.list_ids_recommendation = []
            if (!this.tickAllRecommendation) {
                for (let product of this.recommendation_products) {
                    let data = {
                        id: product.id,
                        name: product.name,
                        price: product.price,
                        compare_at_price: product.compare_at_price,
                        quantity: product.quantity,
                        img: product.img
                    }
                    this.list_recommendation.push(data)
                    this.list_ids_recommendation.push(product.id)
                }
            }
        },
        select_recommendation() {
            let count = 0
            for (let i in this.list_recommendation) {
                let item_data = JSON.parse(JSON.stringify(this.list_recommendation[i]))
                if (item_data !== false) {
                    count++
                }
            }
            if (this.recommendation_products.length === count) {
                this.tickAllRecommendation = true;
            } else {
                this.tickAllRecommendation = false;
            }
            for (let product of this.list_recommendation) {
                if (this.list_ids_recommendation.includes(product.id) === false) {
                    this.list_ids_recommendation.push(product.id)
                }
            }
        },
        SelectAllExcluded() {
            this.list_excluded = []
            this.list_ids_excluded = []
            if (!this.tickAllExcluded) {
                for (let product of this.excluded_products) {
                    let data = {
                        id: product.id,
                        name: product.name,
                        price: product.price,
                        compare_at_price: product.compare_at_price,
                        quantity: product.quantity,
                        img: product.img
                    }
                    this.list_excluded.push(data)
                    this.list_ids_excluded.push(product.id)
                }
            }
            window.list_ids_excluded = this.list_ids_excluded
        },
        select_excluded() {
            let count = 0
            for (let i in this.list_excluded) {
                let item_data = JSON.parse(JSON.stringify(this.list_excluded[i]))
                if (item_data !== false) {
                    count++
                }
            }
            if (this.excluded_products.length === count) {
                this.tickAllExcluded = true;
            } else {
                this.tickAllExcluded = false;
            }
            for (let product of this.list_excluded) {
                if (this.list_ids_excluded.includes(product.id) === false) {
                    this.list_ids_excluded.push(product.id)
                }
            }
        },
    },
    // mounted() {
    //     $('#checkbox-table-recommendation-product').on('click', function () {
    //         if ($(this).is(':checked')) {
    //             $('.item-recommendation-checkbox').each(function (index, item) {
    //                 $(item).prop('checked', true)
    //                 console.log(this)
    //             })
    //         } else {
    //             $('.item-recommendation-checkbox').each(function (index, item) {
    //                 $(item).prop('checked', false)
    //                 console.log(this)
    //             })
    //         }
    //     })
    // }
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
}

#search {
    display: flex;
    width: 100%;
}

#search span {
    background: white;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    margin-left: 20px;
    margin-top: 4px;
    margin-right: 23px;
    height: 40px;
    width: 100%;
}

#table-product {
    width: 95%;
    height: 50%;
    margin-left: 1rem;
    margin-top: 1rem;
}

#table-product table {
    width: 100%;
    font-size: 14px;
    height: 100%;
    margin-bottom: 15px;
}

#table-product table .table-row {
    height: 3rem;
    border-bottom: 1px solid;
    font-size: 14px;
}

#table-product table .table-col-name {
    height: 3rem;
    border-bottom: 1px groove #979191;
    border-top: 1px groove #979191;
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

.recommendation_products {
    margin-left: 21px;
    height: 24px;
    margin-top: 13px;
}

.recommendation_product {
    height: 24px;
    font-style: normal;
    font-weight: 400;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    font-size: 14px;
    background: white;
    display: flex;
    align-items: center;
    line-height: 17px;
    color: black;
}

.excluded_products {
    margin-left: 21px;
    height: 24px;
    margin-top: 13px;
}

.excluded_product {
    height: 17px;
    font-style: normal;
    font-weight: 400;
    border: 1px solid #E2E2E2;
    border-radius: 5px;
    font-size: 14px;
    display: flex;
    align-items: center;
    line-height: 17px;
    color: black;
}

</style>