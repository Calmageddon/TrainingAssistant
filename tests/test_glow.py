"""Lichtsignal: Farbzustand aus dem Trainingszustand (glow.py, ohne HA)."""

from datetime import datetime, timedelta, timezone

from custom_components.training_assistant.glow import COUNT_S, glow_state, seconds_to_count

NOW = datetime(2026, 11, 14, 18, 0, tzinfo=timezone.utc)


def iso(seconds):
    return (NOW + timedelta(seconds=seconds)).isoformat()


def test_no_session_or_paused_is_off():
    assert glow_state(None, NOW) == "off"
    assert glow_state({"phase": "active", "paused": True}, NOW) == "off"
    assert glow_state({"phase": "ready"}, NOW) == "off"  # wartet auf „Los“


def test_set_rest_and_countdown():
    assert glow_state({"phase": "active"}, NOW) == "work"
    assert glow_state({"phase": "active", "rest_until": iso(60)}, NOW) == "rest"
    assert glow_state({"phase": "active", "rest_until": iso(COUNT_S - 0.5)}, NOW) == "count"
    assert seconds_to_count({"phase": "active", "rest_until": iso(60)}, NOW) == 60 - COUNT_S
    assert seconds_to_count({"phase": "active", "rest_until": iso(2)}, NOW) is None


def test_timed_set_phases():
    hold = lambda phase, until=None: {"phase": "active", "hold": {"phase": phase, "until": until}}
    assert glow_state(hold("ready", iso(5)), NOW) == "count"
    assert glow_state(hold("work", iso(30)), NOW) == "work"
    assert glow_state(hold("switch", iso(5)), NOW) == "rest"
    assert glow_state(hold("switch", iso(2)), NOW) == "count"


def test_interval_phases():
    iv = lambda phase, s: {"phase": "interval", "interval": {"phase": phase, "ends_at": iso(s)}}
    assert glow_state(iv("work", 2), NOW) == "work"  # Ende der Arbeit wird nicht rot gezählt
    assert glow_state(iv("rest", 8), NOW) == "rest"
    assert glow_state(iv("rest", 2), NOW) == "count"
    assert seconds_to_count(iv("work", 20), NOW) is None
    assert seconds_to_count(iv("rest", 10), NOW) == 10 - COUNT_S
