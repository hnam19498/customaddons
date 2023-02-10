from odoo import api, models, fields, _
import requests, datetime, base64


class SyncInvoice(models.Model):
    _name = 'sync.invoice'

    start_date = fields.Date()
    financial_status = fields.Char()
    end_date = fields.Date()
    xero_invoice_ids = fields.One2many('xero.invoice', 'sync_invoice_id')
    store_id = fields.Many2one("xero.store")

    def sync_invoice(self):
        list_invoice_ids = []
        count_xero_invoice = 0
        exist_invoices = self.env['xero.invoice'].sudo().search([])
        if exist_invoices:
            for invoice in exist_invoices:
                if invoice.invoice_id not in list_invoice_ids:
                    list_invoice_ids.append(invoice.invoice_id)

        xero_store = self.store_id
        current_app = self.env.ref('shopify_odoo.xero_app_data').sudo()
        xero_token = self.env['xero.token'].sudo().search([('app_id', '=', current_app.id), ("store_id", "=", xero_store.id)])
        xero_token.update_token()

        invoice_headers = {
            'Authorization': "Bearer " + xero_token.access_token,
            'Xero-Tenant-Id': xero_store.tenantId,
            'Accept': "application/json",
        }

        xero_invoices = requests.get('https://api.xero.com/api.xro/2.0/Invoices?ContactIDs=61ef5b44-a7a2-4775-a81d-de61c95bf5e9', headers=invoice_headers).json()['Invoices']
        if xero_invoices:
            for invoice in xero_invoices:
                if invoice['InvoiceID'] not in list_invoice_ids:
                    self.env['xero.invoice'].sudo().create({
                        'invoice_id': invoice['InvoiceID'],
                        'type': invoice['Type'],
                        'invoice_number': invoice['InvoiceNumber'],
                        'reference': invoice['Reference'],
                        'amount_due': invoice['AmountDue'],
                        "financial_status": invoice["Status"].lower(),
                        "currency_code": invoice['CurrencyCode'],
                        'amount_paid': invoice['AmountPaid'],
                        'contact_id': invoice['Contact']['ContactID'],
                        'contact_name': invoice['Contact']['Name'],
                        'invoice_date': datetime.datetime.strptime(invoice['DateString'], "%Y-%m-%dT%H:%M:%S"),
                        'price_total': invoice['Total'],
                        "sync_invoice_id": self.id,
                        'store_id': xero_store.id,
                    })
                    count_xero_invoice += 1
                else:
                    print("Đã trong database!")

        if count_xero_invoice != 0:
            self.env['sync.history'].sudo().create({
                'type': "invoice",
                'start_date': self.start_date.strftime("%Y-%m-%d"),
                'end_date': self.end_date.strftime("%Y-%m-%d"),
                'count': count_xero_invoice,
                'store_name': xero_store.name,
            })

    def put_invoice(self):
        xero_store = self.store_id
        current_app = self.env.ref('shopify_odoo.xero_app_data').sudo()
        xero_token = self.env['xero.token'].sudo().search([('app_id', '=', current_app.id), ("store_id", "=", xero_store.id)])
        xero_token.update_token()
        count_put_invoice = 0
        count_paid_invoice = 0
        orders = self.env['shopify.order'].sudo().search([])
        for order in orders:
            if not order.xero_invoice_id:
                total_tax_xero = 0
                total_price_xero = 0
                lineitems = []
                lines = self.env['quantity.order.line'].sudo().search([('order_id', '=', order.id)])

                for line in lines:
                    lineitems.append({
                        "Description": "Test",
                        "Quantity": line.quantity,
                        "UnitAmount": self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)]).price,
                        "AccountCode": "200",
                        "TaxType": "OUTPUT",
                        "TaxAmount": self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)]).price * 0.1,
                        "LineAmount": line.quantity * self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)]).price
                    })
                    total_price_xero += self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)]).price * line.quantity
                    total_tax_xero += 0.1 * self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)]).price

                body_post_invoice = {
                    "Invoices": [
                        {
                            "Type": "ACCREC",
                            "Contact": {"ContactID": "61ef5b44-a7a2-4775-a81d-de61c95bf5e9"},
                            "LineItems": lineitems,
                            "Date": order.created_date,
                            "DueDate": order.created_date,
                            "Reference": order.name,
                            "Status": 'AUTHORISED'
                        }
                    ]
                }

                hearder_post_invoice = {
                    'Authorization': 'Bearer ' + xero_token.access_token,
                    'Xero-Tenant-Id': xero_store.tenantId,
                    'Content-Type': 'application/json',
                    "Accept": "application/json",
                }

                result_post_invoice = requests.post('https://api.xero.com/api.xro/2.0/Invoices', headers=hearder_post_invoice, json=body_post_invoice).json()
                count_put_invoice += 1

                selected_order = self.env['shopify.order'].sudo().search([('id', '=', order.id)],limit=1)
                selected_order.sudo().write({"xero_invoice_id": result_post_invoice['Invoices'][0]['InvoiceID']})

                if order.financial_status == 'paid':
                    hearder_post_payments = {
                        'Authorization': 'Bearer ' + xero_token.access_token,
                        'Xero-Tenant-Id': xero_store.tenantId,
                        'Content-Type': 'application/json',
                        "Accept": "application/json",
                    }
                    body_post_payments = {
                        "Payments": [
                            {
                                "Invoice": {
                                    "LineItems": [],
                                    "InvoiceID": result_post_invoice['Invoices'][0]['InvoiceID']
                                },
                                "Account": {"Code": "970"},
                                "Amount": total_tax_xero + total_price_xero
                            }
                        ]
                    }
                    requests.post('https://api.xero.com/api.xro/2.0/Payments', headers=hearder_post_payments, json=body_post_payments).json()
                    count_paid_invoice += 1

        if count_put_invoice != 0:
            if count_paid_invoice != 0:
                self.env['sync.history'].sudo().create({
                    'type': "Put invoice",
                    'start_date': self.start_date.strftime("%Y-%m-%d"),
                    'end_date': self.end_date.strftime("%Y-%m-%d"),
                    'count': count_put_invoice,
                    "count_paid": count_paid_invoice,
                    'store_name': xero_store.name,
                })
            else:
                self.env['sync.history'].sudo().create({
                    'type': "Put invoice",
                    'start_date': self.start_date.strftime("%Y-%m-%d"),
                    'end_date': self.end_date.strftime("%Y-%m-%d"),
                    'count': count_put_invoice,
                    "count_paid": 0,
                    'store_name': xero_store.name,
                })
