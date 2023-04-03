<template>
    <div v-if="this.widget.status && !this.widget.list_excluded_shopify_product_ids.includes(this.product_id)"
         id="preview">
        <div :style="{ color: widget.title_color, fontSize: widget.title_font_size }"
             style="margin-top:32px; height: 24px; font-style: normal; font-weight: 700; line-height: 22px">
            {{ this.widget.widget_title }}
        </div>
        <div :style="{ color: widget.description_color, fontSize: widget.description_font_size }"
             style="margin-top: 14px; height: 25px; font-style: normal; font-weight: 400; line-height: 22px">
            {{ this.widget.widget_description }}
        </div>
        <div style="display: flex; flex-direction: row">
            <div style="display: flex; flex-direction: row; margin-top: 50px; width: 100%; justify-content: center">
                <div :key="product.id"
                     v-for="product in this.widget.recommendation_products"
                     style="display: flex; align-items: center">
                    <img :src="product.img"
                         :alt="product.name"
                         @click="redirectToProduct(product.url)"
                         style="border: 1px solid #E2E2E2; border-radius: 5px; width: 65px; height: 65px"
                         class="redirectToProduct">
                    <div style="margin: 5px; font-weight: 600; font-size: 16px"
                         v-if="this.widget.recommendation_products[this.widget.recommendation_products.length - 1].variant_id != product.variant_id">
                        +
                    </div>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; width: 50%; margin-left: auto">
                <div style="display: flex; flex-direction: row; margin-top: 60px; height: 18px; font-style: normal; font-weight: 600; font-size: 16px; line-height: 22px">
                    <div style="color: black">Total:</div>
                    <div style="color: red; margin-left: 3px">${{ this.widget.total_price }}</div>
                </div>
                <button :style="{ background: widget.background_color, borderColor: widget.border_color, color: widget.text_color }"
                        style="min-width: 70px; border-radius: 5px; height: 24px; margin-top: 10px; display: flex; align-items: center"
                        @click="addBoughtTogether">
                    {{ widget.btn_text }}
                </button>
            </div>
        </div>
        <div style="margin-top: 18px; margin-bottom: 17px">
            <div style="display: flex; flex-direction: row"
                 class="item"
                 v-for="product in this.widget.recommendation_products"
                 :key="product.variant_id">
                <input type="checkbox"
                       :value="product.variant_id"
                       :checked="this.cart.includes(product.variant_id)"
                       disabled>
                <div class="redirectToProduct" @click="redirectToProduct(product.url)">{{ product.name }}</div>
                <span style="color: red">${{ product.price }}</span>
            </div>
            <span id="total_compare_at_price">${{ this.widget.total_compare_at_price }}</span>
        </div>
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: "shopify.vue",
    mounted() {
        let self = this
        axios.post('https://odoo.website/bought_together/get_widget', {
            jsonrpc: "2.0",
            params: {
                shop_url: window.location.origin
            }
        }).then(res => {
            self.widget = res.data.result.widget_data
        }).catch(error => {
            console.log(error)
        })
        axios.get(window.location.origin + '/cart.js')
            .then(res => {
                for (let item of res.data.items) {
                    self.cart.push(item.id.toString())
                }
            }).catch(error => {
            console.log(error)
        })
        axios.get(window.location.origin + window.location.pathname + '.js')
            .then(res => {
                self.product_id = res.data.id.toString()
            }).catch(error => {
            console.log(error)
        })
    },
    data() {
        return {
            widget: {},
            cart: [],
            product_id: ''
        }
    },
    methods: {
        redirectToProduct(product_url) {
            window.location.replace(product_url)
        },
        addBoughtTogether() {
            let items = []
            for (let item of this.widget.recommendation_products) {
                items.push({
                    'id': item.variant_id,
                    "quantity": 1
                })
            }
            let formData = {'items': items}
            fetch(window.Shopify.routes.root + 'cart/add.js', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            }).then(res => {
                window.location.replace(window.location.origin + '/cart')
                return res.json()
            }).catch(error => {
                console.log(error)
            })
        }
    }
}
</script>
<style scoped>
#preview {
    display: flex;
    flex-direction: column;
    background: white;
    border: 1px solid #BFBFBF;
    border-radius: 5px;
    text-align: center;
    margin-top: 25px;
    margin-right: 42px;
}

.item {
    height: 16px;
    align-items: center;
    margin-top: 12px;
    margin-left: 200px;
    margin-right: 70px;
}

.item input {
    width: 16px;
    background: white;
    border-radius: 2px;
    margin-left: 30px;
}

.item div {
    color: black;
    font-style: normal;
    font-weight: 400;
    margin-left: 14px;
    font-size: 14px;
    line-height: 17px;
}

.item span {
    color: red;
    font-style: normal;
    font-weight: 600;
    font-size: 12px;
    line-height: 22px;
    margin-right: 84px;
    margin-left: auto;
}

#total_compare_at_price {
    margin-top: -19px;
    margin-right: 16px;
    float: right;
    font-style: normal;
    text-decoration-line: line-through;
    height: 19px;
    font-weight: 600;
    font-size: 12px;
    line-height: 22px;
    color: #848484;
}

.redirectToProduct {
    cursor: pointer;
}
</style>