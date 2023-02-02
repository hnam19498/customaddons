from odoo import http
from odoo.http import request


class ShopifyIframe(http.Controller):
    @http.route('/iframe/shopify_iframe', type='http', auth="public")
    def shopify_iframe(self):
        res = request.render('shopify_odoo.onboarding_stickybar_iframe_template')
        return res
