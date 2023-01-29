{
    'name': 'Contract Expiry Email',
    'description': 'contract_expiry_email',
    'application': True,
    'version': '15.0.1.0.0',

    'data': [
        'data/expiry_email.xml',
        'data/expiry_email_template.xml',
        'views/expiry_email_dates.xml'
    ],

    'depends': ['base', 'hr_contract', 'mail', 'hr']
}
