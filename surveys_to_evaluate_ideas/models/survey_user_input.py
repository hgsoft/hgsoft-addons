# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'
    
    evaluation_amount = fields.Integer(compute='_compute_evaluation_amount')

    evaluation_stage = fields.Selection([('pending', 'Pending'), ('refused', 'Refused'), ('approved', 'Approved')], 
                                        string='Evaluation Stage', default='pending', required=True)
        
    survey_type = fields.Selection(string='Survey Type', related='survey_id.survey_type')
            
    evaluation_ids = fields.One2many('survey.evaluation', 'user_input_id', string='Survey Input Evaluation')
        
    def _compute_evaluation_amount(self):
        for rec in self:
            evaluations = self.env['survey.evaluation'].search([('user_input_id','=', rec.id)])        
            rec.evaluation_amount = len(evaluations)
    
    def evaluate(self):
        
        local_context = dict(
            self.env.context,            
        )            
        
        evaluation = self.env['survey.evaluation'].search([('user_input_id','=', self.id), ('create_uid','=', local_context['uid'])])        
        
        action = self.env.ref('surveys_to_evaluate_ideas.action_survey_evaluation_evaluate').read()[0]
                
        action['res_id'] = evaluation.id if evaluation else None
        
        self._compute_evaluation_amount()        
        
        return action
