from odoo import http
from odoo.http import request


class BoughtTogether(http.Controller):
    @http.route('/instafeed', auth='user', type='http', website=True)
    def instafeed_index(self):
        return request.render('instafeed.instafeed')
