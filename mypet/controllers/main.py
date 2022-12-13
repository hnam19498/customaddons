import odoo
import json
from odoo import http
from odoo.http import request
class MyPetAPI(http.Controller):
    @odoo.http.route(['/pet/<id>'], type='http', auth='none')
    def foo_handler(self, id, **kw):
        try:
            rec = request.env['my.pet'].sudo().search([('id', '=', int(id))], limit=1)
            print(rec)
            response = {
                'status': 'ok',
                'content': {
                    'name': rec.name,
                    'age': rec.age,
                    'weight': rec.weight,
                    'gender': rec.gender,
                }
            }

        except Exception:
            response = {
                'status': 'error',
                'content': 'not found',
            }

        return json.dumps(response)
