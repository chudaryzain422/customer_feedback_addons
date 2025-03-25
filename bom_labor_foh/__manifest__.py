{
    'name': 'BOM Labor and FOH',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Add Labor and FOH components to Bill of Materials',
    'description': """
        This module extends the Bill of Materials to include Labor and FOH components.
        - Adds a new tab in BOM form for Labor and FOH
        - Automatically includes these components in Manufacturing Orders
        - Restricts product selection to consumable products only
    """,
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}