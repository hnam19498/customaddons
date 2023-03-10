if (typeof (axios) === 'undefined') {
    script1 = document.createElement("script")
    script1.src = 'https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js'
    document.getElementsByTagName('head')[0].append(script1)
}

function redirect_to_check_out(draft_order_url) {
    button_check_out = document.getElementsByClassName("cart__checkout-button")[0]
    button_check_out.addEventListener('click', function () {
        location.href = draft_order_url
    })
}

function render_bundle(bundles, quantities, bundle_setting) {
    window.quantities = quantities
    for (let bundle of bundles) {
        string_html = `<div style="border: 1px solid black; color: ${bundle_setting.color}">${bundle_setting.bundle_label} - Mua combo giảm ${bundle.discount_value}%: `
        for (let quantity of quantities) {
            if (quantity.bundle_id == bundle.bundle_id) {
                string_html += `<p>- mua ${quantity.quantity} sản phẩm ${quantity.product_name} <img src="${quantity.img}" style="width: 50px; height: auto"></p>`
            }
        }
        child1.innerHTML += string_html + `<div style="border: 1px solid red; text-align: center" class='add_bundle_to_cart' data-bundle-id="${bundle.bundle_id}">Add bundle to cart</div></div>`
        if (bundle_setting.bundle_position === 'below') {
            document.getElementsByName("add")[0].after(child1)
        }
        if (bundle_setting.bundle_position === 'above') {
            document.getElementsByName("add")[0].before(child1)
        }
    }
    add_bundle_divs = document.getElementsByClassName('add_bundle_to_cart')
    for (let div_add of add_bundle_divs) {
        div_add.addEventListener('click', function () {
            alert("Đã add bundle vào trong giỏ hàng!")
            let items = [];
            for (let quantity of window.quantities) {
                if (quantity.bundle_id == this.getAttribute('data-bundle-id')) {
                    items.push({
                        'id': parseInt(quantity.variant_id),
                        'quantity': quantity.quantity
                    })
                }
            }
            console.log(items)
            let formData = {
                'items': items
            }
            fetch(window.Shopify.routes.root + 'cart/add.js', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            }).then(response => {
                return response.json();
            }).catch((error) => {
                console.error('Error:', error);
            });
        })
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
                params: {product_id: ShopifyAnalytics.meta['product']['id']}
            }).then(response => {
                if (response.data.result.bundle_infors.length > 0) {
                    var bundles = response.data.result.bundle_infors
                    var quantities = response.data.result.quantity_infors
                    var bundle_setting = response.data.result.bundle_setting
                    render_bundle(bundles, quantities, bundle_setting)
                }
            }).catch(error => {
                console.log(error)
            })
        }
    }
}, 500)

var reduce_price = setInterval(function () {
    if (window.location.href.indexOf("cart") > -1) {
        clearInterval(reduce_price)
        var cart_infors = []
        axios.get(window.location.href + ".js").then(function (res) {
            for (let item of res.data.items) {
                cart_infors.push({
                    product_id: item.product_id,
                    variant_id: item.variant_id,
                    quantity: item.quantity
                })
            }
        }).then(function () {
            axios.post("https://odoo.website/shopify_bundle/cart", {
                jsonrpc: "2.0",
                params: {
                    cart_infors: cart_infors,
                    shop_url: window.location.origin
                }
            }).then(response => {
                if (response.data.result.draft_order_url != 0) {
                    var bundle_title = response.data.result.bundle_title
                    var max_bundle = response.data.result.max_bundle
                    var bundle_discount_value = response.data.result.bundle_discount_value
                    var draft_order_url = response.data.result.draft_order_url
                    var string_html = document.createElement("div")
                    string_temp = `
                        <p style="text-align: right">Đã áp dụng bundle "${bundle_title}" được ${max_bundle['time']} lần, giảm giá ${bundle_discount_value}%/combo</p>
                        <p style="text-align: right">Đã giảm giá $${max_bundle['price_reduce']} cho cả đơn hàng</p>
                    `
                    string_html.innerHTML = string_temp
                    document.getElementsByClassName("cart__footer")[0].before(string_html)
                    button_check_out = document.getElementsByClassName("cart__checkout-button")[0]
                    button_check_out.removeAttribute("id")
                    button_check_out.removeAttribute("type")
                    button_check_out.removeAttribute("name")
                    button_check_out.removeAttribute("form")
                    redirect_to_check_out(draft_order_url)
                }
            }).catch(error => {
                console.log(error)
            })
        }).catch(function (error) {
            console.log(error)
        })
    }
}, 500)