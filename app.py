"""Interfaz Streamlit. Ejecutar con: streamlit run app.py."""

import hmac
import os

import streamlit as st
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from streamlit.errors import StreamlitSecretNotFoundError

from inventory import (CATEGORIES, DemoRepository, MongoRepository, export_csv,
                       public_rows, sample_products, select_products, status, validate_product)

st.set_page_config(page_title="Inventario Escolar", page_icon="📦", layout="wide")


def setting(name, default=""):
    value = os.environ.get(name)
    if value is not None:
        return value
    try:
        return str(st.secrets.get(name, default))
    except StreamlitSecretNotFoundError:
        return default


@st.cache_resource
def connect(uri, database):
    client = MongoClient(uri, serverSelectionTimeoutMS=8000, connectTimeoutMS=8000,
                         socketTimeoutMS=10000, tz_aware=True, appname="InventarioEscolar")
    try:
        client.admin.command("ping")
        repository = MongoRepository(client[database]["productos"])
        repository.ensure_indexes()
    except Exception:
        client.close()
        raise
    return repository


def notify(message):
    st.session_state.pop("edit_snapshot", None)
    st.session_state.pop("delete_snapshot", None)
    st.session_state["notice"] = message
    st.rerun()


def run():
    st.title("📦 Inventario Escolar")
    st.caption("Control de productos y existencias · Tienda de útiles escolares · Precios en soles")
    uri = setting("MONGODB_URI")
    demo = not bool(uri)
    if demo:
        st.warning("MODO DEMOSTRACIÓN · Datos temporales de esta sesión. No hay conexión a MongoDB Atlas.")
        if "demo_products" not in st.session_state:
            st.session_state.demo_products = {}
            DemoRepository(st.session_state.demo_products).seed(sample_products())
        repo = DemoRepository(st.session_state.demo_products)
    else:
        try:
            repo = connect(uri, setting("MONGODB_DATABASE", "inventario_escolar"))
        except (PyMongoError, ValueError):
            st.error("No se pudo conectar a MongoDB Atlas. Revisa la URI, el usuario y el acceso de red en la configuración privada.")
            st.stop()
        st.success("Conectado a MongoDB Atlas · Los cambios se guardan en la nube.")

    with st.sidebar:
        st.header("Panel de acceso")
        if demo:
            can_write = True
            st.info("Puedes probar el CRUD en esta sesión de demostración.")
        else:
            password = setting("ADMIN_PASSWORD")
            if not password:
                st.info("Consulta pública. Configura ADMIN_PASSWORD para habilitar la administración.")
            if st.session_state.get("admin"):
                if st.button("Cerrar sesión", width="stretch"):
                    st.session_state.admin = False
                    st.rerun()
            elif password:
                with st.form("login", clear_on_submit=True):
                    provided = st.text_input("Clave de administrador", type="password")
                    login = st.form_submit_button("Ingresar", width="stretch")
                if login:
                    if hmac.compare_digest(provided.encode(), password.encode()):
                        st.session_state.admin = True
                        st.rerun()
                    else:
                        st.error("Clave incorrecta.")
            can_write = bool(password) and st.session_state.get("admin", False)
            st.caption("Administrador" if can_write else "Visitante · Solo consulta")
        st.divider()
        if st.button("Actualizar datos", width="stretch"):
            st.session_state.pop("edit_snapshot", None)
            st.session_state.pop("delete_snapshot", None)
            st.rerun()
        if can_write:
            with st.expander("Cargar productos de ejemplo"):
                st.caption("Agrega los códigos faltantes de la muestra. Conserva los productos ya existentes.")
                if st.button("Cargar los 30 productos"):
                    count = repo.seed(sample_products())
                    notify(f"Se agregaron {count} productos. Los existentes se conservaron.")
        st.caption("Proyecto académico · Datos sintéticos · Sin información personal")

    if "notice" in st.session_state:
        st.success(st.session_state.pop("notice"))
    products = repo.list()
    metrics = st.columns(4)
    metrics[0].metric("Productos", len(products))
    metrics[1].metric("Unidades en stock", sum(p["stock"] for p in products))
    metrics[2].metric("Stock bajo o agotado", sum(status(p) != "Disponible" for p in products))
    value = sum(p["stock"] * p["precio_centimos"] for p in products) / 100
    metrics[3].metric("Valor a precio de venta", f"S/ {value:,.2f}")
    st.caption("El valor del inventario se calcula con el precio de venta; no representa costo ni utilidad.")

    browse, create, edit, remove = st.tabs(["Consultar inventario", "Registrar producto", "Actualizar producto", "Eliminar producto"])
    with browse:
        a, b, c = st.columns([2, 1, 1])
        query = a.text_input("Buscar por código o nombre", placeholder="Ej. UTI-001 o cuaderno")
        category = b.selectbox("Categoría", ["Todas", *CATEGORIES])
        state = c.selectbox("Estado", ["Todos", "Disponible", "Stock bajo", "Agotado"])
        filtered = select_products(products, query, category, state)
        st.caption(f"{len(filtered)} productos encontrados de {len(products)} registrados")
        if filtered:
            st.dataframe(public_rows(filtered), hide_index=True, width="stretch",
                         column_config={"Precio (S/)": st.column_config.NumberColumn(format="S/ %.2f")})
        else:
            st.info("No hay productos para los filtros seleccionados.")
        st.download_button("Descargar resultados CSV", export_csv(filtered), "inventario.csv", "text/csv")
        st.download_button("Descargar muestra original", export_csv(sample_products()), "productos.csv", "text/csv")
        with st.expander("Stock por categoría"):
            totals = {cat: sum(p["stock"] for p in products if p["categoria"] == cat) for cat in CATEGORIES}
            st.bar_chart(totals, horizontal=True)

    with create:
        if not can_write:
            st.info("Ingresa como administrador desde el panel lateral para registrar productos.")
        else:
            with st.form("create", clear_on_submit=True):
                code = st.text_input("Código único", max_chars=20, placeholder="UTI-031")
                name = st.text_input("Nombre del producto", max_chars=100)
                cat = st.selectbox("Categoría del producto", CATEGORIES)
                price = st.number_input("Precio de venta (S/)", 0.0, 1_000_000.0, step=0.50)
                stock = st.number_input("Stock inicial", 0, 1_000_000, step=1)
                minimum = st.number_input("Stock mínimo", 0, 1_000_000, value=5, step=1)
                submitted = st.form_submit_button("Registrar producto", type="primary")
            if submitted:
                p = validate_product(code, name, cat, price, stock, minimum)
                repo.create(p)
                notify(f'Producto {p["codigo"]} registrado correctamente.')

    with edit:
        if not can_write:
            st.info("Ingresa como administrador para actualizar productos.")
        elif not products:
            st.info("Registra o carga productos primero.")
        else:
            by_code = {p["codigo"]: p for p in products}
            code = st.selectbox("Producto a actualizar", list(by_code),
                                format_func=lambda c: f'{c} · {by_code[c]["nombre"]}')
            snapshot = st.session_state.get("edit_snapshot")
            if snapshot is None or snapshot["codigo"] != code:
                st.session_state.edit_snapshot = dict(by_code[code])
            p = st.session_state.edit_snapshot
            # La versión queda vinculada al formulario visible y permite detectar ediciones simultáneas.
            key = f'edit_{code}_{p["version"]}'
            with st.form(key):
                st.caption(f'Código fijo: {code}')
                name = st.text_input("Nombre", p["nombre"], max_chars=100)
                cat = st.selectbox("Categoría nueva", CATEGORIES, index=CATEGORIES.index(p["categoria"]))
                price = st.number_input("Precio nuevo (S/)", 0.0, 1_000_000.0, value=p["precio_centimos"] / 100, step=0.50)
                stock = st.number_input("Stock actual", 0, 1_000_000, value=p["stock"], step=1)
                minimum = st.number_input("Mínimo requerido", 0, 1_000_000, value=p["stock_minimo"], step=1)
                submitted = st.form_submit_button("Guardar cambios", type="primary")
            if submitted:
                updated = validate_product(code, name, cat, price, stock, minimum)
                repo.update(code, updated, p["version"])
                notify(f"Producto {code} actualizado correctamente.")

    with remove:
        if not can_write:
            st.info("Ingresa como administrador para eliminar productos.")
        elif not products:
            st.info("No hay productos para eliminar.")
        else:
            by_code = {p["codigo"]: p for p in products}
            code = st.selectbox("Producto a eliminar", list(by_code),
                                format_func=lambda c: f'{c} · {by_code[c]["nombre"]}')
            snapshot = st.session_state.get("delete_snapshot")
            if snapshot is None or snapshot["codigo"] != code:
                st.session_state.delete_snapshot = dict(by_code[code])
            p = st.session_state.delete_snapshot
            with st.form(f'delete_{code}_{p["version"]}'):
                st.warning(f'Se eliminará {code}: {p["nombre"]}. Esta acción no se puede deshacer.')
                confirmation = st.text_input("Escribe el código del producto para confirmar")
                submitted = st.form_submit_button("Eliminar definitivamente")
            if submitted:
                if confirmation.strip() != code:
                    st.error("El código de confirmación no coincide.")
                else:
                    repo.delete(code, p["version"])
                    notify(f"Producto {code} eliminado correctamente.")


try:
    run()
except ValueError as exc:
    st.error(str(exc))
except PyMongoError:
    st.error("No se pudo completar la operación en MongoDB. Revisa la conexión y actualiza los datos antes de reintentar.")
