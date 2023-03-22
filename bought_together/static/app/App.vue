<template>
    <layout>
        <layout-sider>
            <side-bar-menu/>
        </layout-sider>
        <layout>
            <layout-header>
                <nav-header/>
            </layout-header>
            <layout-content>
                <nav-menu/>
<!--                <add-product/>-->
                <!--<customization/>-->
                <installation/>
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

export default {
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
        Loading
    },
    data() {
        return {}
    }
}
</script>
<style src="./css/main.css"/>