from odoo import http, _
from odoo.http import request
import shopify, binascii, os, werkzeug, json


class WebhookController(http.Controller):

    @http.route("/webhook/<string:topic>", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def webhook_order_create(self, topic, **kw):
        print(topic)
        return {}
