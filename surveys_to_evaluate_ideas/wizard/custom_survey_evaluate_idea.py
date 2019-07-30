# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomSurveyUserInputWizard(models.TransientModel):
    _name = 'survey.user_input.wizard'

    type = fields.Selection([
        ('new_project', 'Novo Projeto'),
        ('upgrade', 'Melhoria')],
    string='Tipo de Idéia', default='new_project', required=True)

    """
    def action_evaluate_survey_idea(self):
        # partner_list = self.env['res.partner'].search([('send_survey','=', True)])
        
        # user_list = self.env['res.users'].search([('send_survey','=', True)])
        
        
                        
        return ''
    """