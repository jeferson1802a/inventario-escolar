"""Reglas de negocio y repositorios de Inventario Escolar."""

import csv
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from pymongo import ASCENDING, UpdateOne
from pymongo.errors import DuplicateKeyError

CATEGORIES = ("Cuadernos", "Escritura", "Arte", "Papelería", "Accesorios", "Organización")
DATA_PATH = Path(__file__).parent / "data" / "productos.csv"


class ConflictError(ValueError):
    """El registro cambió o ya no existe."""


def validate_product(code, name, category, price, stock, minimum):
    code, name = str(code).strip().upper(), str(name).strip()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{2,19}", code):
        raise ValueError("El código debe tener de 3 a 20 letras, números o guiones.")
    if not 2 <= len(name) <= 100:
        raise ValueError("El nombre debe tener entre 2 y 100 caracteres.")
    if category not in CATEGORIES:
        raise ValueError("Selecciona una categoría válida.")
    try:
        amount = Decimal(str(price))
        if not amount.is_finite() or amount < 0 or amount > 1_000_000:
            raise ValueError("El precio debe estar entre 0 y 1 000 000 soles.")
        if amount != amount.quantize(Decimal("0.01")):
            raise ValueError("El precio debe tener como máximo dos decimales.")
    except InvalidOperation as exc:
        raise ValueError("Ingresa un precio válido.") from exc
    counts = []
    for value in (stock, minimum):
        try:
            n = Decimal(str(value))
            if not n.is_finite() or n != n.to_integral_value() or not 0 <= n <= 1_000_000:
                raise ValueError
            counts.append(int(n))
        except (ValueError, InvalidOperation) as exc:
            raise ValueError("El stock y el mínimo deben ser enteros entre 0 y 1 000 000.") from exc
    return dict(codigo=code, nombre=name, categoria=category,
                precio_centimos=int(amount * 100), stock=counts[0], stock_minimo=counts[1])


def sample_products():
    with DATA_PATH.open(encoding="utf-8-sig", newline="") as f:
        return [validate_product(r["codigo"], r["nombre"], r["categoria"],
                                 r["precio"], r["stock"], r["stock_minimo"])
                for r in csv.DictReader(f)]


def status(p):
    if p["stock"] == 0:
        return "Agotado"
    return "Stock bajo" if p["stock"] <= p["stock_minimo"] else "Disponible"


def select_products(products, query="", category="Todas", state="Todos"):
    query = query.strip().casefold()
    return [p for p in products
            if (not query or query in p["codigo"].casefold() or query in p["nombre"].casefold())
            and (category == "Todas" or p["categoria"] == category)
            and (state == "Todos" or status(p) == state)]


def public_rows(products):
    return [{"Código": p["codigo"], "Producto": p["nombre"], "Categoría": p["categoria"],
             "Precio (S/)": p["precio_centimos"] / 100, "Stock": p["stock"],
             "Stock mínimo": p["stock_minimo"], "Estado": status(p)} for p in products]


def export_csv(products):
    import io
    output = io.StringIO(newline="")
    fields = ["codigo", "nombre", "categoria", "precio", "stock", "stock_minimo"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for p in products:
        # Evita fórmulas al abrir texto de usuarios en una hoja de cálculo.
        def safe(text):
            return "'" + text if text.startswith(("=", "+", "-", "@", "\t", "\r")) else text
        writer.writerow(dict(codigo=p["codigo"], nombre=safe(p["nombre"]),
                             categoria=p["categoria"], precio=f'{p["precio_centimos"] / 100:.2f}',
                             stock=p["stock"], stock_minimo=p["stock_minimo"]))
    return output.getvalue().encode("utf-8-sig")


def stamp(product):
    now = datetime.now(timezone.utc)
    return {**product, "creado_en": now, "actualizado_en": now, "version": 1}


class DemoRepository:
    """Persistencia de una sesión, explícitamente sin conexión a Atlas."""
    def __init__(self, storage):
        self.storage = storage

    def list(self):
        return sorted((dict(p) for p in self.storage.values()), key=lambda p: p["codigo"])

    def create(self, product):
        if product["codigo"] in self.storage:
            raise ValueError("Ya existe un producto con ese código.")
        self.storage[product["codigo"]] = stamp(product)

    def update(self, code, product, version):
        current = self.storage.get(code)
        if not current or current["version"] != version:
            raise ConflictError("El producto cambió. Actualiza la página antes de continuar.")
        if product["codigo"] != code:
            raise ValueError("El código no se puede cambiar.")
        self.storage[code] = {**current, **product, "version": version + 1,
                              "actualizado_en": datetime.now(timezone.utc)}

    def delete(self, code, version):
        current = self.storage.get(code)
        if not current or current["version"] != version:
            raise ConflictError("El producto cambió o ya fue eliminado. Actualiza la página.")
        del self.storage[code]

    def seed(self, products):
        added = 0
        for p in products:
            if p["codigo"] not in self.storage:
                self.create(p)
                added += 1
        return added


class MongoRepository:
    def __init__(self, collection):
        self.collection = collection

    def ensure_indexes(self):
        self.collection.create_index([("codigo", ASCENDING)], unique=True, name="codigo_unico")

    def list(self):
        return list(self.collection.find({}, {"_id": 0}).sort("codigo", ASCENDING))

    def create(self, product):
        try:
            self.collection.insert_one(stamp(product))
        except DuplicateKeyError as exc:
            raise ValueError("Ya existe un producto con ese código.") from exc

    def update(self, code, product, version):
        if product["codigo"] != code:
            raise ValueError("El código no se puede cambiar.")
        result = self.collection.update_one(
            {"codigo": code, "version": version},
            {"$set": {**product, "actualizado_en": datetime.now(timezone.utc)},
             "$inc": {"version": 1}})
        if not result.matched_count:
            raise ConflictError("El producto cambió. Actualiza la página antes de continuar.")

    def delete(self, code, version):
        result = self.collection.delete_one({"codigo": code, "version": version})
        if not result.deleted_count:
            raise ConflictError("El producto cambió o ya fue eliminado. Actualiza la página.")

    def seed(self, products):
        # setOnInsert conserva las ediciones existentes al volver a cargar la muestra.
        operations = [UpdateOne({"codigo": p["codigo"]}, {"$setOnInsert": stamp(p)}, upsert=True)
                      for p in products]
        return self.collection.bulk_write(operations, ordered=False).upserted_count if operations else 0
