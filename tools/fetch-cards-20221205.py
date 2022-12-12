import json
from urllib import request

BASE_URL = (
    "https://sg-hk4e-api-static.hoyoverse.com/event/e20221205drawcard/card_config?lang="
)

# English, Simplified Chinese, Traditional Chinese, Japanese, Korean, Indonesian, Thai, Vietnamese, German, French, Portuguese, Spanish, Russian.
ALL_LANGUAGES = [
    "en-us",
    "zh-cn",
    "zh-tw",
    "ja-jp",
    "ko-kr",
    "id-id",
    "th-th",
    "vi-vn",
    "de-de",
    "fr-fr",
    "pt-pt",
    "es-es",
    "ru-ru",
]

for lang in ALL_LANGUAGES:
    print(f"Downloading {lang}")
    card_config = request.urlopen(BASE_URL + lang).read()
    assert len(card_config) > 0

    data = json.loads(card_config.decode("utf-8"))["data"]
    assert data["role_card_infos"][0]["name"]

    with open(f"gisim/cards/resources/cards_20221205_{lang}.json", "w") as f:
        json.dump(data, f, indent=2)
