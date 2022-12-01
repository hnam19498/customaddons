# import customaddons.mypet.controllers.main
# import odoo, json, logging
#
# _logger = logging.getLogger(__name__)
#
#
# class MyPetAPIInherit(customaddons.mypet.controllers.main.MyPetAPI):
#     @odoo.http.route()
#     def foo_handler(self):
#         return "New 'foo' API!"
#
#     @odoo.http.route('/bar2')
#     def bar_handler(self):
#         return json.dumps({
#             'content': "New 'bar' API!"
#         })
#
#     @odoo.http.route()
#     def pet_handler(self, dbname, id, **kw):
#         _logger.warning('Pet handler called~~!')
#         result = super(MyPetAPIInherit, self).pet_handler(dbname, id)
#         _logger.warning("Processing~!")
#         return result
