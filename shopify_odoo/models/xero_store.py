from odoo import api, models, fields


class XeroStore(models.Model):
    _name = 'xero.store'

    name = fields.Char()
    status_connect = fields.Char(default='Disconnected')
    shop_shopify_id = fields.Many2one('shop.shopify')
    tenantId = fields.Char()

    def connect_xero(self):
        shop_url = self.env['shop.shopify'].sudo().search([("id", '=', self.shop_shopify_id.id)]).url
        client_id = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.client_id")
        redirect_uri = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.redirect_uri")
        redirectUrl = 'https://login.xero.com/identity/connect/authorize?response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=openid%20profile%20email%20accounting.transactions%20offline_access&state=' + shop_url

        return {
            'type': "ir.actions.act_url",
            'url': redirectUrl
        }
