import os
import unittest
from pathlib import Path
from unittest.mock import patch

import mongomock
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")

class AppTests(unittest.TestCase):
    def run_app(self):
        with patch.dict(os.environ, {"MONGODB_URI": "", "ADMIN_PASSWORD": ""}):
            return AppTest.from_file(APP, default_timeout=30).run()

    def test_demo_renders_and_searches(self):
        at = self.run_app()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "30")
        search = next(x for x in at.text_input if x.label == "Buscar por código o nombre")
        search.set_value("UTI-001").run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.dataframe[0].value), 1)

    def test_demo_create_update_delete(self):
        at = self.run_app()
        next(x for x in at.text_input if x.label == "Código único").set_value("UTI-031")
        next(x for x in at.text_input if x.label == "Nombre del producto").set_value("Producto de prueba")
        next(x for x in at.button if x.label == "Registrar producto").click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "31")
        next(x for x in at.selectbox if x.label == "Producto a actualizar").select("UTI-031").run()
        next(x for x in at.number_input if x.label == "Stock actual").set_value(42)
        next(x for x in at.button if x.label == "Guardar cambios").click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.session_state.demo_products["UTI-031"]["stock"], 42)
        next(x for x in at.selectbox if x.label == "Producto a eliminar").select("UTI-031").run()
        next(x for x in at.text_input if x.label == "Escribe el código del producto para confirmar").set_value("UTI-031")
        next(x for x in at.button if x.label == "Eliminar definitivamente").click().run()
        self.assertFalse(at.exception)
        self.assertEqual(at.metric[0].value, "30")

    def test_atlas_mode_requires_admin_for_writes(self):
        # Mongo simulado: comprueba la interfaz y autorización, no una conexión real.
        client = mongomock.MongoClient()
        with patch.dict(os.environ, {"MONGODB_URI": "mongodb://mock-auth", "ADMIN_PASSWORD": "clave-prueba"}), patch("pymongo.MongoClient", return_value=client):
            at = AppTest.from_file(APP, default_timeout=30).run()
            self.assertFalse(at.exception)
            self.assertFalse(any(x.label == "Código único" for x in at.text_input))
            next(x for x in at.text_input if x.label == "Clave de administrador").set_value("incorrecta")
            next(x for x in at.button if x.label == "Ingresar").click().run()
            self.assertFalse(any(x.label == "Código único" for x in at.text_input))
            next(x for x in at.text_input if x.label == "Clave de administrador").set_value("clave-prueba")
            next(x for x in at.button if x.label == "Ingresar").click().run()
            self.assertTrue(any(x.label == "Código único" for x in at.text_input))
            next(x for x in at.button if x.label == "Cerrar sesión").click().run()
            self.assertFalse(any(x.label == "Código único" for x in at.text_input))


if __name__ == "__main__":
    unittest.main()
