"""
fix_patch.py — Ejecuta este script en la raíz de tu proyecto
para corregir el VarTypeError en frontend.py automáticamente.

Uso:
    python fix_patch.py
"""

import re, sys, shutil
from pathlib import Path

# ── Localiza el archivo ─────────────────────────────────────────────────────
TARGET = Path(
    r"C:\Users\elp48\OneDrive\Escritorio\PWcine\cine-reservas-app"
    r"\frontend\frontend\frontend.py"
)

if not TARGET.exists():
    # Intenta encontrarlo relativamente si el script está en el proyecto
    matches = list(Path(".").rglob("frontend.py"))
    if not matches:
        sys.exit("❌  No se encontró frontend.py. "
                 "Edita la variable TARGET en este script con la ruta correcta.")
    TARGET = matches[0]

print(f"📄  Archivo: {TARGET}")

# ── Backup ──────────────────────────────────────────────────────────────────
backup = TARGET.with_suffix(".py.bak")
shutil.copy2(TARGET, backup)
print(f"💾  Backup guardado en: {backup}")

src = TARGET.read_text(encoding="utf-8")
original = src  # conservar para comparar

# ── FIX 1: reemplaza la f-string rota por State.boletos_label ──────────────
BROKEN = (
    r"f\"\{State\.num_asientos\} boleto\{'s' if State\.num_asientos != 1 else ''\}"
    r" · RD\$\{State\.total_boletos\}\","
)
FIXED_LINE = "State.boletos_label,"

src, n1 = re.subn(BROKEN, FIXED_LINE, src)
if n1:
    print(f"✅  FIX 1 aplicado ({n1} ocurrencia/s): f-string rota → State.boletos_label")
else:
    print("ℹ️   FIX 1: la línea rota ya no está (quizás ya fue corregida).")

# ── FIX 2: inyecta el @rx.var boletos_label en la clase State ──────────────
LABEL_VAR = '''
    @rx.var
    def boletos_label(self) -> str:
        count = len(self.selected_seats)
        suffix = "s" if count != 1 else ""
        return f"{count} boleto{suffix} · RD${self.total_boletos}"
'''

# Solo lo agrega si todavía no existe
if "def boletos_label" not in src:
    # Inserta justo después de can_proceed
    anchor = "    @rx.var\n    def can_proceed(self) -> bool:\n        return len(self.selected_seats) > 0"
    if anchor in src:
        src = src.replace(anchor, anchor + LABEL_VAR, 1)
        print("✅  FIX 2 aplicado: @rx.var boletos_label agregado a State.")
    else:
        print("⚠️   FIX 2: no se encontró el ancla 'can_proceed'. "
              "Agrega boletos_label manualmente (ver instrucciones en README).")
else:
    print("ℹ️   FIX 2: boletos_label ya existe en State.")

# ── Escribe el archivo corregido ────────────────────────────────────────────
if src != original:
    TARGET.write_text(src, encoding="utf-8")
    print("\n🎉  Archivo guardado. Vuelve a ejecutar: reflex run")
else:
    print("\nℹ️   No se realizaron cambios (el archivo ya estaba corregido).")
