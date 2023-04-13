from odoo import fields, api, models


class WidgetData(models.Model):
    _name = 'widget.data'
    feed_title = fields.Char()
    on_post_click = fields.Char()
    spacing = fields.Char()
    layout = fields.Char()
    configuration = fields.Char()
    rows = fields.Char()
    columns = fields.Char()
    show_likes = fields.Char()
    show_followers = fields.Char()
    post_to_show = fields.Char()
    display_tag_post = fields.Char()
    instagram_user = fields.Many2one('instagram.user', ondelete='cascade')
