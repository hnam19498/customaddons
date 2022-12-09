from odoo import http
from odoo.http import request


class Main(http.Controller):
    @http.route('/my_library/books', type='http', auth="none")
    def books(self):
        books = request.env()
