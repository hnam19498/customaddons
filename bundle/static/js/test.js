var child = document.createElement('div');

var el = document.querySelector('form[action="/shop/cart/update"]')
el.appendChild(child);

var template_id = parseInt($($("input.product_template_id")[0]).val())

function render_bundle(data) {
    var html_string = ''
    for (let item of data) {
        if (item.type == 'tier') {
            for (let quantity of item.qty) {
                for (let value of item.discount_value) {
                    if (quantity.qty_end < quantity.qty_start && quantity.id == value.id) {
                        html_string += `
                    <div>${item.title}: mua ${quantity.qty_start} trở lên, giảm giá ${value.discount_value}</div><hr>
                `
                    }
                    if (quantity.qty_end > quantity.qty_start && quantity.id == value.id) {
                        html_string += `
                    <div>${item.title}: mua từ ${quantity.qty_start} đến ${quantity.qty_end}, giảm giá ${value.discount_value}</div><hr>
                `
                    }
                }
            }
        }

        if (item.type == 'bundle') {
            if (item.discount_rule == 'discount_total') {
                var html_string_b = ''
                var html_string_a = `<div> ${item.title}:`
                var html_string_c = `, giảm ${item.discount_value}</div><hr>`
                for (let qty of item.qty_total) {
                    for (let product of item.product_total) {
                        if (qty.id == product.id) {
                            html_string_b += `<span> mua ${qty.qty} ${product.display_name}</span>`
                        }
                    }
                }
                html_string += html_string_a + html_string_b + html_string_c
            }
            if (item.discount_rule == 'discount_product') {
                html_string += `<div>${item.title}: mua mỗi ${item.qty_each} sản phẩm, giảm ${item.discount_value_each}</div><hr>`
            }
        }
    }
    child.innerHTML = html_string
}

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
