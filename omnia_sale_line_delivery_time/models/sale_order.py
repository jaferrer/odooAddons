# -*- encoding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Open Source Management Solution    
#    Copyright (C) 2010-2011 OmniaSolutions (<http://www.omniasolutions.eu>). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


'''
Created on Jul 21, 2017

@author: daniel
'''
import datetime
from datetime import timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('customer_lead')
    def _get_default_product_datetime_value(self):
        for sale_order_line in self:
            if sale_order_line.product_id:
                order_date = datetime.datetime.strptime(
                    sale_order_line.order_id.date_order,
                    DEFAULT_SERVER_DATETIME_FORMAT)
                new_date = order_date + timedelta(
                    days=sale_order_line.customer_lead)
                sale_order_line.product_delivery_date = new_date.strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT)

    @api.onchange('customer_lead')
    def changed_customer_lead(self):
        for sale_order_line in self:
            sale_order_line._get_default_product_datetime_value()

    product_delivery_date = fields.Datetime(
        string=_('Delivery Date'),
        compute='_get_default_product_datetime_value')