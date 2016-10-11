# -*- coding: utf-8 -*-
{
    'name': "Consignment Sales",

    'summary': """
        Customizations for Consignment Sales """,

    'description': """
        Customizations for Consignment Sales
    """,

    'author': "S Patel",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'General',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','stock','account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_view.xml',
        'views/sale_view.xml',
        'views/stock.xml',
        'views/import_wizard_product_adj.xml',
        'views/consignment_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
}