if (typeof (axios) === 'undefined') {
    script1 = document.createElement("script")
    script1.src = 'https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js'
    document.getElementsByTagName('head')[0].append(script1)
}

var child1 = document.createElement("div");

function render_bundle(bundles, quantities) {
    if (bundles.length > 0) {
        for (let bundle of bundles) {
            string_html = `<div style="border: 1px solid black">${bundle.title} - Mua combo giảm ${bundle.discount_value}%: `
            for (let quantity of quantities) {
                if (quantity.bundle_id == bundle.bundle_id) {
                    string_html += `<p> - mua ${quantity.quantity} sản phẩm ${quantity.product_name} <img src="${quantity.img}" style="width: 50px; height: auto"></p>`
                }
            }
            child1.innerHTML += string_html + `</div>`
        }
    }
}

var get_product_id = setInterval(function () {
    if (window.location.href.indexOf("products") > -1) {
        clearInterval(get_product_id)
        var el1 = document.querySelector("div.product-form__quantity")

        if (el1) {
            el1.appendChild(child1);
            axios.post("https://odoo.website/shopify_bundle/get_bundle_detail", {
                jsonrpc: "2.0",
                params: {product_id: ShopifyAnalytics.meta['product']['id']}
            }).then(response => {
                console.log(response.data.result)
                var bundles = response.data.result.bundle_infors
                var quantities = response.data.result.quantity_infors
                render_bundle(bundles, quantities)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}, 100)

var child2 = document.createElement("div");
var cart_infors = []
var reduce_price = setInterval(function () {
    if (window.location.href.indexOf("cart") > -1) {
        clearInterval(reduce_price)
        var el2 = document.querySelector("div.totals")
        axios.get("https://shop-odoo-hnam.myshopify.com/cart.js").then(function (res) {
            console.log("abc")
            console.log(res)
            for (item of res.data.items) {
                cart_infors.push({
                    product_id: item.product_id, quantity: item.quantity
                })
            }
        }).then(function () {
            if (el2) {
                el2.appendChild(child2);
                axios.post("https://odoo.website/shopify_bundle/cart", {
                    jsonrpc: "2.0",
                    params: {cart_infors: cart_infors}
                }).then(response => {
                    console.log(response.data.result)
                }).catch(error => {
                    console.log(error)
                })
            }
        }).catch(function (error) {
            console.log(error)
        })
    }
}, 100)