import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN

class SuperLigaAPIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Superliga service."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Superliga service", data={})
        
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({})
        )