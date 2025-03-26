from odoo import models, api,fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    labor_foh_line_ids = fields.One2many(
        'mrp.bom.labor.foh',
        compute='_compute_labor_foh_lines',
        string="Labor and FOH Components"
    )

    @api.depends('bom_id')
    def _compute_labor_foh_lines(self):
        for record in self:
            record.labor_foh_line_ids = record.bom_id.labor_foh_line_ids

    # @api.model
    # def create(self, values):
    #     production = super().create(values)
    #     if production.bom_id:
    #         # Add Labor and FOH components to the manufacturing order
    #         for labor_foh in production.bom_id.labor_foh_line_ids:
    #             self.env['stock.move'].create({
    #                 'name': labor_foh.product_id.name,
    #                 'product_id': labor_foh.product_id.id,
    #                 'product_uom_qty': labor_foh.product_qty,
    #                 'product_uom': labor_foh.product_id.uom_id.id,
    #                 'location_id': production.location_src_id.id,
    #                 'location_dest_id': production.product_id.property_stock_production.id,
    #                 'raw_material_production_id': production.id,
    #                 'company_id': production.company_id.id,
    #             })
    #     return production


    def button_mark_done(self):
        """Create journal entries when the manufacturing order is fully completed."""
        res = super().button_mark_done()
        # Ensure journal entries are only created when the order is DONE
        if self.state == 'done':
            self._create_labor_foh_journal_entries()

        return res

    def _create_labor_foh_journal_entries(self):
        account_move = self.env['account.move']
        for record in self:
            move_lines = []
            for labor_foh in record.bom_id.labor_foh_line_ids:
                category = labor_foh.product_id.categ_id
                if not category.property_account_expense_categ_id or not category.property_stock_account_production_cost_id:
                    continue  # Skip if accounts are missing

                move_lines.append((0, 0, {
                    'account_id': category.property_account_expense_categ_id.id,
                    'credit': labor_foh.cost,
                    'debit': 0.0,
                    'name': f'Labor/FOH Expense: {labor_foh.product_id.name}',
                }))

                move_lines.append((0, 0, {
                    'account_id': category.property_stock_account_production_cost_id.id,
                    'debit': labor_foh.cost,
                    'credit': 0.0,
                    'name': f'Production Cost: {labor_foh.product_id.name}',
                }))

            if move_lines:
                entry = account_move.create({
                    'move_type': 'entry',
                    'ref': record.name +" - "+ record.product_id.name,
                    'date': fields.Date.today(),
                    'journal_id': category.property_stock_journal.id,
                    'line_ids': move_lines,
                })
                entry.action_post()
