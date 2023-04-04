import shopify
from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char('API Key', config_parameter='bought_together.api_key')
    base_url = fields.Char('Base URL', config_parameter='bought_together.base_url')
    api_version = fields.Char('API version', config_parameter='bought_together.api_version')
    secret_key = fields.Char('Secret Key', config_parameter='bought_together.secret_key')
    ngrok_url = fields.Char('Ngrok URL', config_parameter='bought_together.ngrok_url')
    script_tag_url = fields.Char('Script tag URL', config_parameter='bought_together.script_tag_url')

    def change_script_tag_url(self):
        try:
            shops = self.env['shop.shopify'].sudo().search([])
            if shops:
                for shop in shops:
                    shop.is_update_script_tag = False

                old_shops = self.env['shop.shopify'].sudo().search([('is_update_script_tag', '=', False)], limit=10)
                for shop in old_shops:
                    new_session = shopify.Session(shop.url, self.api_version, token=shop.access_token)
                    shopify.ShopifyResource.activate_session(new_session)
                    existing_script_tags = shopify.ScriptTag.find()
                    if existing_script_tags:
                        for script_tag in existing_script_tags:
                            if script_tag.src != self.script_tag_url:
                                shopify.ScriptTag.find(script_tag.id).destroy()
                                shopify.ScriptTag.create({
                                    "event": "onload",
                                    "src": self.script_tag_url
                                })
                    else:
                        shopify.ScriptTag.create({
                            "event": "onload",
                            "src": self.script_tag_url
                        })
                    shop.is_update_script_tag = True
        except Exception as e:
            print(e)


class Shop(models.Model):
    _name = "shop.shopify"

    shopify_id = fields.Char()
    name = fields.Char()
    email = fields.Char()
    access_token = fields.Char()
    currencyCode = fields.Char()
    url = fields.Char()
    country = fields.Char()
    status = fields.Boolean()
    shopify_owner = fields.Char()
    password = fields.Char()
    product_ids = fields.One2many("shopify.product", 'shop_id')
    admin = fields.Many2one('res.users')
    is_update_script_tag = fields.Boolean()


class ShopifyProduct(models.Model):
    _name = 'shopify.product'

    shopify_product_id = fields.Char()
    name = fields.Char()
    shop_id = fields.Many2one('shop.shopify')
    price = fields.Float()
    qty = fields.Integer('Quantity')
    url = fields.Char()
    url_img = fields.Char()
    compare_at_price = fields.Float()
    variant_id = fields.Char()


class ShopifyWidget(models.Model):
    _name = "shopify.widget"

    widget_description = fields.Char()
    title_color = fields.Char()
    status = fields.Boolean()
    recommendation_product_ids = fields.Many2many('shopify.product', "widget_recommendation_product")
    background_color = fields.Char()
    excluded_product_ids = fields.Many2many('shopify.product', "widget_excluded_product")
    description_font_size = fields.Char()
    btn_text = fields.Char()
    widget_title = fields.Char()
    total_price = fields.Float()
    total_compare_at_price = fields.Float()
    description_color = fields.Char()
    border_color = fields.Char()
    title_font_size = fields.Char()
    text_color = fields.Char()
    shop_id = fields.Many2one('shop.shopify')
