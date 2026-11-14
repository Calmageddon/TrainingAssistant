"""Einrichtung und Optionen für TrainingAssistant.

Die Einrichtung fragt bewusst keine Hardware ab. In den Optionen kann ein
Standard-Satellit gewählt werden (für Trainings, die per Knopf/Dashboard starten).
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
)

from .const import (
    CONF_ANNOUNCE,
    CONF_ASK_AFTER_SET,
    CONF_DEFAULT_SATELLITE,
    CONF_DEFAULT_LIGHT,
    CONF_SATELLITE_LIGHT,
    CONF_NOTIFY,
    CONF_QUESTION_TIMEOUT,
    CONF_VOICE_LANGUAGE,
    DEFAULT_QUESTION_TIMEOUT,
    DOMAIN,
)


class TrainingAssistantConfigFlow(ConfigFlow, domain=DOMAIN):
    """Einrichtung über Einstellungen → Geräte & Dienste."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="TrainingAssistant", data={})
        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return TrainingAssistantOptionsFlow()


class TrainingAssistantOptionsFlow(OptionsFlow):
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            if CONF_QUESTION_TIMEOUT in user_input:
                user_input[CONF_QUESTION_TIMEOUT] = int(user_input[CONF_QUESTION_TIMEOUT])
            return self.async_create_entry(data=user_input)
        opts = self.config_entry.options
        # Handy-Benachrichtigung: alle notify-Dienste (z. B. mobile_app_…) zur Auswahl
        notify = sorted(self.hass.services.async_services().get("notify", {}))
        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_DEFAULT_SATELLITE,
                    description={"suggested_value": opts.get(CONF_DEFAULT_SATELLITE)},
                ): EntitySelector(EntitySelectorConfig(domain="assist_satellite")),
                vol.Required(CONF_VOICE_LANGUAGE, default=opts.get(CONF_VOICE_LANGUAGE, "auto")): SelectSelector(
                    SelectSelectorConfig(options=["auto", "en", "de"], translation_key="voice_language")
                ),
                vol.Required(CONF_ANNOUNCE, default=opts.get(CONF_ANNOUNCE, True)): BooleanSelector(),
                vol.Required(CONF_ASK_AFTER_SET, default=opts.get(CONF_ASK_AFTER_SET, True)): BooleanSelector(),
                vol.Required(
                    CONF_QUESTION_TIMEOUT, default=opts.get(CONF_QUESTION_TIMEOUT, DEFAULT_QUESTION_TIMEOUT)
                ): NumberSelector(
                    NumberSelectorConfig(min=5, max=60, step=1, unit_of_measurement="s",
                                         mode=NumberSelectorMode.BOX)
                ),
                vol.Optional(CONF_NOTIFY, description={"suggested_value": opts.get(CONF_NOTIFY)}): SelectSelector(
                    SelectSelectorConfig(options=notify, custom_value=True)
                ),
                vol.Optional(
                    CONF_DEFAULT_LIGHT, description={"suggested_value": opts.get(CONF_DEFAULT_LIGHT)}
                ): EntitySelector(EntitySelectorConfig(domain="light")),
                vol.Required(CONF_SATELLITE_LIGHT, default=opts.get(CONF_SATELLITE_LIGHT, True)): BooleanSelector(),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
