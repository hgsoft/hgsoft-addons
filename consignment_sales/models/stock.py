from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class stock_location(models.Model):
    _inherit = 'stock.location'

    consignee_id = fields.Many2one('res.partner','Consignee', readonly=True)
    is_consignment = fields.Boolean('Consignment Location', readonly=True)


    @api.one
    @api.constrains('consignee_id')
    def _check_internal_location(self):
        if self.consignee_id and self.usage != 'internal':
            raise Warning(_('A consignee Location must be always internal'))


class procurement_order(models.Model):
    _inherit = 'procurement.order'

    def _run_move_create(self, cr, uid, procurement, context=None):
    	print "OVERRIDDEN METHOD------------------------------"
        ''' Returns a dictionary of values that will be used to create a stock move from a procurement.
        This function assumes that the given procurement has a rule (action == 'move') set on it.

        :param procurement: browse record
        :rtype: dictionary
        '''
        print "_run_move_create-----------procurement-----",procurement
        newdate = (datetime.strptime(procurement.date_planned, '%Y-%m-%d %H:%M:%S') - relativedelta(days=procurement.rule_id.delay or 0)).strftime('%Y-%m-%d %H:%M:%S')
        group_id = False
        if procurement.rule_id.group_propagation_option == 'propagate':
            group_id = procurement.group_id and procurement.group_id.id or False
        elif procurement.rule_id.group_propagation_option == 'fixed':
            group_id = procurement.rule_id.group_id and procurement.rule_id.group_id.id or False
        #it is possible that we've already got some move done, so check for the done qty and create
        #a new move with the correct qty
        already_done_qty = 0
        already_done_qty_uos = 0
        for move in procurement.move_ids:
            already_done_qty += move.product_uom_qty if move.state == 'done' else 0
            already_done_qty_uos += move.product_uos_qty if move.state == 'done' else 0
        qty_left = max(procurement.product_qty - already_done_qty, 0)
        qty_uos_left = max(procurement.product_uos_qty - already_done_qty_uos, 0)
        # INHERITED PART START
        src_loc_id = procurement.rule_id.location_src_id.id
        dest_loc_id = procurement.location_id.id
        if procurement.sale_line_id.order_id.order_type == 'con_order':
        	# change the dest loc to consignee loc, as we are moving stock to consignee loc
        	dest_loc_id = procurement.sale_line_id.order_id.partner_id.consignee_location_id.id
        elif procurement.sale_line_id.order_id.order_type == 'con_sale':
    		# change the source loc to consignee loc, as this is the stock to be moved to customer from consignment loc
    		src_loc_id = procurement.sale_line_id.order_id.partner_id.consignee_location_id.id
        # INHERITED PART END
        vals = {
            'name': procurement.name,
            'company_id': procurement.rule_id.company_id.id or procurement.rule_id.location_src_id.company_id.id or procurement.rule_id.location_id.company_id.id or procurement.company_id.id,
            'product_id': procurement.product_id.id,
            'product_uom': procurement.product_uom.id,
            'product_uom_qty': qty_left,
            'product_uos_qty': (procurement.product_uos and qty_uos_left) or qty_left,
            'product_uos': (procurement.product_uos and procurement.product_uos.id) or procurement.product_uom.id,
            'partner_id': procurement.rule_id.partner_address_id.id or (procurement.group_id and procurement.group_id.partner_id.id) or False,
            'location_id': src_loc_id,
            'location_dest_id': dest_loc_id,
            'move_dest_id': procurement.move_dest_id and procurement.move_dest_id.id or False,
            'procurement_id': procurement.id,
            'rule_id': procurement.rule_id.id,
            'procure_method': procurement.rule_id.procure_method,
            'origin': procurement.origin,
            'picking_type_id': procurement.rule_id.picking_type_id.id,
            'group_id': group_id,
            'route_ids': [(4, x.id) for x in procurement.route_ids],
            'warehouse_id': procurement.rule_id.propagate_warehouse_id.id or procurement.rule_id.warehouse_id.id,
            'date': newdate,
            'date_expected': newdate,
            'propagate': procurement.rule_id.propagate,
            'priority': procurement.priority,
        }
        return vals