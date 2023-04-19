<template>

</template>

<script>
import axios from 'axios'

export default {
    name: "TagProduct",
    data() {
        return {}
    },
    mounted() {
        let self = this
        axios.post('https://odoo.website/shopify/get_product', {
            jsonrpc: "2.0",
            params: {}
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })
    }
}
</script>

<style scoped>

</style>