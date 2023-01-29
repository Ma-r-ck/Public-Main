{
    'name': "Sales Dashboard",
    'summary': 'Show case Sales Details',
    'description': "Shows Sales Details",
    'application': True,
    'category': '',
    'version': '1.0',
    'depends': ['sale', 'base'],
    'data': [
        'views/dashboard_client_action.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_sales_dashboard/static/js/custom_dasboard.js',
            'custom_sales_dashboard/static/xml/sale_dashboard_view.xml',
            'custom_sales_dashboard/static/css/sales_dash_board.css',
            'https://www.gstatic.com/charts/loader.js',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js',
        ],
    },
    'license': 'LGPL-3',
}
