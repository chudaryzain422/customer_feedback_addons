{
    'name': 'POS Feedback System',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Customer Feedback System with QR Codes for POS',
    'description': """
        This module enables:
        - QR Code generation for each POS
        - Customer feedback collection using surveys
        - Automatic discount voucher generation
        - Integration with Odoo Survey module
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'point_of_sale',
        'pos_loyalty',
        'survey',
        'website',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'data/survey_template.xml',
        'views/survey_templates.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_feedback/static/src/xml/js/pos_order.js',
            'pos_feedback/static/src/xml/custom_order_recipt.xml',
        ],

    },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
