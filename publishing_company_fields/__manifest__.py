# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# Copyright (C) 2017 HGSOFT - www.hgsoft.com.br                               #
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
    'name': "publishing_company_fields",

    'summary': """Adds new fields to handle publishers.""",

    'description': """Adds new control fields for 'author' and 'publisher' in 'Partner' and 'Product' base modules.""",

    'author': "HGSoft - Soluções Criativas e Inteligentes",
    
    'website': "http://www.hgsoft.com.br/",

    'category': 'Site',
    
    'version': '1.0',

    'depends': ['base', 'product', 'sale', 'sale_management'],

    'data': [
        'security/ir.model.access.csv',
        #'security/security.xml',
        'views/partner.xml',
        'views/product.xml',
        'views/royalties_report.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}