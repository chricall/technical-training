# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging
from odoo import exceptions
from odoo.exceptions import ValidationError

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    
    _inherit = ['mail.thread']

    customer_id = fields.Many2one('res.partner', string='Customer')
    copy_id = fields.Many2one('library.copy', string="Book Copy")
    book_id = fields.Many2one('library.book', string='Book', related='copy_id.book_id', readonly=True)

    rental_date = fields.Date(default=fields.Date.context_today)
    return_date = fields.Date(default=fields.Date.context_today)

    customer_address = fields.Text(compute='_compute_customer_address')
    customer_email = fields.Char(related='customer_id.email')
    
    returned = fields.Boolean(string="Returned")
    fee = fields.Float(string="Standard Fee") 
    totalfee = fields.Float(string="Standard (+ extra)")
    state = fields.Selection([('progress', 'In progress'), ('expired', 'Expired'), ('returned', 'Returned'),('lost','Lost')],string='State', default='progress')
    
    book_authors = fields.Many2many(related='copy_id.author_ids')
    book_edition_date = fields.Date(related='copy_id.edition_date')
    book_publisher = fields.Many2one(related='copy_id.publisher_id')

    @api.onchange('rental_date','return_date')
    def _validate_dates(self):
        for rec in self:
            if rec.rental_date > rec.return_date:
                 raise ValidationError('Return date is sooner that rental? Impossible.')
    
    @api.depends('customer_id')
    def _compute_customer_address(self):
        self.customer_address = self.customer_id.address_get()
    
    """ @api.depends('return_date','rental_date')
    def _calculate_fee(self):
        if(self.returned == False):
            for rec in self:
                days = fields.Date.from_string(rec.return_date) - fields.Date.from_string(rec.rental_date)
                rec.fee = days.days * 0.10

    
    @api.depends('return_date','rental_date')
    def _calculate_total(self):
        if(self.returned == False):
            for rec in self:
                if rec._check_expiry() and not rec.returned:
                    extradays = fields.Date.from_string(fields.Date.today()) - fields.Date.from_string(rec.return_date)
                    rec.totalfee = (extradays * 0.50) + rec.fee
    """
    # ----- TODO: refactor ---------
    
    @api.model
    def create(self, values):
        so = super(Rentals, self).create(values)
        so.copy_id.inrent = True
        return so
    
    def _set_status(self):
        for rec in self:
            rec.state = 'progress'
            if rec._check_expiry():
                rec.state = 'expired'
            if rec.returned:
                rec.state = 'returned'
    
    def action_lost(self):
        for rec in self:
            rec.action_calculate()
            rec.state = 'lost'
            rec.returned = True
            rec.totalfee += 10.00
            rec.customer_id.owed += rec.totalfee
            rec.copy_id.active = False
            rec.copy_id.inrent = False
    
    def _check_expiry(self):
        if(self.return_date < fields.Date.today()):
            return True
        return False
    
    def action_calculate(self):
        for rec in self:
            days = fields.Date.from_string(rec.return_date) - fields.Date.from_string(rec.rental_date)
            rec.fee = days.days * 0.10
            rec.totalfee = rec.fee
            if rec._check_expiry():
                extradays = fields.Date.from_string(fields.Date.today()) - fields.Date.from_string(rec.return_date)
                rec.totalfee += (extradays.days * 0.50)
            rec._set_status()
    
    def action_reminder(self):
        for rec in self:
            if(rec._check_expiry()):
                  rec.env.ref('library.rental_reminder_mail_template').send_mail(rec.id)
    
    def action_return(self):
        for rec in self:
            rec.action_calculate()
            rec.returned = True
            rec.customer_id.owed += rec.totalfee
            rec._set_status()
            rec.copy_id.inrent = False


