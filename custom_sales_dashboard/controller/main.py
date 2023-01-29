import json

from odoo import http
from odoo.http import request


class SalesDashboard(http.Controller):
    @http.route(['/sales_dashboard'], type='json', auth="user", website=True)
    def sales_dashboard_values(self, **kw):
        record = request.env['crm.team'].search([])
        sales_rec = request.env['sale.report'].search(['|',
                                                       ('state', '=', 'sale'),
                                                       ('state', '=', 'done')],
                                                      order='user_id')

        flag1 = 0
        sales_person = []
        for thing in sales_rec:
            count = 0
            total_price = 0
            flag2 = thing.user_id.id
            if flag1 != thing.user_id.id:
                user_id = thing.user_id.id
                user_name = thing.user_id.name
                for tec in sales_rec:
                    if thing.user_id.id == tec.user_id.id:
                        total_price += tec.price_total
                        count += 1
                sales_person.append({
                    'id': user_id,
                    'name': user_name,
                    'total_amt': total_price,
                    'order_count': count
                })
                flag1 = flag2
        records = []
        for rec in record:
            records.append({
                'name': rec.name,
                'id': rec.id
            })
        query = """select count(*) as sale_count, max(res_partner.id) as id,
         res_partner.name from sale_order 
         join res_partner on partner_id = res_partner.id 
        group by res_partner.name order by sale_count desc limit 10"""
        request.env.cr.execute(query)
        customer_record = request.env.cr.dictfetchall()
        record_count = request.env['product.product'].search([])
        sample_list = []
        for i in record_count:
            sample_list.append({
                'name': i.name,
                'count': i.sales_count
            })
        count_list = sorted(sample_list, key=lambda d: d['count'])
        product_count = [count_list[0], count_list[-1]]
        lowest_selling = [count_list[0], count_list[1], count_list[2],
                          count_list[3], count_list[4], count_list[5],
                          count_list[6]]
        highest_selling = [count_list[-1], count_list[-2],
                           count_list[-3], count_list[-4], count_list[-5],
                           count_list[-6], count_list[-7]]
        draft_sales = request.env['sale.order'].search_count(
            [('state', '=', 'draft')])
        sent_sales = request.env['sale.order'].search_count(
            [('state', '=', 'sent')])
        sale_sales = request.env['sale.order'].search_count(
            [('state', '=', 'sale')])
        done_sales = request.env['sale.order'].search_count(
            [('state', '=', 'done')])
        cancel_sales = request.env['sale.order'].search_count(
            [('state', '=', 'cancel')])
        sale_states = [{
            'draft': draft_sales,
            'sent': sent_sales,
            'sale': sale_sales,
            'done': done_sales,
            'cancel': cancel_sales
        }]

        upselling_invoice = request.env['sale.order'].search_count(
            [('invoice_status', '=', 'upselling')])
        invoiced_invoice = request.env['sale.order'].search_count(
            [('invoice_status', '=', 'invoiced')])
        to_invoice_invoice = request.env['sale.order'].search_count(
            [('invoice_status', '=', 'to invoice')])
        no_invoice = request.env['sale.order'].search_count(
            [('invoice_status', '=', 'no')])
        invoice_states = [{
            'upselling': upselling_invoice,
            'invoiced': invoiced_invoice,
            'to_invoice': to_invoice_invoice,
            'no': no_invoice
        }]

        vals = {
            'record': records,
            'sales_person': sales_person,
            'customers': customer_record,
            'product_count': product_count,
            'lowest_selling': lowest_selling,
            'highest_selling': highest_selling,
            'sale_states': sale_states,
            'invoice_states': invoice_states
        }
        return vals
