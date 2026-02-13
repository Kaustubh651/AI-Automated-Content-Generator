# services/scoring_engine/trend_bias_engine.py

from services.scoring_engine.trend_evolution import get_trend_evolution_status


def apply_trend_bias(trends, boost=0.15, penalty=0.2):
    """
    Apply learning-based bias using historical trend evolution.
    """

    print("\n[SPRINT 5] Applying trend bias engine")

    evolution_map = get_trend_evolution_status()
    biased_trends = []

    for trend in trends:
        name = trend["topic"]
        score = trend["score"]
        status = evolution_map.get(name, "NEW")

        original_score = score

        if status == "RISING":
            score += score * boost
            print(f"[SPRINT 5] 🔼 '{name}' boosted (RISING) {original_score:.3f} → {score:.3f}")

        elif status == "FALLING":
            score -= score * penalty
            print(f"[SPRINT 5] 🔽 '{name}' penalized (FALLING) {original_score:.3f} → {score:.3f}")

        else:
            print(f"[SPRINT 5] ⏸ '{name}' unchanged ({status})")

        trend["score"] = round(score, 4)
        trend["bias_status"] = status
        biased_trends.append(trend)

    biased_trends.sort(key=lambda x: x["score"], reverse=True)
    return biased_trends
