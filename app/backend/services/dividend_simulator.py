"""
AIDE (AI Dividend Economy) simulator.

This module calculates projected universal dividend payments
based on automation surplus, policy parameters, and user contribution.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class DividendParams(BaseModel):
    """Parameters for dividend simulation."""

    # Economic inputs
    sector: str = Field(description="Economic sector")
    automation_score: float = Field(ge=0.0, le=1.0, description="Automation probability")
    base_salary: float = Field(gt=0, description="User's current salary")
    country: str = Field(default="US", description="Country code")

    # Policy parameters (user-adjustable)
    tax_rate: float = Field(
        default=0.25,
        ge=0.0,
        le=0.5,
        description="Tax on automation surplus (τ)"
    )
    distribution_share: float = Field(
        default=0.60,
        ge=0.0,
        le=1.0,
        description="Share of tax distributed as dividend (δ)"
    )
    growth_rate: float = Field(
        default=0.03,
        ge=0.0,
        le=0.10,
        description="Annual growth rate (g)"
    )

    # User contribution (affects personal multiplier)
    contribution_hours_weekly: float = Field(
        default=0.0,
        ge=0.0,
        le=40.0,
        description="Hours/week contributing to commons (learning, creating, volunteering)"
    )


class DividendProjection(BaseModel):
    """Dividend projection results."""

    year_5: float = Field(description="Annual dividend in year 5")
    year_10: float = Field(description="Annual dividend in year 10")
    year_20: float = Field(description="Annual dividend in year 20")

    # Detailed time series for charts
    series: List[Dict[str, float]] = Field(
        description="Year-by-year breakdown with base + contribution bonus"
    )

    # Contextual info
    percentage_of_current_salary_y5: float
    percentage_of_current_salary_y10: float
    percentage_of_current_salary_y20: float

    explanation: str = Field(description="Human-readable explanation")


class DividendSimulator:
    """
    Simulate AIDE dividend projections.

    This is an illustrative macro model, not a precise economic forecast.

    Formula:
    D_y = (S * τ * δ / P) * (1 + g)^y * γ_adj

    Where:
    - S: Sector automation surplus (derived from automation_score × productivity gains)
    - τ: Tax rate on automation surplus
    - δ: Distribution share (what % of tax revenue goes to dividend)
    - P: Population (regional proxy)
    - g: Annual growth rate
    - y: Year
    - γ_adj: User contribution adjustment (1.0 to 1.5x based on contribution hours)
    """

    # Regional population proxies (millions)
    POPULATION = {
        "US": 330,
        "EU": 450,
        "UK": 67,
        "CA": 38,
        "AU": 26,
        "JP": 125,
        "IN": 1400,
        "CN": 1400,
        "BR": 215,
        "default": 100,
    }

    # Sector productivity multipliers (how much automation surplus per worker)
    SECTOR_MULTIPLIERS = {
        "Technology": 2.5,
        "Finance": 2.2,
        "Healthcare": 1.3,
        "Education": 1.1,
        "Manufacturing": 1.8,
        "Retail": 1.4,
        "Transportation": 1.6,
        "Hospitality": 1.2,
        "Construction": 1.5,
        "Agriculture": 1.4,
        "Legal": 2.0,
        "Creative": 1.3,
        "Media": 1.7,
        "Business": 1.9,
        "Services": 1.3,
        "Public Safety": 1.1,
        "Government": 1.0,
        "Nonprofit": 0.9,
        "default": 1.5,
    }

    def simulate(self, params: DividendParams) -> DividendProjection:
        """
        Run dividend simulation.

        Args:
            params: Simulation parameters

        Returns:
            DividendProjection with year 5/10/20 + time series
        """
        # Calculate sector automation surplus per capita
        surplus_per_capita = self._calculate_surplus(
            params.sector,
            params.automation_score,
            params.base_salary
        )

        # Get population
        population_millions = self.POPULATION.get(
            params.country,
            self.POPULATION["default"]
        )

        # Calculate contribution adjustment (1.0 to 1.5x)
        contribution_adj = self._calculate_contribution_adjustment(
            params.contribution_hours_weekly
        )

        # Generate year-by-year projections
        series = []
        projections = {}

        for year in range(1, 21):
            # Base dividend (shared equally)
            base_dividend = (
                surplus_per_capita *
                params.tax_rate *
                params.distribution_share *
                ((1 + params.growth_rate) ** year)
            )

            # User's dividend with contribution bonus
            user_dividend = base_dividend * contribution_adj

            series.append({
                "year": year,
                "base_dividend": round(base_dividend, 2),
                "user_dividend": round(user_dividend, 2),
                "contribution_bonus": round(user_dividend - base_dividend, 2),
            })

            # Capture key years
            if year == 5:
                projections["y5"] = user_dividend
            elif year == 10:
                projections["y10"] = user_dividend
            elif year == 20:
                projections["y20"] = user_dividend

        # Calculate percentages of current salary
        pct_y5 = (projections["y5"] / params.base_salary) * 100
        pct_y10 = (projections["y10"] / params.base_salary) * 100
        pct_y20 = (projections["y20"] / params.base_salary) * 100

        # Generate explanation
        explanation = self._generate_explanation(
            params,
            projections,
            pct_y5,
            pct_y10,
            contribution_adj
        )

        return DividendProjection(
            year_5=round(projections["y5"], 2),
            year_10=round(projections["y10"], 2),
            year_20=round(projections["y20"], 2),
            series=series,
            percentage_of_current_salary_y5=round(pct_y5, 1),
            percentage_of_current_salary_y10=round(pct_y10, 1),
            percentage_of_current_salary_y20=round(pct_y20, 1),
            explanation=explanation
        )

    def _calculate_surplus(
        self,
        sector: str,
        automation_score: float,
        base_salary: float
    ) -> float:
        """
        Estimate automation surplus per capita.

        This is highly simplified: assumes automation creates surplus
        proportional to productivity gains.

        Args:
            sector: Economic sector
            automation_score: 0-1 automation probability
            base_salary: Current salary as proxy for productivity value

        Returns:
            Estimated surplus per capita
        """
        sector_multiplier = self.SECTOR_MULTIPLIERS.get(
            sector,
            self.SECTOR_MULTIPLIERS["default"]
        )

        # Surplus = base_value × automation% × sector_productivity × scale_factor
        # Scale factor accounts for broader economic gains beyond direct labor
        scale_factor = 0.15  # Assumes 15% of labor savings flow to surplus pool

        surplus = (
            base_salary *
            automation_score *
            sector_multiplier *
            scale_factor
        )

        return surplus

    def _calculate_contribution_adjustment(
        self,
        hours_weekly: float
    ) -> float:
        """
        Calculate contribution bonus multiplier.

        Users contributing to the commons (learning, creating, volunteering)
        receive a modest bonus (up to 1.5x).

        Args:
            hours_weekly: Hours per week of contribution

        Returns:
            Multiplier between 1.0 and 1.5
        """
        if hours_weekly <= 0:
            return 1.0

        # Linear scale: 0 hrs = 1.0x, 20 hrs = 1.5x, capped at 20 hrs
        max_bonus_hours = 20.0
        bonus_rate = 0.5 / max_bonus_hours  # 0.5x bonus for 20 hrs

        adjustment = 1.0 + min(hours_weekly, max_bonus_hours) * bonus_rate

        return round(adjustment, 2)

    def _generate_explanation(
        self,
        params: DividendParams,
        projections: Dict[str, float],
        pct_y5: float,
        pct_y10: float,
        contribution_adj: float
    ) -> str:
        """
        Generate human-readable explanation.

        Args:
            params: Simulation parameters
            projections: Year projections
            pct_y5: Percentage of salary at year 5
            pct_y10: Percentage of salary at year 10
            contribution_adj: Contribution multiplier

        Returns:
            Explanation string
        """
        opening = (
            f"Based on a {int(params.tax_rate * 100)}% automation surplus tax "
            f"and {int(params.distribution_share * 100)}% distribution rate, "
        )

        projections_text = (
            f"you could receive approximately ${projections['y5']:,.0f}/year "
            f"in 5 years ({pct_y5:.0f}% of current salary) and "
            f"${projections['y10']:,.0f}/year in 10 years ({pct_y10:.0f}%)."
        )

        if contribution_adj > 1.0:
            bonus_pct = int((contribution_adj - 1.0) * 100)
            contribution_text = (
                f" Your {params.contribution_hours_weekly:.0f} hours/week of "
                f"contribution earns a {bonus_pct}% bonus."
            )
        else:
            contribution_text = (
                " Consider contributing to the commons (learning, creating, "
                "volunteering) to earn a participation bonus of up to 50%."
            )

        disclaimer = (
            " Note: These are illustrative projections based on current "
            "policy scenarios, not guaranteed forecasts."
        )

        return opening + projections_text + contribution_text + disclaimer


# Global simulator instance
simulator = DividendSimulator()
