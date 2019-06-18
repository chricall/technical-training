# -*- coding: utf-8 -*-
from odoo import fields, models


class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'
    
    bookcopy_ids = fields.One2many('library.bookcopy','book_id',string="Book copies")
    
    name = fields.Char(string='Title')

    author_ids = fields.Many2many("library.partner", string="Authors")
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')

    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')

class BookCopy(models.Model):
    _name = "library.bookcopy"
    _inherits = {'library.book': 'book_id'} #because we have delegate is true in Book_id
    _description = "Book copy"
    
    book_id = fields.Many2one("library.book",string="Book",required=True,ondelete="cascade")
    name = fields.Char(string="Copy name")
    uniqueid = fields.Char(string="Internal Reference")
    
