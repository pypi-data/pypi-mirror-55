# Copyright (C) 2019 Konos
# Copyright (C) 2019 Blanco Martín & Asociados
# Copyright (C) 2019 CubicERP
# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SiiReference(models.Model):
    _inherit = "sii.reference"

    invoice_id = fields.Many2one("account.invoice", string="Invoice",
                                 ondelete="cascade", index=True, copy=False)
