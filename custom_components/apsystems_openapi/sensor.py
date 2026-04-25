from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower, UnitOfEnergy, PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

SENSORS = [
    ("power_production",    "Production Solaire",    UnitOfPower.WATT,            SensorDeviceClass.POWER,  SensorStateClass.MEASUREMENT,       "mdi:solar-power"),
    ("power_consumption",   "Consommation Maison",   UnitOfPower.WATT,            SensorDeviceClass.POWER,  SensorStateClass.MEASUREMENT,       "mdi:home-lightning-bolt"),
    ("power_import",        "Import Réseau",         UnitOfPower.WATT,            SensorDeviceClass.POWER,  SensorStateClass.MEASUREMENT,       "mdi:transmission-tower-import"),
    ("power_export",        "Export Réseau",         UnitOfPower.WATT,            SensorDeviceClass.POWER,  SensorStateClass.MEASUREMENT,       "mdi:transmission-tower-export"),
    ("today_produced",      "Produit Aujourd'hui",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:solar-power-variant"),
    ("today_consumed",      "Consommé Aujourd'hui",  UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:lightning-bolt"),
    ("today_imported",      "Importé Aujourd'hui",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-import"),
    ("today_exported",      "Exporté Aujourd'hui",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-export"),
    ("today_autoconso",     "Autoconso Aujourd'hui", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:recycle"),
    ("today_autoconso_pct", "Taux Autoconso Jour",   PERCENTAGE,                  None,                     SensorStateClass.MEASUREMENT,       "mdi:percent"),
    ("month_produced",      "Produit Ce Mois",       UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:solar-power-variant"),
    ("month_consumed",      "Consommé Ce Mois",      UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:lightning-bolt"),
    ("month_imported",      "Importé Ce Mois",       UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-import"),
    ("month_exported",      "Exporté Ce Mois",       UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-export"),
    ("month_autoconso",     "Autoconso Ce Mois",     UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:recycle"),
    ("month_autoconso_pct", "Taux Autoconso Mois",   PERCENTAGE,                  None,                     SensorStateClass.MEASUREMENT,       "mdi:percent"),
    ("year_produced",       "Produit Cette Année",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:solar-power-variant"),
    ("year_imported",       "Importé Cette Année",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-import"),
    ("year_exported",       "Exporté Cette Année",   UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING,  "mdi:transmission-tower-export"),
    ("year_autoconso_pct",  "Taux Autoconso Année",  PERCENTAGE,                  None,                     SensorStateClass.MEASUREMENT,       "mdi:percent"),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        APsystemsSensor(coordinator, *s) for s in SENSORS
    )

class APsystemsSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, unit, dev_class, state_class, icon):
        super().__init__(coordinator)
        self._key                             = key
        self._attr_name                       = f"APsystems {name}"
        self._attr_unique_id                  = f"apsystems_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class               = dev_class
        self._attr_state_class                = state_class
        self._attr_icon                       = icon
        self._attr_device_info                = {
            "identifiers": {(DOMAIN, "apsystems_main")},
            "name": "APsystems Solar",
            "manufacturer": "APsystems",
            "model": "OpenAPI v2",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)