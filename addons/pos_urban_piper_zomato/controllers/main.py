from odoo.addons.pos_urban_piper.controllers.main import PosUrbanPiperController
from odoo.http import request


class PosZomatoController(PosUrbanPiperController):

    def _get_tax_value(self, taxes_data, pos_config):
        taxes = super()._get_tax_value(taxes_data, pos_config)
        if request.env.ref('pos_urban_piper_zomato.pos_delivery_provider_zomato', False) in pos_config.urbanpiper_delivery_provider_ids and taxes:
            parent_tax = request.env['account.tax'].sudo().search([('children_tax_ids', 'in', taxes.ids)])
            if parent_tax:
                taxes = parent_tax
        return taxes

    def _tax_amount_to_remove(self, lines, pos_config):
        if pos_config.company_id.country_id.code != 'IN':
            return super()._tax_amount_to_remove(lines, pos_config)
        tax_amt_to_remove = 0
        for line in lines:
            if line.get('taxes', [{}])[0].get('rate') == 2.5:
                tax_amt_to_remove += float(line.get('total_with_tax', 0.0)) - float(line.get('price', 0.0))
        return tax_amt_to_remove
