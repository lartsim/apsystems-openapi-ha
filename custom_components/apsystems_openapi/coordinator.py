import hmac, hashlib, base64, uuid, time, logging
from datetime import timedelta, date
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, BASE_URL, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class APsystemsCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, app_id, app_secret, sid, eid):
        super().__init__(hass, _LOGGER, name=DOMAIN,
                         update_interval=timedelta(seconds=SCAN_INTERVAL))
        self.app_id     = app_id
        self.app_secret = app_secret
        self.sid        = sid
        self.eid        = eid

    def _make_headers(self, path, method="GET"):
        last  = path.rstrip("/").split("/")[-1]
        ts    = str(int(time.time() * 1000))
        nonce = uuid.uuid4().hex
        sm    = "HmacSHA256"
        s2s   = "/".join([ts, nonce, self.app_id, last, method, sm])
        sig   = base64.b64encode(
            hmac.new(self.app_secret.encode(), s2s.encode(), hashlib.sha256).digest()
        ).decode()
        return {"X-CA-AppId": self.app_id, "X-CA-Timestamp": ts,
                "X-CA-Nonce": nonce, "X-CA-Signature-Method": sm,
                "X-CA-Signature": sig, "Content-Type": "application/json"}

    async def _api_get(self, session, path, params=None):
        url = BASE_URL + path
        async with session.get(url, headers=self._make_headers(path),
                               params=params,
                               timeout=aiohttp.ClientTimeout(total=10)) as r:
            d = await r.json()
            return d.get("code"), d.get("data")

    async def _async_update_data(self):
        today = date.today().isoformat()
        result = {}
        try:
            async with aiohttp.ClientSession() as session:

                # Puissance instantanée
                code, data = await self._api_get(
                    session,
                    f"/user/api/v2/systems/{self.sid}/devices/meter/period/{self.eid}",
                    params={"energy_level": "minutely", "date_range": today}
                )
                if code == 0 and data and data.get("time"):
                    power     = data.get("power", {})
                    prod_list = power.get("produced", [])
                    ie_list   = power.get("imported_exported", [])
                    prod_w    = float(prod_list[-1] or 0) if prod_list else 0
                    ie_w      = float(ie_list[-1]   or 0) if ie_list   else 0
                    imp_w     = max(ie_w, 0)
                    exp_w     = max(-ie_w, 0)
                    result["power_production"]  = round(prod_w, 1)
                    result["power_consumption"] = round(prod_w + imp_w - exp_w, 1)
                    result["power_import"]      = round(imp_w, 1)
                    result["power_export"]      = round(exp_w, 1)
                    result["last_reading"]       = data["time"][-1]
                    t = data.get("today", {})
                    result["today_produced"] = round(float(t.get("produced") or 0), 3)
                    result["today_consumed"] = round(float(t.get("consumed") or 0), 3)
                    result["today_imported"] = round(float(t.get("imported") or 0), 3)
                    result["today_exported"] = round(float(t.get("exported") or 0), 3)
                else:
                    result.update({"power_production": 0, "power_consumption": 0,
                                   "power_import": 0, "power_export": 0, "last_reading": "—"})

                # Résumé jour / mois / an
                code2, data2 = await self._api_get(
                    session,
                    f"/user/api/v2/systems/{self.sid}/devices/meter/summary/{self.eid}"
                )
                if code2 == 0 and data2:
                    for period in ["today", "month", "year"]:
                        p = data2.get(period, {})
                        for key in ["produced", "consumed", "imported", "exported"]:
                            result[f"{period}_{key}"] = round(float(p.get(key) or 0), 3)

                # Calculs autoconsommation
                for pfx in ["today", "month", "year"]:
                    prod = result.get(f"{pfx}_produced", 0)
                    exp  = result.get(f"{pfx}_exported", 0)
                    auto = round(prod - exp, 3)
                    result[f"{pfx}_autoconso"]     = auto
                    result[f"{pfx}_autoconso_pct"] = round(auto / prod * 100, 1) if prod > 0 else 0

        except Exception as e:
            raise UpdateFailed(f"APsystems API error: {e}")
        return result