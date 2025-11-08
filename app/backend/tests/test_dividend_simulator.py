"""
Tests for AIDE dividend simulator.
"""
import pytest
from app.backend.services.dividend_simulator import (
    DividendSimulator,
    DividendParams
)


@pytest.fixture
def simulator():
    """Create simulator instance."""
    return DividendSimulator()


@pytest.fixture
def base_params():
    """Base simulation parameters."""
    return DividendParams(
        sector="Technology",
        automation_score=0.70,
        base_salary=100000,
        country="US",
        tax_rate=0.25,
        distribution_share=0.60,
        growth_rate=0.03,
        contribution_hours_weekly=0.0
    )


class TestDividendSimulator:
    """Test dividend simulation logic."""

    def test_basic_simulation(self, simulator, base_params):
        """Basic simulation should return valid projections."""
        result = simulator.simulate(base_params)

        assert result.year_5 > 0
        assert result.year_10 > 0
        assert result.year_20 > 0

        # Growth: y10 should be > y5
        assert result.year_10 > result.year_5
        assert result.year_20 > result.year_10

    def test_series_generated(self, simulator, base_params):
        """Time series should have 20 years of data."""
        result = simulator.simulate(base_params)

        assert len(result.series) == 20
        assert result.series[0]["year"] == 1
        assert result.series[19]["year"] == 20

        # Each entry should have required fields
        for entry in result.series:
            assert "year" in entry
            assert "base_dividend" in entry
            assert "user_dividend" in entry
            assert "contribution_bonus" in entry

    def test_higher_tax_increases_dividend(self, simulator, base_params):
        """Higher tax rate should increase dividend."""
        low_tax = base_params.copy()
        low_tax.tax_rate = 0.15

        high_tax = base_params.copy()
        high_tax.tax_rate = 0.35

        low_result = simulator.simulate(low_tax)
        high_result = simulator.simulate(high_tax)

        assert high_result.year_5 > low_result.year_5
        assert high_result.year_10 > low_result.year_10

    def test_higher_distribution_increases_dividend(self, simulator, base_params):
        """Higher distribution share should increase dividend."""
        low_dist = base_params.copy()
        low_dist.distribution_share = 0.40

        high_dist = base_params.copy()
        high_dist.distribution_share = 0.80

        low_result = simulator.simulate(low_dist)
        high_result = simulator.simulate(high_dist)

        assert high_result.year_5 > low_result.year_5

    def test_contribution_bonus(self, simulator, base_params):
        """Contribution hours should increase user dividend."""
        no_contrib = base_params.copy()
        no_contrib.contribution_hours_weekly = 0

        with_contrib = base_params.copy()
        with_contrib.contribution_hours_weekly = 10

        no_result = simulator.simulate(no_contrib)
        contrib_result = simulator.simulate(with_contrib)

        assert contrib_result.year_5 > no_result.year_5
        assert contrib_result.series[0]["contribution_bonus"] > 0

    def test_contribution_capped(self, simulator, base_params):
        """Contribution bonus should cap at 1.5x (20 hrs)."""
        params_20hrs = base_params.copy()
        params_20hrs.contribution_hours_weekly = 20

        params_40hrs = base_params.copy()
        params_40hrs.contribution_hours_weekly = 40

        result_20 = simulator.simulate(params_20hrs)
        result_40 = simulator.simulate(params_40hrs)

        # Should be same (capped at 20 hrs)
        assert result_20.year_5 == result_40.year_5

    def test_growth_rate_affects_future(self, simulator, base_params):
        """Higher growth rate should increase future dividends more."""
        low_growth = base_params.copy()
        low_growth.growth_rate = 0.02

        high_growth = base_params.copy()
        high_growth.growth_rate = 0.05

        low_result = simulator.simulate(low_growth)
        high_result = simulator.simulate(high_growth)

        # Effect should compound over time
        y5_diff = high_result.year_5 - low_result.year_5
        y20_diff = high_result.year_20 - low_result.year_20

        assert y20_diff > y5_diff

    def test_sector_multiplier_varies(self, simulator, base_params):
        """Different sectors should yield different dividends."""
        tech_params = base_params.copy()
        tech_params.sector = "Technology"

        hospitality_params = base_params.copy()
        hospitality_params.sector = "Hospitality"

        tech_result = simulator.simulate(tech_params)
        hospitality_result = simulator.simulate(hospitality_params)

        # Tech should have higher surplus multiplier
        assert tech_result.year_5 > hospitality_result.year_5

    def test_automation_score_affects_surplus(self, simulator, base_params):
        """Higher automation score should increase dividend."""
        low_auto = base_params.copy()
        low_auto.automation_score = 0.30

        high_auto = base_params.copy()
        high_auto.automation_score = 0.90

        low_result = simulator.simulate(low_auto)
        high_result = simulator.simulate(high_auto)

        assert high_result.year_5 > low_result.year_5

    def test_percentage_calculations(self, simulator, base_params):
        """Percentage of salary should be calculated correctly."""
        result = simulator.simulate(base_params)

        # Manually verify year 5 percentage
        expected_pct_y5 = (result.year_5 / base_params.base_salary) * 100
        assert abs(result.percentage_of_current_salary_y5 - expected_pct_y5) < 0.1

    def test_explanation_present(self, simulator, base_params):
        """Explanation should be generated."""
        result = simulator.simulate(base_params)

        assert isinstance(result.explanation, str)
        assert len(result.explanation) > 100
        assert str(int(base_params.tax_rate * 100)) in result.explanation

    def test_contribution_adjustment_calculation(self, simulator):
        """Test contribution adjustment calculation directly."""
        assert simulator._calculate_contribution_adjustment(0) == 1.0
        assert simulator._calculate_contribution_adjustment(10) == 1.25
        assert simulator._calculate_contribution_adjustment(20) == 1.5
        assert simulator._calculate_contribution_adjustment(30) == 1.5  # Capped
