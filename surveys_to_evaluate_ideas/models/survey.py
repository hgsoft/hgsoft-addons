# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Survey(models.Model):
    _inherit = 'survey.survey'            
        
    survey_type = fields.Selection([('common', 'Common'), ('ideas', 'Ideas')], 
                                        string='Survey type', default='common', required=True)
