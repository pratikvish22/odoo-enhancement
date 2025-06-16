import logging
from odoo import api, fields, models

_logger = logging.getLogger("--------Sale Order--------")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warehouse_cost = fields.Monetary(
        string="Warehouse Cost",
        compute="_compute_warehouse_cost",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "order_line.product_id",
        "order_line.product_uom_qty",
        "order_line.product_id.standard_price",
    )
    def _compute_warehouse_cost(self):
        for order in self:
            total_cost = 0.0
            for line in order.order_line:
                if line.product_id:
                    total_cost += line.product_id.standard_price * line.product_uom_qty
            order.warehouse_cost = total_cost
            _logger.debug(
                f"Computed warehouse cost for sale order ID {order.id}: {total_cost}"
            )
