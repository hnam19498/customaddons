from odoo import api, fields, models
from datetime import datetime


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'ref'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender', string='Gender')
    appointment_time = fields.Datetime(string='Appointment time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very high')], string='Priority')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In consultation'), ('done', 'Done'), ('cancel', 'Cancel')],
        default='draft', required=True, string='Status')
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy line')
    hide_sales_price = fields.Boolean(string='Hide sales price')

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        today = datetime.today()
        int_today = int(today.strftime('%y%m%d'))
        a = int(self.appointment_time.strftime('%y%m%d'))
        b = int(self.booking_date.strftime('%y%m%d'))
        if a<=int_today<=b:
            print('Còn bảo hành!')
        else:
            print('Hết bảo hành!')
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "ahihi",
                'type': "rainbow_man",
            }
        }

    def action_in_consultation(self):
        for h in self:
            h.state = 'in_consultation'

    def action_done(self):
        for h in self:
            h.state = 'done'

    def action_draft(self):
        for h in self:
            h.state = 'draft'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', reqrired=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
