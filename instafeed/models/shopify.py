import shopify
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ShopifySettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shopify_client_id = fields.Char('Shopify client ID', config_parameter='instafeed.shopify_client_id')
    base_url = fields.Char('Base URL', config_parameter='instafeed.base_url')
    shopify_api_version = fields.Char('Shopify API version', config_parameter='instafeed.shopify_api_version')
    shopify_client_secret = fields.Char('Shopify client secret', config_parameter='instafeed.shopify_client_secret')
    ngrok_url = fields.Char('Ngrok URL', config_parameter='instafeed.ngrok_url')
    shopify_script_tag_url = fields.Char('Shopify script tag URL', config_parameter='instafeed.shopify_script_tag_url')

    def change_script_tag_url(self):
        shops = self.env['shop.shopify'].sudo().search([])
        if shops:
            for shop in shops:
                shop.is_update_script_tag = False

    def change_ngrok_url(self):
        shops = self.env['shop.shopify'].sudo().search([])
        if shops:
            for shop in shops:
                shop.is_update_ngrok = False


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

    def change_script_tag_url(self):
        try:
            print("start cron job change_script_tag!")
            old_shops = self.env['shop.shopify'].sudo().search([('is_update_script_tag', '=', False)], limit=10)
            shopify_api_version = self.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_api_version')
            for shop in old_shops:
                new_session = shopify.Session(token=shop.access_token, shop_url=shop.url, version=shopify_api_version)
                shopify.ShopifyResource.activate_session(new_session)
                existing_script_tags = shopify.ScriptTag.find()
                if existing_script_tags:
                    for script_tag in existing_script_tags:
                        if script_tag.src != self.shopify_script_tag_url:
                            shopify.ScriptTag.find(script_tag.id).destroy()
                            shopify.ScriptTag.create({
                                "event": "onload",
                                "src": self.shopify_script_tag_url
                            })
                else:
                    shopify.ScriptTag.create({
                        "event": "onload",
                        "src": self.shopify_script_tag_url
                    })
                shop.is_update_script_tag = True
            print("end cron job change_script_tag!")
        except Exception as e:
            print(e)

    def change_ngrok_url(self):
        try:
            print("start cron job change_ngrok!")
            old_shops = self.env['shop.shopify'].sudo().search([('is_update_ngrok', '=', False)], limit=10)
            shopify_api_version = self.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_api_version')
            for shop in old_shops:
                new_session = shopify.Session(token=shop.access_token, shop_url=shop.url, version=shopify_api_version)
                shopify.ShopifyResource.activate_session(new_session)
                existing_webhooks = shopify.Webhook.find()

                if existing_webhooks:
                    for webhook in existing_webhooks:
                        webhook.destroy()

                webhook_products_create = shopify.Webhook()
                webhook_products_create.topic = "products/create"
                webhook_products_create.address = self.ngrok_url + "/webhook/products_create/" + shop.shopify_id
                webhook_products_create.format = "json"
                webhook_products_create.save()
                print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

                webhook_products_update = shopify.Webhook()
                webhook_products_update.topic = "products/update"
                webhook_products_update.address = self.ngrok_url + "/webhook/products_update/" + shop.shopify_id
                webhook_products_update.format = "json"
                webhook_products_update.save()
                print(f"{webhook_products_update.id}: {webhook_products_update.topic}")

                shop.is_update_ngrok = True
            print("end cron job change_ngrok!")
        except Exception as e:
            print(e)

    def fetch_product(self):
        try:
            new_session = shopify.Session(self.url, self.env['ir.config_parameter'].sudo().get_param(
                'instafeed.shopify_api_version'), token=self.access_token)
            shopify.ShopifyResource.activate_session(new_session)
            products = shopify.Product.find()

            exist_products = self.env['shopify.product'].sudo().search([('shop_id', '=', self.id)])
            list_product_ids = []

            if exist_products:
                for product in exist_products:
                    if str(product.shopify_product_id) not in list_product_ids:
                        list_product_ids.append(product.shopify_product_id)

            if products:
                for product in products:
                    if str(product.id) not in list_product_ids:
                        try:
                            self.env['shopify.product'].sudo().create({
                                'shopify_product_id': product.id,
                                'name': product.title,
                                'url': self.url + "/products/" + product.handle,
                                'shop_id': self.id,
                                'price': float(product.variants[0].price),
                                "compare_at_price": product.variants[0].compare_at_price,
                                'qty': product.variants[0].inventory_quantity,
                                "variant_id": product.variants[0].id,
                                'url_img': product.image.src
                            })
                        except Exception as error_create_product:
                            print("error_create_product: " + str(error_create_product))
                            continue
                    else:
                        print(f'Product id "{product.id}" đã trong database!')

        except Exception as e:
            raise ValidationError(_(e))


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
