var child1 = document.createElement("div");
var child2 = document.createElement("div");
var el1 = document.querySelector("form[action='/shop/cart/update']")
var el2 = document.querySelector("div#cart_total")

if (el1) {
    el1.appendChild(child1);
    var template_id = parseInt($($("input.product_template_id")[0]).val())
    $.ajax({
        url: "/bundle/get_bundle_detail",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            jsonrpc: "2.0",
            params: {
                template_id: template_id
            },
        })
    }).then(response => {
            console.log(response.result);
            var data = response.result.bundles
            render_bundle(data)
        }
    ).catch((error) => {
        console.log(error);
    });
}

function render_bundle(data) {
    var html_string = ""
    for (let item of data) {
        if (item.type == "tier") {
            for (let quantity of item.qty) {
                for (let value of item.discount_value) {
                    if (quantity.qty_end < quantity.qty_start && quantity.id == value.id) {
                        html_string += `<div style="display: flex; align-items: center; gap: 12px;"><div>${item.title}: mua ${quantity.qty_start} trở lên, giảm giá ${value.discount_value}</div><div style="border: 1px solid red;" class="bundle-add-to-cart" data-quantity="${quantity.qty_start}" data-template-id="${value.template_id}">Add to cart</div></div><hr>`
                    }
                    if (quantity.qty_end > quantity.qty_start && quantity.id == value.id) {
                        html_string += `<div style="display: flex; align-items: center; gap: 12px;"><div>${item.title}: mua từ ${quantity.qty_start} đến ${quantity.qty_end}, giảm giá ${value.discount_value}</div><div style="border: 1px solid red;" class="bundle-add-to-cart" data-template-id="${value.template_id}" data-quantity="${quantity.qty_start}">Add to cart</div></div><hr>`
                    }
                }
            }
        }

        if (item.type == "bundle") {
            if (item.discount_rule == "discount_total") {
                var count = 0
                var html_string_b = ""
                for (let qty of item.qty_total) {
                    for (let product of item.product_total) {
                        for (let line of item.qty_order) {
                            if (product.template_id == qty.template_id && line.template_id == qty.template_id) {
                                if (line.qty_order >= qty.qty_for_total) {
                                    count += 1
                                }
                            }
                        }
                        if (qty.template_id == product.template_id) {
                            html_string_b += `<div style="display: flex; align-items: center; gap: 12px;"><div> mua ${qty.qty_for_total} ${product.display_name} <img src="${product.img}"></div><div style="border: 1px solid red;" class="bundle-add-to-cart" data-quantity="${qty.qty_for_total}" data-template-id="${product.template_id}">Add to cart</div></div>`
                        }
                    }
                }
                if (item.discount_type == "percentage") {
                    var html_string_a = `<div> ${item.title}: mua combo trọn bộ, giảm ${item.discount_value}% `
                }
                if (item.discount_type == "hard_fixed") {
                    var html_string_a = `<div> ${item.title}: chỉ $${item.discount_value} mua combo trọn bộ `
                }
                if (item.discount_type == "total_fixed") {
                    var html_string_a = `<div> ${item.title}: mua combo trọn bộ, giảm $${item.discount_value}/tổng hóa đơn `
                }
                html_string += html_string_a + html_string_b + `</div><hr>`
            }
            if (item.discount_rule == "discount_product") {
                if (item.discount_type == "percentage") {
                    html_string += `<div style="display: flex; align-items: center; gap: 12px;"><div>${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm ${item.discount_value_each}%</div><div style="border: 1px solid red;" data-quantity="${item.qty_each}" class="bundle-add-to-cart" data-template-id="${item.template_id}">Add to cart</div></div><hr>`
                }
                if (item.discount_type == "hard_fixed") {
                    html_string += `<div style="display: flex; align-items: center; gap: 12px;"><div>${item.title}: chỉ $${item.discount_value_each}/mỗi ${item.qty_each} sản phẩm</div><div style="border: 1px solid red;" data-quantity="${item.qty_each}" class="bundle-add-to-cart" data-template-id="${item.template_id}">Add to cart</div></div><hr>`
                }
                if (item.discount_type == "total_fixed") {
                    html_string += `<div style="display: flex; align-items: center; gap: 12px;"><div>${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm $${item.discount_value_each}</div><div style="border: 1px solid red;" data-quantity="${item.qty_each}" class="bundle-add-to-cart" data-template-id="${item.template_id}">Add to cart</div></div><hr>`
                }
            }
        }
    }
    child1.innerHTML = html_string
}

if (el2) {
    el2.appendChild(child2);
    var order_id = parseInt($($("sup.my_cart_quantity")[0]).attr("data-order-id"))
    $.ajax({
        url: "/bundle/get_bundle_cart",
        method: "POST",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            jsonrpc: "2.0",
            params: {order_id: order_id},
        })
    }).then(response => {
            console.log(response.result);
            var data = response.result.bundle_infors
            render_bundle_cart(data)
        }
    ).catch((error) => {
        console.log(error);
    });
}

function render_bundle_cart(data) {
    var total_price = parseFloat($($("div#cart_total table tbody tr td span.monetary_field span.oe_currency_value")[0]).text().replace(",", ""))
    var list_reduce = []
    var max = 0.0
    for (let item of data) {
        list_reduce.push(item.sale_off)
    }
    for (let i of list_reduce) {
        if (max < i) {
            max = i
        }
    }
    for (let item of data) {
        if (item) {
            $(function () {
                $($("tr#order_total_untaxed td.text-xl-right span.monetary_field span.oe_currency_value")[0]).css("text-decoration", "line-through")
                $($("tr#order_total td.text-xl-right strong.monetary_field span.oe_currency_value")[0]).text((total_price - max).toFixed(2))
                $($("tr#order_total_taxes td.text-right")).text("Sale off")
                $($("tr#order_total_taxes span.oe_currency_value")).text(max)
                $($("tr td.text-xl-right span a.show_coupon")).text('Đã áp dụng mã giảm giá ' + item.title)
            })
        }
    }
}

var check_add_to_cart = setInterval(function () {
    if (document.getElementsByClassName('bundle-add-to-cart').length > 0) {
        clearInterval(check_add_to_cart)
        var divs = document.getElementsByClassName('bundle-add-to-cart')
        if (divs) {
            for (let div of divs) {
                div.addEventListener('click', function () {

                    let add_template_id = div.getAttribute('data-template-id')
                    let add_quantity = div.getAttribute('data-quantity')
                    let add_order_id = parseInt($($("sup.my_cart_quantity")[0]).attr("data-order-id"))

                    $.ajax({
                        url: "/bundle/add_to_cart",
                        method: "POST",
                        contentType: "application/json",
                        dataType: "json",
                        data: JSON.stringify({
                            jsonrpc: "2.0",
                            params: {
                                order_id: add_order_id,
                                quantity: add_quantity,
                                template_id: add_template_id
                            },
                        })
                    }).then(response => {
                            console.log(response.result);
                            window.location.reload()
                        }
                    ).catch((error) => {
                        console.log(error);
                    });
                })
            }
        }
    }
}, 100)
