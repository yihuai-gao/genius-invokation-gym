"""
Global configuration
"""

import json
import locale
import logging
import os

logger = logging.getLogger(__name__)
try:
    DISPLAY_LANGUAGE = locale.getdefaultlocale(("LANG",))[0].replace("_", "-").lower()
except AttributeError:
    DISPLAY_LANGUAGE = "en-us"


path = os.path.join(os.path.dirname(__file__), "resources", "cards_20221205_i18n.json")
with open(path, "r", encoding="utf-8") as f:
    I18N_DATA = json.load(f)

ALL_LANGUAGES = list(I18N_DATA.keys())

if DISPLAY_LANGUAGE not in ALL_LANGUAGES:
    logger.warning(f"Unsupported language {DISPLAY_LANGUAGE}, falling back to en-us")
    DISPLAY_LANGUAGE = "en-us"


def get_display_text(key):
    return I18N_DATA[DISPLAY_LANGUAGE].get(key, key)


INF_INT = 99999
