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
    'name': "Custom Invoice PDF Report",

    'summary': """Adds all due dates in the PDF report.""",

    'author': "HGSoft - Soluções Criativas e Inteligentes",
    
    'website': "http://www.hgsoft.com.br/",

    'category': 'Reports',
    
    'version': '11.0.0',

    'depends': ['base', 'account'],

    'data': [
        'views/custom_report_invoice.xml',
    ],
    
}