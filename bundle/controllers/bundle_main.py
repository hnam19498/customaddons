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
                            "qty": temp.qty,
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
                                'qty_order': qty_order,
                                'product_price': temp.list_price,
                                "discount_value_each": temp.discount_value,
                            })

        return {"bundles": bundles}

    @http.route("/bundle/get_bundle_cart", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle_cart(self, **kw):

        today = datetime.now()
        price_total = 0
        price_reduce = 0.0
        line_infor = []
        order_id = kw["order_id"]
        order = request.env["sale.order"].sudo().search([("id", "=", order_id)])
        bundle_ids = []
        product_total = []

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
                bundle.sale_off = 0
                for line in order.order_line:
                    if bundle.indefinite_bundle or bundle.start_time <= today <= bundle.end_time:
                        if bundle.type == 'tier':
                            for item in bundle.bundle_tier_product_ids:
                                if line.product_template_id.id == item.id:
                                    if bundle.discount_type == 'total_fixed':
                                        for temp in bundle.bundle_to_qty_ids:
                                            if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                                bundle.price_after_reduce = line.price_unit * line.product_uom_qty - temp.discount_value
                                                bundle.sale_off = temp.discount_value

                                            if temp.qty_start > temp.qty_end:
                                                if line.product_uom_qty >= temp.qty_start:
                                                    bundle.price_after_reduce = line.price_unit * line.product_uom_qty - temp.discount_value
                                                    bundle.sale_off = temp.discount_value

                                    if bundle.discount_type == 'hard_fixed':
                                        for temp in bundle.bundle_to_qty_ids:
                                            if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                                bundle.price_after_reduce = line.price_unit * line.product_uom_qty - temp.discount_value * line.product_uom_qty
                                                bundle.sale_off = temp.discount_value * line.product_uom_qty

                                            if temp.qty_start > temp.qty_end:
                                                if line.product_uom_qty >= temp.qty_start:
                                                    bundle.price_after_reduce = line.price_unit * line.product_uom_qty - temp.discount_value * line.product_uom_qty
                                                    bundle.sale_off = temp.discount_value * line.product_uom_qty

                                    if bundle.discount_type == 'percentage':
                                        for temp in bundle.bundle_to_qty_ids:
                                            if temp.qty_start <= line.product_uom_qty <= temp.qty_end:
                                                bundle.price_after_reduce = line.price_unit * line.product_uom_qty * (
                                                        1 - temp.discount_value / 100)
                                                bundle.sale_off = temp.discount_value / 100 * line.price_unit * line.product_uom_qty

                                            if temp.qty_start > temp.qty_end:
                                                if line.product_uom_qty >= temp.qty_start:
                                                    bundle.sale_off = temp.discount_value / 100 * line.price_unit * line.product_uom_qty
                                                    bundle.price_after_reduce = line.price_unit * line.product_uom_qty * (
                                                            1 - temp.discount_value / 100)

                        if bundle.type == 'bundle':
                            if bundle.discount_rule == 'discount_product':
                                for item in bundle.bundle_each_product_ids:
                                    if line.product_template_id.id == item.id:
                                        time = line.product_uom_qty // bundle.bundle_each_product_ids.qty
                                        remainder = line.product_uom_qty % bundle.bundle_each_product_ids.qty
                                        if bundle.discount_type == 'total_fixed':
                                            bundle.price_after_reduce = line.price_unit * line.product_uom_qty - time * bundle.bundle_each_product_ids.discount_value
                                            bundle.sale_off = line.price_unit * line.product_uom_qty - bundle.price_after_reduce
                                        if bundle.discount_type == 'hard_fixed':
                                            bundle.price_after_reduce = line.price_unit * line.product_uom_qty - time * bundle.bundle_each_product_ids.discount_value * line.product_uom_qty
                                            bundle.sale_off = line.price_unit * line.product_uom_qty - bundle.price_after_reduce
                                        if bundle.discount_type == 'percentage':
                                            bundle.price_after_reduce = line.price_unit * line.product_uom_qty - time * (
                                                    1 - bundle.bundle_each_product_ids.discount_value / 100)
                                            bundle.sale_off = line.price_unit * line.product_uom_qty - bundle.price_after_reduce

                            if bundle.discount_rule == 'discount_total':
                                for item in bundle.bundle_total_product_ids:
                                    if line.product_template_id.id == item.id:
                                        if line.product_uom_qty >= item.qty:
                                            bundle.check_total = True
                                        else:
                                            bundle.check_total = False
                                    else:
                                        bundle.check_total = False

                                if bundle.check_total:
                                    for item in bundle.bundle_total_product_ids:
                                        if line.product_template_id.id == item.id:
                                            price_total += line.product_uom_qty * item.list_price
                                    if bundle.discount_type == 'percentage':
                                        bundle.price_after_reduce = price_total * (1 - bundle.discount_value / 100)
                                        bundle.sale_off = price_total * bundle.discount_value / 100
                                    if bundle.discount_type == 'total_fixed':
                                        bundle.price_after_reduce = price_total - bundle.discount_value
                                        bundle.sale_off = bundle.discount_value
                                    if bundle.discount_type == 'hard_fixed':
                                        for item in bundle.bundle_total_product_ids:
                                            if line.product_template_id.id == item.id:
                                                price_reduce -= line.product_uom_qty * bundle.discount_value
                                        bundle.price_after_reduce = price_total + price_reduce
                                        bundle.sale_off = -price_reduce


        bundle_infors = []
        for bundle in bundles:
            if bundle.sale_off != 0:
                bundle_infors.append({
                    'id': bundle.id,
                    'title': bundle.title,
                    'sale_off': bundle.sale_off,
                    'price_after_reduce': bundle.price_after_reduce,
                })

        return {'bundle_infors': bundle_infors}
