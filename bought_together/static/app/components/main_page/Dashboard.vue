<template>
    <div id="welcome">WELCOME, {{ this.user }}!</div>
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
            <tr class="table-row" v-if="'id' in this.widget">
                <td>{{ this.widget.id }}</td>
                <td>{{ this.widget.widget_title }}</td>
                <td>{{ this.widget.widget_description }}</td>
                <td style="text-align: center">{{ this.products_included }}</td>
                <td>${{ parseFloat(this.widget.total_price).toFixed(2) }}</td>
                <td class="status">
                    <a-switch @change="changeWidgetStatus"
                              v-model:checked="this.widget.status"
                              checked-children="ON"
                              un-checked-children="OFF"/>
                </td>
            </tr>
        </table>
    </div>
</template>
<script>
import {reactive, toRefs} from 'vue'
import axios from "axios"

export default {
    methods: {
        changeWidgetStatus() {
            let self = this
            axios.post('https://odoo.website/bought_together/change_status_widget', {
                jsonrpc: "2.0",
                params: {widget_status: self.widget.status}
            }).then(res => {
                if (res.data.result.error) {
                    console.log(res.data.result.error)
                }
            }).catch(error => {
                console.log(error)
            })
        }
    },
    props: {
        user: String
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/bought_together/get_widget', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            self.widget = res.data.result.widget_data
            self.products_included = res.data.result.products_included
        }).catch(error => {
            console.log(error)
        })
    },
    data() {
        return {
            widget: [],
            products_included: 0
        }
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
    width: 90%;
    height: 50%;
    margin-left: 60px;
    margin-top: 1rem;
    margin-right: 100px;
}

table {
    width: 100%;
    margin-top: 81px;
    font-size: 14px;
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

.status {
    width: 70px;
}

.ant-switch {
    width: 56px
}
</style>