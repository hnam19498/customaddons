from odoo import http, _
from odoo.http import request


class BundleMain(http.Controller):
    @http.route('/bundle/get_bundle', auth="public", type="json", csrf=False, cors='*', save_session=False)
    def get_bundle(self, **kw):
        bundle_ids = []
        bundles = []
        template_id = kw['template_id']
        template = request.env['product.template'].sudo().search([('id', '=', template_id)], limit=1)

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
            qty_tier = []
            qty_total = []
            discount_value_tier = []
            if item.type == "tier":
                for temp in item.bundle_to_qty_ids:
                    qty_tier.append({
                        'id': temp.id,
                        'qty_start': temp.qty_start,
                        'qty_end': temp.qty_end,
                    })
                    discount_value_tier.append({
                        "id": temp.id,
                        "discount_value": temp.discount_value,
                    })

                bundles.append({
                    'title': item.title,
                    'type': item.type,
                    'qty': qty_tier,
                    "discount_value": discount_value_tier,
                })

            if item.type == 'bundle' and item.discount_rule == 'discount_total':
                for temp in item.bundle_total_product_ids:
                    qty_total.append({
                        "id": temp.id,
                        'qty': temp.qty
                    })
                    product_total.append({
                        'display_name': temp.display_name,
                        'id': temp.id
                    })

                bundles.append({
                    'title': item.title,
                    'type': item.type,
                    "discount_rule": item.discount_rule,
                    'qty_total': qty_total,
                    'product_total': product_total,
                    "discount_value": item.discount_value,
                })

        return {'bundles': bundles}
