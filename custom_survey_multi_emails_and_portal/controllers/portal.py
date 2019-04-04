# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

SURVEYS_DEFAULT_DOMAIN = ['|', ('stage_id.name','ilike', '%PROGRESS%'), ('stage_id.name','ilike', '%PERMANENT%')]

class PortalSurveys(CustomerPortal):

    def _prepare_portal_layout_values(self):

        values = super(PortalSurveys, self)._prepare_portal_layout_values()
        
        values['surveys_count'] = request.env['survey.survey'].search_count(SURVEYS_DEFAULT_DOMAIN)
                
        return values


    @http.route(['/my/surveys', '/my/surveys/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_surveys(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
    
        values = self._prepare_portal_layout_values()
                    
        # Verificar se é possível ordenar pelo nome do stage_id
        searchbar_sortings = {
            'name': {'label': _('Pesquisa'), 'order': 'title'},
            'stage': {'label': _('Estágio'), 'order': 'stage_id'},
            'date': {'label': _('Create Date'), 'order': 'create_date'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']        
        
        pager = portal_pager(
            url="/my/surveys",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=values['surveys_count'],
            page=page,
            step=self._items_per_page
        )
        
        surveys = request.env['survey.survey'].search(SURVEYS_DEFAULT_DOMAIN, order=order, limit=self._items_per_page, offset=pager['offset'])                
        
        values = {
            'surveys': surveys,
            'page_name': 'survey',
            'pager': pager,
            'default_url': '/my/surveys',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'surveys_count': values['surveys_count'],
        }
                
        return request.render("custom_survey_multi_emails_and_portal.portal_my_surveys", values)
