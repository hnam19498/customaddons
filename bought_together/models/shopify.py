from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char('API Key', config_parameter='bought_together.api_key')
    base_url = fields.Char('Base URL', config_parameter='bought_together.base_url')
    api_version = fields.Char('API version', config_parameter='bought_together.api_version')
    secret_key = fields.Char('Secret Key', config_parameter='bought_together.secret_key')


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
