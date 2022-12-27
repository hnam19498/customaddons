from odoo import http, _
from odoo.http import request


class BundleMain(http.Controller):
    @http.route("/bundle/get_bundle", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle(self, **kw):

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
                        'qty_order': line.product_uom_qty
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
                    "discount_value": discount_value_tier,
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
                                "discount_rule": item.discount_rule,
                                "qty_each": temp.qty,
                                'qty_order': qty_order,
                                "discount_value_each": temp.discount_value,
                            })

        return {"bundles": bundles}
