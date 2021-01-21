# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomMaintenance(models.Model):
    _inherit = "maintenance.equipment"
    
    product_id = fields.Many2one('product.product', string='Product', domain="[('product_tmpl_id.type', '=', 'equipment')]", tracking=True)
    
    image_1920 = fields.Binary('Image 1920', related='product_id.image_1920')
    
    image_128 = fields.Binary('Image 128', related='product_id.image_128')
    
    kanban_state = fields.Selection([
        ('0', 'machine off, no power'),
        ('1', 'machine energized but stopped'),
        ('2', 'preparation 1'),
        ('3', 'preparation 2'),
        ('4', 'preparation 3'),
        ('5', 'machine ready'),
        ('6', 'machine being operated manually'),
        ('7', 'machine working without repeatability'),
        ('8', 'machine working with repeatability'),
        ('9', 'machine producing with repeatability'),
        ('10', 'machine producing with repeatability and quality')
    ], string='Kanban State', copy=False, default='0', required=True)
    
    @api.constrains('kanban_state')
    def _onchange_kanban_state(self):
        self.color = int(self.kanban_state)
            
    @api.model
    def sync_colors(self):
        for equipment in self.search([]):
            equipment.kanban_state = str(equipment.color)

    @api.model
    def get_setting(self):
        setting = self.env['res.config.settings'].search([], order='id desc', limit=1)

        refresh_time_seconds = setting.refresh_time_seconds
                
        refresh_time_seconds = refresh_time_seconds if refresh_time_seconds > 0 else 30
        
        return {'refresh_time_seconds': refresh_time_seconds}

