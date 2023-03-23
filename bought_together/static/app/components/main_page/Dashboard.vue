<template>
    <div id="welcome">WELCOME, NAM!</div>
    <div id="table-product">
        <table>
            <tr class="table-col-name">
                <td>#</td>
                <td>Widget Title</td>
                <td>Widget Description</td>
                <td style="text-align: center">Products included</td>
                <td>Total Price</td>
                <td class="status">Status</td>
            </tr>
            <tr class="table-row">
                <td>1</td>
                <td>You May Also Like...</td>
                <td>Good deals only for you!</td>
                <td style="text-align: center">3</td>
                <td>$100.05</td>
                <td class="status">
                    <a-switch v-model:checked="checked1" checked-children="ON" un-checked-children="OFF"/>
                </td>
            </tr>
        </table>
    </div>
</template>
<script>
import {reactive, toRefs} from 'vue'

export default {

    data() {
        return {}
    },
    setup() {
        const state = reactive({checked1: false})
        return {...toRefs(state)}
    },
}
</script>
<style scoped>
#welcome {
    color: black;
    height: 24px;
    font-style: normal;
    font-weight: 600;
    font-size: 27px;
    margin-left: 57px;
    margin-top: 51px;
    line-height: 24px;
}

#table-product {
    width: 95%;
    height: 50%;
    margin-left: 1rem;
    margin-top: 1rem;
}

#table-product table {
    width: 100%;
    margin-top: 81px;
    font-size: 14px;
}

#table-product table .table-row {
    height: 3rem;
    border-bottom: 1px groove #EFEFEF;
    font-size: 14px;
}

#table-product table .table-col-name {
    height: 3rem;
    border-bottom: 1px groove #EFEFEF;
    border-top: 1px groove #EFEFEF;
    color: rgba(0, 0, 0);
    font-weight: 700;
    font-size: 14px;
}

.status {
    width: 70px;
}
</style>