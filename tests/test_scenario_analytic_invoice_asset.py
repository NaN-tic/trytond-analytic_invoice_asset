import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import create_chart, create_fiscalyear
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install account_invoice
        activate_modules('analytic_invoice_asset')

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)

        # Create analytic accounts
        AnalyticAccount = Model.get('analytic_account.account')
        root = AnalyticAccount(type='root', name='Root')
        root.save()
        analytic_account = AnalyticAccount(root=root,
                                           parent=root,
                                           name='Analytic')
        analytic_account.save()
        mandatory_root = AnalyticAccount(type='root', name='Root')
        mandatory_root.save()
        mandatory_analytic_account = AnalyticAccount(root=mandatory_root,
                                                     parent=mandatory_root,
                                                     name='Mandatory Analytic')
        mandatory_analytic_account.save()

        # Create party
        Party = Model.get('party.party')
        party = Party(name='Party')
        party.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        product = Product()
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'service'
        template.list_price = Decimal('40')
        template.cost_price = Decimal('25')
        template.save()
        product.template = template
        product.save()

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create an asset
        Asset = Model.get('asset')
        asset = Asset()
        asset.name = 'Asset'
        entry, mandatory_entry = asset.analytic_accounts
        entry.root = root
        entry.account = analytic_account
        mandatory_entry.root = mandatory_root
        mandatory_entry.account = mandatory_analytic_account
        asset.save()

        # Create invoice with analytic accounts
        Invoice = Model.get('account.invoice')
        invoice = Invoice()
        invoice.party = party
        invoice.payment_term = payment_term
        line = invoice.lines.new()
        line.invoice_asset = asset
        entry, mandatory_entry = line.analytic_accounts
        self.assertEqual(entry.root, root)
        self.assertEqual(entry.account, analytic_account)
        self.assertEqual(mandatory_entry.root, mandatory_root)
        self.assertEqual(mandatory_entry.account, mandatory_analytic_account)
