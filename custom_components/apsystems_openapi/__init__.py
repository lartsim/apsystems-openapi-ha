from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_APP_ID, CONF_APP_SECRET, CONF_SID, CONF_EID
from .coordinator import APsystemsCoordinator

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = APsystemsCoordinator(
        hass,
        app_id     = entry.data[CONF_APP_ID],
        app_secret = entry.data[CONF_APP_SECRET],
        sid        = entry.data[CONF_SID],
        eid        = entry.data[CONF_EID],
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True