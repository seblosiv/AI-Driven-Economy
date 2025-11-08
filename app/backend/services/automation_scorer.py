"""
Deterministic automation risk scoring algorithm.

This module provides the core logic for calculating automation risk,
timeline estimates, and confidence scores for occupations.
"""
from typing import Dict, List, Tuple
from pydantic import BaseModel
from app.backend.models.occupation import Occupation


class AutomationScore(BaseModel):
    """Automation scoring result."""

    score: float  # 0-1 overall automation probability
    band: str  # "Low", "Medium", "High"
    eta_years: int  # Years until substantial (30%+) automation
    confidence: float  # 0-1 confidence in prediction
    drivers: Dict[str, float]  # Key risk factors with weights
    explanation: str  # Human-readable explanation


class AutomationScorer:
    """
    Calculate automation risk using a hybrid deterministic model.

    Model components:
    1. Base risk from research (Frey & Osborne, etc.)
    2. AI advancement velocity in domain
    3. Remote/digital feasibility
    4. Protection factors: creativity, social, physical

    Formula:
    score = w1*baseline + w2*ai_velocity + w3*remote - w4*(creativity + social + physical)/3

    Where weights sum to 1.0 for the positive factors.
    """

    # Scoring weights
    W_BASELINE = 0.30
    W_AI_VELOCITY = 0.35
    W_REMOTE = 0.25
    W_PROTECTION = 0.10  # Applied inversely

    # Band thresholds
    BAND_LOW = 0.35
    BAND_HIGH = 0.65

    # ETA calibration (piecewise function)
    # Maps score ranges to (min_years, max_years) for substantial automation
    ETA_RANGES = [
        (0.0, 0.3, (15, 20)),  # Low risk: 15-20 years
        (0.3, 0.5, (10, 15)),  # Low-medium: 10-15 years
        (0.5, 0.7, (5, 10)),   # Medium-high: 5-10 years
        (0.7, 0.85, (3, 7)),   # High: 3-7 years
        (0.85, 1.0, (1, 5)),   # Very high: 1-5 years
    ]

    def calculate_score(self, occupation: Occupation) -> AutomationScore:
        """
        Calculate automation score for an occupation.

        Args:
            occupation: Occupation model instance

        Returns:
            AutomationScore with all metrics
        """
        # Calculate protection factor (average of human-centric skills)
        protection = (
            occupation.creativity_weight +
            occupation.social_weight +
            occupation.physical_weight
        ) / 3.0

        # Calculate raw score
        raw_score = (
            self.W_BASELINE * occupation.baseline_risk +
            self.W_AI_VELOCITY * occupation.ai_velocity +
            self.W_REMOTE * occupation.remote_feasibility -
            self.W_PROTECTION * protection
        )

        # Clamp to [0, 1]
        score = max(0.0, min(1.0, raw_score))

        # Determine band
        if score < self.BAND_LOW:
            band = "Low"
        elif score < self.BAND_HIGH:
            band = "Medium"
        else:
            band = "High"

        # Calculate ETA
        eta_years = self._calculate_eta(score, occupation.ai_velocity)

        # Calculate confidence based on data quality signals
        confidence = self._calculate_confidence(occupation)

        # Extract key drivers
        drivers = self._extract_drivers(occupation)

        # Generate explanation
        explanation = self._generate_explanation(
            occupation, score, band, eta_years, drivers
        )

        return AutomationScore(
            score=round(score, 3),
            band=band,
            eta_years=eta_years,
            confidence=round(confidence, 2),
            drivers=drivers,
            explanation=explanation
        )

    def _calculate_eta(self, score: float, ai_velocity: float) -> int:
        """
        Estimate years until substantial automation.

        Args:
            score: Automation risk score (0-1)
            ai_velocity: Rate of AI advancement (0-1)

        Returns:
            Years until 30%+ automation impact
        """
        # Find appropriate range
        for min_score, max_score, (min_years, max_years) in self.ETA_RANGES:
            if min_score <= score < max_score:
                # Interpolate within range
                range_position = (score - min_score) / (max_score - min_score)
                base_eta = min_years + (max_years - min_years) * (1 - range_position)

                # Adjust for AI velocity (higher velocity = sooner)
                velocity_factor = 1.0 - (ai_velocity * 0.3)  # Up to 30% reduction
                eta = base_eta * velocity_factor

                return max(1, int(round(eta)))

        # Fallback (shouldn't reach here)
        return 10

    def _calculate_confidence(self, occupation: Occupation) -> float:
        """
        Calculate confidence in prediction.

        Factors:
        - Extreme scores are less certain (novelty, rapid change)
        - Mid-range scores are more certain
        - High protection factors increase certainty

        Args:
            occupation: Occupation model

        Returns:
            Confidence score 0-1
        """
        # Start with base confidence
        confidence = 0.75

        # Penalize extreme automation scores (more uncertainty)
        score_factor = occupation.baseline_risk
        if score_factor < 0.2 or score_factor > 0.85:
            confidence -= 0.15

        # Boost confidence for strong protection factors
        protection = max(
            occupation.creativity_weight,
            occupation.social_weight,
            occupation.physical_weight
        )
        if protection > 0.8:
            confidence += 0.10

        # Reduce confidence for rapidly advancing AI domains
        if occupation.ai_velocity > 0.85:
            confidence -= 0.10

        return max(0.5, min(1.0, confidence))

    def _extract_drivers(self, occupation: Occupation) -> Dict[str, float]:
        """
        Extract key risk drivers with their contributions.

        Args:
            occupation: Occupation model

        Returns:
            Dictionary of driver name to weight
        """
        drivers = {
            "baseline_research": occupation.baseline_risk * self.W_BASELINE,
            "ai_advancement": occupation.ai_velocity * self.W_AI_VELOCITY,
            "remote_feasible": occupation.remote_feasibility * self.W_REMOTE,
        }

        # Protection factors (shown as negative/protective)
        if occupation.creativity_weight > 0.5:
            drivers["creativity_shield"] = -occupation.creativity_weight * 0.15
        if occupation.social_weight > 0.5:
            drivers["social_shield"] = -occupation.social_weight * 0.15
        if occupation.physical_weight > 0.5:
            drivers["physical_shield"] = -occupation.physical_weight * 0.10

        # Sort by absolute impact
        return dict(
            sorted(drivers.items(), key=lambda x: abs(x[1]), reverse=True)
        )

    def _generate_explanation(
        self,
        occupation: Occupation,
        score: float,
        band: str,
        eta_years: int,
        drivers: Dict[str, float]
    ) -> str:
        """
        Generate human-readable explanation.

        Args:
            occupation: Occupation model
            score: Automation score
            band: Risk band
            eta_years: Years to automation
            drivers: Risk drivers

        Returns:
            Explanation string
        """
        # Start with band assessment
        if band == "Low":
            opening = f"{occupation.title} has a relatively low automation risk."
        elif band == "Medium":
            opening = f"{occupation.title} faces moderate automation pressure."
        else:
            opening = f"{occupation.title} is at high risk of automation."

        # Add timeline
        timeline = f" We estimate substantial impact within {eta_years} years."

        # Extract top driver
        top_driver = next(iter(drivers.keys()))
        driver_text = {
            "baseline_research": "existing automation research",
            "ai_advancement": "rapid AI advancement in this domain",
            "remote_feasible": "high digital feasibility",
            "creativity_shield": "strong creative requirements",
            "social_shield": "important social/interpersonal elements",
            "physical_shield": "essential physical presence",
        }.get(top_driver, "multiple factors")

        reasoning = f" Key factor: {driver_text}."

        # Add protection note if relevant
        protection_max = max(
            occupation.creativity_weight,
            occupation.social_weight,
            occupation.physical_weight
        )
        if protection_max > 0.7:
            protection_text = " However, significant human-centric skills provide protection."
        else:
            protection_text = ""

        return opening + timeline + reasoning + protection_text


# Global scorer instance
scorer = AutomationScorer()
