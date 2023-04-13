from odoo import http
from odoo.http import request


class BoughtTogether(http.Controller):
    @http.route('/instafeed', auth='user', type='http', website=True)
    def instafeed_index(self, **kw):
        current_user = request.env.user
        current_shopify = request.env['shop.shopify'].sudo().search([('admin', '=', current_user.id)], limit=1)
        instagram_user = request.env['instagram.user'].sudo().search([('shop_shopify', "=", current_shopify.id)], limit=1)
        facebook_user = request.env['facebook.user'].sudo().search([('shop_shopify', "=", current_shopify.id)])
        return request.render(
            'instafeed.instafeed', {
                'data': {
                    'users': {
                        'instagram_username': instagram_user.username,
                        'facebook_username': facebook_user.username
                    }
                }
            }
        )
