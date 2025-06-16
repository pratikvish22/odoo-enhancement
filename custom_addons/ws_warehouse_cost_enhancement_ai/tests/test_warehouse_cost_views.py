# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged("ws_warehouse_cost_enhancement_ai")
class TestWarehouseCostViews(TransactionCase):
    """Test the presence of warehouse_cost field in sale.order and stock.picking views."""

    def test_sale_order_view_has_warehouse_cost(self):
        view = self.env.ref(
            "ws_warehouse_cost_enhancement_ai.view_order_form_warehouse_cost",
            raise_if_not_found=False,
        )
        self.assertTrue(view, "Custom sale.order form view not found")
        self.assertIn(
            "warehouse_cost",
            view.arch_db,
            "'warehouse_cost' field not found in sale.order form view",
        )
        self.assertIn(
            'widget="monetary"',
            view.arch_db,
            "'warehouse_cost' field does not have the correct widget in sale.order view",
        )

    def test_stock_picking_view_has_warehouse_cost(self):
        view = self.env.ref(
            "ws_warehouse_cost_enhancement_ai.view_picking_form_warehouse_cost",
            raise_if_not_found=False,
        )
        self.assertTrue(view, "Custom stock.picking form view not found")
        self.assertIn(
            "warehouse_cost",
            view.arch_db,
            "'warehouse_cost' field not found in stock.picking form view",
        )
