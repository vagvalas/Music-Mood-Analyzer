import re
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def arousal_score(features: dict) -> float:
    bpm_norm = min(features.get("bpm", 100), 200) / 200 * 100
    return round(
        features.get("energy", 0) * 0.45 +
        features.get("danceability", 0) * 0.30 +
        bpm_norm * 0.25,
        1
    )


def depth_score(features: dict) -> float:
    return round(
        features.get("melodicness", 0) * 0.60 +
        features.get("acousticness", 0) * 0.40,
        1
    )


def positivity_score(features: dict) -> float:
    return round(features.get("valence", 0), 1)


def add_derived_scores(features: dict) -> dict:
    enriched = dict(features)
    enriched["arousal"] = arousal_score(features)
    enriched["depth"] = depth_score(features)
    enriched["positivity"] = positivity_score(features)
    enriched["expressiveness"] = expressiveness_score(features)
    enriched["movement"] = movement_score(features)
    return enriched

def expressiveness_score(features: dict) -> float:
    return round(
        features.get("melodicness", 0) * 0.65 +
        features.get("acousticness", 0) * 0.35,
        1
    )

def movement_score(features: dict) -> float:
    return round(
        features.get("danceability", 0) * 0.60 +
        features.get("energy", 0) * 0.40,
        1
    )


def extract_features(shazam_url: str) -> dict | None:
    try:
        html = requests.get(shazam_url, headers=HEADERS, timeout=30).text

        keys = ["melodicness", "acousticness", "valence", "danceability", "energy"]
        data = {}

        for key in keys:
            match = re.search(
                rf'\\"{key}\\".*?\\"left\\":\\"([\d.]+)%\\"',
                html,
                re.DOTALL
            )
            if match:
                data[key] = float(match.group(1))

        bpm_match = re.search(
            r'\\"bpm\\".*?\\"children\\":(\d+(?:\.\d+)?)',
            html,
            re.DOTALL
        )
        if bpm_match:
            data["bpm"] = float(bpm_match.group(1))

        if not data:
            return None

        return add_derived_scores(data)

    except Exception as e:
        print(f"[ERROR] Failed for {shazam_url}: {e}")
        return None