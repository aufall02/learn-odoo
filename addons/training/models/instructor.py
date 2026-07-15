from odoo import fields, models

class Instructor(models.Model):
    _name = 'training.instructor'
    _description = 'Instructor'
    _inherits = {'res.partner':'partner_id'}


    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True, ondelete='cascade')
    expertise_ids = fields.Many2many(comodel_name='training.expertise', string='Expertise')


class Expertise(models.Model):
    _name = 'training.expertise'
    _description = 'Expertise'

    name = fields.Char(string='Expertise', required=True)
