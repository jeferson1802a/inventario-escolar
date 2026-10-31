"""Prueba CRUD real aislada; no toca la colección productos.

Ejecutar desde la raíz: python -m scripts.test_atlas
Lee secretos locales o MONGODB_URI / MONGODB_DATABASE del entorno.
"""
import os
import tomllib
import uuid
from pathlib import Path

from pymongo import MongoClient

from inventory import MongoRepository, sample_products


def main():
    secrets_file = Path(".streamlit/secrets.toml")
    secrets = tomllib.loads(secrets_file.read_text(encoding="utf-8")) if secrets_file.exists() else {}
    uri = os.environ.get("MONGODB_URI") or secrets.get("MONGODB_URI")
    if not uri:
        raise SystemExit("PENDIENTE: configura MONGODB_URI en .streamlit/secrets.toml o en el entorno.")
    database = os.environ.get("MONGODB_DATABASE") or secrets.get("MONGODB_DATABASE", "inventario_escolar")
    with MongoClient(uri, serverSelectionTimeoutMS=10000, socketTimeoutMS=10000) as client:
        client.admin.command("ping")
        collection = client[database]["prueba_crud_" + uuid.uuid4().hex]
        repo = MongoRepository(collection)
        try:
            repo.ensure_indexes()
            p = sample_products()[0]
            repo.create(p)
            assert repo.list()[0]["codigo"] == p["codigo"]
            print("PASS registro y consulta")
            repo.update(p["codigo"], {**p, "stock": 99}, 1)
            assert repo.list()[0]["stock"] == 99
            print("PASS actualización")
            repo.delete(p["codigo"], 2)
            assert not repo.list()
            print("PASS eliminación")
            assert repo.seed(sample_products()) == 30
            assert repo.seed(sample_products()) == 0
            print("PASS carga inicial sin duplicados")
        finally:
            # Solamente se elimina la colección temporal creada por esta ejecución.
            collection.drop()
    print("PASS integración CRUD real con Atlas")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # No imprimir excepciones que puedan contener la URI o la contraseña.
        raise SystemExit("FALLO: revisa conexión, usuario, permisos y acceso de red en Atlas. Credenciales ocultas.")
