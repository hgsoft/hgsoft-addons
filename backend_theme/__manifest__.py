# -*- coding: utf-8 -*-
# Copyright 2016, 2020 Openworx - Mario Gielissen
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "HGSOFT Material Backend Theme",
    "summary": "HGSOFT Material Backend Theme V13 forked from OpenWorx",
    "version": "13.0.0.4",
    "category": "Theme/Backend",
    "website": "http://www.hgsoft.com.br",
	"description": """
		HGSOFT Material Backend theme for Odoo 13.0 community edition.
    """,
	'images':[
        'images/screen.png'
	],
    "author": "HGSOFT/Openworx",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
        'web_responsive',

    ],
    "data": [
        'views/assets.xml',
		'views/res_company_view.xml',
		'views/users.xml',
        	'views/sidebar.xml',
    ],

}

