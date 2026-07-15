from odoo import fields, models, api


class Province(models.Model):
    _name = 'training.province'
    _description = 'Province'

    name = fields.Char(string='Name', help='Name of the Province')
    code = fields.Char(string='Code', help='Code of the Province')
    alias = fields.Char(string='Alias', help='Alias for province')
    description = fields.Text(string='Description', help='Description of the province')

    city_ids = fields.One2many(comodel_name='training.city', inverse_name='province_id')


class City(models.Model):
    _name = 'training.city'
    _description = 'City'

    name = fields.Char(string='Name', help='Name of the City')
    code = fields.Char(string='Code', help='Code of the City')
    description = fields.Text(string='Description', help='Description of the city')

    province_id = fields.Many2one(comodel_name='training.province', string='Province', help='Province of the City')
    district_ids = fields.One2many(comodel_name='training.district', inverse_name='city_id')


class District(models.Model):
    _name = 'training.district'
    _description = 'District'

    name = fields.Char(string='Name', help='Name of the District')
    code = fields.Char(string='Code', help='Code of the District')
    description = fields.Text(string='Description', help='Description of the District')

    city_id = fields.Many2one(comodel_name='training.city', string='City', help='City of the District')
    village_ids = fields.One2many(comodel_name='training.village', inverse_name='district_id')


class Village(models.Model):
    _name = 'training.village'
    _description = 'Village'

    name = fields.Char(string='Name', help='Name of the Village')
    code = fields.Char(string='Code', help='Code of the Village')
    description = fields.Text(string='Description', help='Description of the Village')
    district_id = fields.Many2one(comodel_name='training.district', string='District', help='District of the Village')

