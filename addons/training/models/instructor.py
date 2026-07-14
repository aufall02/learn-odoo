from odoo import fields, models

from addons.base_accounting_kit import report


class Instructor(models.Model):
    _name = 'instructor'
    _description = 'Instructor'
    _inherit = {'res.partner':'partner_id'}


    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True, ondelete='cascade')
    expertise_ids = fields.Many2one(comodel_name='expertise', string='Expertise')


class Expertise(models.Model):
    _name = 'expertise'
    _description = 'Expertise'

    name = fields.Char(string='Expertise', required=True)
