# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomMailActivity(models.Model):
    _inherit = "mail.activity"
    
    show_user_ids = fields.Boolean(default=True)
    
    user_ids = fields.Many2many('res.users', 'mail_activities_user_ids', 'activity_id', 'user_id', string='Recipients', index=True)
        
    @api.model
    def create(self, vals):
        
        print('=' * 30)
        print('')
        print('[CREATE][START]')
        #print(vals)
        #print(self.env.__dict__)
        obj = self.env['document.page'].search([])
        print(obj)
        print('[CREATE][START]')
        print('')
        print('=' * 30)
        
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


    '''
    
    Usar: default_res_model, default_res_id
    
    Valida se default_res_model = document.page
    
    Busca self.env... pelo default_res_id
    
    Seta os dados que forem necessários (ex.: revisão) na activity com base no objeto retornado
    
    {'cr': <odoo.sql_db.Cursor object at 0x7f4c365f4c88>, 'uid': 2, 'context': {'lang': 'pt_BR', 'tz': 'Europe/Brussels', 'uid': 2, 'allowed_company_ids': [1], 'default_res_id': 2, 'default_res_model': 'document.page'}, 'su': False, 'args': (<odoo.sql_db.Cursor object at 0x7f4c365f4c88>, 2, {'lang': 'pt_BR', 'tz': 'Europe/Brussels', 'uid': 2, 'allowed_company_ids': [1], 'default_res_id': 2, 'default_res_model': 'document.page'}, False), 'registry': <odoo.modules.registry.Registry object at 0x7f4c3822c5f8>, 'cache': <odoo.api.Cache object at 0x7f4c3570dac8>, '_protected': <odoo.tools.misc.StackMap object at 0x7f4c3f6c3678>, 'all': <odoo.api.Environments object at 0x7f4c3570de48>}
    '''
