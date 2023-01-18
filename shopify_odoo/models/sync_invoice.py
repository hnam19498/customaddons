from odoo import api, models, fields, _
import requests


class SyncInvoice(models.Model):
    _name = 'sync.invoice'

    start_date = fields.Date()
    end_date = fields.Date()
    xero_invoice_ids = fields.One2many('xero.invoice', 'sync_invoice_id')
    shop_id = fields.Many2one('shop.shopify')

    def sync_invoice(self):
        list_invoice_ids = []
        exist_invoices = self.env['xero.invoice'].sudo().search([])
        if exist_invoices:
            for invoice in exist_invoices:
                if invoice.invoice_id not in list_invoice_ids:
                    list_invoice_ids.append(invoice.invoice_id)

        xero_token = self.env['xero.token'].sudo().search([('shop_id', '=', self.shop_id.id)], limit=1)

        invoice_headers = {
            'Authorization': "Bearer " + xero_token.access_token,
            'Xero-Tenant-Id': self.env['xero.store'].sudo().search([('shop_shopify_id', '=', self.shop_id.id)],limit=1).tenantId,
            'Accept': "application/json",
        }

        xero_invoices = requests.get(
            'https://api.xero.com/api.xro/2.0/Invoices?ContactIDs=61ef5b44-a7a2-4775-a81d-de61c95bf5e9',
            headers=invoice_headers).json()['Invoices']
        if xero_invoices:
            for invoice in xero_invoices:
                if invoice['InvoiceID'] not in list_invoice_ids:
                    self.env['xero.invoice'].sudo().create({
                        'invoice_id': invoice['InvoiceID'],
                        'type': invoice['Type'],
                        'invoice_number': invoice['InvoiceNumber'],
                        'reference': invoice['Reference'],
                        'amount_due': invoice['AmountDue'],
                        'amount_paid': invoice['AmountPaid'],
                        'contact_id': invoice['Contact']['ContactID'],
                        'contact_name': invoice['Contact']['Name'],
                        'invoice_date': datetime.datetime.strptime(invoice['DateString'], "%Y-%m-%dT%H:%M:%S"),
                        'price_total': invoice['Total'],
                    })
                    count_xero_invoice += 1
                else:
                    print("Đã trong database!")

        if count_xero_invoice != 0:
            self.env['sync.history'].sudo().create({
                'type': "invoice",
                'start_date': start_date,
                'end_date': end_date,
                'count': count_xero_invoice,
                'shopify_name': self.shop_id.name,
            })
