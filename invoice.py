# The COPYRIGHT file at the top level of  this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @fields.depends('invoice_asset', 'analytic_accounts')
    def on_change_invoice_asset(self):
        pool = Pool()
        Entry = pool.get('analytic.account.entry')
        if self.invoice_asset:
            entries = []
            for entry in self.invoice_asset.analytic_accounts:
                new_entry = Entry(root=entry.root, account=entry.account)
                entries.append(new_entry)
            self.analytic_accounts = entries
