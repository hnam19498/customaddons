import shopify, binascii, os, werkzeug, json, string, random, datetime, base64
from odoo import http, _
from odoo.http import request
from odoo.modules import get_resource_path


class ShopifyMain(http.Controller):
    @http.route("/instafeed/shopify_auth", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopify_auth(self, **kw):
        try:
            if "shop" in kw:
                shopify_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_client_id')
                shopify_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_client_secret')
                base_url = request.env['ir.config_parameter'].sudo().get_param('instafeed.base_url')
                api_version = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_api_version')

                shopify.Session.setup(api_key=shopify_client_id, secret=shopify_client_secret)
                state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
                redirect_uri = f"{base_url}/instafeed/shopify/callback"
                scopes = [
                    "read_products",
                    "read_orders",
                    'read_script_tags',
                    'write_script_tags',
                    "read_draft_orders",
                    'write_draft_orders'
                ]
                new_session = shopify.Session(kw['shop'], api_version)
                auth_url = new_session.create_permission_url(scopes, redirect_uri, state)
                return werkzeug.utils.redirect(auth_url)
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')

    @http.route("/instafeed/shopify/callback", auth="public", type="http", csrf=False, cors="*")
    def shopify_callback(self, **kw):
        try:
            if 'shop' in kw:
                shopify_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_client_id')
                shopify_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_client_secret')
                api_version = request.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_api_version')

                shopify.Session.setup(api_key=shopify_client_id, secret=shopify_client_secret)
                session = shopify.Session(kw["shop"], api_version)
                access_token = session.request_token(kw)
                shopify.ShopifyResource.activate_session(session)
                shopify_infor = shopify.GraphQL().execute('''
                {
                    shop{
                        id 
                        name 
                        email
                        currencyCode 
                        url 
                        billingAddress{
                            country
                        }
                    }
                }''')
                shopify_data = json.loads(shopify_infor)
                shopify_id = shopify_data["data"]["shop"]["id"].split("/")[-1]

                if access_token:
                    existing_webhooks = shopify.Webhook.find()
                    ngrok_url = request.env['ir.config_parameter'].sudo().get_param('instafeed.ngrok_url')
                    if not ngrok_url:
                        ngrok_url = 'https://bab6-116-97-240-10.ap.ngrok.io'
                    if not existing_webhooks:
                        print("*******************")

                        webhook_products_create = shopify.Webhook()
                        webhook_products_create.topic = "products/create"
                        webhook_products_create.address = ngrok_url + "/webhook/products_create/" + shopify_id
                        webhook_products_create.format = "json"
                        webhook_products_create.save()
                        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

                        webhook_products_update = shopify.Webhook()
                        webhook_products_update.topic = "products/update"
                        webhook_products_update.address = ngrok_url + "/webhook/products_update/" + shopify_id
                        webhook_products_update.format = "json"
                        webhook_products_update.save()
                        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")
                    else:
                        print('existing_webhooks:')
                        for webhook in existing_webhooks:
                            print(f"---{webhook.id}: {webhook.topic}")

                    existing_script_tags = shopify.ScriptTag.find()
                    base_url = request.env['ir.config_parameter'].sudo().get_param('instafeed.base_url')
                    new_script_tag_url = base_url + '/instafeed/static/js/shopify.js?v=' + str(datetime.datetime.now())
                    new_script_tag = ''
                    if existing_script_tags:
                        for script_tag in existing_script_tags:
                            if script_tag.src != new_script_tag_url:
                                shopify.ScriptTag.find(script_tag.id).destroy()
                                new_script_tag = shopify.ScriptTag.create({
                                    "event": "onload",
                                    "src": new_script_tag_url
                                })
                    else:
                        new_script_tag = shopify.ScriptTag.create({
                            "event": "onload",
                            "src": new_script_tag_url
                        })

                    current_company = request.env['res.company'].sudo().search([('name', '=', kw['shop'])], limit=1)
                    current_user = request.env['res.users'].sudo().search([('login', '=', kw['shop'])], limit=1)
                    password_generate = ''.join(random.choice(string.ascii_letters) for i in range(20))

                    if not current_company:
                        current_company = request.env['res.company'].sudo().create({
                            'logo': False,
                            'currency_id': 2,
                            'sequence': 10,
                            'name': kw['shop'],
                            'street': False,
                            'street2': False,
                            'city': False,
                            'state_id': False,
                            'zip': False,
                            'country_id': False,
                            'phone': False,
                            'email': False,
                            'website': False,
                            'vat': False,
                            'company_registry': False,
                            'parent_id': False
                        })

                    if not current_user:
                        img_path = get_resource_path('instafeed', 'static/images', 'HOF.jpg')
                        img_content = base64.b64encode(open(img_path, "rb").read())
                        current_user = request.env['res.users'].sudo().create({
                            'company_ids': [[6, False, [current_company.id]]],
                            'company_id': current_company.id,
                            'active': True,
                            'lang': 'en_US',
                            'tz': 'Europe/Brussels',
                            '__last_update': False,
                            'name': kw['shop'],
                            'email': shopify_data["data"]["shop"]["email"],
                            'login': kw['shop'],
                            'password': password_generate,
                            'action_id': False,
                            'image_1920': img_content
                        })

                    current_shopify = shopify.Shop.current()
                    current_shop = request.env["shop.shopify"].sudo().search([("shopify_id", "=", shopify_id)], limit=1)

                    if current_shop:
                        current_shop.status = True
                        if not current_shop.shopify_owner:
                            current_shop.shopify_owner = current_shopify.shop_owner
                            current_shop.sudo().write({
                                "access_token": access_token,
                                "name": shopify_data["data"]["shop"]["name"],
                                "email": shopify_data["data"]["shop"]["email"],
                                "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                                "url": shopify_data["data"]["shop"]["url"],
                                "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                            })
                    else:
                        current_shop = request.env["shop.shopify"].sudo().create({
                            "shopify_id": shopify_id,
                            'access_token': access_token,
                            "name": shopify_data["data"]["shop"]["name"],
                            "email": shopify_data["data"]["shop"]["email"],
                            'status': True,
                            "shopify_owner": current_shopify.shop_owner,
                            "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                            "url": shopify_data["data"]["shop"]["url"],
                            "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                        })

                    if not current_shop.admin:
                        current_shop.admin = current_user.id
                    if not current_shop.password:
                        current_shop.password = password_generate
                    if not existing_script_tags:
                        if not new_script_tag:
                            current_shop.is_update_script_tag = False
                        else:
                            current_shop.is_update_script_tag = True
                    else:
                        current_shop.is_update_script_tag = True

                    products = shopify.Product.find()
                    exist_products = request.env['shopify.product'].sudo().search([])
                    list_product_ids = []

                    if exist_products:
                        for product in exist_products:
                            if str(product.shopify_product_id) not in list_product_ids:
                                list_product_ids.append(product.shopify_product_id)

                    if products:
                        for product in products:
                            if str(product.id) not in list_product_ids:
                                try:
                                    request.env['shopify.product'].sudo().create({
                                        'shopify_product_id': product.id,
                                        'name': product.title,
                                        'url': "https://" + kw['shop'] + "/products/" + product.handle,
                                        'shop_id': current_shop.id,
                                        'url_img': product.image.src,
                                        'price': float(product.variants[0].price),
                                        "compare_at_price": product.variants[0].compare_at_price,
                                        'qty': product.variants[0].inventory_quantity,
                                        "variant_id": product.variants[0].id
                                    })
                                except Exception as error_create_product:
                                    print("error_create_product: " + str(error_create_product))
                                    continue
                            else:
                                print(f'Product id "{product.id}" đã trong database!')
                    db = http.request.env.cr.dbname
                    request.env.cr.commit()
                    request.session.authenticate(db, kw['shop'], current_shop.password)
                    return werkzeug.utils.redirect('/instafeed')
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')

    @http.route('/shopify/get_product', type='json', auth="user")
    def shopify_get_product(self, **kw):
        current_user = request.env.user
        current_shop = request.env['shop.shopify'].sudo().search([('admin', "=", current_user.id)])
        products = request.env['shopify.product'].sudo().search([('shop_id', '=', current_shop.id)])
        list_product = []
        for product in products:
            list_product.append({
                'shopify_product_id': product.shopify_product_id,
                "name": product.name,
                'price': product.price,
                'url': product.url,
                "id": product.id,
                "url_img": product.url_img,
                "variant_id": product.variant_id,
                'qty': product.qty,
                "compare_at_price": product.compare_at_price
            })
        return {'list_product': list_product}
