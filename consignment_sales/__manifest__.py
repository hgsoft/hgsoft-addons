# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# Copyright (C) 2018 HGSOFT - www.hgsoft.com.br                               #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

{
    'name': "Consignment Sales",

    'summary': """Customizações para Vendas Consignadas. """,

    'description': """Customizações para Vendas Consignadas. """,

    'author': "HGSoft - Soluções Criativas e Inteligentes [v11] | S Patel [v8]",
    
    'website': "http://www.hgsoft.com.br/",
    
    'category': 'General',
    
    'version': '1.0',

    'depends': ['base','sale_management','purchase','stock', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_view.xml',
        'views/sale_view.xml',
        'views/stock.xml',
        'views/import_wizard_product_adj.xml',
        'views/consignment_view.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
        # 'demo.xml',
    #],
}