"""Test-Lampe light.test_rgb für das Lichtsignal (nur Testinstanz). Befehle landen im fake_voice-Protokoll."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ATTR_COLOR_TEMP_KELVIN, ATTR_HS_COLOR, ATTR_RGB_COLOR, ColorMode, LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "fake_voice"


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback, discovery_info=None) -> None:
    async_add_entities([TestLight()])


class TestLight(LightEntity):
    _attr_name = "Test RGB"
    _attr_unique_id = "fake_voice_test_rgb"
    _attr_supported_color_modes = {ColorMode.RGB, ColorMode.COLOR_TEMP}
    _attr_min_color_temp_kelvin = 2000
    _attr_max_color_temp_kelvin = 6500

    def __init__(self) -> None:
        # anfangs an, warmweiß, halbe Helligkeit
        self._attr_is_on = True
        self._attr_brightness = 128
        self._attr_color_mode = ColorMode.COLOR_TEMP
        self._attr_color_temp_kelvin = 2700
        self._attr_rgb_color = None

    def _log(self, *entry: Any) -> None:
        log = self.hass.data.get(DOMAIN)
        if log is not None:
            log.append(["light", *entry])

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._log("turn_on", {k: (list(v) if isinstance(v, tuple) else v) for k, v in kwargs.items()})
        self._attr_is_on = True
        if ATTR_BRIGHTNESS in kwargs:
            self._attr_brightness = kwargs[ATTR_BRIGHTNESS]
        if ATTR_RGB_COLOR in kwargs:
            self._attr_color_mode, self._attr_rgb_color = ColorMode.RGB, kwargs[ATTR_RGB_COLOR]
        elif ATTR_HS_COLOR in kwargs:
            from homeassistant.util.color import color_hs_to_RGB
            self._attr_color_mode, self._attr_rgb_color = ColorMode.RGB, color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])
        elif ATTR_COLOR_TEMP_KELVIN in kwargs:
            self._attr_color_mode, self._attr_color_temp_kelvin = ColorMode.COLOR_TEMP, kwargs[ATTR_COLOR_TEMP_KELVIN]
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._log("turn_off", {})
        self._attr_is_on = False
        self.async_write_ha_state()
