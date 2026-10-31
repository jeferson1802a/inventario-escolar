"""Empaqueta solo archivos públicos explícitamente autorizados, nunca secretos."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ".gitignore", "README.md", "app.py", "inventory.py", "requirements.txt",
    "requirements-dev.txt", "INICIAR_APP.bat", ".streamlit/config.toml",
    ".streamlit/secrets.toml.example", "data/productos.csv", ".github/workflows/tests.yml",
    "docs/GUIA_PASO_A_PASO.md", "docs/INFORME.md", "docs/Informe_Inventario_Escolar.docx",
    "docs/PLAN_DE_PRUEBAS.md", "docs/RESULTADOS_LOCALES.md", "docs/capturas/README.md",
    "tests/test_app.py", "tests/test_inventory.py", "scripts/test_atlas.py",
    "scripts/build_report.py", "scripts/package_project.py",
    "docs/ESTADO_PUBLICACION.md",
    "docs/capturas/01_cluster.jpg", "docs/capturas/02_coleccion.jpg",
    "docs/capturas/03_consulta_atlas.jpg", "docs/capturas/04_registro.jpg",
    "docs/capturas/05_documento_atlas.jpg", "docs/capturas/06_eliminacion.jpg",
]


def main():
    output = ROOT / "Inventario_Escolar_Entrega.zip"
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for filename in FILES:
            archive.write(ROOT / filename, filename)
    print(f"{output} ({len(FILES)} archivos públicos)")


if __name__ == "__main__":
    main()
