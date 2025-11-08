"""
Life After AI - Streamlit Version

A simplified version for Streamlit Cloud deployment.
Predict automation risk and simulate AI dividends.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, List, Tuple

# Page config
st.set_page_config(
    page_title="Life After AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #5AA9FF 0%, #64FBD2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(90, 169, 255, 0.1) 0%, rgba(100, 251, 210, 0.1) 100%);
        border: 1px solid rgba(90, 169, 255, 0.3);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    .risk-high {
        color: #FF5722;
        font-weight: bold;
    }
    .risk-medium {
        color: #FFC107;
        font-weight: bold;
    }
    .risk-low {
        color: #64FBD2;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# CORE ALGORITHMS (adapted from backend)
# ============================================================================

class AutomationScorer:
    """Calculate automation risk scores."""

    W_BASELINE = 0.30
    W_AI_VELOCITY = 0.35
    W_REMOTE = 0.25
    W_PROTECTION = 0.10

    BAND_LOW = 0.35
    BAND_HIGH = 0.65

    ETA_RANGES = [
        (0.0, 0.3, (15, 20)),
        (0.3, 0.5, (10, 15)),
        (0.5, 0.7, (5, 10)),
        (0.7, 0.85, (3, 7)),
        (0.85, 1.0, (1, 5)),
    ]

    @classmethod
    def calculate_score(cls, occupation: Dict) -> Dict:
        """Calculate automation score for an occupation."""
        # Calculate protection factor
        protection = (
            occupation['creativity_weight'] +
            occupation['social_weight'] +
            occupation.get('physical_weight', 0)
        ) / 3.0

        # Calculate raw score
        raw_score = (
            cls.W_BASELINE * occupation['baseline_risk'] +
            cls.W_AI_VELOCITY * occupation['ai_velocity'] +
            cls.W_REMOTE * occupation['remote_feasibility'] -
            cls.W_PROTECTION * protection
        )

        # Clamp to [0, 1]
        score = max(0.0, min(1.0, raw_score))

        # Determine band
        if score < cls.BAND_LOW:
            band = "Low"
        elif score < cls.BAND_HIGH:
            band = "Medium"
        else:
            band = "High"

        # Calculate ETA
        eta_years = cls._calculate_eta(score, occupation['ai_velocity'])

        # Calculate confidence
        confidence = cls._calculate_confidence(occupation, score)

        # Generate explanation
        explanation = cls._generate_explanation(occupation, band, eta_years)

        return {
            'score': round(score, 3),
            'band': band,
            'eta_years': eta_years,
            'confidence': round(confidence, 2),
            'explanation': explanation
        }

    @classmethod
    def _calculate_eta(cls, score: float, ai_velocity: float) -> int:
        """Estimate years until substantial automation."""
        for min_score, max_score, (min_years, max_years) in cls.ETA_RANGES:
            if min_score <= score < max_score:
                range_position = (score - min_score) / (max_score - min_score)
                base_eta = min_years + (max_years - min_years) * (1 - range_position)
                velocity_factor = 1.0 - (ai_velocity * 0.3)
                eta = base_eta * velocity_factor
                return max(1, int(round(eta)))
        return 10

    @classmethod
    def _calculate_confidence(cls, occupation: Dict, score: float) -> float:
        """Calculate prediction confidence."""
        confidence = 0.75

        if score < 0.2 or score > 0.85:
            confidence -= 0.15

        protection = max(
            occupation['creativity_weight'],
            occupation['social_weight'],
            occupation.get('physical_weight', 0)
        )
        if protection > 0.8:
            confidence += 0.10

        if occupation['ai_velocity'] > 0.85:
            confidence -= 0.10

        return max(0.5, min(1.0, confidence))

    @classmethod
    def _generate_explanation(cls, occupation: Dict, band: str, eta_years: int) -> str:
        """Generate human-readable explanation."""
        if band == "Low":
            opening = f"{occupation['title']} has a relatively low automation risk."
        elif band == "Medium":
            opening = f"{occupation['title']} faces moderate automation pressure."
        else:
            opening = f"{occupation['title']} is at high risk of automation."

        timeline = f" We estimate substantial impact within {eta_years} years."

        return opening + timeline


class DividendSimulator:
    """Simulate AIDE dividend projections."""

    POPULATION = {
        "US": 330, "EU": 450, "UK": 67, "CA": 38, "AU": 26,
        "JP": 125, "IN": 1400, "CN": 1400, "BR": 215, "default": 100,
    }

    SECTOR_MULTIPLIERS = {
        "Technology": 2.5, "Finance": 2.2, "Healthcare": 1.3,
        "Education": 1.1, "Manufacturing": 1.8, "Retail": 1.4,
        "Transportation": 1.6, "Hospitality": 1.2, "Construction": 1.5,
        "Agriculture": 1.4, "Legal": 2.0, "Creative": 1.3,
        "Media": 1.7, "Business": 1.9, "Services": 1.3,
        "Public Safety": 1.1, "Government": 1.0, "default": 1.5,
    }

    @classmethod
    def simulate(cls, params: Dict) -> Dict:
        """Run dividend simulation."""
        surplus_per_capita = cls._calculate_surplus(
            params['sector'],
            params['automation_score'],
            params['base_salary']
        )

        contribution_adj = cls._calculate_contribution_adjustment(
            params.get('contribution_hours_weekly', 0)
        )

        # Generate year-by-year projections
        series = []
        projections = {}

        for year in range(1, 21):
            base_dividend = (
                surplus_per_capita *
                params.get('tax_rate', 0.25) *
                params.get('distribution_share', 0.60) *
                ((1 + params.get('growth_rate', 0.03)) ** year)
            )

            user_dividend = base_dividend * contribution_adj

            series.append({
                'year': year,
                'base_dividend': round(base_dividend, 2),
                'user_dividend': round(user_dividend, 2),
            })

            if year == 5:
                projections['y5'] = user_dividend
            elif year == 10:
                projections['y10'] = user_dividend
            elif year == 20:
                projections['y20'] = user_dividend

        # Calculate percentages
        pct_y5 = (projections['y5'] / params['base_salary']) * 100
        pct_y10 = (projections['y10'] / params['base_salary']) * 100
        pct_y20 = (projections['y20'] / params['base_salary']) * 100

        return {
            'year_5': round(projections['y5'], 2),
            'year_10': round(projections['y10'], 2),
            'year_20': round(projections['y20'], 2),
            'series': series,
            'pct_y5': round(pct_y5, 1),
            'pct_y10': round(pct_y10, 1),
            'pct_y20': round(pct_y20, 1),
        }

    @classmethod
    def _calculate_surplus(cls, sector: str, automation_score: float, base_salary: float) -> float:
        """Estimate automation surplus per capita."""
        sector_multiplier = cls.SECTOR_MULTIPLIERS.get(sector, cls.SECTOR_MULTIPLIERS["default"])
        scale_factor = 0.15
        return base_salary * automation_score * sector_multiplier * scale_factor

    @classmethod
    def _calculate_contribution_adjustment(cls, hours_weekly: float) -> float:
        """Calculate contribution bonus multiplier."""
        if hours_weekly <= 0:
            return 1.0
        max_bonus_hours = 20.0
        bonus_rate = 0.5 / max_bonus_hours
        adjustment = 1.0 + min(hours_weekly, max_bonus_hours) * bonus_rate
        return round(adjustment, 2)


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_occupations() -> pd.DataFrame:
    """Load occupation data from CSV."""
    csv_path = Path(__file__).parent / "data" / "occupations.csv"

    if not csv_path.exists():
        # Fallback: create sample data
        return pd.DataFrame({
            'title': ['Software Developer', 'Nurse', 'Teacher', 'Accountant'],
            'sector': ['Technology', 'Healthcare', 'Education', 'Finance'],
            'median_salary': [110000, 77600, 62870, 77250],
            'baseline_risk': [0.50, 0.30, 0.30, 0.70],
            'ai_velocity': [0.85, 0.55, 0.50, 0.75],
            'remote_feasibility': [0.98, 0.50, 0.60, 0.95],
            'creativity_weight': [0.75, 0.65, 0.75, 0.30],
            'social_weight': [0.50, 0.90, 0.95, 0.45],
            'physical_weight': [0.02, 0.55, 0.20, 0.05],
        })

    return pd.read_csv(csv_path)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = {}
if 'results' not in st.session_state:
    st.session_state.results = None


# ============================================================================
# PAGE: HOME
# ============================================================================

def show_home():
    """Display home page."""
    st.markdown('<h1 class="main-header">Life After AI</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 1.2rem; color: #888; margin-bottom: 2rem;'>
        Predict which jobs AI will automate, simulate your <span style='color: #64FBD2; font-weight: bold;'>AI Dividend</span>,
        and plan your future in the AI economy.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🤖 Automation Prediction
        Get personalized risk assessment and timeline for your occupation based on latest AI research.
        """)

    with col2:
        st.markdown("""
        ### 💰 AIDE Dividend Simulator
        See your potential universal income from automation surplus over 5, 10, and 20 years.
        """)

    with col3:
        st.markdown("""
        ### 🎯 Personal Action Plan
        Get custom career tracks with skills and resources to future-proof your career.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start the 3-Minute Test", use_container_width=True, type="primary"):
            st.session_state.page = 'quiz'
            st.rerun()


# ============================================================================
# PAGE: QUIZ
# ============================================================================

def show_quiz():
    """Display quiz page."""
    st.markdown('<h1 class="main-header">Life After AI Assessment</h1>', unsafe_allow_html=True)

    occupations_df = load_occupations()

    # Progress indicator
    progress = st.progress(0.33)
    st.markdown("### Step 1 of 3: About You")

    with st.form("quiz_form"):
        # Job selection
        job_titles = occupations_df['title'].tolist()
        selected_job = st.selectbox(
            "Current Job Title",
            options=job_titles,
            index=0,
            help="Select your current occupation"
        )

        # Salary
        selected_occupation = occupations_df[occupations_df['title'] == selected_job].iloc[0]
        default_salary = int(selected_occupation['median_salary'])

        current_salary = st.number_input(
            "Annual Salary (USD)",
            min_value=10000,
            max_value=500000,
            value=default_salary,
            step=5000,
            help="Your current annual salary"
        )

        # Demographics
        col1, col2 = st.columns(2)

        with col1:
            age_range = st.selectbox(
                "Age Range",
                options=["18-24", "25-34", "35-44", "45-54", "55+"],
                index=1
            )

        with col2:
            country = st.selectbox(
                "Country",
                options=["US", "UK", "EU", "CA", "AU", "Other"],
                index=0
            )

        st.markdown("---")
        st.markdown("### Step 2 of 3: Your Goals")

        # Planning preferences
        time_horizon = st.slider(
            "Planning Time Horizon (years)",
            min_value=5,
            max_value=20,
            value=10,
            step=5,
            help="How many years ahead do you want to plan?"
        )

        learning_hours = st.slider(
            "Learning Time Available (hours/week)",
            min_value=0,
            max_value=20,
            value=5,
            step=1,
            help="How many hours per week can you dedicate to learning?"
        )

        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Low", "Medium", "High"],
            value="Medium",
            help="Your comfort level with career changes"
        )

        st.markdown("---")
        st.markdown("### Step 3 of 3: Preferences")

        # Contribution hours for dividend bonus
        contribution_hours = st.slider(
            "Potential Contribution to Commons (hours/week)",
            min_value=0,
            max_value=20,
            value=0,
            step=1,
            help="Time you might spend learning, creating, or volunteering (earns up to 50% dividend bonus)"
        )

        # Policy preferences
        st.markdown("**AIDE Dividend Policy Scenarios**")
        col1, col2 = st.columns(2)

        with col1:
            tax_rate = st.slider(
                "Automation Tax Rate",
                min_value=0.0,
                max_value=0.5,
                value=0.25,
                step=0.05,
                format="%.0f%%",
                help="Tax on automation surplus"
            )

        with col2:
            distribution_share = st.slider(
                "Distribution Share",
                min_value=0.0,
                max_value=1.0,
                value=0.60,
                step=0.05,
                format="%.0f%%",
                help="Share of tax revenue distributed as dividend"
            )

        submitted = st.form_submit_button("📊 See My Results", use_container_width=True, type="primary")

        if submitted:
            # Store quiz data
            st.session_state.quiz_data = {
                'job_title': selected_job,
                'occupation_data': selected_occupation.to_dict(),
                'salary': current_salary,
                'age_range': age_range,
                'country': country,
                'time_horizon': time_horizon,
                'learning_hours': learning_hours,
                'risk_tolerance': risk_tolerance,
                'contribution_hours': contribution_hours,
                'tax_rate': tax_rate,
                'distribution_share': distribution_share,
            }

            # Calculate results
            automation_result = AutomationScorer.calculate_score(
                st.session_state.quiz_data['occupation_data']
            )

            dividend_result = DividendSimulator.simulate({
                'sector': selected_occupation['sector'],
                'automation_score': automation_result['score'],
                'base_salary': current_salary,
                'country': country,
                'tax_rate': tax_rate,
                'distribution_share': distribution_share,
                'growth_rate': 0.03,
                'contribution_hours_weekly': contribution_hours,
            })

            st.session_state.results = {
                'automation': automation_result,
                'dividend': dividend_result,
            }

            st.session_state.page = 'results'
            st.rerun()


# ============================================================================
# PAGE: RESULTS
# ============================================================================

def show_results():
    """Display results page."""
    if not st.session_state.results:
        st.session_state.page = 'quiz'
        st.rerun()
        return

    st.markdown('<h1 class="main-header">Your AI Future Report</h1>', unsafe_allow_html=True)

    automation = st.session_state.results['automation']
    dividend = st.session_state.results['dividend']
    quiz_data = st.session_state.quiz_data

    # Key Metrics
    st.markdown("### 📊 Key Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        band_class = f"risk-{automation['band'].lower()}"
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 0.9rem; color: #888;'>Automation Risk</div>
            <div class='{band_class}' style='font-size: 2.5rem;'>{automation['band']}</div>
            <div style='font-size: 1rem; color: #64FBD2;'>{automation['eta_years']} years timeline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 0.9rem; color: #888;'>10-Year AIDE Dividend</div>
            <div style='font-size: 2.5rem; color: #64FBD2; font-weight: bold;'>${dividend['year_10']:,.0f}</div>
            <div style='font-size: 1rem; color: #888;'>{dividend['pct_y10']:.0f}% of current salary</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 0.9rem; color: #888;'>Confidence Score</div>
            <div style='font-size: 2.5rem; color: #5AA9FF; font-weight: bold;'>{int(automation['confidence'] * 100)}%</div>
            <div style='font-size: 1rem; color: #888;'>Based on current research</div>
        </div>
        """, unsafe_allow_html=True)

    # Automation Analysis
    st.markdown("---")
    st.markdown("### 🤖 Automation Analysis")

    st.info(automation['explanation'])

    # Dividend Projections
    st.markdown("---")
    st.markdown("### 💰 AIDE Dividend Projections")

    # Create chart
    df_series = pd.DataFrame(dividend['series'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_series['year'],
        y=df_series['user_dividend'],
        mode='lines',
        name='Your Dividend',
        line=dict(color='#64FBD2', width=3),
        fill='tozeroy',
        fillcolor='rgba(100, 251, 210, 0.1)'
    ))

    fig.update_layout(
        title="Annual AIDE Dividend Over Time",
        xaxis_title="Year",
        yaxis_title="Annual Dividend (USD)",
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary table
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("5-Year Dividend", f"${dividend['year_5']:,.0f}", f"{dividend['pct_y5']:.0f}% of salary")
    with col2:
        st.metric("10-Year Dividend", f"${dividend['year_10']:,.0f}", f"{dividend['pct_y10']:.0f}% of salary")
    with col3:
        st.metric("20-Year Dividend", f"${dividend['year_20']:,.0f}", f"{dividend['pct_y20']:.0f}% of salary")

    # Policy explanation
    st.info(f"""
    **Policy Scenario**: Based on a {int(quiz_data['tax_rate']*100)}% automation tax and
    {int(quiz_data['distribution_share']*100)}% distribution rate.
    {'Your ' + str(quiz_data['contribution_hours']) + ' hours/week of contribution earns a bonus!' if quiz_data['contribution_hours'] > 0 else 'Contribute to the commons (learning, creating, volunteering) to earn up to 50% bonus!'}
    """)

    # Action Items
    st.markdown("---")
    st.markdown("### 🎯 Recommended Actions")

    if automation['band'] == "High":
        st.warning("""
        **High automation risk detected.** Consider:
        - Developing automation-resistant skills (creativity, social, strategic thinking)
        - Exploring adjacent career paths with lower risk
        - Building a strong professional network
        - Starting a side project or business
        """)
    elif automation['band'] == "Medium":
        st.info("""
        **Moderate automation pressure.** Recommendations:
        - Stay current with AI tools in your field
        - Develop complementary skills (human-AI collaboration)
        - Explore upskilling opportunities
        - Monitor industry trends regularly
        """)
    else:
        st.success("""
        **Lower automation risk.** Stay ahead by:
        - Continuing to develop human-centric skills
        - Learning to work effectively with AI tools
        - Sharing your expertise with others
        - Exploring leadership opportunities
        """)

    # Disclaimer
    st.markdown("---")
    st.caption("""
    **Disclaimer**: These projections are illustrative scenarios based on current research and assumptions,
    not guaranteed forecasts. Actual automation timelines and economic policies may differ significantly.
    Data sources: Frey & Osborne (2013), O*NET, World Bank.
    """)

    # Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Take Quiz Again", use_container_width=True):
            st.session_state.page = 'quiz'
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with col3:
        st.button("📥 Download Report (Pro)", use_container_width=True, disabled=True)


# ============================================================================
# MAIN APP ROUTER
# ============================================================================

def main():
    """Main application router."""

    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Life After AI")
        st.markdown("Plan your future in the AI economy")

        st.markdown("---")

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

        if st.button("📝 Take Quiz", use_container_width=True):
            st.session_state.page = 'quiz'
            st.rerun()

        if st.session_state.results:
            if st.button("📊 View Results", use_container_width=True):
                st.session_state.page = 'results'
                st.rerun()

        st.markdown("---")
        st.markdown("### 💎 Premium Features")
        st.markdown("""
        - Advanced policy scenarios
        - Multi-job comparison
        - PDF report export
        - Career transition plans
        - Weekly updates
        """)
        st.button("✨ Upgrade to Pro", use_container_width=True, disabled=True)

        st.markdown("---")
        st.caption("© 2024 Life After AI")
        st.caption("[GitHub](https://github.com/seblosiv/AI-Driven-Economy) | [Docs](https://github.com/seblosiv/AI-Driven-Economy/blob/main/README.md)")

    # Route to appropriate page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'quiz':
        show_quiz()
    elif st.session_state.page == 'results':
        show_results()


if __name__ == "__main__":
    main()
