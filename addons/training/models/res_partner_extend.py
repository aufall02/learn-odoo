from odoo import api, fields, models

class ResPartnerExtend(models.Model):
    _inherit = 'res.partner'

    province_id = fields.Many2one(comodel_name='training.province', string='Province')
    city_id = fields.Many2one(comodel_name='training.city', string='City')
    district_id = fields.Many2one(comodel_name='training.district', string='District')
    village_id = fields.Many2one(comodel_name='training.village', string='Village')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])