<template>
    <!--    <div v-if="data">-->
    <div class="setting-btn">
        <button class="btn-setting" id="btn-cancel">Cancel</button>
        <button class="btn-setting" id="btn-save">SAVE</button>
    </div>
    <div id="setting_widget">
        <label id="enable_widget">Enable Widget</label>
        <a-switch v-model:checked="checked" checked-children="ON" un-checked-children="OFF"/>
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
                <a-input placeholder="Search product by name" suffix="0 selected"/>
            </div>
            <div id="table-product">
                <table>
                    <tr class="table-col-name">
                        <td><input id="checkbox-table-recommendation-product" type="checkbox"/></td>
                        <td>Image</td>
                        <td>Product Name</td>
                        <td>Price</td>
                        <td>Compare At Price</td>
                        <td>In Stock</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 1</td>
                        <td>Price test 1</td>
                        <td>Test 1</td>
                        <td>Quantity 1</td>
                    </tr>yuu
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 2</td>
                        <td>Price test 2</td>
                        <td>Test 2</td>
                        <td>Quantity 2</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 3</td>
                        <td>Price test 3</td>
                        <td>Test 3</td>
                        <td>Quantity 3</td>
                    </tr>
                </table>
            </div>
        </div>

        <div id="choose-excluded-product">
            <div id="choose-excluded">
                <font-awesome-icon icon="fa-solid fa-circle-question"/>
                <span>Choose excluded product(s)</span>
            </div>
            <div id="search">
                <a-input placeholder="Search product by name" suffix="0 selected"/>
            </div>
            <div id="table-product">
                <table>
                    <tr class="table-col-name">
                        <td><input id="checkbox-table-excluded-product" type="checkbox"/></td>
                        <td>Image</td>
                        <td>Product Name</td>
                        <td>Price</td>
                        <td>Compare At Price</td>
                        <td>In Stock</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 1</td>
                        <td>Price test 1</td>
                        <td>Test 1</td>
                        <td>Quantity 1</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 2</td>
                        <td>Price test 2</td>
                        <td>Test 2</td>
                        <td>Quantity 2</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 3</td>
                        <td>Price test 3</td>
                        <td>Test 3</td>
                        <td>Quantity 3</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 4</td>
                        <td>Price test 4</td>
                        <td>Test 4</td>
                        <td>Quantity 4</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 5</td>
                        <td>Price test 5</td>
                        <td>Test 5</td>
                        <td>Quantity 5</td>
                    </tr>
                    <tr class="table-row">
                        <td><input type="checkbox"/></td>
                        <td>
                            <img src="/bought_together/static/app/img/LogoNestScale.png"
                                 style="width: 28px; height: 30px">
                        </td>
                        <td>Name test 6</td>
                        <td>Price test 6</td>
                        <td>Test 6</td>
                        <td>Quantity 6</td>
                    </tr>
                </table>
            </div>
        </div>
        <div v-if="!checked" class="blur"></div>
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
        const state = reactive({checked: false})
        return {...toRefs(state)}
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
    border-radius: 4px;
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
    border-radius: 4px;
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
    border-radius: 6px;
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
    height: 100%;
    margin-bottom: 15px;
}

#table-product table .table-row {
    height: 3rem;
    border-bottom: 1px solid;
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
</style>