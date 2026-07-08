# -*- coding: utf-8 -*-
# from odoo import http


# class TestingBang(http.Controller):
#     @http.route('/testing_bang/testing_bang', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/testing_bang/testing_bang/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('testing_bang.listing', {
#             'root': '/testing_bang/testing_bang',
#             'objects': http.request.env['testing_bang.testing_bang'].search([]),
#         })

#     @http.route('/testing_bang/testing_bang/objects/<model("testing_bang.testing_bang"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('testing_bang.object', {
#             'object': obj
#         })

