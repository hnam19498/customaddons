from odoo import http, _
from odoo.http import request
from datetime import datetime, time


class BundleMain(http.Controller):
    @http.route("/bundle/get_bundle_detail", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle_detail(self, **kw):

        order_id = request.session.sale_order_id
        order = request.env["sale.order"].sudo().search([("id", "=", order_id)], limit=1)
        bundle_ids = []
        bundles = []
        template_id = kw["template_id"]
        template = request.env["product.template"].sudo().search([("id", "=", template_id)], limit=1)

        bundle_tier_ids = template.get_list_bundle_tier()
        for id in bundle_tier_ids:
            if id not in bundle_ids:
                bundle_ids.append(id)

        bundle_product_ids = template.get_list_bundle_product()
        for id in bundle_product_ids:
            if id not in bundle_ids:
                bundle_ids.append(id)

        bundle_total_ids = template.get_list_bundle_total()
        for id in bundle_total_ids:
            if id not in bundle_ids:
                bundle_ids.append(id)

        bundle_detail = request.env["product.bundle"].browse(bundle_ids)

        for item in bundle_detail:
            product_total = []
            qty_order = []
            qty_tier = []
            qty_total = []
            discount_value_tier = []
            if item.type == "tier":
                for line in order.order_line:
                    qty_order.append({
                        "template_id": line.product_template_id.id,
                        'qty_order': line.product_uom_qty,
                    })
                for temp in item.bundle_to_qty_ids:
                    qty_tier.append({
                        "id": temp.id,
                        "template_id": template_id,
                        "qty_start": temp.qty_start,
                        "qty_end": temp.qty_end,
                    })
                    discount_value_tier.append({
                        "id": temp.id,
                        'template_id': template_id,
                        "discount_value": temp.discount_value,
                    })

                bundles.append({
                    "title": item.title,
                    "qty_order": qty_order,
                    "type": item.type,
                    "qty": qty_tier,
                    'discount_type': item.discount_type,
                    "discount_value": discount_value_tier,
                    'product_price': template.list_price,
                })

            if item.type == "bundle":
                if item.discount_rule == "discount_total":
                    for line in order.order_line:
                        qty_order.append({
                            "template_id": line.product_template_id.id,
                            'qty_order': line.product_uom_qty,
                            'bundle_id': item.id,
                        })
                    for temp in item.bundle_total_product_ids:
                        qty_total.append({
                            "template_id": temp.id,
                            "qty_for_total": temp.qty,
                            'bundle_id': item.id,
                        })
                        product_total.append({
                            "template_id": temp.id,
                            "display_name": temp.display_name,
                            'bundle_id': item.id,
                            'product_price': temp.list_price,
                            'img': 'data:image/jpeg;base64,' + temp.image_128.decode("utf-8")
                        })

                    bundles.append({
                        "title": item.title,
                        "type": item.type,
                        "discount_rule": item.discount_rule,
                        "qty_total": qty_total,
                        'qty_order': qty_order,
                        "product_total": product_total,
                        "discount_value": item.discount_value,
                        'id': item.id,
                        'discount_type': item.discount_type,
                    })

                if item.discount_rule == "discount_product":
                    for line in order.order_line:
                        qty_order.append({
                            "template_id": line.product_template_id.id,
                            'qty_order': line.product_uom_qty
                        })
                    for temp in item.bundle_each_product_ids:
                        if temp.id == template_id:
                            bundles.append({
                                "title": item.title,
                                "type": item.type,
                                'discount_type': item.discount_type,
                                "discount_rule": item.discount_rule,
                                "qty_each": temp.qty,
                                "template_id": template_id,
                                'qty_order': qty_order,
                                'product_price': temp.list_price,
                                "discount_value_each": temp.discount_value,
                            })

        return {"bundles": bundles}

    @http.route("/bundle/get_bundle_cart", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle_cart(self, **kw):

        today = datetime.now()
        list_time = []
        price_total = 0.0
        price_total2 = 0.0
        price_reduce = 0.0
        line_infor = []
        order_id = kw["order_id"]
        order = request.env["sale.order"].sudo().search([("id", "=", order_id)])
        bundle_ids = []
        product_total = []
        count_time = 0

        for line in order.order_line:
            for template in line.product_template_id:
                bundle_tier_ids = template.get_list_bundle_tier()
                for id in bundle_tier_ids:
                    if id not in bundle_ids:
                        bundle_ids.append(id)

                bundle_product_ids = template.get_list_bundle_product()
                for id in bundle_product_ids:
                    if id not in bundle_ids:
                        bundle_ids.append(id)

                bundle_total_ids = template.get_list_bundle_total()
                for id in bundle_total_ids:
                    if id not in bundle_ids:
                        bundle_ids.append(id)
                bundles = request.env["product.bundle"].browse(bundle_ids)

        if bundles:
            for bundle in bundles:
                count_product = 0
                count = 0
                bundle.sale_off = 0
                for line in order.order_line:
                    if bundle.indefinite_bundle or bundle.start_time <= today <= bundle.end_time:
                        if bundle.type == 'tier':
                            for item in bundle.bundle_tier_product_ids:
                                if line.product_template_id.id == item.id:
                                    if bundle.discount_type == 'total_fixed':
                                        for temp in bundle.bundle_to_qty_ids:
                                            if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                                bundle.sale_off = temp.discount_value

                                            if temp.qty_start > temp.qty_end:
                                                if line.product_uom_qty >= temp.qty_start:
                                                    bundle.sale_off = temp.discount_value

                                    # if bundle.discount_type == 'hard_fixed':
                                    #     for temp in bundle.bundle_to_qty_ids:
                                    #         if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                    #             bundle.sale_off = line.product_uom_qty * line.price_unit - temp.discount_value
                                    #
                                    #         if temp.qty_start > temp.qty_end:
                                    #             if line.product_uom_qty >= temp.qty_start:
                                    #                 bundle.sale_off = line.product_uom_qty * line.price_unit - temp.discount_value

                                    if bundle.discount_type == 'percentage':
                                        for temp in bundle.bundle_to_qty_ids:
                                            if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                                bundle.sale_off = temp.discount_value / 100 * line.price_unit * line.product_uom_qty

                                            if temp.qty_start > temp.qty_end:
                                                if line.product_uom_qty >= temp.qty_start:
                                                    bundle.sale_off = temp.discount_value / 100 * line.price_unit * line.product_uom_qty

                        if bundle.type == 'bundle':
                            if bundle.discount_rule == 'discount_product':
                                for item in bundle.bundle_each_product_ids:
                                    if line.product_template_id.id == item.id:
                                        time = line.product_uom_qty // bundle.bundle_each_product_ids.qty
                                        remainder = line.product_uom_qty % bundle.bundle_each_product_ids.qty
                                        if bundle.discount_type == 'total_fixed':
                                            bundle.price_after_reduce = line.price_unit * line.product_uom_qty - time * bundle.bundle_each_product_ids.discount_value
                                            bundle.sale_off = time * bundle.bundle_each_product_ids.discount_value
                                        if bundle.discount_type == 'hard_fixed':
                                            bundle.sale_off = bundle.bundle_each_product_ids.qty * line.price_unit * time - time * bundle.bundle_each_product_ids.discount_value
                                        if bundle.discount_type == 'percentage':
                                            bundle.sale_off = time * (1 - bundle.bundle_each_product_ids.discount_value / 100)

                            if bundle.discount_rule == 'discount_total':
                                for item in bundle.bundle_total_product_ids:
                                    for linee in order.order_line:
                                        if item.id == linee.product_template_id.id:
                                            if linee.product_uom_qty >= item.qty:
                                                count_product += 1
                                                b = {'bundle_id': bundle.id, "template_id": item.id, 'time': linee.product_uom_qty // item.qty}
                                                if b not in list_time:
                                                    list_time.append(b)

                                if count_product == len(bundle.bundle_total_product_ids):
                                    price_total = 0
                                    for item in bundle.bundle_total_product_ids:
                                        min_time = 1000000
                                        for x in list_time:
                                            if x['bundle_id'] == bundle.id and x['template_id'] == item.id:
                                                if x['time'] < min_time:
                                                    min_time = x['time']

                                        for linee in order.order_line:
                                            if linee.product_template_id.id == item.id:
                                                price_total += linee.product_uom_qty * item.list_price

                                    if bundle.discount_type == 'total_fixed':
                                        bundle.sale_off = bundle.discount_value * min_time
                                    if bundle.discount_type == 'percentage':
                                        bundle.price_after_reduce = price_total * (1 - bundle.discount_value / 100)
                                        bundle.sale_off = price_total * bundle.discount_value / 100
                                    if bundle.discount_type == 'hard_fixed':
                                        for item in bundle.bundle_total_product_ids:
                                            for linee in order.order_line:
                                                if linee.product_template_id.id == item.id and count < len(bundle.bundle_total_product_ids):
                                                    price_total2 += min_time * item.qty * linee.price_unit
                                                    count += 1
                                        bundle.sale_off = price_total2 - min_time * bundle.discount_value

        bundle_infors = []
        for bundle in bundles:
            if bundle.sale_off != 0:
                bundle_infors.append({
                    'id': bundle.id,
                    'sale_off': bundle.sale_off,
                    'title': bundle.title,
                })

        return {'bundle_infors': bundle_infors}

    @http.route("/bundle/add_to_cart", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def add_to_cart(self, **kw):
        order_id = int(kw['order_id'])
        product = request.env["product.template"].sudo().search([("id", "=", kw['template_id'])]).product_variant_id
        order = request.env["sale.order"].sudo().search([("id", "=", order_id)])
        template = request.env["product.template"].sudo().search([("id", "=", int(kw['template_id']))])
        template_in_order = order.order_line.product_template_id
        if order.order_line:
            for line in order.order_line:
                if template in template_in_order:
                    if int(kw['template_id']) == line.product_template_id.id:
                        line.sudo().write({
                            'product_uom_qty': line.product_uom_qty + int(kw['quantity']),
                        })
                else:
                    request.env["sale.order.line"].sudo().create({
                        'product_template_id': int(kw['template_id']),
                        'product_uom_qty': int(kw['quantity']),
                        'order_id': order_id,
                        'name': template.name,
                        'product_id': product.id,
                        'customer_lead': 0,
                        "price_unit": product.lst_price,
                    })

        else:
            request.env["sale.order.line"].sudo().create({
                'product_template_id': int(kw['template_id']),
                'product_uom_qty': int(kw['quantity']),
                'order_id': order_id,
                'name': template.name,
                'product_id': product.id,
                'customer_lead': 0,
                "price_unit": product.lst_price,
            })
