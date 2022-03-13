# -*- coding: utf-8 -*-

from collections import OrderedDict

from odoo import http, _
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomWebsite(CustomerPortal):

    @http.route()
    def account(self, **kw):
        """ Add documents to main account page """
        response = super(CustomWebsite, self).account(**kw)
        partner = request.env.user.partner_id
        PortalDashboard = request.env['portal.dashboard']
        dashboard_count = PortalDashboard.search_count([
            ('active', '=', True),
            # ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ])
        # dashboard
        portal_dashboard = PortalDashboard.search([
            ('active', '=', True),
            # ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ])
        response.qcontext.update({
            'dashboard_count': dashboard_count,
            'portal_dashboard': portal_dashboard,
        })
        return response

    @http.route(['/my/dashboard', '/my/dashboard/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_dashboard(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PortalDashboard = request.env['portal.dashboard']
        dashbs = ''
        # dashboard
        dashboard_partner = PortalDashboard.search([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ])
        pager = ''
        if dashboard_partner:
            for dash in dashboard_partner:
                active = dash.active
            domain = [('active', '=', active)]
            dashboard_count = PortalDashboard.search_count(domain)
            # make pager
            pager = request.website.pager(
                url="/my/dashboard",
                url_args={'date_begin': date_begin, 'date_end': date_end},
                total=dashboard_count,
                page=page,
                step=self._items_per_page
            )
            # search the count to display, according to the pager data
            dashbs = PortalDashboard.search(domain, limit=self._items_per_page, offset=pager['offset'])
        if date_begin and date_end:
            domain += [('create_date', '>=', date_begin), ('create_date', '<=', date_end)]
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'dashbs': dashbs,
            'pager': pager,
            'default_url': '/my/dashboard',
        })
        return request.render("website_iframe.portal_my_dashboard", values)
