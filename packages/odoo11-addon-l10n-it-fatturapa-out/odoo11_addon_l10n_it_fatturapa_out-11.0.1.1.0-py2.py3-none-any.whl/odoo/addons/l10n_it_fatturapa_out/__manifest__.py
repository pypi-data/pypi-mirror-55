# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Sergio Corato
# Copyright 2018 Lara Baggio (Link IT srl)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura Elettronica - Emissione',
    "version": "11.0.1.1.0",
    'development_status': 'Beta',
    'category': 'Localization/Italy',
    'summary': 'Emissione fatture elettroniche',
    'author': 'Davide Corio, Agile Business Group, Innoviu,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n_italy',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_fatturapa',
        'l10n_it_split_payment',
        ],
    'data': [
        'wizard/wizard_export_fatturapa_view.xml',
        'views/attachment_view.xml',
        'views/account_view.xml',
        'security/ir.model.access.csv',
        'data/l10n_it_fatturapa_out_data.xml',
    ],
    'installable': True,
}
