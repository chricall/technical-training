from odoo import http
import logging

class Library(http.Controller):
    _logger = logging.getLogger( __name__ )
    
    @http.route('/academy/test/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('library.index', {
            'books': http.request.env['product.product'].search([('book','=',True)])
        })
    
    @http.route('/academy/test/rent', auth='public', website=True, methods=['POST'], csrf=False)
    def rent_book(self, **kw):
        email = kw.get('email')
        for book in kw.keys():
            tmp = book.split('-')
            if tmp[0] == 'book':
                book_id = tmp[1]
                available_book_copies = http.request.env['library.copy'].search([
                    ('book_id', '=', int(book_id)),
                    ('book_state','=','available')
                ])
                self._logger.info( available_book_copies )
                if len(available_book_copies) > 0:
                    customer = http.request.env['res.partner'].search([('email','=',email)])
                    if not customer:
                        # TODO: Chris will do a new accounts here
                        continue
                    else:
                        http.request.env['library.rental'].create({ 
                            'customer_id': customer.id, 
                            'copy_id': available_book_copies[0].id 
                        })
                        available_book_copies[0].book_state = 'rented'
                        return http.request.render('library.confirmation', {})