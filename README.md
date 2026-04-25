# APsystems OpenAPI — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Custom integration for Home Assistant to monitor your APsystems solar installation 
via the official APsystems OpenAPI v2.

## Features

- ⚡ Real-time power: production, consumption, grid import/export
- 📅 Daily / monthly / yearly energy totals
- ♻️ Self-consumption rate calculation
- 🔄 Auto-refresh every 5 minutes
- 🏠 Native HA energy dashboard compatible

## Requirements

- APsystems EMA account with OpenAPI access
- App ID + App Secret (from apsystemsema.com → OpenAPI)
- System ID (SID) + ECU ID (EID)

> Register your OpenAPI account at:  
> https://apsystemsema.com → Menu → OpenAPI

## Installation

### Via HACS (recommended)
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/VOTRE_PSEUDO/apsystems-openapi-ha`
3. Category: Integration
4. Install → Restart HA

### Manual
Copy `custom_components/apsystems_openapi/` into your HA `/config/custom_components/`

## Configuration

1. Settings → Devices & Services → Add Integration
2. Search **APsystems**
3. Fill in your App ID, App Secret, SID, EID

## Sensors (20 total)

| Sensor | Unit | Description |
|--------|------|-------------|
| Production Solaire | W | Instant solar production |
| Consommation Maison | W | Instant home consumption |
| Import Réseau | W | Instant grid import |
| Export Réseau | W | Instant grid export |
| Produit Aujourd'hui | kWh | Daily solar production |
| Importé Aujourd'hui | kWh | Daily grid import |
| Exporté Aujourd'hui | kWh | Daily grid export |
| Autoconso Aujourd'hui | kWh | Daily self-consumption |
| Taux Autoconso Jour | % | Daily self-consumption rate |
| ... | | + month & year equivalents |

## Credits

Built with the APsystems OpenAPI v2 — End User edition.  
Signature: HMAC-SHA256 authentication.

## License

MIT
