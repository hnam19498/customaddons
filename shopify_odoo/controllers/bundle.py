from odoo import http, _
from odoo.http import request
import datetime, shopify


class ShopifyBundle(http.Controller):
    @http.route("/shopify_bundle/get_bundle_detail/", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle_detail(self, **kw):

        bundle_ids = []
        shopify_product_id = kw["product_id"]
        product = request.env["shopify.product"].sudo().search([("shopify_product_id", "=", shopify_product_id)], limit=1)
        list_bundle_ids = product.get_list_bundle()
        today = datetime.datetime.now()
        setting_data = request.env["shopify.bundle.setting"].sudo().search([("shop_id", "=", request.env["shopify.product"].sudo().search([("shopify_product_id", "=", kw["product_id"])]).shop_id.id)])
        if setting_data:
            bundle_setting = {
                "color": setting_data.color,
                "bundle_position": setting_data.bundle_position,
                "bundle_label": setting_data.bundle_label,
            }
        else:
            bundle_setting = {
                "color": "black",
                "bundle_position": 'above',
                "bundle_label": ''
            }

        if list_bundle_ids:
            for id in list_bundle_ids:
                if id not in bundle_ids:
                    bundle_ids.append(id)

        if bundle_ids:
            bundle_detail = request.env["shopify.bundle"].sudo().browse(bundle_ids)
            bundle_infors = []
            quantity_infors = []
            for bundle in bundle_detail:
                bundle_infors.append({
                    "bundle_id": bundle.id,
                    "discount_value": bundle.discount_value,
                    "title": bundle.title
                })

                if bundle.indefinite_bundle or bundle.start_time <= today <= bundle.end_time:
                    product_lines = request.env["bundle.product.quantity"].sudo().search([("bundle_id", "=", bundle.id)])
                    for line in product_lines:
                        quantity_infors.append({
                            "product_id": line.product_id.id,
                            "product_name": request.env["shopify.product"].sudo().search([("id", "=", line.product_id.id)], limit=1).name,
                            "bundle_id": line.bundle_id.id,
                            "quantity": line.qty,
                            "img": request.env["shopify.product"].sudo().search([("id", "=", line.product_id.id)], limit=1).url_img,
                        })

            return {
                "bundle_infors": bundle_infors,
                "bundle_setting": bundle_setting,
                "quantity_infors": quantity_infors
            }
        else:
            return {"bundle_infors": []}

    @http.route("/shopify_bundle/cart/", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def cart(self, **kw):

        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")
        list_time = []
        list_bundle = []
        draft_order_url = 0
        price = []

        for line in kw["cart_infors"]:
            product_id = request.env["shopify.product"].sudo().search([("shopify_product_id", "=", line["product_id"])]).id
            bundles = request.env["bundle.product.quantity"].sudo().search([("product_id", "=", product_id)])
            if bundles:
                for bundle in bundles:
                    if product_id == bundle.product_id.id and line["quantity"] >= bundle.qty:
                        b = {
                            "bundle_id": bundle.bundle_id.id,
                            "product_id": product_id,
                            "quantity": request.env["bundle.product.quantity"].sudo().search([("product_id", "=", product_id), ("bundle_id", "=", bundle["bundle_id"].id)]).qty,
                            "time": line["quantity"] // bundle.qty
                        }
                        if b not in list_time:
                            list_time.append(b)

        for item in list_time:
            count = 0
            line = request.env["bundle.product.quantity"].sudo().search([("bundle_id", "=", item["bundle_id"])])
            line_bundle = {
                "bundle_id": item["bundle_id"],
                "line": len(line)
            }

            for x in list_time:
                if x["bundle_id"] == line_bundle["bundle_id"]:
                    count += 1

            if count == line_bundle["line"]:
                min_time = 100000
                for line in list_time:
                    if line["bundle_id"] == line_bundle["bundle_id"]:
                        if min_time > line["time"]:
                            min_time = line["time"]

                bundle = request.env["shopify.bundle"].sudo().search([("id", "=", line_bundle["bundle_id"])], limit=1)
                data_bundle = {"bundle": bundle, "time": min_time}
                if data_bundle not in list_bundle:
                    list_bundle.append(data_bundle)

        bundles = []
        for line in list_bundle:
            bundles.append({
                "bundle_id": line["bundle"].id,
                "discount_value": line["bundle"].discount_value,
                "description": line["bundle"].description,
                "title": line["bundle"].title,
                "time": line["time"]
            })

        for bundle in bundles:
            price_reduce = 0
            for time in list_time:
                if bundle["bundle_id"] == time["bundle_id"]:
                    price_reduce += bundle["time"] * request.env["shopify.product"].sudo().search([("id", "=", time["product_id"])]).price * time["quantity"] * bundle["discount_value"] / 100

            temp_price = {
                "bundle_id": bundle["bundle_id"],
                "price_reduce": price_reduce,
                "time": bundle["time"],
            }

            if temp_price not in price:
                price.append(temp_price)

        if price:
            maxx = 0
            list_items = []
            for line in price:
                if line["price_reduce"] > maxx:
                    maxx = line["price_reduce"]
                    max_bundle = line

            for line in kw["cart_infors"]:
                list_items.append({
                    "quantity": line["quantity"],
                    "variant_id": line["variant_id"]
                })

            session = shopify.Session(kw["shop_url"], api_version, request.env["shop.shopify"].sudo().search([("url", "=", kw["shop_url"])]).token)
            shopify.ShopifyResource.activate_session(session)

            # price_rule = shopify.PriceRule.create({
            #     "title": "Hnam",
            #     "target_selection": "all",
            #     "allocation_method": "across",
            #     "value_type": "fixed_amount",
            #     "value": str(-max_bundle["price_reduce"]),
            #     "once_per_customer": "true",
            #     "customer_selection": "all",
            #     "starts_at": str(today)
            # })
            #
            # discount_code = shopify.DiscountCode.create({
            #     "code": "discount_code_" + str(int(max_bundle["price_reduce"])),
            #     "price_rule_id": price_rule.attributes["id"],
            # })
            # print(discount_code)

            draft_order = shopify.DraftOrder.create({
                "line_items": list_items,
                "applied_discount": {
                    "value": max_bundle["price_reduce"],
                    "value_type": "fixed_amount"
                }
            })

            count_bundle = request.env["count.bundle.order"].sudo().search([("draft_order_id", "=", draft_order.attributes["id"])])
            if not count_bundle:
                count_bundle.sudo().create({
                    "draft_order_id": draft_order.attributes["id"],
                    "bundle_id": max_bundle["bundle_id"],
                    "time": max_bundle["time"],
                    "price_reduce": max_bundle["price_reduce"],
                    "date": datetime.date.today()
                })

            draft_order_url = draft_order.invoice_url

        if draft_order_url != 0:
            bundle = request.env["shopify.bundle"].sudo().search([("id", "=", max_bundle["bundle_id"])])
            return {
                "draft_order_url": draft_order_url,
                "max_bundle": max_bundle,
                "bundle_discount_value": bundle.discount_value,
                "bundle_title": bundle.title,
            }
