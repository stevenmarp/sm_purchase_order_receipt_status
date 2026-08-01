# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import float_compare


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sm_receipt_status = fields.Selection(
        selection=[
            ('waiting', 'Waiting'),
            ('input_stock', 'Input Stock'),
            ('quality_stock', 'Quality Stock'),
            ('partial', 'Partially Received'),
            ('overdue', 'Overdue'),
            ('full', 'Fully Received'),
        ],
        string='Detailed Receipt Status',
        compute='_compute_sm_receipt_status',
        search='_search_sm_receipt_status')

    def _get_receipt_pickings(self):
        """Receipt pickings plus the chained internal transfers (2/3-step)."""
        pickings = self.picking_ids
        extra = pickings.move_ids.move_dest_ids.picking_id - pickings
        while extra:
            pickings |= extra
            extra = pickings.move_ids.move_dest_ids.picking_id - pickings
        return pickings

    def _get_pending_internal_pickings(self):
        return self._get_receipt_pickings().filtered(
            lambda p: p.picking_type_id.code == 'internal'
            and p.state not in ('done', 'cancel'))

    @api.depends('state', 'date_planned', 'order_line.qty_received',
                 'order_line.product_qty', 'picking_ids.state')
    def _compute_sm_receipt_status(self):
        today = fields.Date.context_today(self)
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for order in self:
            order_sudo = order.sudo()
            lines = order_sudo.order_line.filtered(
                lambda l: not l.display_type
                and l.product_id.type == 'consu')
            if order_sudo.state not in ('purchase', 'done') or not lines:
                order.sm_receipt_status = False
                continue
            received_full = all(
                float_compare(line.qty_received, line.product_qty,
                              precision_digits=precision) >= 0
                for line in lines)
            pending_internal = order_sudo._get_pending_internal_pickings()
            if pending_internal:
                warehouses = pending_internal.picking_type_id.warehouse_id
                qc_locations = warehouses.wh_qc_stock_loc_id
                input_locations = warehouses.wh_input_stock_loc_id
                if any(p.location_id in input_locations
                       for p in pending_internal):
                    order.sm_receipt_status = 'input_stock'
                elif any(p.location_id in qc_locations
                         for p in pending_internal):
                    order.sm_receipt_status = 'quality_stock'
                else:
                    order.sm_receipt_status = 'input_stock'
            elif received_full:
                order.sm_receipt_status = 'full'
            elif order_sudo.date_planned and order_sudo.date_planned.date() < today:
                order.sm_receipt_status = 'overdue'
            elif any(line.qty_received for line in lines):
                order.sm_receipt_status = 'partial'
            else:
                order.sm_receipt_status = 'waiting'

    def _search_sm_receipt_status(self, operator, value):
        if operator == '=':
            operator, value = 'in', [value]
        if operator != 'in':
            return NotImplemented
        # ponytail: computes status of every confirmed order; add SQL if
        # purchase volume makes the filter slow
        orders = self.search([('state', 'in', ('purchase', 'done'))])
        return [('id', 'in', orders.filtered(
            lambda o: o.sm_receipt_status in value).ids)]

    def action_view_internal_pickings(self):
        return self._get_action_view_picking(
            self._get_pending_internal_pickings())
