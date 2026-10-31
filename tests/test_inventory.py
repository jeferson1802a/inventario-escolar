import csv
import io
import unittest
from decimal import Decimal

import mongomock

from inventory import (ConflictError, DemoRepository, MongoRepository, export_csv,
                       sample_products, select_products, status, validate_product)


class ValidationTests(unittest.TestCase):
    def test_sample_has_30_unique_valid_products(self):
        products = sample_products()
        self.assertEqual(len(products), 30)
        self.assertEqual(len({p["codigo"] for p in products}), 30)
        self.assertEqual({status(p) for p in products}, {"Agotado", "Stock bajo", "Disponible"})

    def test_normalization_and_exact_money(self):
        p = validate_product(" uti-031 ", " Lápiz ", "Escritura", "0.29", 1, 2)
        self.assertEqual(p["codigo"], "UTI-031")
        self.assertEqual(p["nombre"], "Lápiz")
        self.assertEqual(p["precio_centimos"], 29)

    def test_invalid_input(self):
        for price, stock in [("-1", 2), ("NaN", 2), ("Infinity", 2), ("1.005", 2), (1, -1), (1, 1.5)]:
            with self.subTest(price=price, stock=stock), self.assertRaises(ValueError):
                validate_product("UTI-031", "Lápiz", "Escritura", price, stock, 1)
        with self.assertRaises(ValueError):
            validate_product("$where", "Lápiz", "Escritura", 1, 2, 1)

    def test_filters_and_boundaries(self):
        products = sample_products()
        self.assertEqual(len(select_products(products, "uti-001")), 1)
        self.assertTrue(all(p["categoria"] == "Arte" for p in select_products(products, category="Arte")))
        self.assertEqual(len(select_products(products, state="Agotado")), 3)
        self.assertEqual(status(dict(stock=5, stock_minimo=5)), "Stock bajo")

    def test_csv_and_formula_escape(self):
        products = sample_products()
        rows = list(csv.DictReader(io.StringIO(export_csv(products).decode("utf-8-sig"))))
        self.assertEqual(len(rows), 30)
        self.assertEqual(Decimal(rows[0]["precio"]), Decimal("8.50"))
        products[0]["nombre"] = "=SUM(A1:A2)"
        self.assertIn("'=SUM(A1:A2)", export_csv(products).decode("utf-8-sig"))


class RepositoryContract:
    def test_crud_and_duplicate(self):
        p = sample_products()[0]
        self.repo.create(p)
        with self.assertRaises(ValueError):
            self.repo.create(p)
        saved = self.repo.list()[0]
        self.assertEqual(saved["version"], 1)
        self.repo.update(p["codigo"], {**p, "stock": 99}, saved["version"])
        self.assertEqual(self.repo.list()[0]["stock"], 99)
        with self.assertRaises(ConflictError):
            self.repo.update(p["codigo"], p, 1)
        with self.assertRaises(ConflictError):
            self.repo.delete(p["codigo"], 1)
        self.repo.delete(p["codigo"], 2)
        self.assertEqual(self.repo.list(), [])

    def test_code_is_immutable(self):
        p = sample_products()[0]
        self.repo.create(p)
        with self.assertRaises(ValueError):
            self.repo.update(p["codigo"], {**p, "codigo": "UTI-099"}, 1)


class DemoTests(RepositoryContract, unittest.TestCase):
    def setUp(self):
        self.repo = DemoRepository({})

    def test_seed_preserves_existing_edits(self):
        products = sample_products()
        self.assertEqual(self.repo.seed(products), 30)
        p = self.repo.list()[0]
        self.repo.update(p["codigo"], {**products[0], "stock": 7}, p["version"])
        self.assertEqual(self.repo.seed(products), 0)
        self.assertEqual(self.repo.list()[0]["stock"], 7)


class MongoMockTests(RepositoryContract, unittest.TestCase):
    """Contrato Mongo simulado: estas pruebas no validan una conexión a Atlas."""
    def setUp(self):
        self.repo = MongoRepository(mongomock.MongoClient().test.productos)
        self.repo.ensure_indexes()


if __name__ == "__main__":
    unittest.main()
