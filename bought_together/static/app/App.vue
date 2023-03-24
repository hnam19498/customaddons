<template>
    <layout>
        <layout-sider>
            <side-bar-menu :currentTab="currentTab" :tabs="tabs" @changeTab="changeTab"/>
        </layout-sider>
        <layout>
            <layout-header>
                <nav-header/>
            </layout-header>
            <layout-content>
                <nav-menu @changeTab="changeTab" :currentTab='currentTab' :navtabs="navtabs"
                          v-if="navtabs.includes(currentTab)"/>
                <add-product @addProductToCustomization="addProductToCustomization" :products="products"
                             v-if="currentTab=='AddProduct'"/>
                <customization @changeTab="changeTab" v-if="currentTab=='Customization'"
                               :list_recommendation="list_recommendation"/>
                <installation @changeTab="changeTab" :shop_url="shop_url" v-if="currentTab=='Installation'"/>
                <dashboard v-if="currentTab=='Dashboard'"/>
            </layout-content>
        </layout>
    </layout>
</template>
<script>
import NavHeader from "./components/NavHeader.vue"
import SideBarMenu from "./components/SideBarMenu.vue"
import NavMenu from "./components/NavMenu.vue"
import Loading from "./components/main_page/Loading.vue"
import AddProduct from "./components/main_page/AddProduct.vue"
import {Layout, LayoutHeader, LayoutContent, LayoutSider} from "ant-design-vue"
import Customization from './components/main_page/Customization.vue'
import Installation from "./components/main_page/Installation.vue"
import Dashboard from "./components/main_page/Dashboard.vue"
import axios from 'axios'

export default {
    mounted() {
        let self = this
        axios.post('https://odoo.website/bought_together/get_product', {
            jsonrpc: "2.0",
            params: {}
        }).then(function (res) {
            self.products = res.data.result.product_data
            self.shop_url = res.data.result.shop_url
        }).catch(error => {
            console.log(error)
        })
    },
    components: {
        NavHeader,
        Installation,
        SideBarMenu,
        Customization,
        AddProduct,
        NavMenu,
        Layout,
        LayoutHeader,
        LayoutContent,
        LayoutSider,
        Loading,
        Dashboard
    },
    data() {
        return {
            products: [],
            shop_url: '',
            currentTab: 'AddProduct',
            tabs: ['AddProduct', 'Customization', 'Installation', 'Dashboard'],
            navtabs: ['AddProduct', 'Customization', 'Installation'],
            list_recommendation: [], list_product_customization: []
        }
    },
    methods: {
        changeTab(tab) {
            this.currentTab = tab
        },
        addProductToCustomization(tab, list_recommendation) {
            this.currentTab = tab
            this.list_recommendation = list_recommendation
        }
    }
}
</script>
<style src="./css/main.css"/>