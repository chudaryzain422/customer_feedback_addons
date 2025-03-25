from odoo import models, fields, api

class MrpBomLaborFoh(models.Model):
    _name = 'mrp.bom.labor.foh'
    _description = 'BOM Labor and FOH Components'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Material', required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', 
        string='Product',
        required=True,
        domain=[('type', '=', 'consu')],  # Only consumable products
    )
    product_qty = fields.Float(
        'Quantity',
        default=1.0,
        required=True,
    )
    cost = fields.Float(
        related='product_id.standard_price',
        string='Cost',
        readonly=True,
        store=True,
    )