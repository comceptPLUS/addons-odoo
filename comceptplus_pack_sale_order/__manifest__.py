# -*- coding: utf-8 -*-
{
    'name': "Pack records (attachments) - sale orders",
    'version': '1.0',
    'author' : 'comceptPlus',
    'website' : 'https://comceptplus.com',
    'category': 'Accounting',
    'summary': "Export selected sale order's attachments into a compressed file",
    'description': 'This module allows the user to select sale orders and pack their attachments in a zip file.',
    'depends': [
                'sale_management',
                'comceptplus_pack_records',
                ],
    'data': ['data/action_data.xml'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
