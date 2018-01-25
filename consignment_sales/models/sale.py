# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

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
                    
                    result['warning'] = {'title': "Opção inválida.",'message': "Não é permitido realizar operações de consignação para este Partner."}
                    
        elif self.order_type and self.order_type == 'sale':
            result['domain'] = {'partner_id':[('customer','=',True)]}
            
        return result
        
    order_type = fields.Selection([('sale','Regular Sale'),('con_order','Consignment Order'),
                                   ('con_sale','Consignment Sales')], string = "Sale Order Type",
                                   default='sale', required=True)
    
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
    
    #
    @api.one
    @api.depends('product_id')
    def _compute_consignment_stock(self):
        print ("##### _compute_consignment_stock [START] #####")
        
        if not self.product_id:
            print ("##### _compute_consignment_stock [A] #####")
            return
        
        consignent_location = self.order_id.partner_id.consignee_location_id
        print ("##### consignent_location [", consignent_location,"] #####")
        
        if not consignent_location:
            print ("##### _compute_consignment_stock [B] #####")
            print ("##### consignent_location [", consignent_location,"] #####")
            return False
        
        consignment_quants = self.env['stock.quant'].search([('location_id','=',consignent_location.id),
                                                              ('product_id','=', self.product_id.id)
                                                            ])
        print ("##### _compute_consignment_stock [", consignment_quants,"] #####")
        
        line_data = []
        print ("##### _compute_consignment_stock [", line_data,"] #####")
        
        product_qty = 0
        
        for each_quant in consignment_quants:
            print ("##### _compute_consignment_stock [B] #####")
            print ("##### _compute_consignment_stock [", each_quant,"] #####")
            product_qty += each_quant.quantity

        print ("##### _compute_consignment_stock [", product_qty,"] #####")
        consignment_stock = product_qty
        print ("##### _compute_consignment_stock [", consignment_stock,"] #####")
        
    print ("##### _compute_consignment_stock [END] #####")
    #
    
    #####===TESTE===#####
    #
    @api.onchange('product_id')
    def onchange_product(self):
        print ("##### onchange_product [START] #####")
        
        title = self.product_id
        
        message = self.order_id.partner_id
        
        return {
            'warning': {
                'title': title,
                'message': message,
            },
        }
        
    #
    #####===TESTE===#####
    
    @api.onchange('price_unit')
    def _onchange_consignment_stock(self):
        print ("##### _onchange_consignment_stock [START] #####")
        
        if self.product_id and self.order_id.order_type == 'con_sale':
            stock = self.env.cr.execute("""SELECT consignment_stock stock, product_id product_id
            FROM public.sale_order_line where product_id = {} and consignment_stock > 0;
            """.format(self.product_id.id))
             
            consignment_stock = 0.0
             
            for x in self._cr.dictfetchall():
                consignment_stock = x["stock"]
                
            print ("##### _onchange_consignment_stock [END] #####")
            if self.product_uom_qty > consignment_stock:
                return {
                    'warning': {
                        'title': "Negativação - Consignment Sale",
                        'message': "Esta Consignment Sale irá negativar o estoque atual de consignação para este produto.",
                    },
                }
        