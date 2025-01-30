from odoo import models, fields, api
import random
import string

class DiscountVoucher(models.Model):
    _name = 'discount.voucher'
    _description = 'Discount Voucher'

    name = fields.Char(string='Voucher Code', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    pos_feedback_id = fields.Many2one('pos.feedback', string='POS Feedback')
    discount_percentage = fields.Float(string='Discount Percentage', default=10.0)
    expiry_date = fields.Date(string='Expiry Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('valid', 'Valid'),
        ('used', 'Used'),
        ('expired', 'Expired')
    ], default='draft')
    
    @api.model
    def create(self, vals):
        vals['name'] = self._generate_voucher_code()
        return super(DiscountVoucher, self).create(vals)
    
    def _generate_voucher_code(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(8))