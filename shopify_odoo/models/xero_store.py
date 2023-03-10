from odoo import api, models, fields


class XeroStore(models.Model):
    _name = 'xero.store'

    name = fields.Char()
    status_connect = fields.Char(default='Disconnected')
    shop_shopify_id = fields.Many2one('shop.shopify')
    tenantId = fields.Char()

    def connect_xero(self):
        try:
            xero_app = self.env.ref('shopify_odoo.xero_app_data').sudo()
            shop_url = self.env['shop.shopify'].sudo().search([("id", '=', self.shop_shopify_id.id)]).url
            redirectUrl = 'https://login.xero.com/identity/connect/authorize?response_type=code&client_id=' + xero_app.client_id + '&redirect_uri=' + xero_app.redirect_uri + '&scope=openid%20profile%20email%20accounting.transactions%20accounting.contacts%20accounting.settings%20offline_access&state=' + shop_url

            return {
                'type': "ir.actions.act_url",
                'url': redirectUrl
            }
        
        except Exception as e:
            print(e)
            return {
                'type': "ir.actions.act_url",
                'url': 'https://www.xero.com/'
            }
