# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# Copyright (C) 2019 HGSOFT - www.hgsoft.com.br                               #
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
    'name': "Custom Accounting Invoice Lines",

    'summary': """Accounting Invoice Lines custom view.""",

    'description': """Accounting Invoice Lines custom view, with new filters and group by.""",

    'author': "HGSoft - Soluções Criativas e Inteligentes",
    
    'website': "http://www.hgsoft.com.br/",

    'category': 'General',
    
    'version': '2.0',

    'depends': ['br_account', 'br_nfe'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/account_invoice_line_view.xml',
    ],
    
}