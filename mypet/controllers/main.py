import odoo, logging, json

_logger = logging.getLogger(__name__)


class MyPetAPI(odoo.http.Controller):
    @odoo.http.route(['/pet/<dbname>/<id>'], type='http', auth='none', sitemap=False, cors='*', csrf=False)
    def foo_handler(self, dbname, id, **kw):
        model_name = 'my.pet'

        try:
            registry = odoo.modules.registry.Registry(dbname)
            with odoo.api.Environment.manage(), registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
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
