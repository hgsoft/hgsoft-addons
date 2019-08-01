# -*- coding: utf-8 -*-
from odoo import fields, models, api

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'
    
    evaluation_amount = fields.Integer(compute='_compute_evaluation_amount')

    evaluation_stage = fields.Selection([('pending', 'Pending'), ('refused', 'Refused'), ('approved', 'Approved')], 
                                        string='Evaluation Stage', default='pending', required=True)
        
    can_evaluate = fields.Boolean(default=False)
    
    #active = fields.Boolean(default=True)

        
    @api.one
    def _compute_evaluation_amount(self):
        evaluations = self.env['survey.evaluation'].search([('user_input_id','=', self.id)])        
        self.evaluation_amount = len(evaluations)
        if evaluations:
            self.can_evaluate = True
        else:
            self.can_evaluate = False
        print('=========')
        print(self)
        print(self.can_evaluate)
        print('=========')
    
    def evaluate(self):
        
        local_context = dict(
            self.env.context,            
        )
        
        local_context['create'] = False
        
        
        evaluation = self.env['survey.evaluation'].search([('user_input_id','=', self.id), ('create_uid','=', local_context['uid'])])        
        
        action = self.env.ref('surveys_to_evaluate_ideas.action_survey_evaluation_evaluate').read()[0]
        
        print('=' * 30)
        print('')
        print('USER_ID')
        print(local_context['uid'])
        print('SURVEY_INPUT_ID')
        print(self.id)
        print('EVALUATION_ID')
        print(evaluation.id)
        print(local_context)
        print('ACTION')
        print(action)        
        print('')
        print('=' * 30)
        
        action['res_id'] = evaluation.id if evaluation else None
        
        
        return action


        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey.evaluation',
            'target': 'new',
            'context': local_context,
            'view': [('wizard_form_view','form')],
            'res_id': evaluation.id if evaluation else None,            
        }
        

class SurveyEvaluation(models.Model):
    _name = 'survey.evaluation'
    
    def _default_survey_user_input(self):
        return self.env['survey.user_input'].browse(self._context.get('active_id'))    
        
    user_input_id = fields.Many2one('survey.user_input', string='Survey User Input', ondelete='cascade', required=True, readonly=True, default=_default_survey_user_input)
    
    project_type = fields.Selection([('new_project', 'New Project'), ('improvement', 'Improvement')], 
                                        string='Project type', default='new_project', required=True)
    
    project_category = fields.Selection([('costs', 'Costs'), ('productivity', 'Productivity'), ('safety', 'Safety'), ('environment', 'Environment'), ('organization', 'Organization'), ('quality', 'Quality / Process / Product or Quality of life')], 
                                    string='Considering the project description, it generally refers more to', default='costs', required=True)
    
    project_innovation = fields.Selection([('groundbreaking', 'Groundbreaking'), ('creative', 'Creative'), ('relevant_improvement', 'Relevant Improvement'), ('simple_improvement', 'Simple Improvement')], 
                                  string='Considering the project description, he suggests being', default='groundbreaking', required=True)
    
    project_complexity = fields.Selection([('very_complex', 'Very Complex'), ('difficult', 'Difficult'), ('middle_level', 'Middle Level'), ('simple', 'Simple')],
                                          string='Assessing the degree of difficulty / complexity in the implementation', default='very_complex', required=True)
    
    project_investment = fields.Selection([('estimate', 'Estimate'), ('payback', 'PayBack')], 
                                          string='Investment', default='estimate', required=True)
    
    project_impact = fields.Selection([('not', 'Not'), ('not_relevant', 'Not Relevant'), ('relevant', 'Relevant')], 
                                      string='impact on other sectors', default='not', required=True)
    
    
    
    
    
    
    
    
    
    
    
