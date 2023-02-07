from odoo import api, models, fields
import datetime


class BundleAnalytic(models.Model):
    _name = 'bundle.analytic'

    end_time = fields.Datetime()
    start_time = fields.Datetime()
    bundle_id = fields.Many2one('shopify.bundle')
    count_bundle_database_ids = fields.One2many("count.bundle.database", "bundle_analytic_id")
    check_analytic = fields.Boolean(default=False)
    html_iframe = fields.Html(compute='gen_html_iframe', sanitize=False)

    @api.constrains("bundle_id", 'end_time', 'start_time')
    def gen_html_iframe(self):
        if self.check_analytic:
            self.html_iframe = f'<iframe src="/iframe/shopify_iframe?bundle_id={self.bundle_id.id}" width="1000px" height="500px"></iframe>'
        else:
            self.html_iframe = f'<iframe src="/iframe/shopify_iframe"></iframe>'

    def bundle_analytic(self):
        try:
            if self.end_time and self.start_time and self.bundle_id:
                list_count = []
                end_time = self.end_time
                start_time = self.start_time
                bundle = self.bundle_id
                count_bundles = self.env['count.bundle.order'].sudo().search([('bundle_id', '=', bundle.id)])

                for count_bundle in count_bundles:
                    count = 0
                    price_reduce = 0

                    if start_time <= count_bundle.create_date <= end_time:
                        count += count_bundle.time
                        price_reduce += count_bundle.price_reduce

                    b = {
                        "count": count,
                        "price_reduce": price_reduce,
                        "date": count_bundle.date,
                        'bundle_id': self.bundle_id.id
                    }

                    if b not in list_count:
                        list_count.append(b)

                    count_hhh = 0
                    sodem = 0

                list_date = []
                for i in range(len(list_count)):
                    date_temp = list_count[i]['date']
                    if date_temp not in list_date:
                        list_date.append(date_temp)

                min_date = min(list_date)
                max_date = max(list_date)

                for single_date in (min_date + datetime.timedelta(n) for n in range((max_date - min_date).days + 1)):
                    count_hhh = 0
                    sodem = 0
                    price_reduce = 0
                    for i in range(len(list_count)):
                        sodem += 1
                        if list_count[i]['date'] == single_date:
                            if sodem <= len(list_count):
                                price_reduce += list_count[i]['price_reduce']
                                count_hhh += list_count[i]['count']

                    if count_hhh > 0:
                        exist_analytic = self.env['count.bundle.database'].sudo().search(
                            [('bundle_id', '=', bundle.id), ("date", "=", single_date)], limit=1)
                        if not exist_analytic:
                            self.env['count.bundle.database'].sudo().create({
                                'bundle_id': bundle.id,
                                'time': count_hhh,
                                "bundle_analytic_id": self.id,
                                "price_reduce": price_reduce,
                                "date": single_date,
                            })
                        else:
                            if exist_analytic.time != count_hhh:
                                exist_analytic.sudo().write({
                                    "time": count_hhh,
                                    'price_reduce': price_reduce,
                                    "bundle_analytic_id": self.id
                                })

                            if exist_analytic.bundle_analytic_id != self.id:
                                exist_analytic.sudo().write({
                                    "bundle_analytic_id": self.id
                                })

                        self.check_analytic = True

        except Exception as e:
            print(e)
