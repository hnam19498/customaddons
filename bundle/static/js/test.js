var child = document.createElement('div');
var el = document.querySelector('form[action="/shop/cart/update"]')

if (el) {
    el.appendChild(child);
    var template_id = parseInt($($("input.product_template_id")[0]).val())
    $.ajax({
        url: '/bundle/get_bundle',
        method: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
            jsonrpc: "2.0",
            params: {
                message: 'Hi',
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
    var selected_style = ''
    var html_string = ""
    for (let item of data) {
        if (item.type == 'tier') {
            for (let quantity of item.qty) {
                for (let line of item.qty_order) {
                    if (line.template_id == quantity.template_id) {
                        if (quantity.qty_start <= quantity.qty_end) {
                            if (quantity.qty_start <= line.qty_order && line.qty_order <= quantity.qty_end) {
                                selected_style = 'border: 1px solid red'
                            } else {
                                selected_style = ''
                            }
                        }
                        if (quantity.qty_start >= quantity.qty_end) {
                            if (quantity.qty_start <= line.qty_order) {
                                selected_style = 'border: 1px solid red'
                            } else {
                                selected_style = ''
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

        if (item.type == 'bundle') {
            if (item.discount_rule == 'discount_total') {
                var html_string_b = ''
                var html_string_a = `<div style="${selected_style}"> ${item.title}: mua combo trọn bộ, giảm ${item.discount_value}`
                for (let qty of item.qty_total) {
                    for (let product of item.product_total) {
                        for (let line of item.qty_order) {
                            if (product.template_id == qty.template_id) {
                                if (line.qty_order >= qty.qty) {
                                    selected_style = 'border: 1px solid red'
                                } else {
                                    selected_style = ''
                                }
                            } else {
                                selected_style = ''
                            }
                        }
                        if (qty.template_id == product.template_id) {
                            html_string_b += `<p> mua ${qty.qty} ${product.display_name} <img src="${product.img}"></p>`
                        }
                    }
                }
                html_string += html_string_a + html_string_b + `</div><hr>`
            }
            if (item.discount_rule == 'discount_product') {
                for (let line of item.qty_order) {
                    if (line.qty_order >= item.qty_each) {
                        selected_style = 'border: 1px solid red'
                    } else {
                        selected_style = ''
                    }
                }
                html_string += `<div style="${selected_style}">${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm ${item.discount_value_each}</div><hr>`
            }
        }
    }
    child.innerHTML = html_string
}