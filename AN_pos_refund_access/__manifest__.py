{
    'name': 'POS Refund Access',
    'version': '17.0.1.0.0',
    'summary': 'POS | Refund Order Authorization.',
    'description': """This module restricts POS order refunds, allowing access only to authorized group members.""",
    'category': 'Point of Sale',
    'author': 'Ahmed Alnahal',
    'maintainer': 'Ahmed Alnahal',
    'website': 'https://www.linkedin.com/in/ahmed-alnahal/',
    'license': 'OPL-1',
    'depends': ['point_of_sale'],
    "data": [
        'security/group_refund.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'AN_pos_refund_access/static/src/js/pos_control_button.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
