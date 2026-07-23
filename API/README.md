# API — Integraciones de datos

Claves y configuración de las fuentes de mercado. **Las claves nunca se suben al
repositorio** (las bloquea `../.gitignore`).

---

## Cómo pasar tus claves (paso a paso)

1. Copia la plantilla a un archivo real:
   ```
   # desde la carpeta API/
   cp .env.example .env        # PowerShell: Copy-Item .env.example .env
   ```
2. Abre `API/.env` y rellena cada valor con tu clave.
3. Listo. Git **ignora** `API/.env` automáticamente, así que nunca se sube.

> Verifica que está ignorado: `git status` **no** debe mostrar `API/.env`.
> Comprobar con: `git check-ignore API/.env` (debe imprimir la ruta).

---

## Fuentes y dónde obtener la clave

| Servicio | Variable(s) | Dónde |
|---|---|---|
| **FMP** (fundamentales, precios, múltiplos) | `FMP_API_KEY` | site.financialmodelingprep.com/developer/docs |
| **Finnhub** (perfil, estimados, insiders) | `FINNHUB_API_KEY` | finnhub.io/dashboard |
| **FRED** (macro: tasas, inflación) | `FRED_API_KEY` | fredaccount.stlouisfed.org/apikeys |
| **Robinhood** (precios, cuenta) | `ROBINHOOD_USERNAME` / `ROBINHOOD_PASSWORD` / `ROBINHOOD_MFA_TOKEN` | Login de tu cuenta (no es API pública oficial) |

---

## Reglas de seguridad

- **Nunca** escribas claves en el chat, en `.env.example`, ni en ningún archivo
  versionado.
- Si una clave se filtra por error, **revócala y genera una nueva** en el panel
  del proveedor; no basta con borrarla del historial.
- El código lee las claves desde variables de entorno / `API/.env`, nunca
  hardcodeadas.
- Para Robinhood, preferir sesión/token sobre guardar la contraseña en claro
  cuando sea posible.

---

## Qué archivos hay aquí

| Archivo | ¿Se sube? | Contenido |
|---|---|---|
| `.env.example` | ✅ Sí | Plantilla con nombres de variables, sin valores |
| `.env` | ❌ No | Tus claves reales (lo crea cada quien en su equipo) |
