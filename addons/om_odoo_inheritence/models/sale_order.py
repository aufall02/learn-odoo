# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit= 'sale.order'
    _description = 'Percobaan inherit module'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')

    def action_confirm(self):
        print('suceesssss')
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id
