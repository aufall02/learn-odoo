# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'training.course'

    name = fields.Char(string='Course Name', required=True)
    description = fields.Text(string='Course Description')

