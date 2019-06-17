from odoo import api, models, fields

class LibraryRental (models.Model):
    _name = 'library.rental'
    _description = "Class for rental"
    
    startdate = fields.Date(string="Renting Start Date")
    enddate = fields.Date(string="Rent Expiry")
    
    book_id = fields.Many2one('library.book',string="Book")

    customer_id = fields.Many2one('res.partner',string="Customer")