from odoo import http
from odoo.http import request


class ShopifyIframe(http.Controller):
    @http.route('/iframe/shopify_iframe', type='http', auth="public")
    def shopify_iframe(self):
        return request.render("shopify_odoo.chart_bundle")
