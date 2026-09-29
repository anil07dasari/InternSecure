from typing import Tuple


def calculate_trust_score(
    domain_age_months: int,
    total_reports: int,
    money_demanded_count: int,
) -> Tuple[int, str]:
    """
    Calculate a trust score for a domain/service based on:
    - Domain age
    - Number of community reports
    - Number of reports involving money demands

    Returns:
        Tuple[int, str]: (trust_score, risk_status)
    """

    # ------------------------------------------------------------------
    # Validate input
    # ------------------------------------------------------------------
    if domain_age_months < 0:
        raise ValueError("domain_age_months cannot be negative.")

    if total_reports < 0:
        raise ValueError("total_reports cannot be negative.")

    if money_demanded_count < 0:
        raise ValueError("money_demanded_count cannot be negative.")

    if money_demanded_count > total_reports:
        raise ValueError(
            "money_demanded_count cannot exceed total_reports."
        )

    # ------------------------------------------------------------------
    # Base score
    # ------------------------------------------------------------------
    score = 100

    # ------------------------------------------------------------------
    # 1. Domain age penalty
    # ------------------------------------------------------------------
    if domain_age_months < 3:
        score -= 25
    elif domain_age_months < 6:
        score -= 15
    elif domain_age_months < 12:
        score -= 5

    # ------------------------------------------------------------------
    # 2. Community report penalty
    # ------------------------------------------------------------------
    standard_reports = total_reports - money_demanded_count

    score -= standard_reports * 5

    # Reports involving money demands are treated as a stronger signal.
    score -= money_demanded_count * 15

    # ------------------------------------------------------------------
    # 3. Keep score within valid boundaries
    # ------------------------------------------------------------------
    final_score = max(0, min(score, 100))

    # ------------------------------------------------------------------
    # 4. Determine risk category
    # ------------------------------------------------------------------
    if final_score >= 80:
        status = "LOW RISK"
    elif final_score >= 60:
        status = "MODERATE RISK"
    elif final_score >= 40:
        status = "HIGH RISK"
    else:
        status = "CRITICAL RISK"

    return final_score, status
