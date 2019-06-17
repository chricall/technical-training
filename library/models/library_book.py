from odoo import api, models, fields

class LibraryBook (models.Model):
    _name = 'library.book'
    _description = "Class for Library"
    
    name = fields.Char(string="Book Name")
    isbn = fields.Char(string="ISBN")
    yearofedition = fields.Integer(string="Year of Edition")
    editor_id = fields.Many2one('res.partner',name="Editor")
    authors_ids = fields.Many2many('res.partner',name="Authors")
    
    rental_ids = fields.One2many('library.rental','book_id',string="Rented Books")
