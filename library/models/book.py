# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many("res.partner", string="Authors", domain=[('is_author', '=', True)])
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN', unique=True)
    publisher_id = fields.Many2one('res.partner', string='Publisher', domain=[('is_publisher', '=', True)])

    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")
    is_book = fields.Boolean(string='Is a Book', default=False)
    
    book_rent_count = fields.Integer(compute="_count_rent")

    @api.depends('copy_ids.rental_ids')
    def _count_rent(self):
        for rec in self:
            rec.book_rent_count = len(rec.mapped('copy_ids.rental_ids.customer_id'))
    
    @api.multi
    def action_load_rents(self):
        return {
            'domain': [('id', 'in', self.mapped('copy_ids.rental_ids.customer_id').ids)],
            'name': 'Rentals',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window'
        } 
            
class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", domain=[('is_book', "=", True)], required=True, ondelete="cascade", delegate=True)
    reference = fields.Char(required=True, string="Ref")

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
    book_state = fields.Selection([('available', 'Available'), ('rented', 'Rented'), ('lost', 'Lost')], default="available")
