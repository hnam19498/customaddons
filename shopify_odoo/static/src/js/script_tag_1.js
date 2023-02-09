if (window.location.href.indexOf("products") > -1) {
    document.getElementsByClassName("shopify-payment-button__button--unbranded")[0].remove()
}

if (typeof (axios) === 'undefined') {
    script1 = document.createElement("script")
    script1.src = 'https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js'
    document.getElementsByTagName('head')[0].append(script1)
}

function redirect_to_check_out(draft_order_url) {
    button_check_out = document.getElementsByClassName("cart__checkout-button")[0]
    button_check_out.removeAttribute("id")
    button_check_out.removeAttribute("type")
    button_check_out.removeAttribute("name")
    button_check_out.removeAttribute("form")
    button_check_out.addEventListener('click', function () {
        location.href = draft_order_url
    })
}

function render_bundle(bundles, quantities, bundle_setting) {
    if(bundle_setting)
    if (bundles.length > 0) {
        for (let bundle of bundles) {
            string_html = `<div style="border: 1px solid black; color: ${bundle_setting.color}">${bundle_setting.bundle_label} - Mua combo giảm ${bundle.discount_value}%: `
            for (let quantity of quantities) {
                if (quantity.bundle_id == bundle.bundle_id) {
                    string_html += `<p>- mua ${quantity.quantity} sản phẩm ${quantity.product_name} <img src="${quantity.img}" style="width: 50px; height: auto"></p>`
                }
            }
            child1.innerHTML += string_html + `</div>`
            if (bundle_setting.bundle_position === 'below') {
                document.getElementsByName("add")[0].after(child1)
            }
            if (bundle_setting.bundle_position === 'above') {
                document.getElementsByName("add")[0].before(child1)
            }
        }
    }
}

var child1 = document.createElement("div")
var get_product_id = setInterval(function () {
    if (window.location.href.indexOf("products") > -1) {
        clearInterval(get_product_id)
        var el1 = document.querySelector("div.product__info-wrapper")
        if (el1) {
            el1.appendChild(child1);
            axios.post("https://odoo.website/shopify_bundle/get_bundle_detail", {
                jsonrpc: "2.0",
                params: { product_id: ShopifyAnalytics.meta['product']['id'] }
            }).then(response => {
                var bundles = response.data.result.bundle_infors
                var quantities = response.data.result.quantity_infors
                var bundle_setting = response.data.result.bundle_setting
                render_bundle(bundles, quantities, bundle_setting)
            }).catch(error => {
                console.log(error)
            })
        }
    }
}, 100)
