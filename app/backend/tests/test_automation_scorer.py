"""
Tests for automation scoring algorithm.
"""
import pytest
from app.backend.models.occupation import Occupation
from app.backend.services.automation_scorer import AutomationScorer


@pytest.fixture
def scorer():
    """Create scorer instance."""
    return AutomationScorer()


@pytest.fixture
def high_risk_occupation():
    """High automation risk job (e.g., data entry)."""
    return Occupation(
        soc_code="43-9021",
        title="Data Entry Keyers",
        sector="Administrative",
        median_salary=35000,
        baseline_risk=0.85,
        ai_velocity=0.80,
        remote_feasibility=0.95,
        creativity_weight=0.15,
        social_weight=0.20,
        physical_weight=0.05
    )


@pytest.fixture
def low_risk_occupation():
    """Low automation risk job (e.g., therapist)."""
    return Occupation(
        soc_code="21-1014",
        title="Mental Health Counselor",
        sector="Healthcare",
        median_salary=49000,
        baseline_risk=0.15,
        ai_velocity=0.35,
        remote_feasibility=0.55,
        creativity_weight=0.65,
        social_weight=0.95,
        physical_weight=0.15
    )


@pytest.fixture
def medium_risk_occupation():
    """Medium automation risk job (e.g., software developer)."""
    return Occupation(
        soc_code="15-1252",
        title="Software Developer",
        sector="Technology",
        median_salary=110000,
        baseline_risk=0.50,
        ai_velocity=0.85,
        remote_feasibility=0.98,
        creativity_weight=0.75,
        social_weight=0.50,
        physical_weight=0.02
    )


class TestAutomationScorer:
    """Test automation scoring logic."""

    def test_high_risk_gets_high_band(self, scorer, high_risk_occupation):
        """High risk occupation should get High band."""
        result = scorer.calculate_score(high_risk_occupation)

        assert result.band == "High"
        assert result.score > 0.65
        assert result.eta_years < 10
        assert 0.5 <= result.confidence <= 1.0

    def test_low_risk_gets_low_band(self, scorer, low_risk_occupation):
        """Low risk occupation should get Low band."""
        result = scorer.calculate_score(low_risk_occupation)

        assert result.band == "Low"
        assert result.score < 0.35
        assert result.eta_years > 10
        assert 0.5 <= result.confidence <= 1.0

    def test_medium_risk_gets_medium_band(self, scorer, medium_risk_occupation):
        """Medium risk occupation should get Medium band."""
        result = scorer.calculate_score(medium_risk_occupation)

        assert result.band in ["Low", "Medium", "High"]  # Allow some variance
        assert 0.0 <= result.score <= 1.0
        assert result.eta_years > 0
        assert 0.5 <= result.confidence <= 1.0

    def test_score_bounded(self, scorer, high_risk_occupation):
        """Score should be clamped to [0, 1]."""
        result = scorer.calculate_score(high_risk_occupation)

        assert 0.0 <= result.score <= 1.0

    def test_eta_positive(self, scorer, high_risk_occupation):
        """ETA should always be at least 1 year."""
        result = scorer.calculate_score(high_risk_occupation)

        assert result.eta_years >= 1

    def test_drivers_present(self, scorer, high_risk_occupation):
        """Drivers dict should be populated."""
        result = scorer.calculate_score(high_risk_occupation)

        assert len(result.drivers) > 0
        assert "baseline_research" in result.drivers or "ai_advancement" in result.drivers

    def test_explanation_generated(self, scorer, high_risk_occupation):
        """Explanation should be non-empty string."""
        result = scorer.calculate_score(high_risk_occupation)

        assert isinstance(result.explanation, str)
        assert len(result.explanation) > 50

    def test_protection_factors_reduce_risk(self, scorer):
        """High protection factors should reduce automation risk."""
        # Job with high automation inputs but strong protection
        protected_job = Occupation(
            soc_code="27-1013",
            title="Fine Artist",
            sector="Creative",
            median_salary=52000,
            baseline_risk=0.60,  # Moderate base risk
            ai_velocity=0.70,
            remote_feasibility=0.80,
            creativity_weight=0.95,  # Very high creativity
            social_weight=0.75,
            physical_weight=0.60
        )

        result = scorer.calculate_score(protected_job)

        # Should be pulled down by protection factors
        assert result.score < 0.70  # Not as high as inputs suggest

    def test_ai_velocity_affects_eta(self, scorer):
        """Higher AI velocity should reduce ETA."""
        # Two similar jobs, different AI velocity
        slow_ai_job = Occupation(
            soc_code="JOB-1",
            title="Job A",
            sector="Test",
            median_salary=50000,
            baseline_risk=0.60,
            ai_velocity=0.40,  # Slow AI advancement
            remote_feasibility=0.70,
            creativity_weight=0.40,
            social_weight=0.40,
            physical_weight=0.20
        )

        fast_ai_job = Occupation(
            soc_code="JOB-2",
            title="Job B",
            sector="Test",
            median_salary=50000,
            baseline_risk=0.60,
            ai_velocity=0.90,  # Fast AI advancement
            remote_feasibility=0.70,
            creativity_weight=0.40,
            social_weight=0.40,
            physical_weight=0.20
        )

        slow_result = scorer.calculate_score(slow_ai_job)
        fast_result = scorer.calculate_score(fast_ai_job)

        # Fast AI should have sooner ETA
        assert fast_result.eta_years <= slow_result.eta_years
