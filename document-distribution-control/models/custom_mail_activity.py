# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomMailActivity(models.Model):
    _inherit = "mail.activity"
    
    show_user_ids = fields.Boolean(default=True)
    
    user_ids = fields.Many2many('res.users', 'mail_activities_user_ids', 'activity_id', 'user_id', string='Recipients', index=True)
        
    @api.model
    def create(self, vals):
        user_ids = [vals['user_id']] + vals['user_ids'][0][2]
        vals['user_ids'] = None
        vals['show_user_ids'] = False
        rec = None

        for user_id in user_ids:
            vals['user_id'] = user_id
            rec = super(CustomMailActivity, self).create(vals)
        return rec
    
    @api.onchange('user_id')
    def _user_id_onchange(self):
        self.user_ids = None
        if self._ids[0].origin == False:
            # Criação
            return {'domain': {'user_ids': [('user_ids', '!=', self.user_id.id)]}}
        else:
            # Edição
            return {'domain': {'user_ids': [('user_ids', '=', None)]}}
    
    @api.onchange('user_ids')
    def _user_ids_onchange(self):
        if self._ids[0].origin == False:
            # Criação
            return {'domain': {'user_ids': [('user_ids', '!=', self.user_id.id)]}}
        else:
            # Edição
            return {'domain': {'user_ids': [('user_ids', '=', None)]}}

