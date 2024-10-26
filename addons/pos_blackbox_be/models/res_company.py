# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model_create_multi
    def create(self, vals_list):
        existing_pos_configs_with_blackbox = self.env['pos.config'].search(['|', ('iface_fiscal_data_module', '!=', False), ('certified_blackbox_identifier', '!=', False)])
        if len(existing_pos_configs_with_blackbox):
            raise UserError(_('The multi-company feature cannot be use with certified PoS config.'))
        return super().create(vals_list)
