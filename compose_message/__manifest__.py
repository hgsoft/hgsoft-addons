# -*- encoding: utf-8 -*-
{
    'name': "Send message button on topbar",
    'description': """
Just revert the compose message code which is removed from official code base, please follow this discussion for detail:
https://github.com/odoo/odoo/commit/5209fbc7ed9fcad966ab064654a8a8697142be42
Migrate to Odoo 10 by HGSOFT
""",
    'author': "xujl",
    'category': 'Mail',
    'version': '10.0.0.1',
    'website': 'http://www.hgsoft.com.br',
    'contributors': ['Alexsandro Haag <alex@hgsoft.com.br>'],

    'depends': ['base', 'mail'],

    'data': [
        # 'security/ir.model.access.csv',
        'template.xml',
    ],
    'qweb':[
        'static/src/xml/mail.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'license': 'LGPL-3',
    'installable': True,
}
