"""
Tests de estadisticas-service — lógica pura sin BD.
Correr: python3 -m pytest tests/test_estadisticas.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# --- Test 1: Endpoint /livez ---
def test_livez_estructura():
    """El endpoint /livez debe retornar status alive."""
    from app.main import livez
    resp = livez()
    assert "status" in resp
    assert resp["status"] == "alive"


# --- Test 2: Imports correctos ---
def test_imports_basicos():
    """Verifica que los módulos principales se importan sin error."""
    from app import main
    from app import auth
    assert hasattr(main, 'app')
    assert hasattr(auth, 'usuario_actual')


# --- Test 3: App tiene rutas esperadas ---
def test_app_tiene_rutas():
    """La app FastAPI debe tener las rutas registradas."""
    from app.main import app
    rutas = [r.path for r in app.routes]
    assert "/livez" in rutas
    assert "/readyz" in rutas
    assert "/api/estadisticas/mias" in rutas
    assert "/api/estadisticas/globales" in rutas


# --- Test 4: Rutas son GET ---
def test_rutas_son_get():
    """Las rutas principales deben ser GET."""
    from app.main import app
    for route in app.routes:
        if hasattr(route, 'methods') and route.path in ["/livez", "/readyz"]:
            assert "GET" in route.methods


# --- Test 5: Función ping existe en db ---
def test_ping_existe():
    """El módulo db debe tener la función ping."""
    from app import db
    assert hasattr(db, 'ping')
    assert callable(db.ping)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallos = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except AssertionError as e:
            fallos += 1
            print(f"FAIL  {fn.__name__}: {e}")
    print(f"\n{len(fns) - fallos}/{len(fns)} tests OK")
    sys.exit(1 if fallos else 0)
