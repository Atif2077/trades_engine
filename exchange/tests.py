from django.test import TestCase
from exchange.models import Asset

class AssetTest(TestCase):
    def setUp(self):
        self.a1 = Asset.objects.create(tkr="AAPL", name="Apple Inc.", prc=150.00)

    def test_c(self):
        a2 = Asset.objects.create(tkr="GOOGL", name="Alphabet", prc=2800.00)
        self.assertEqual(Asset.objects.count(), 2)
        self.assertEqual(a2.tkr, "GOOGL")

    def test_r(self):
        a = Asset.objects.get(tkr="AAPL")
        self.assertEqual(a.name, "Apple Inc.")
        self.assertEqual(a.prc, 150.00)

    def test_u(self):
        a = Asset.objects.get(tkr="AAPL")
        a.prc = 155.00
        a.save()
        a_upd = Asset.objects.get(tkr="AAPL")
        self.assertEqual(a_upd.prc, 155.00)

    def test_d(self):
        a = Asset.objects.get(tkr="AAPL")
        a.delete()
        self.assertEqual(Asset.objects.count(), 0)