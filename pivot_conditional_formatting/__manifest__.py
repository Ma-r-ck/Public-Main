{
    'name': 'Pivot View Conditional Formatting',
    'summary': 'Conditional Formatting in Pivot View',
    'version': '16.0.1.0.0',
    'installable': True,
    'application': True,
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'description': "",
    'depends': ['base'],
    'assets': {
            'web.assets_backend': [
                'pivot_conditional_formatting/static/src/xml/pivot_view_extend.xml',
                'pivot_conditional_formatting/static/src/css/conditionalstyle.css',
                'pivot_conditional_formatting/static/src/js/pivot_render_extend.js',
            ],
        },
    'images': [''],
    'data': [
        'security/ir.model.access.csv',
        'views/rules_in_settings.xml'
    ],

    'auto_install': False,
    'license': 'LGPL-3',
}