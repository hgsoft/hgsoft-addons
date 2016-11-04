#coding=utf-8

{
    'name': 'partner_kanban_phone',
    'category': 'Sale',
    'summary': 'Telefone na visão kanban do cadastro de parceiros',
    'version': '1.0',
    'description': "Exibe o telefone na visão kanban do cadastro de parceiros",
    'author': 'HGSOFT - Alexsandro Haag',
    'depends': ['base','sale'],
    'data': [
        'views/partner_phone_kanban_view.xml',
    ],
    'installable': True,
}