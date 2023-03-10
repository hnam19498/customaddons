import shopify, datetime
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class FetchShopify(models.Model):
    _name = 'fetch.shopify'

    start_date = fields.Date()
    end_date = fields.Date()
    shopify_order_ids = fields.One2many('shopify.order', "fetch_order_id")
    shop_id = fields.Many2one('shop.shopify')
    shopify_product_ids = fields.One2many('shopify.product', "fetch_product_id")

    def fetch_order(self):
        try:
            shopify_access_token = self.env['shop.app.shopify'].sudo().search([('shopify_id', "=", self.shop_id.id), ("app_id", "=", self.env.ref('shopify_odoo.shopify_app_data').sudo().id)]).access_token
            new_session = shopify.Session(self.shop_id.url, self.env.ref('shopify_odoo.shopify_app_data').sudo().api_version, token=shopify_access_token)
            shopify.ShopifyResource.activate_session(new_session)
            list_order_ids = []
            count_fetch_order = 0
            list_quantity = []

            exist_orders = self.env['shopify.order'].sudo().search([])
            if exist_orders:
                for order in exist_orders:
                    if order.shopify_order_id not in list_order_ids:
                        list_order_ids.append(order.shopify_order_id)

            start_date = self.start_date.strftime("%Y-%m-%d")
            end_date = self.end_date.strftime("%Y-%m-%d")
            orders = shopify.Order.find(published_at_min=start_date, published_at_max=end_date, status='any')

            if orders:
                for order in orders:
                    product_ids = []
                    for line in order.line_items:
                        product = self.env['shopify.product'].sudo().search([('shopify_product_id', '=', line.product_id)])
                        if product.id not in product_ids:
                            product_ids.append(product.id)
                    if str(order.id) not in list_order_ids:
                        if order.attributes["shipping_lines"]:
                            self.env['shopify.order'].sudo().create({
                                'shopify_order_id': order.id,
                                'ship_cost': float(order.attributes["shipping_lines"][0].attributes['price']),
                                'name': order.name,
                                'financial_status': order.financial_status,
                                'total_price': order.total_price,
                                'shop_id': self.shop_id.id,
                                'fetch_order_id': self.id,
                                'products': product_ids,
                                'created_date': datetime.datetime.strptime(order.attributes['created_at'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")
                            })
                        else:
                            self.env['shopify.order'].sudo().create({
                                'shopify_order_id': order.id,
                                'ship_cost': 0,
                                'name': order.name,
                                'financial_status': order.financial_status,
                                'total_price': order.total_price,
                                'shop_id': self.shop_id.id,
                                'fetch_order_id': self.id,
                                'products': product_ids,
                                'created_date': datetime.datetime.strptime(order.attributes['created_at'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d")
                            })
                        count_fetch_order += 1
                    else:
                        print(f'Order id {order.id} đã tồn tại trong database!')

                    for line in order.line_items:
                        product = self.env['shopify.product'].sudo().search([('shopify_product_id', '=', line.product_id)])
                        order_line = {
                            "product_id": product.id,
                            'order_id': self.env['shopify.order'].sudo().search([('shopify_order_id', '=', order.id)]).id,
                            "quantity": line.attributes['quantity']
                        }
                        if order_line not in list_quantity:
                            list_quantity.append(order_line)

            if count_fetch_order != 0:
                fetch_history = self.env['fetch.history'].sudo().search([("type", '=', 'order'), ("end_date", '=', self.end_date), ("start_date", '=', self.start_date), ('shop_id', "=", self.shop_id.id)])
                if fetch_history:
                    fetch_history.sudo().write({
                        "count": count_fetch_order + fetch_history.count
                    })
                else:
                    self.env['fetch.history'].sudo().create({
                        'type': "order",
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': count_fetch_order,
                        "shop_id": self.shop_id.id,
                        'shopify_name': self.shop_id.name
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
                        self.env["quantity.order.line"].sudo().create({
                            'quantity': quantity['quantity'],
                            'product_id': quantity['product_id'],
                            'order_id': quantity['order_id']
                        })
        except Exception as e:
            raise ValidationError(_(e))

    def fetch_product(self):
        try:
            shopify_access_token = self.env['shop.app.shopify'].sudo().search([('shopify_id', "=", self.shop_id.id), ("app_id", "=", self.env.ref('shopify_odoo.shopify_app_data').sudo().id)]).access_token
            new_session = shopify.Session(self.shop_id.url, self.env.ref('shopify_odoo.shopify_app_data').sudo().api_version, token=shopify_access_token)
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
                            'url_img': product.attributes['images'][0].attributes['src'],
                            'fetch_product_id': self.id,
                            'price': float(product.variants[0].price),
                            'variant_id': product.variants[0].id
                        })
                        count_fetch_product += 1
                    else:
                        print(f'Product id "{product.id}" đã trong database!')

            if count_fetch_product != 0:
                fetch_history = self.env['fetch.history'].sudo().search([("type", '=', 'product'), ("end_date", '=', self.end_date), ("start_date", '=', self.start_date), ('shop_id', "=", self.shop_id.id)])
                if fetch_history:
                    fetch_history.sudo().write({
                        "count": count_fetch_product + fetch_history.count
                    })
                else:
                    self.env['fetch.history'].sudo().create({
                        'type': "product",
                        'start_date': start_date,
                        'end_date': end_date,
                        'count': count_fetch_product,
                        'shopify_name': self.shop_id.name
                    })

        except Exception as e:
            raise ValidationError(_(e))
