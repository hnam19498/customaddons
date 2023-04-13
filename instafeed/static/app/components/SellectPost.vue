<template>
    <div v-if="posts">
        <div class="setting-btn">
            <button class="btn-setting" id="btn-cancel" @click="cancelAddProducts">Cancel</button>
            <button class="btn-setting" id="btn-next" @click="nextToCustomization">NEXT</button>
        </div>
        <div id="setting_widget">
            <label id="enable_widget">Enable Widget</label>
            <a-switch v-model:checked="enable_widget" checked-children="ON" un-checked-children="OFF"/>
        </div>
        <div style="position: relative; width: 100%">
            <div id="choose-post">
                <div class="selected_products" v-if="this.list_recommendation.length > 0">
                    <div :key="recommendation_product.id"
                         v-for="recommendation_product in this.list_recommendation"
                         class="selected_product">
                        <div style="height: 17px; margin-left: 10px; margin-bottom: 5px; margin-top: 5px">
                            {{ recommendation_product.name }}
                        </div>
                        <font-awesome-icon icon="fa-solid fa-circle-xmark"
                                           @click="handleChoosePost(recommendation_product.id)"
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
                                       :disabled="list_excluded.filter(e => e.id == product.id).length > 0"
                                       type="checkbox">
                            </td>
                            <td><img :alt="product.name" :src="product.url_img" style="width: 30px; height: 30px"></td>
                            <td>{{ product.name }}</td>
                            <td>{{ parseFloat(product.price).toFixed(2) }}</td>
                            <td>{{ parseFloat(product.compare_at_price).toFixed(2) }}</td>
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
            </div>
            <div v-if="!enable_widget" class="blur"/>
            <div class="blur" v-if="loading">
                <a-spin size="large"/>
            </div>
        </div>
    </div>
    <div v-else>
        <loading/>
    </div>
</template>

<script>
export default {
    data() {
        return {}
    }
}
</script>
<style scope>

</style>