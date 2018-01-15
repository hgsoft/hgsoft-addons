# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def onchange_order_type(self, order_type, partner_id):
        result = {}
        if order_type and order_type != 'sale':
            result['domain'] = {'partner_id':[('allow_consignment','=',True),('customer','=',True)]}
            if partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if not partner.allow_consignment:
                    result['value'] = {'partner_id':False}
        elif order_type and order_type == 'sale':
            result['domain'] = {'partner_id':[('customer','=',True)]}
        return result
        # domain = {'partner_id':[('allow_consignment','=',True)]}
        # return {'domain':domain,'value':{'partner_id':False}}

    order_type = fields.Selection([('sale','Regular Sale'),('con_order','Consignment Order'),
                                   ('con_sale','Consignment Sales')], string = "Sale Order Type",
                                   default='sale', required=True)


    @api.multi
    def action_view_sale_consignment_products(self):
        # invoice_ids = self.mapped('invoice_ids')
        imd = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        action_id = imd.xmlid_to_res_id('consignment_sales.consignee_open_quants')
        action = act_obj.browse(action_id)
        list_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_tree')
        form_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            # 'target': action.target,

            'context': {'search_default_locationgroup': 1, 'search_default_internal_loc': 1, 
                        'search_default_productgroup': 1},
            # 'domain': {''}
            'res_model': action.res_model,
            'domain': "[('location_id','=',%s)]" % self.partner_id.consignee_location_id.id,
            'target':'new'
        }

        return result

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    @api.depends('product_id')
    def _compute_consignment_stock(self):
        if not self.product_id:
            return
        consignent_location = self.order_id.partner_id.consignee_location_id
        if not consignent_location:
            return False
        # Fetch the stock at this customer's consignee location
        consignment_quants = self.env['stock.quant'].search([('location_id','=',consignent_location.id),
                                                              ('product_id','=', self.product_id.id)
                                                            ])
        # order_type = self.Char(related='order_id.order_type', store=True, readonly=True, copy=False)

        line_data = []
        product_qty = 0
        for each_quant in consignment_quants:
            product_qty += each_quant.qty

        self.consignment_stock = product_qty
        
    consignment_stock = fields.Float(string='Consignment Stock',
        compute='_compute_consignment_stock', store=True)