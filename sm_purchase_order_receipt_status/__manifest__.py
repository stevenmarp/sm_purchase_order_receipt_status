# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order Receipt Status',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Purchase',
    'summary': 'Track goods receipt progress on purchase orders: Waiting, Input Stock, Quality Stock, Partially Received, Overdue or Fully Received badge with filters and a direct link to the pending input or quality transfer, for 1, 2 and 3-step receiving in Odoo 19.',
    'description': """
Purchase Order Receipt Status for Odoo 19
==========================================

By default Odoo only shows a billing status on purchase orders. This
module tracks the physical receipt side across the whole receiving
flow, including multi-step (2-step and 3-step) reception warehouses.

Main Features
-------------

* Receipt status badge on the purchase order form and list view:

  - Waiting: order confirmed, nothing received yet
  - Input Stock: goods arrived, waiting to be moved into stock
    (2-step and 3-step receiving)
  - Quality Stock: goods waiting in quality control (3-step receiving)
  - Partially Received: part of the ordered quantities received
  - Overdue: expected date passed and order not fully received
  - Fully Received: all quantities received and processed

* Status updates automatically when receipts and internal transfers
  are validated, including backorders
* Input / Quality button on the purchase order opens the pending
  internal transfer directly
* Search filters by receipt status on the purchase order list
* Supports 1-step, 2-step and 3-step receiving configurations
* Works with Odoo Community and Enterprise

Search Keywords
---------------

Odoo purchase order receipt status, PO receiving status, goods receipt
tracking, input stock quality control status, multi step reception,
overdue receipt, Odoo 19 purchase receipt.
    """,
    'author': 'Steven Marp',
    'website': 'https://apps.odoo.com/apps/modules/browse?author=Steven Marp',
    'license': 'OPL-1',
    'price': 5.00,
    'currency': 'USD',
    'depends': [
        'purchase_stock',
    ],
    'data': [
        'security/ir_rule.xml',
        'views/purchase_order_views.xml',
    ],
    'images': [
        'static/description/banner.gif',
        'static/description/icon.png',
        'static/description/screenshot_input_stock.png',
        'static/description/screenshot_quality_stock.png',
        'static/description/screenshot_fully_received.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
