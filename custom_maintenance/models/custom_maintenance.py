# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomMaintenance(models.Model):
    _inherit = "maintenance.equipment"
    
    product_id = fields.Many2one('product.product', string='Product', domain="[('product_tmpl_id.type', '=', 'equipment')]", tracking=True)
    
    image_1920 = fields.Binary('Image 1920', related='product_id.image_1920')
    
    image_128 = fields.Binary('Image 128', related='product_id.image_128')
    
    kanban_state = fields.Selection([
        ('0', 'máquina desligada, sem energia'),
        ('1', 'máquina energizada mas parada'),
        ('2', 'preparação 1'),
        ('3', 'preparação 2'),
        ('4', 'preparação 3'),
        ('5', 'máquina pronta'),
        ('6', 'máquina sendo operada manualmente'),
        ('7', 'máquina trabalhando sem repetibilidade'),
        ('8', 'máquina trabalhando com repetibilidade'),
        ('9', 'máquina produzindo com repetibilidade'),
        ('10', 'máquina produzindo com repetibilidade e qualidade')
    ], string='Kanban State', copy=False, default='0', required=True)
    
    '''
    máquina desligada, sem energia
    máquina energizada mas parada
    preparação 1
    preparação 2
    preparação 3
    máquina pronta
    máquina sendo operada manualmente
    máquina trabalhando sem repetibilidade
    máquina trabalhando com repetibilidade
    máquina produzindo com repetibilidade
    máquina produzindo com repetibilidade e qualidade
    '''
    
    @api.onchange('color', 'kanban_state')
    def _compute_color_and_kanban_state(self):
        pass
        '''
        if self.kanban_state == 'done':
            self.color = 10
        elif self.kanban_state == 'blocked':
            self.color = 1
        else:
            self.color = 0
        '''
            
    @api.model
    def sync_colors(self):
        pass
        '''
        for equipment in self.search([]):
            if equipment.color == 10:
                equipment.kanban_state = 'done'
            elif equipment.color == 1:
                equipment.kanban_state = 'blocked'
            else:
                equipment.kanban_state = 'normal'
        '''
