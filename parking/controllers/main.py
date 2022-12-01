import json, werkzeug
from odoo import http
from odoo.http import request


class MountainController(http.Controller):

    # truyền biến vào controller
    @http.route('/mountain/<int:id>', auth='public', type='http')
    def mountain_check(self, id):
        return f'Mountain check, id là: {id}'

    # redirect
    @http.route('/mountain/redirect', auth='public')
    def mountain_redirect(self):
        return werkzeug.utils.redirect('https://www.google.com/')

    # render ra 1 template
    @http.route('/mountain', auth='public')
    def mountain_login(self):
        return request.render("web.login")

    # return 1 json
    @http.route('/mountain/json', auth='public', type='http')
    def mountain_json(self):
        return json.dumps({
            'check': 'json check 123',
        })

    # database
    @http.route("/mountain/database", auth='public', type='http')
    def mountain_database(self):
        lit = []
        car_search_names = request.env['parking.car'].sudo().search([])
        for car in car_search_names:
            if car['name'] == "Car 2":
                lit.append(car)
        print(lit)
        return f'car: {lit[0].name}'
