<template>
    <Layout>
        <LayoutSider>
            <side-bar-menu/>
        </LayoutSider>
        <Layout>
            <LayoutHeader>
                <nav-header/>
            </LayoutHeader>
            <LayoutContent>
                <nav-menu/>
                <add-product/>
            </LayoutContent>
        </Layout>
    </Layout>
</template>
<script>
import NavHeader from "./components/NavHeader.vue"
import SideBarMenu from "./components/SideBarMenu.vue"
import NavMenu from "./components/NavMenu.vue"
import Loading from "./components/main_page/Loading.vue"
import AddProduct from "./components/main_page/AddProduct.vue"
import {Layout, LayoutHeader, LayoutContent, LayoutSider} from "ant-design-vue"

export default {
    components: {
        NavHeader,
        SideBarMenu,
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