from odoo import api, models, fields, _
import shopify,datetime


class FetchShopify(models.Model):
    _name = 'fetch.shopify'

    start_date = fields.Date()
    end_date = fields.Date()
    shopify_order_ids = fields.One2many('shopify.order', "fetch_order_id")
    shop_id = fields.Many2one('shop.shopify')
    shopify_product_ids = fields.One2many('shopify.product', "fetch_product_id")

    def fetch_order(self):
        list_order_ids = []
        count_fetch_order = 0

        api_key = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify_access_token = self.shop_id.token
        store_url = self.shop_id.url
        new_session = shopify.Session(store_url, api_version, token=shopify_access_token)
        shopify.ShopifyResource.activate_session(new_session)

        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")

        exist_orders = self.env['shopify.order'].sudo().search([])
        if exist_orders:
            for order in exist_orders:
                if order.shopify_order_id not in list_order_ids:
                    list_order_ids.append(order.shopify_order_id)

        list_quantity = []
        orders = shopify.Order.find(published_at_min=start_date, published_at_max=end_date, status='any')

        if orders:
            for order in orders:
                odoo_products = []
                for line in order.line_items:
                    test_product = self.env['shopify.product'].sudo().search([('shopify_product_id', '=', line.product_id)])
                    if test_product:
                        odoo_products.append(test_product.id)
                    else:
                        print("Chưa có sản phẩm trong database!")

                    temp = {"product_id": test_product.id,
                            'order_id': self.env['shopify.order'].sudo().search([('shopify_order_id', '=', order.id)]).id,
                            "quantity": line.attributes['quantity']}

                    if temp not in list_quantity:
                        list_quantity.append(temp)

                if str(order.id) not in list_order_ids:
                    self.env['shopify.order'].sudo().create({
                        'shopify_order_id': order.id,
                        'name': order.name,
                        'financial_status': order.financial_status,
                        'total_price': order.total_price,
                        'shop_id': self.shop_id.id,
                        'fetch_order_id': self.id,
                        'products': odoo_products,
                        'created_date': datetime.datetime.strptime(order.attributes['created_at'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")
                    })
                    count_fetch_order += 1
                else:
                    print("Đã trong database!")

        if count_fetch_order != 0:
            self.env['fetch.history'].sudo().create({
                'type': "order",
                'start_date': start_date,
                'end_date': end_date,
                'count': count_fetch_order,
                'shopify_name': self.shop_id.name,
            })

        if list_quantity:
            for quantity in list_quantity:
                x = self.env["quantity.order.line"].sudo().search([('product_id', "=", quantity['product_id']), ("order_id", '=', quantity["order_id"])])
                if x:
                    if x.quantity != quantity['quantity']:
                        x.write({
                            'quantity': quantity['quantity']
                        })
                    else:
                        print('quantity_order_line đã tồn tại!')
                else:
                    self.env["quantity.order.line"].sudo().create({
                        'quantity': quantity['quantity'],
                        'product_id': quantity['product_id'],
                        'order_id': quantity['order_id'],
                    })

    def fetch_product(self):
        api_key = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = self.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify_access_token = self.shop_id.token
        store_url = self.shop_id.url
        new_session = shopify.Session(store_url, api_version, token=shopify_access_token)
        shopify.ShopifyResource.activate_session(new_session)

        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")

        products = shopify.Product.find(published_at_min=start_date, published_at_max=end_date)

        exist_products = self.env['shopify.product'].sudo().search([])
        list_product_ids = []

        if exist_products:
            for product in exist_products:
                if str(product.shopify_product_id) not in list_product_ids:
                    list_product_ids.append(product.shopify_product_id)

        if products:
            count_fetch_product = 0
            for product in products:
                if str(product.id) not in list_product_ids:
                    self.env['shopify.product'].sudo().create({
                        'shopify_product_id': product.id,
                        'name': product.title,
                        'shop_id': self.shop_id.id,
                        'fetch_product_id': self.id,
                        'price': float(product.variants[0].price),
                    })
                    count_fetch_product += 1
                else:
                    print("Đã trong database!")

        if count_fetch_product != 0:
            self.env['fetch.history'].sudo().create({
                'type': "product",
                'start_date': start_date,
                'end_date': end_date,
                'count': count_fetch_product,
                'shopify_name': self.shop_id.name,
            })
