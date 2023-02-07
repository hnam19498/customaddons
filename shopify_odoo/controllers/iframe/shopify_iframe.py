from odoo import http
from odoo.http import request


class ShopifyIframe(http.Controller):
    @http.route('/iframe/shopify_iframe', auth="public", type='http')
    def shopify_iframe(self, **kw):
        data = []
        bundle_id = kw['bundle_id']
        data_analytic = request.env["count.bundle.database"].sudo().search([("bundle_id", '=', bundle_id)])
        if data_analytic:
            for line in data_analytic:
                data.append({"date": str(line.date), "time": line.time, 'price_reduce': line.price_reduce})

        return request.render("shopify_odoo.chart_bundle", {'data': data})
