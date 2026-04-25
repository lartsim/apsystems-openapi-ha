import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_APP_ID, CONF_APP_SECRET, CONF_SID, CONF_EID

class APsystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="APsystems Solar", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_APP_ID,     default=""): str,
                vol.Required(CONF_APP_SECRET, default=""): str,
                vol.Required(CONF_SID,        default=""): str,
                vol.Required(CONF_EID,        default=""): str,
            })
        )
