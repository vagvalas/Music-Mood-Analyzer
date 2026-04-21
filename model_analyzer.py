from typing import Any, Dict, List


def arousal_score(features: Dict[str, float]) -> float:
    bpm_norm = min(features.get("bpm", 100), 200) / 200 * 100
    return round(
        features.get("energy", 0) * 0.45 +
        features.get("danceability", 0) * 0.30 +
        bpm_norm * 0.25,
        1
    )


def positivity_score(features: Dict[str, float]) -> float:
    return round(features.get("valence", 0), 1)


def expressiveness_score(features: Dict[str, float]) -> float:
    return round(
        features.get("melodicness", 0) * 0.65 +
        features.get("acousticness", 0) * 0.35,
        1
    )


def movement_score(features: Dict[str, float]) -> float:
    return round(
        features.get("danceability", 0) * 0.60 +
        features.get("energy", 0) * 0.40,
        1
    )


def _dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _tempo_label(bpm: float) -> str:
    if bpm >= 150:
        return "very fast"
    if bpm >= 120:
        return "fast"
    if bpm >= 90:
        return "moderate"
    return "slow"


def analyze_averaged_profile(summary: Dict[str, Any]) -> Dict[str, Any]:
    raw = summary.get("raw_averages", {}) or {}
    derived = summary.get("derived_averages", {}) or {}

    mel = raw.get("melodicness", 0) or 0
    ac = raw.get("acousticness", 0) or 0
    v = raw.get("valence", 0) or 0
    dnc = raw.get("danceability", 0) or 0
    e = raw.get("energy", 0) or 0
    bpm = raw.get("bpm", 100) or 100

    a = derived.get("arousal")
    if a is None:
        a = arousal_score(raw)

    pos = derived.get("positivity")
    if pos is None:
        pos = positivity_score(raw)

    expr = derived.get("expressiveness")
    if expr is None:
        expr = expressiveness_score(raw)

    move = derived.get("movement")
    if move is None:
        move = movement_score(raw)

    tags: List[str] = []
    use_cases: List[str] = []
    listener_fit: List[str] = []
    explanation_parts: List[str] = []

    # Primary emotional profile
    if pos >= 75 and a >= 70:
        primary_state = "Euphoric / Uplifting"
        explanation_parts.append(
            "The listening profile is strongly positive and clearly activation-heavy."
        )
    elif pos >= 60 and a >= 55:
        primary_state = "Optimistic / Driving"
        explanation_parts.append(
            "The profile leans positive and active without feeling extreme."
        )
    elif pos >= 60 and a < 45:
        primary_state = "Calm / Content"
        explanation_parts.append(
            "The profile is positive but gently paced, suggesting steadiness rather than intensity."
        )
    elif pos < 40 and a >= 65:
        primary_state = "Tense / Intense"
        explanation_parts.append(
            "Lower positivity combined with higher activation gives the profile a charged or urgent feel."
        )
    elif pos < 40 and a < 45:
        primary_state = "Melancholic / Reflective"
        explanation_parts.append(
            "Lower positivity and lower activation suggest a more inward, bittersweet, or reflective profile."
        )
    else:
        primary_state = "Balanced / Mixed"
        explanation_parts.append(
            "The profile sits between strong extremes and suggests varied emotional usage."
        )

    # Listening orientation
    if expr >= 75 and move < 55:
        orientation = "Reflective / expressive"
        explanation_parts.append(
            "Melodic clarity and organic texture matter more here than physical momentum."
        )
    elif expr >= 65 and move >= 60:
        orientation = "Expressive with rhythmic pull"
        explanation_parts.append(
            "The profile balances emotional shape with a noticeable rhythmic drive."
        )
    elif move >= 75 and expr < 55:
        orientation = "Rhythm-forward / kinetic"
        explanation_parts.append(
            "This listening pattern is led more by momentum and movement than by melodic or organic detail."
        )
    elif move >= 65:
        orientation = "Social / movement-friendly"
        explanation_parts.append(
            "The profile has a clear social or movement-ready quality."
        )
    else:
        orientation = "General / mixed-orientation"
        explanation_parts.append(
            "The listening profile does not lean heavily toward either movement or inward expressiveness."
        )

    # Texture profile
    if ac >= 75:
        texture_profile = "Organic / acoustic-leaning"
        explanation_parts.append(
            "The average texture leans instrument-led and organic rather than heavily synthetic."
        )
    elif ac <= 25:
        texture_profile = "Synthetic / produced-leaning"
        explanation_parts.append(
            "The average texture leans more produced, electronic, or studio-shaped than acoustic."
        )
    else:
        texture_profile = "Balanced texture"
        explanation_parts.append(
            "The texture profile balances organic and produced elements."
        )

    # Melodic profile
    if mel >= 75:
        melodic_profile = "Strong melodic identity"
    elif mel >= 55:
        melodic_profile = "Melodically clear"
    elif mel < 35:
        melodic_profile = "Melody-light"
    else:
        melodic_profile = "Moderately melodic"

    # Movement profile
    if move >= 80:
        movement_profile = "Highly movement-oriented"
    elif move >= 65:
        movement_profile = "Rhythmically engaging"
    elif move < 40:
        movement_profile = "Still / non-movement-led"
    else:
        movement_profile = "Moderate movement pull"

    # Emotional regulation style
    if pos >= 70 and a >= 65:
        regulation_style = "Mood elevation and activation"
    elif pos >= 60 and a < 50:
        regulation_style = "Comfort and emotional steadiness"
    elif pos < 40 and expr >= 65:
        regulation_style = "Reflection and emotional processing"
    elif pos < 40 and a >= 60:
        regulation_style = "Release of tension or intensity"
    else:
        regulation_style = "Mixed emotional utility"

    # Tags
    if expr >= 75:
        tags.append("expressive")
    elif expr >= 60:
        tags.append("emotionally legible")

    if move >= 75:
        tags.append("kinetic")
    elif move >= 60:
        tags.append("rhythmic")

    if ac >= 75:
        tags.append("organic")
    elif ac <= 25:
        tags.append("produced")

    if mel >= 75:
        tags.append("tuneful")
    elif mel < 35:
        tags.append("melody-light")

    if pos >= 75:
        tags.append("bright")
    elif pos < 40:
        tags.append("heavy-toned")

    if a >= 75:
        tags.append("high-activation")
    elif a < 45:
        tags.append("low-activation")

    # Use cases
    if pos >= 70 and a >= 65:
        use_cases.extend(["mood lift", "daytime energy", "light motivation"])

    if expr >= 70 and a < 60:
        use_cases.extend(["reflective listening", "quiet focus", "late-night listening"])

    if move >= 70:
        use_cases.extend(["casual movement", "social setting", "driving playlist"])

    if pos < 40 and expr >= 65:
        use_cases.extend(["emotional processing", "introspective listening"])

    if not use_cases:
        use_cases.append("general listening")

    # Listener fit
    if expr >= 70:
        listener_fit.append(
            "may appeal to listeners who value melody, clarity, and emotional shape"
        )

    if move >= 70:
        listener_fit.append(
            "may appeal to listeners who enjoy rhythmic immediacy and physical momentum"
        )

    if pos >= 70:
        listener_fit.append(
            "may fit listeners seeking warmth, optimism, or emotional reassurance"
        )

    if pos < 40:
        listener_fit.append(
            "may fit listeners comfortable with bittersweet, darker, or heavier emotional tone"
        )

    if ac >= 75:
        listener_fit.append(
            "may appeal to listeners who prefer organic or instrument-led textures"
        )

    # Narrative explanation
    rhythmic_strength = (
        "strong" if move >= 70 else
        "moderate" if move >= 50 else
        "limited"
    )
    expressive_strength = (
        "high" if expr >= 70 else
        "moderate" if expr >= 50 else
        "lower"
    )

    summary_explanation = (
        f"This listening profile leans {primary_state.lower()}, with "
        f"{rhythmic_strength} rhythmic pull and {expressive_strength} expressive structure. "
        f"The overall texture feels {texture_profile.lower()}, while the music seems to function mainly as "
        f"{regulation_style.lower()}."
    )

    full_explanation = " ".join(explanation_parts + [summary_explanation])

    result = {
        "total_songs": summary.get("total_songs", 0),
        "raw_averages": raw,
        "derived_averages": {
            **derived,
            "arousal": round(a, 2),
            "positivity": round(pos, 2),
            "expressiveness": round(expr, 2),
            "movement": round(move, 2),
        },
        "primary_state": primary_state,
        "orientation": orientation,
        "texture_profile": texture_profile,
        "melodic_profile": melodic_profile,
        "movement_profile": movement_profile,
        "regulation_style": regulation_style,
        "tempo_feel": _tempo_label(bpm),
        "tags": _dedupe_keep_order(tags),
        "use_cases": _dedupe_keep_order(use_cases),
        "listener_fit": _dedupe_keep_order(listener_fit),
        "explanation": full_explanation,
        "note": (
            "This interpretation describes the emotional and sonic profile of the music set. "
            "It should be treated as a listening-pattern summary, not a diagnosis or fixed personality label."
        ),
    }

    return result