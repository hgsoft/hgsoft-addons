# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection([('sale','Regular Sale'),('con_order','Consignment Order'),
    ('con_sale','Consignment Sales')], string = "Sale Order Type", default='sale', required=True)
    
    @api.onchange('order_type', 'partner_id')
    def onchange_order_type_partner(self):
        print("##### onchange_order_type_partner [START] #####")
        
        result = {}
        
        count = 0
        
        for each_line in self.order_line:
            count += 1
        
        if count > 0:
            result['warning'] = {'title': "Aviso!",'message': "Alterações no Cliente ou Order Type após inserir um produto, pode causar inconsistência nos dados."}
        
        print("##### onchange_order_type_partner [END] #####")
        return result
    
    @api.onchange('order_type')
    def onchange_order_type(self):
        print("##### onchange_order_type [START] #####")
        
        result = {}
        
        if self.order_type and self.order_type != 'sale':
            result['domain'] = {'partner_id':[('allow_consignment','=',True),('customer','=',True)]}
            
            if self.partner_id:
                partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
                
                if not partner['allow_consignment']:
                    result['value'] = {'partner_id':False}
                    
                    result['warning'] = {'title': "Aviso!",'message': "Não é permitido realizar operações de consignação para este Partner."}
                    
        elif self.order_type and self.order_type == 'sale':
            result['domain'] = {'partner_id':[('customer','=',True)]}
        
        print("##### onchange_order_type [END] #####")
        return result
    
    @api.multi
    def action_view_sale_consignment_products(self):
        imd = self.env['ir.model.data']
        
        list_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_tree')
        
        form_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_form')
        
        action = self.env.ref('consignment_sales.consignee_open_quants').read()[0]
        
        action['views'] = [[list_view_id, 'tree'], [form_view_id, 'form']]
        
        action['context'] = {'search_default_internal_loc': 1, 'search_default_productgroup': 1}
        
        action['domain'] = "[('location_id','=',%s)]" % self.partner_id.consignee_location_id.id
        
        action['target'] = "new"
        
        return action
    
class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    consignment_stock = fields.Float(string='Consignment Stock', compute='_compute_consignment_stock', store=True)
    
    @api.one
    @api.depends('product_id')
    def _compute_consignment_stock(self):
        print ("##### _compute_consignment_stock [START] #####")
        
        if not self.product_id:
            return
        
        consignent_location = self.order_id.partner_id.consignee_location_id
        
        if not consignent_location:
            return False
        
        consignment_quants = self.env['stock.quant'].search([('location_id','=',consignent_location.id),
            ('product_id','=', self.product_id.id)])
        
        line_data = []
        
        product_qty = 0
        
        for each_quant in consignment_quants:
            product_qty += each_quant.quantity

        consignment_stock = product_qty
        
    print ("##### _compute_consignment_stock [END] #####")

    @api.onchange('product_id')
    def onchange_product(self):
        print ("##### onchange_product [START] #####")
        
        if self.product_id:
            consignment_quants = self.env['stock.quant'].search([('location_id','=',self.order_id.partner_id.consignee_location_id.id),
                ('product_id','=', self.product_id.id)])
            
            product_qty = 0
            
            for each_quant in consignment_quants:
                product_qty += each_quant.quantity

            consignment_stock = product_qty
            
            self.consignment_stock = consignment_stock
            
            print ("##### onchange_product [END] #####")
    
    @api.onchange('product_uom_qty', 'product_id')
    def _onchange_consignment_stock(self):
        print ("##### _onchange_consignment_stock [START] #####")
        
        print("##### SALE ORDER LINE OR SALE ORDER CHANGED #####")
        
        if self.product_id and self.order_id.order_type == 'con_sale':
            
            consignment_quants = self.env['stock.quant'].search([('location_id','=',self.order_id.partner_id.consignee_location_id.id),
                ('product_id','=', self.product_id.id)])
            
            product_qty = 0
            
            for each_quant in consignment_quants:
                product_qty += each_quant.quantity

            consignment_stock = product_qty
                
            print ("##### _onchange_consignment_stock [END] #####")
            
            if self.product_uom_qty > consignment_stock:
                return {
                    'warning': {
                        'title': "Negativação - Consignment Sale",
                        'message': "Esta Consignment Sale irá negativar o estoque atual de consignação para este produto.",
                    },
                }
        