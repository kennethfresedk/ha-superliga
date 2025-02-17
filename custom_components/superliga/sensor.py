import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [SuperligaMatchSensor(coordinator)]
    async_add_entities(sensors, True)

class SuperligaMatchSensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor that retrieves Superliga match data."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Superliga Match Data"
        self._attr_unique_id = "superliga_match_data"
        self._state = None

    @property
    def native_value(self):
        """Return the most recent match data."""
        if self.coordinator.data:
            return self.coordinator.data[0].homeName  # Example: return home team name
        return "No Data"

    @property
    def extra_state_attributes(self):
        """Return additional attributes for the sensor."""
        if self.coordinator.data:
            return {
                "home_team": self.coordinator.data[0].homeName,
                "away_team": self.coordinator.data[0].awayName,
                "tv_channel": self.coordinator.data[0].tvChannel().name()
            }
        return {}

    async def async_update(self):
        """Manually trigger an update."""
        await self.coordinator.async_request_refresh()
