"""Locked v0 versions for the council engine (plan §4.7 / P1.0).

Stored on each council run / blueprint so outputs are traceable and later
migrations are explicit. Bump these deliberately, never silently.
"""

from __future__ import annotations

COUNCIL_SCHEMA_VERSION = "0.1.0"
PROMPT_PACK_VERSION = "0.1.0"
SCORING_WEIGHTS_VERSION = "0.1.0"
PROVIDER_CONFIG_VERSION = "0.1.0"
BLUEPRINT_VERSION = "0.1.0"


def version_stamp() -> dict[str, str]:
    """The version block attached to a council run's metadata."""
    return {
        "council_schema_version": COUNCIL_SCHEMA_VERSION,
        "prompt_pack_version": PROMPT_PACK_VERSION,
        "scoring_weights_version": SCORING_WEIGHTS_VERSION,
        "provider_config_version": PROVIDER_CONFIG_VERSION,
    }
