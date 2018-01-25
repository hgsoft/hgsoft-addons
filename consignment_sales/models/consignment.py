
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class consignment_order(models.Model):
    _name = 'consignment.order'

    partner_id = fields.Many2one("res.partner", string="Customer", 
                                domain=[('customer','=',True),('allow_consignment','=',True)], required=True)
    order_date = fields.Datetime("Date", default=fields.Datetime.now, required=True)
    
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist", required=True)
    
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),
                              ('transferred','Transferred'),('cancelled','Cancelled')], string='State', default='draft')
    
    name = fields.Char("Name",default=lambda self: self.env['ir.sequence'].next_by_code('con.order'), required=True, readonly=True)
    
    client_order_ref = fields.Char("Client Ref.")
    
    order_line = fields.One2many('consignment.order.line','order_id','Order Lines')
    
    user_id = fields.Many2one('res.partner', string="Sale Person")
    
    warehouse_id = fields.Many2one('stock.warehouse','Source Warehouse', required=True)
    
    picking_id = fields.Many2one('stock.picking','Transfer Document')
    
    invoice_id = fields.Many2one('account.invoice','Consignment Invoice')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        """
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
        }
        self.update(values)

    @api.multi
    def button_confirm(self):
        picking = self.create_picking()
        
        self.picking_id = picking.id
        
        self.state = 'confirmed'
        
        try:
            invoice = self.create_invoice()
            self.invoice_id = invoice.id
            print ("invoice-------",invoice)
        except Exception as e:
            print ("##### Erro ao criar fatura: ",e)
        
    @api.multi
    def button_view_invoice(self):
        action = self.env.ref('account.action_invoice_tree')
        
        result = action.read()[0]

        #override the context to get rid of the default filtering
        result['context'] = {'type': 'out_invoice' }
        
        if self.invoice_id:
        #choose the view_mode accordingly
            result['domain'] = "[('id', '=', " + str(self.invoice_id.id) + ")]"
            # res = self.env.ref('account.invoice_supplier_form', False)
            # result['views'] = [(res and res.id or False, 'form')]
            # result['res_id'] = self.invoice_ids.id
        return result

    @api.multi
    def create_picking(self):
        moves = []
        pick_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        pick_type = self.env['stock.picking.type'].search([('code','=','internal'),
                                                            ('warehouse_id','=',self.warehouse_id.id)], limit=1)
        print ("pick_type-------",pick_type)
        source_loc_id = pick_type.default_location_src_id and pick_type.default_location_src_id.id or \
                            self.env['ir.model.data'].get_object_reference('stock', 'stock_location_stock')[1]
        dest_loc_id = self.partner_id.consignee_location_id.id
        picking = False
        for line in self.order_line:
            product = line.product_id.id
            move_val = {}
            move_default = move_obj.default_get(['invoice_state', 'priority', 'date_expected',
                                                               'partner_id', 'procure_method', 'picking_type_id',
                                                               'company_id', 'reserved_quant_ids', 'product_uom'])
            move_val.update(move_default)
            print ("\n\nmove_val----after-------default----",move_val,product)
            # prd_onchange_vals = move_obj.onchange_product_id(product)['value']
            prd_onchange_vals = {'product_uos': False, 'product_uos_qty': 1.0, 'product_uom_qty': 1.0, 'name': line.product_id.name, 'product_uom': line.product_id.uom_id.id}
            print ("prd_onchange_vals-----------",prd_onchange_vals)
            move_val.update(prd_onchange_vals)
            print ("\n\nmove_val----after-------onchange----",move_val)
            # source_loc_id = self.env['ir.model.data'].get_object_reference('stock', 'stock_location_customers')[1]
            # dest_loc_id = self.source_loc_id.id
            # lot_id = self.env['stock.production.lot'].create({'name':self.name,'product_id':product})
            move_val.update({
                            'partner_id': self.partner_id.id,
                            'product_id':product or False,
                            'product_uos_qty': line.quantity,
                            'product_uom_qty':line.quantity,
                            'name': self.env['product.product'].browse(product) and (self.env['product.product'].browse(product)).name or False,
                            'location_id': source_loc_id or False,
                            'location_dest_id': dest_loc_id or False,
                            'picking_type_id': pick_type.id,
                            # 'restrict_lot_id': lot_id.id or False,
                        })
            print ("move_val-----after manually update-------",move_val)
            
            move = move_obj.create(move_val)
            print ("move-------",move)
            if not picking:
                values = {
                            'origin': move.origin,
                            'company_id': move.company_id and move.company_id.id or False,
                            'move_type': move.group_id and move.group_id.move_type or 'direct',
                            'partner_id': move.partner_id.id or False,
                            'picking_type_id': move.picking_type_id and move.picking_type_id.id or False,
                        }
                print ("values------",values)
                picking = pick_obj.create(values)
            move.write({'picking_id': picking.id})

        return picking

    @api.multi
    def create_invoice(self):
        vals = {}
        product_vals = []
        account_invoice_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line']
        res_partner = account_invoice_obj.onchange_partner_id('out_invoice', self.partner_id.id)
        # product_package_id = self.env['ir.model.data'].get_object_reference('package_management',
        #                                                                'product_product_package')[1]
        # product_package_brw = self.env['product.product'].browse(product_package_id)
        
        for line in self.order_line:
            product_package = account_invoice_line_obj.product_id_change( line.product_id.id,
                                                        line.product_uom.id,
                                                        qty=line.quantity, name='',
                                                        type='out_invoice',
                                                        partner_id=self.partner_id.id)
            product_line_vals = {
                'account_analytic_id': False,
                'account_id': product_package['value'] and product_package['value']['account_id'] or False,
                'discount': 0,
                'invoice_line_tax_id': [[6, False, []]],
                'name': product_package['value'] and product_package['value']['name'] or False,
                'price_unit': line.price_unit or False,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uos_id': line.product_uom.id
            }
            product_vals.append((0,0,product_line_vals))
        vals.update({
            'partner_id': self.partner_id and self.partner_id.id,
            'fiscal_position': res_partner['value'] and res_partner['value']['fiscal_position'] or False,
            'journal_id': account_invoice_obj._default_journal() and (account_invoice_obj._default_journal()).id or False,
            'account_id': res_partner['value'] and res_partner['value']['account_id'] or False,
            'currency_id': account_invoice_obj._default_currency() and (account_invoice_obj._default_currency()).id or False,
            'company_id': self.env['res.company']._company_default_get('account.invoice'),
            'invoice_line': product_vals,
        })
        invoice_id = account_invoice_obj.create(vals)

        return invoice_id

    @api.multi
    def button_transfer(self):
        self.picking_id.move_lines.action_done()
        self.state = 'transferred'

    @api.multi
    def button_cancel(self):
        self.state = 'cancelled'

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
            'domain': "[('location_id','=',%s)]" % self.partner_id.consignee_location_id.id
        }

        return result


class consignment_order_line(models.Model):
    _name = 'consignment.order.line'

    order_id = fields.Many2one("consignment.order", string="Order", )
    product_id = fields.Many2one("product.product", string="Product",required=True)
    name = fields.Text('Description', required=True,)
    quantity = fields.Integer("Quantity")
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True, invisible=True)
    price_unit = fields.Float('Unit Price', store=True, digits= dp.get_precision('Product Price'), 
                                compute='_compute_subtotal', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', store=True, readonly=True, compute='_compute_subtotal',
                                    digits= dp.get_precision('Account'),)
    consignment_stock = fields.Float(string='Consignment Stock',
                                        compute='_compute_consignment_stock')

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
        line_data = []
        product_qty = 0
        for each_quant in consignment_quants:
            product_qty += each_quant.qty

        self.consignment_stock = product_qty



    @api.one
    @api.depends('quantity', 'product_id','order_id.pricelist_id')
    def _compute_subtotal(self):
        price_unit = 0
        subtotal = 0
        if self.product_id and self.quantity:
            price_unit = self.order_id.pricelist_id.price_get(self.product_id.id, self.quantity, self.order_id.partner_id.id)[self.order_id.pricelist_id.id]
        self.price_unit = price_unit or 0.0
        self.price_subtotal = self.quantity*self.price_unit


        


    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.category_id.id != self.product_uom.category_id.id):
            vals['product_uom'] = self.product_id.uom_id

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=self.quantity,
            date=self.order_id.order_date,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name
        vals['quantity'] = 1
        vals['price_unit'] = self.order_id.pricelist_id.price_get(self.product_id.id, vals['quantity'], self.order_id.partner_id.id)[self.order_id.pricelist_id.id]
        print ("vals---------",vals)
        self.update(vals)

        return {'domain': domain}


class consignment_sale(models.Model):
    _name = 'consignment.sale'

    partner_id = fields.Many2one("res.partner", string="Customer", domain=[('customer','=',True)])
    order_date = fields.Datetime("Date", default=fields.Datetime.now)
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),
                              ('transferred','Transferred'),('cancelled','Cancelled')], string='State', default='draft')
    name = fields.Char("Name",default=lambda self: self.env['ir.sequence'].next_by_code('con.sale'))
    client_order_ref = fields.Char("Client Ref.",readonly=True)
    order_line = fields.One2many('consignment.order.line','order_id','Order Lines')

    @api.multi
    def button_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def button_transfer(self):
        self.state = 'transferred'

    @api.multi
    def button_cancel(self):
        self.state = 'cancelled'

    @api.multi
    def button_restock(self):
        return True
        
    @api.multi
    def button_invoice_view(self):
        
        return True



class consignment_sale_line(models.Model):
    _name = 'consignment.sale.line'

    order_id = fields.Many2one("consignment.sale", string="Order")
    product_id = fields.Many2one("product.template", string="Product")
    description = fields.Char(string="Description")
    quantity = fields.Integer("Quantity")
    unit_price = fields.Float("Unit Price")
    price_subtotal = fields.Float("Subtotal")
 