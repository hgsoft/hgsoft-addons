# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re

class CustomSurveyMailComposeMessage(models.TransientModel):
    _inherit = 'survey.mail.compose.message'
    
    def _default_multi_email(self):
        partner_list = self.env['res.partner'].search([('send_survey','=', True)])
        
        user_list = self.env['res.users'].search([('send_survey','=', True)])
        
        if (len(partner_list) + len(user_list)) > 0:
            
            survey_email_list = []
                                    
            for partner in partner_list:
                if partner.email:
                    survey_email_list.append(partner.email)
                    
            for user in user_list:
                email = None
                
                if '@' in user.login:
                    email = user.login
                else:
                    if user.partner_id:
                         if '@' in user.partner_id.email:
                            email = user.partner_id.email

                if email:
                    survey_email_list.append(email)                    
        
            if len(survey_email_list) > 0:               
                return re.sub(r"(\[|\]|\'|\")", '', str(list(set(survey_email_list))))
                        
        return ''
    
    multi_email = fields.Text(string='List of emails', help="This list of emails of recipients will not be converted in contacts.\
        Emails must be separated by commas, semicolons or newline.", default=_default_multi_email)