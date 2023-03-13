from odoo import api, models, fields


class AppShopify(models.Model):
    _name = 'shopify.app'

    api_key = fields.Char()
    base_url = fields.Char()
    name = fields.Char()
    api_version = fields.Char()
    secret_key = fields.Char()


class Shop(models.Model):
    _name = "shop.shopify"

    shopify_id = fields.Char()
    name = fields.Char()
    email = fields.Char()
    currencyCode = fields.Char()
    url = fields.Char()
    country = fields.Char()
    status = fields.Boolean()
    shopify_owner = fields.Char()
    password = fields.Char()
    admin = fields.Many2one('res.users')
    # fetch_ids = fields.One2many('fetch.shopify', 'shop_id')


class ShopAppShopify(models.Model):
    _name = "shop.app.shopify"

    access_token = fields.Char()
    shop_id = fields.Many2one("shop.shopify")
    app_id = fields.Many2one('shopify.app')
    status = fields.Boolean()
