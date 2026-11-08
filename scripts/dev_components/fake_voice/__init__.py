"""Test-Satellit für die lokale Testinstanz – NICHT für echte Installationen.

Registriert assist_satellite.announce und assist_satellite.ask_question als Attrappen:
Ansagen werden protokolliert, Rückfragen mit vorher gesetzten Antworten beantwortet.

  fake_voice.set_answers  {answers: ["ja", "acht mal sechzehn", ""]}
  fake_voice.get_log      → {"log": [[art, entity_id, text], ...]}
  fake_voice.clear
"""

from __future__ import annotations

import asyncio

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.helpers.typing import ConfigType

DOMAIN = "fake_voice"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    log: list[list[str]] = []
    answers: list[str] = []

    async def announce(call: ServiceCall) -> None:
        log.append(["announce", call.data.get("entity_id"), call.data.get("message")])

    async def ask(call: ServiceCall):
        log.append(["ask", call.data.get("entity_id"), call.data.get("question")])
        await asyncio.sleep(0.3)  # „zuhören“
        sentence = answers.pop(0) if answers else ""
        log.append(["answer", call.data.get("entity_id"), sentence])
        return {"id": None, "sentence": sentence, "slots": {}}

    async def set_answers(call: ServiceCall) -> None:
        answers[:] = list(call.data.get("answers", []))

    async def get_log(call: ServiceCall):
        return {"log": list(log)}

    async def clear(call: ServiceCall) -> None:
        log.clear()
        answers.clear()

    hass.services.async_register("assist_satellite", "announce", announce)
    hass.services.async_register("assist_satellite", "ask_question", ask, supports_response=SupportsResponse.ONLY)
    hass.services.async_register(DOMAIN, "set_answers", set_answers)
    hass.services.async_register(DOMAIN, "get_log", get_log, supports_response=SupportsResponse.ONLY)
    hass.services.async_register(DOMAIN, "clear", clear)
    return True
