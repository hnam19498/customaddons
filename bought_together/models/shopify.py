import shopify
from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    client_id = fields.Char('Client ID', config_parameter='bought_together.client_id')
    base_url = fields.Char('Base URL', config_parameter='bought_together.base_url')
    api_version = fields.Char('API version', config_parameter='bought_together.api_version')
    client_secret = fields.Char('Client secret', config_parameter='bought_together.client_secret')
    ngrok_url = fields.Char('Ngrok URL', config_parameter='bought_together.ngrok_url')
    script_tag_url = fields.Char('Script tag URL', config_parameter='bought_together.script_tag_url')

    def change_script_tag_url(self):
        try:
            shops = self.env['shop.shopify'].sudo().search([])
            if shops:
                for shop in shops:
                    shop.is_update_script_tag = False
        except Exception as e:
            print(e)

    def change_ngrok_url(self):
        try:
            shops = self.env['shop.shopify'].sudo().search([])
            if shops:
                for shop in shops:
                    shop.is_update_ngrok = False

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
    is_update_ngrok = fields.Boolean(default=True)

    def change_ngrok_url(self):
        try:
            old_shops = self.sudo().search([('is_update_ngrok', '=', False)], limit=10)
            for shop in old_shops:
                api_version = self.env['ir.config_parameter'].sudo().get_param('bought_together.api_version')
                new_session = shopify.Session(token=shop.access_token, shop_url=shop.url, version=api_version)
                shopify.ShopifyResource.activate_session(new_session)
                ngrok_url = self.env['ir.config_parameter'].sudo().get_param('bought_together.ngrok_url')
                if ngrok_url:
                    existing_webhooks = shopify.Webhook.find()
                    if existing_webhooks:
                        for webhook in existing_webhooks:
                            if webhook.address != ngrok_url + "/webhook/products_create/" + shop.shopify_id:
                                shopify.Webhook.find(webhook.id).destroy()

                                webhook_products_create = shopify.Webhook()
                                webhook_products_create.topic = "products/create"
                                webhook_products_create.address = ngrok_url + "/webhook/products_create/" + shop.shopify_id
                                webhook_products_create.format = "json"
                                webhook_products_create.save()
                                print(f"{webhook_products_create.id}: {webhook_products_create.topic}")
                            else:
                                print(f"{webhook.id}: {webhook.topic}")

                            if webhook.address != ngrok_url + "/webhook/products_update/" + shop.shopify_id:
                                shopify.Webhook.find(webhook.id).destroy()

                                webhook_products_update = shopify.Webhook()
                                webhook_products_update.topic = "products/update"
                                webhook_products_update.address = ngrok_url + "/webhook/products_update/" + shop.shopify_id
                                webhook_products_update.format = "json"
                                webhook_products_update.save()
                                print(f"{webhook_products_update.id}: {webhook_products_update.topic}")
                            else:
                                print(f"{webhook.id}: {webhook.topic}")
                    else:
                        webhook_products_create = shopify.Webhook()
                        webhook_products_create.topic = "products/create"
                        webhook_products_create.address = ngrok_url + "/webhook/products_create/" + shop.shopify_id
                        webhook_products_create.format = "json"
                        webhook_products_create.save()
                        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

                        webhook_products_update = shopify.Webhook()
                        webhook_products_update.topic = "products/update"
                        webhook_products_update.address = ngrok_url + "/webhook/products_update/" + shop.shopify_id
                        webhook_products_update.format = "json"
                        webhook_products_update.save()
                        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")

                shop.is_update_ngrok = True
        except Exception as e:
            print(e)

    def change_script_tag_url(self):
        try:
            new_script_tag = self.env['ir.config_parameter'].sudo().get_param('bought_together.script_tag_url')
            if new_script_tag:
                old_shops = self.sudo().search([('is_update_ngrok', '=', False)], limit=10)
                for shop in old_shops:
                    api_version = self.env['ir.config_parameter'].sudo().get_param('bought_together.api_version')
                    new_session = shopify.Session(token=shop.access_token, shop_url=shop.url, version=api_version)
                    shopify.ShopifyResource.activate_session(new_session)
                    existing_script_tags = shopify.ScriptTag.find()
                    if existing_script_tags:
                        for script_tag in existing_script_tags:
                            if script_tag.src != new_script_tag:
                                shopify.ScriptTag.find(script_tag.id).destroy()
                                shopify.ScriptTag.create({
                                    "event": "onload",
                                    "src": new_script_tag
                                })
                    else:
                        shopify.ScriptTag.create({
                            "event": "onload",
                            "src": new_script_tag
                        })
                    shop.is_update_script_tag = True
        except Exception as e:
            print(e)


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
