# -*- coding: utf-8 -*-
{
    'name': "publishing_company_fields",

    'summary': """Adds new fields to handle publishers.""",

    'description': """Adds new control fields for 'author' and 'publisher' in 'Partner' and 'Product' base modules.""",

    'author': "HGSoft - Soluções Criativas e Inteligentes",
    
    'website': "http://www.hgsoft.com.br/",

    'category': 'Site',
    
    'version': '0.5',

    'depends': ['base', 'product'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/partner.xml',
        'views/product.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}