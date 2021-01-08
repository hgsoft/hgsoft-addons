# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomMaintenance(models.Model):
    _inherit = "maintenance.equipment"
    
    product_id = fields.Many2one('product.product', string='Product', domain="[('product_tmpl_id.type', '=', 'equipment')]", tracking=True)
    
    image_1920 = fields.Binary('Image 1920', related='product_id.image_1920')
    
    image_128 = fields.Binary('Image 128', related='product_id.image_128')
    
    kanban_state = fields.Selection([
        ('normal', 'Machine Out of Goal'),
        ('done', 'Machine on Goal'),
        ('blocked', 'Machine Stopped')], string='Kanban State',
        copy=False, default='normal', required=True)
    
    @api.onchange('color', 'kanban_state')
    def _compute_color_and_kanban_state(self):
        if self.kanban_state == 'done':
            self.color = 10
        elif self.kanban_state == 'blocked':
            self.color = 1
        else:
            self.color = 0
            
    @api.model
    def sync_colors(self):
        for equipment in self.search([]):
            if equipment.color == 10:
                equipment.kanban_state = 'done'
            elif equipment.color == 1:
                equipment.kanban_state = 'blocked'
            else:
                equipment.kanban_state = 'normal'
