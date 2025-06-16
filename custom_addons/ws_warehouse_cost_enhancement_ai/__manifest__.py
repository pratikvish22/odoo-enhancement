{
    "name": "Warehouse Cost Enhancement AI",
    "version": "15.0.1.0.0",
    "summary": "Show and sync warehouse cost in Sale and Delivery Orders",
    "category": "Sales",
    "author": "Your Company",
    "website": "",
    "depends": ["sale_management", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
