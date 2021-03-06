# -*- coding: utf-8 -*-
from odoo import fields, models, api


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
