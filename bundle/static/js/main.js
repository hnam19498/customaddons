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
    var selected_style = ""
    var html_string = ""
    for (let item of data) {
        if (item.type == "tier") {
            for (let quantity of item.qty) {
                for (let line of item.qty_order) {
                    if (line.template_id == quantity.template_id) {
                        if (quantity.qty_start <= quantity.qty_end) {
                            if (quantity.qty_start <= line.qty_order && line.qty_order <= quantity.qty_end) {
                                selected_style = "border: 1px solid red"
                            } else {
                                selected_style = ""
                            }
                        }
                        if (quantity.qty_start >= quantity.qty_end) {
                            if (quantity.qty_start <= line.qty_order) {
                                selected_style = "border: 1px solid red"
                            } else {
                                selected_style = ""
                            }
                        }
                    }
                }
                for (let value of item.discount_value) {
                    if (quantity.qty_end < quantity.qty_start && quantity.id == value.id) {
                        html_string += `<div style="${selected_style}">${item.title}: mua ${quantity.qty_start} trở lên, giảm giá ${value.discount_value}</div><hr>`
                    }
                    if (quantity.qty_end > quantity.qty_start && quantity.id == value.id) {
                        html_string += `<div style="${selected_style}">${item.title}: mua từ ${quantity.qty_start} đến ${quantity.qty_end}, giảm giá ${value.discount_value}</div><hr>`
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
                            if (count == (item.product_total).length) {
                                selected_style = "border: 1px solid red"
                            } else selected_style = ""
                            html_string_b += `<p> mua ${qty.qty_for_total} ${product.display_name} <img src="${product.img}"></p>`
                        }
                    }
                }
                if (item.discount_type == "percentage") {
                    var html_string_a = `<div style="${selected_style}"> ${item.title}: mua combo trọn bộ, giảm ${item.discount_value}%`
                }
                if (item.discount_type == "hard_fixed") {
                    var html_string_a = `<div style="${selected_style}"> ${item.title}: chỉ $${item.discount_value} mua combo trọn bộ`
                }
                if (item.discount_type == "total_fixed") {
                    var html_string_a = `<div style="${selected_style}"> ${item.title}: mua combo trọn bộ, giảm $${item.discount_value}/tổng hóa đơn`
                }
                html_string += html_string_a + html_string_b + `</div><hr>`
            }
            if (item.discount_rule == "discount_product") {
                for (let line of item.qty_order) {
                    if (line.qty_order >= item.qty_each) {
                        selected_style = "border: 1px solid red"
                    } else {
                        selected_style = ""
                    }
                }
                if (item.discount_type == "percentage") {
                    html_string += `<div style="${selected_style}">${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm ${item.discount_value_each}%</div><hr>`
                }
                if (item.discount_type == "hard_fixed") {
                    html_string += `<div style="${selected_style}">${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm $${item.discount_value_each}/sản phẩm</div><hr>`
                }
                if (item.discount_type == "total_fixed") {
                    html_string += `<div style="${selected_style}">${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm $${item.discount_value_each}</div><hr>`
                }
            }
        }
    }
    child1.innerHTML = html_string
}

if (el2) {
    el2.appendChild(child2);
    var order_id = parseInt($($("sup.my_cart_quantity.badge-primary")[0]).attr("data-order-id"))
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
            })
        }
    }
}