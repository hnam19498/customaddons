import requests, datetime
from odoo import api, models, fields


class SyncInvoice(models.Model):
    _name = 'sync.invoice'

    start_date = fields.Date()
    account_code_id = fields.Many2one('xero.account.code')
    end_date = fields.Date()
    xero_invoice_ids = fields.One2many('xero.invoice', 'sync_invoice_id')
    store_id = fields.Many2one("xero.store")

    def sync_invoice(self):
        try:
            list_invoice_ids = []
            count_xero_invoice = 0
            exist_invoices = self.env['xero.invoice'].sudo().search([])
            if exist_invoices:
                for invoice in exist_invoices:
                    if invoice.invoice_id not in list_invoice_ids:
                        list_invoice_ids.append(invoice.invoice_id)

            xero_token = self.env['xero.token'].sudo().search([('app_id', '=', self.env.ref('shopify_odoo.xero_app_data').sudo().id), ("store_id", "=", self.store_id.id)])
            xero_token.update_token()

            headers_get = {
                'Authorization': f"Bearer {xero_token.access_token}",
                'Xero-Tenant-Id': self.store_id.tenantId,
                'Accept': "application/json"
            }

            result_get_contact = requests.get(url='https://api.xero.com/api.xro/2.0/contacts', headers=headers_get).json()
            params = {'where': f'Date >= Datetime({(self.start_date.strftime("%Y,%m,%d"))}) && Date <= Datetime({self.end_date.strftime("%Y,%m,%d")})'}
            request_return = requests.get(url=f"https://api.xero.com/api.xro/2.0/invoices?contactids={result_get_contact['Contacts'][0]['ContactID']}", headers=headers_get, params=params).json()
            xero_invoices = request_return['Invoices']
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
                            'store_id': self.store_id.id
                        })
                        count_xero_invoice += 1
                    else:
                        print(f'Invoice id "{invoice["InvoiceID"]}" đã trong database!')

            sync_history = self.env['sync.history'].sudo().search([("end_date", '=', self.end_date), ("start_date", '=', self.start_date), ('store_id', "=", self.store_id.id)])
            if count_xero_invoice != 0:
                if sync_history:
                    sync_history.sudo().write({
                        "count": count_xero_invoice + sync_history.count
                    })
                else:
                    self.env['sync.history'].sudo().create({
                        'start_date': self.start_date.strftime("%Y-%m-%d"),
                        'end_date': self.end_date.strftime("%Y-%m-%d"),
                        'count': count_xero_invoice,
                        'store_id': self.store_id.id,
                        'store_name': self.store_id.name
                    })
        except Exception as e:
            print(e)
            return {
                'type': "ir.actions.act_url",
                'url': 'https://odoo.website/404'
            }

    def put_invoice(self):
        try:
            xero_token = self.env['xero.token'].sudo().search([('app_id', '=', self.env.ref('shopify_odoo.xero_app_data').sudo().id), ("store_id", "=", self.store_id.id)])
            xero_token.update_token()
            count_payments = 0
            count_invoices = 0
            invoices = []

            orders = self.env['shopify.order'].sudo().search([])

            header_post = {
                'Authorization': f'Bearer {xero_token.access_token}',
                'Xero-Tenant-Id': self.store_id.tenantId,
                'Content-Type': 'application/json',
                "Accept": "application/json"
            }

            header_get = {
                'Authorization': 'Bearer ' + xero_token.access_token,
                'Xero-Tenant-Id': self.store_id.tenantId,
                "Accept": "application/json",
            }
            result_get_contact = requests.get(url='https://api.xero.com/api.xro/2.0/contacts', headers=header_get).json()

            for order in orders:
                if order.financial_status == 'paid':
                    count_payments += 1
                if order.status_xero == False:
                    if self.end_date >= order.create_date.date() >= self.start_date:
                        line_items = []
                        lines = self.env['quantity.order.line'].sudo().search([('order_id', '=', order.id)])

                        for line in lines:
                            product = self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)], limit=1)
                            line_items.append({
                                "Description": product.name,
                                "Quantity": line.quantity,
                                "UnitAmount": product.price,
                                "AccountCode": self.account_code_id.account_code,
                                "TaxType": "OUTPUT",
                                "TaxAmount": product.price * 0.1,
                                "LineAmount": line.quantity * product.price
                            })

                        invoices.append({
                            "Type": "ACCREC",
                            "Contact": {"ContactID": result_get_contact['Contacts'][0]['ContactID']},
                            "LineItems": line_items,
                            "Date": str(order.create_date.date()),
                            "DueDate": str(order.create_date.date()),
                            "Reference": order.id,
                            "Status": 'AUTHORISED'
                        })
                        count_invoices += 1

            if count_invoices > 0:
                body_post_invoice = {
                    "Invoices": invoices
                }
                result_post_invoices = requests.post(url='https://api.xero.com/api.xro/2.0/invoices', headers=header_post, json=body_post_invoice).json()
                print(f'Invoices: {result_post_invoices}')

            if count_payments > 0:
                payments = []
                for order in orders:
                    total_tax_xero = 0
                    total_price_xero = 0
                    for invoice in result_post_invoices['Invoices']:
                        if int(invoice['Reference']) == order.id:
                            order.status_xero = True
                            lines = self.env['quantity.order.line'].sudo().search([('order_id', '=', order.id)])
                            for line in lines:
                                product = self.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)], limit=1)
                                total_price_xero += product.price * line.quantity
                                total_tax_xero += 0.1 * product.price

                            payments.append({
                                "Invoice": {
                                    "LineItems": [],
                                    "InvoiceID": invoice['InvoiceID']
                                },
                                "Account": {"Code": '970'},
                                "Amount": total_tax_xero + total_price_xero
                            })
                        count_payments += 1

                body_post_payments = {
                    "Payments": payments
                }

            if count_payments > 0:
                result_post_payments = requests.post(url='https://api.xero.com/api.xro/2.0/payments', headers=header_post, json=body_post_payments).json()
                print(f'Payments: {result_post_payments}')

            if count_invoices != 0:
                put_history = self.env['put.history'].sudo().search([("end_date", '=', self.end_date), ("start_date", '=', self.start_date), ('store_id', "=", self.store_id.id)])
                if count_payments != 0:
                    if put_history:
                        put_history.sudo().write({
                            "count": put_history.count + count_invoices,
                            'count_paid': put_history.count_paid + count_payments
                        })
                    else:
                        self.env['put.history'].sudo().create({
                            'start_date': self.start_date.strftime("%Y-%m-%d"),
                            'end_date': self.end_date.strftime("%Y-%m-%d"),
                            'count': count_invoices,
                            "count_paid": count_payments,
                            'store_name': self.store_id.name,
                            'store_id': self.store_id.id
                        })
                else:
                    if put_history:
                        put_history.sudo().write({
                            'count': put_history.count + count_invoices
                        })
                    else:
                        self.env['put.history'].sudo().create({
                            'start_date': self.start_date.strftime("%Y-%m-%d"),
                            'end_date': self.end_date.strftime("%Y-%m-%d"),
                            'count': count_invoices,
                            "count_paid": 0,
                            'store_id': self.store_id.id,
                            'store_name': self.store_id.name
                        })
        except Exception as e:
            print(e)
            return {
                'type': "ir.actions.act_url",
                'url': 'https://odoo.website/404'
            }

    def get_xero_account_code(self):
        try:
            xero_token = self.env['xero.token'].sudo().search([('app_id', '=', self.env.ref('shopify_odoo.xero_app_data').sudo().id), ("store_id", "=", self.store_id.id)])
            xero_token.update_token()
            list_exist_account_codes = []

            headers_get = {
                'Authorization': f"Bearer {xero_token.access_token}",
                'Xero-Tenant-Id': self.store_id.tenantId,
                'Accept': "application/json"
            }

            result_get_xero_account_code = requests.get(url='https://api.xero.com/api.xro/2.0/accounts', headers=headers_get).json()
            exist_account_codes = self.env['xero.account.code'].sudo().search([])
            if exist_account_codes:
                for account_code in exist_account_codes:
                    list_exist_account_codes.append(account_code.account_code)

            for line in result_get_xero_account_code['Accounts']:
                if ('SystemAccount' not in line or not line['SystemAccount']) and line['Code'] not in list_exist_account_codes:
                    self.env['xero.account.code'].sudo().create({
                        'account_code': line['Code'],
                        "name": line['Name']
                    })

        except Exception as err:
            print(err)
