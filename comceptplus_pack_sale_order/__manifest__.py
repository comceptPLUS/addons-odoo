# -*- coding: utf-8 -*-
{
    'name': "Pack records (attachments) - sale orders",
    'version': '1.0',
    'license': 'AGPL-3',
    'author' : 'comceptPLUS',
    'website' : 'https://comceptplus.com',
    'category': 'Accounting',
    'summary': "Export selected sale order's attachments into a compressed file",
    'description': 'This module allows the user to select sale orders and pack their attachments in a zip file.',
    'depends': [
                'sale_management',
                'comceptplus_pack_records',
                ],
    'data': ['data/action_data.xml'],
    'images': ['static/images/main_screenshot.png'],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
