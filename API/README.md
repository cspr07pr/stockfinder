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
| **Charles Schwab** (bróker + market data) | `SCHWAB_APP_KEY` / `SCHWAB_APP_SECRET` / `SCHWAB_CALLBACK_URL` | developer.schwab.com |
| **Robinhood** (opcional) | `ROBINHOOD_USERNAME` / `ROBINHOOD_PASSWORD` / `ROBINHOOD_MFA_TOKEN` | Login de tu cuenta (no es API pública oficial) |

### Charles Schwab — OAuth 2.0 (no es una simple API key)

Schwab requiere un flujo OAuth, no solo pegar una clave:

1. En **developer.schwab.com** crea una app y activa los productos
   **"Market Data Production"** y **"Accounts and Trading"**.
2. Copia el **App Key** (client ID) y el **App Secret** a `API/.env`
   (`SCHWAB_APP_KEY`, `SCHWAB_APP_SECRET`).
3. Configura la **Callback URL** de la app igual a `SCHWAB_CALLBACK_URL`
   (por defecto `https://127.0.0.1`).
4. La primera vez, autorizas en el navegador y se generan los **tokens**
   (access ~30 min + refresh ~7 días). Se guardan en `API/schwab_token.json`,
   que **git ignora**. Cuando el refresh token caduque, hay que reautorizar.

> El App Secret y el archivo de tokens son tan sensibles como una contraseña:
> nunca al repo ni al chat.

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
| `schwab_token.json` | ❌ No | Tokens OAuth de Schwab (se generan al autorizar) |
