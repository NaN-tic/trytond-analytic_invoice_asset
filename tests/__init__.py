# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.analytic_invoice_asset.tests.test_analytic_invoice_asset import suite
except ImportError:
    from .test_analytic_invoice_asset import suite

__all__ = ['suite']
