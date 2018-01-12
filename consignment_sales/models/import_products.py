from odoo import models, fields, api
#try:
#    import cStringIO as StringIO
#except ImportError:
#    import StringIO
#import csv
#import base64


class import_wizard_product_adj(models.Model):
    _name = 'import.wizard.product.adj'

    csv_file = fields.Binary("CSV File", required=True)
    log = fields.Char()

    @api.multi
    def process_csv_file(self):
        input = StringIO.StringIO(base64.decodestring(self.csv_file))

        reader = csv.reader(input, delimiter=',')
        product_obj = self.env['product.product']
        sil_obj = self.env['stock.inventory.line']
        stock_inv = self.env['stock.inventory'].browse(self._context.get('active_id'))
        line_vals = []
        log = ''
        
        if stock_inv.state not in  ['draft','confirm']:
            raise except_orm(_('Please Try in Draft State'),
                 _('Please try in draft state only'))
        if stock_inv.filter != 'partial':
            stock_inv.filter = 'partial'
        stock_inv.prepare_inventory()
        default_location_id = stock_inv.location_id.id
        ctx = dict(self._context)
        ctx.update({'default_location_id':default_location_id})
        line_no=0
        # for line in reader:
        #     line_no += 1
        #     if len(line) >= 4:
        #         product = product_obj.search(['|',('ean13','=',line[2]),('name','=',line[1])], limit=1)
        #         if not product:
        #             log += 'No product found for Barcode "%s" on Line %s \n'%(str(line[0]), str(line_no))
        #             continue
        #         try:
        #             qty = float(line[1])
        #         except:
        #             log += 'Improper Qty "%s" for Product "%s" on Line %s \n'%(str(line[1]), product.name,str(line_no))
        #             continue
        #         existing_line = sil_obj.search([('product_id','=',product.id),
        #                                         ('inventory_id', '=', stock_inv.id)], limit=1)
        #         # Check if that products line already exist, if exist, then just update the quantity,
        #         # else create new line
        #         if existing_line:
        #             existing_line.product_qty = qty
        #             updated_vals = existing_line.onchange_createline( location_id=existing_line.location_id and existing_line.location_id.id or False,
        #                                                               product_id=existing_line.product_id and existing_line.product_id.id or False, 
        #                                                               uom_id=existing_line.product_uom_id and existing_line.product_uom_id.id or False, 
        #                                                               package_id=existing_line.package_id and existing_line.package_id.id or False, 
        #                                                               prod_lot_id=existing_line.prod_lot_id and existing_line.prod_lot_id.id or False, 
        #                                                               partner_id=existing_line.partner_id and existing_line.partner_id.id or False, 
        #                                                               company_id=existing_line.company_id and existing_line.company_id.id or False, context=None)

        #             if updated_vals and updated_vals.get('value') and updated_vals['value'].get('theoretical_qty'):
        #                 existing_line._model._store_set_values(self._cr, self._uid, [x.id for x in existing_line], ['theoretical_qty'], self._context)
                        
        #         else:
        #             line_vals = sil_obj.with_context(ctx).onchange_createline(product_id=product.id, 
        #                                                                       location_id=stock_inv.location_id.id)
        #             line_vals.update({'inventory_id':stock_inv.id,'location_id':default_location_id,
        #                               'product_qty':qty, 'product_id': product.id})
        #             inv_line = sil_obj.create(line_vals)

        # if log:
        #     self.log = log
        # else:
        #     self.log = 'No errors found in importing the products'

        return {
                'name': _('File Processed Successfully'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'update.real.stock',
                'view_id': self.env.ref('physical_inventory.update_real_stock_form').id,
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new'
        }
