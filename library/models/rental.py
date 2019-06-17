# -*- coding: utf-8 -*-
from odoo import fields, models


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    
    #bookname = fields.Char(related="book_id.name",string="Book name")
    author_ids = fields.Many2many(related="book_id.author_ids",string="Author")
    edition_date = fields.Date(related="book_id.edition_date", string="Edition Date")
    
    customer_email = fields.Char(related="customer_id.email",string="Customer email")
    customer_address = fields.Text(related="customer_id.address",string="Customer Address")
    
    customer_id = fields.Many2one('library.partner', string='Customer')
    book_id = fields.Many2one('library.book', string='Book')

    rental_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()
    
    