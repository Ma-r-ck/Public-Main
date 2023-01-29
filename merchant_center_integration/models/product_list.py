from odoo import models,fields


class ProductList(models.Model):
    _name = "merchant.product.list"
    _description = "Product List"

    merchant_item_id = fields.Char(string="Item ID")
    product_offer_id = fields.Char(string="Offer ID")
    product_id = fields.Many2one('product.product')
    content_lang = fields.Selection(string='Content Language',
                                    selection=[('en', 'English'),
            ('hi', 'Hindi'),('ar', 'Arabic'),('zh', 'Chinese'),('cs', 'Czech'),
            ('da', 'Danish'),('nl', 'Dutch'),('fi', 'Finnish'),
            ('fr', 'French'),('de', 'german'),('el', 'Greek'),('he', 'Hebrew'),
            ('hu', 'Hungarian'),('id', 'Indonesian'),('it', 'Italian'),
            ('ja', 'Japanese'),('ko', 'Korean'),('no', 'Norwegian'),
            ('pl', 'Polish'),('pt', 'Portuguese'),('ro', 'Romanian'),
            ('ru', 'Russian'),('sk', 'Slovak'),('es', 'Spanish'),
            ('sv', 'Swedish'),('th', 'Thai'),('tr', 'Turkish'),
            ('uk', 'Ukrainian'),('vi', 'Vietnamese')])

    target_cntry = fields.Selection(string='Target Country', selection=([
        ('DZ', 'Algeria'), ('AO', 'Angola'), ('AR', 'Argentina'),
        ('AU', 'Australia'),
        ('AT', 'Austria'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'), ('BR', 'Brazil'), ('KH', 'Cambodia'),
        ('CM', 'Cameroon'),
        ('CA', 'Canada'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'),
        ('CR', 'Costa Rica'), ('CI', 'Côte d’Ivoire'), ('CZ', 'Czechia'),
        ('DK', 'Denmark'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'),
        ('EG', 'Egypt'), ('SV', 'El Salvador'), ('ET', 'Ethiopia'),
        ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'),
        ('DE', 'Germany'),
        ('GH', 'Ghana'), ('GR', 'Greece'), ('GT', 'Guatemala'),
        ('HK', 'Hong Kong'),
        ('HU', 'Hungary'), ('IN', 'India'), ('ID', 'Indonesia'),
        ('IE', 'Ireland'),
        ('IL', 'Israel'), ('IT', 'Italy'), ('JP', 'Japan'), ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KW', 'Kuwait'),
        ('LB', 'Lebanon'),
        ('MG', 'Madagascar'), ('MY', 'Malaysia'), ('MU', 'Mauritius'),
        ('MX', 'Mexico'), ('MA', 'Morocco'), ('MZ', 'Mozambique'),
        ('MM', 'Myanmar(Burma)'), ('NP', 'Nepal'), ('NL', 'Netherlands'),
        ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NG', 'Nigeria'),
        ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PA', 'Panama'),
        ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('RO', 'Romania'),
        ('RU', 'Russia'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'),
        ('SG', 'Singapore'), ('SK', 'Slovakia'), ('ZA', 'South Africa'),
        ('KR', 'South Korea'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
        ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TW', 'Taiwan'),
        ('TZ', 'Tanzania'),
        ('TH', 'Thailand'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
        ('UG', 'Uganda'),
        ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'),
        ('US', 'United States'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'),
        ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe')]))

    description = fields.Text(string="Description")
    website_link = fields.Char('Link')
    image_link = fields.Char(string="Image Link")
    availability = fields.Selection(selection=[('backorder', 'BackOrder'),
                                               ('in stock', 'In Stock'),
                                               ('limited availability',
                                                'Limited Availability'),
                                               (
                                               'out of stock', 'Out Of Stock'),
                                               ('preorder', 'PreOrder')],
                                    default="in stock")
    condition = fields.Selection(selection=[('new', 'New'),
                                            ('refurbished', 'Refurbished'),
                                            ('used', 'Used')], default="new")
    product_ctgry = fields.Char(string='Google Product Category')
    price = fields.Float(string='Price')
    currency = fields.Selection(string='Currency', selection=([
        ('AED', 'AED'), ('AOA', 'AOA'), ('ARS', 'ARS'), ('AUD', 'AUD'),
        ('BDT', 'BDT'),
        ('BHD', 'BHD'), ('BRL', 'BRL'), ('BYN', 'BYN'), ('CAD', 'CAD'),
        ('CHF', 'CHF'),
        ('CLP', 'CLP'), ('CNY', 'CNY'), ('COP', 'COP'), ('CRC', 'CRC'),
        ('CZK', 'CZK'),
        ('DKK', 'DKK'), ('DOP', 'DOP'), ('DZD', 'DZD'), ('EGP', 'EGP'),
        ('ETB', 'ETB'),
        ('EUR', 'EUR'), ('GBP', 'GBP'), ('GEL', 'GEL'), ('GHS', 'GHS'),
        ('GTQ', 'GTQ'),
        ('HKD', 'HKD'), ('HUF', 'HUF'), ('IDR', 'IDR'), ('ILS', 'ILS'),
        ('INR', 'INR'),
        ('JOD', 'JOD'), ('JPY', 'JPY'), ('KES', 'KES'), ('KHR', 'KHR'),
        ('KRW', 'KRW'),
        ('KWD', 'KWD'), ('KZT', 'KZT'), ('LBP', 'LBP'), ('LKR', 'LKR'),
        ('MAD', 'MAD'),
        ('MGA', 'MGA'), ('MMK', 'MMK'), ('MUR', 'MUR'), ('MXN', 'MXN'),
        ('MYR', 'MYR'),
        ('MZN', 'MZN'), ('NGN', 'NGN'), ('NIO', 'NIO'), ('NOK', 'NOK'),
        ('NPR', 'NPR'),
        ('NZD', 'NZD'), ('OMR', 'OMR'), ('PAB', 'PAB'), ('PEN', 'PEN'),
        ('PHP', 'PHP'),
        ('PKR', 'PKR'), ('PLN', 'PLN'), ('PYG', 'PYG'), ('RON', 'RON'),
        ('RUB', 'RUB'),
        ('SAR', 'SAR'), ('SEK', 'SEK'), ('SGD', 'SGD'), ('THB', 'THB'),
        ('TND', 'TND'),
        ('TRY', 'TRY'), ('TWD', 'TWD'), ('TZS', 'TZS'), ('UAH', 'UAH'),
        ('UGX', 'UGX'),
        ('USD', 'USD'), ('UYU', 'UYU'), ('UZS', 'UZS'), ('VES', 'VES'),
        ('VND', 'VND'),
        ('XAF', 'XAF'), ('XOF', 'XOF'), ('ZAR', 'ZAR'), ('ZMW', 'ZMW')]),
                                default="USD")
    gtin_no = fields.Integer(string="GTIN", help="Global Trade Item Number")
    show_gtin = fields.Boolean(string="Use GTIN",
                               help="Use Global Trade item number")