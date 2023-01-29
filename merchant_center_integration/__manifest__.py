{
    'name': "Google Merchant Center",
    'summary': 'Show case Sales Details',
    'description': "Shows Sales Details",
    'application': True,
    'category': '',
    'version': '1.0',
    'depends': ['sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/merchent_authentication_view.xml',
        'views/publish_button_view.xml',
        'views/product_add_wizard_view.xml'
    ],
    'license': 'LGPL-3',
}
