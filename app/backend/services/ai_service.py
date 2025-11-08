"""
AI service abstraction layer.

Supports multiple LLM providers with fallback to rules-based generation.
"""
from typing import Optional, Dict, List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from app.backend.core.config import settings


class PlanTrack(BaseModel):
    """A single career transition track."""

    name: str  # "Fast Track", "Balanced Path", "Deep Transformation"
    timeline: str  # "3-6 months"
    description: str
    modules: List[Dict[str, str]]  # [{title, description, affiliate_link}, ...]
    success_factors: List[str]


class PersonalPlan(BaseModel):
    """Complete personal transition plan."""

    summary: str
    tracks: List[PlanTrack]  # Fast, Balanced, Deep
    wellbeing_tips: List[str]
    resources: List[Dict[str, str]]


class AIProvider(ABC):
    """Abstract base for AI providers."""

    @abstractmethod
    async def generate_plan(
        self,
        occupation: str,
        skills: List[str],
        interests: List[str],
        risk_tolerance: str,
        learning_hours: float
    ) -> PersonalPlan:
        """Generate personalized career plan."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: str):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_plan(
        self,
        occupation: str,
        skills: List[str],
        interests: List[str],
        risk_tolerance: str,
        learning_hours: float
    ) -> PersonalPlan:
        """Generate plan using OpenAI."""
        prompt = self._build_prompt(
            occupation, skills, interests, risk_tolerance, learning_hours
        )

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career counselor specializing in AI-era transitions."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        # Parse response into structured plan
        content = response.choices[0].message.content
        return self._parse_plan(content)

    def _build_prompt(
        self,
        occupation: str,
        skills: List[str],
        interests: List[str],
        risk_tolerance: str,
        learning_hours: float
    ) -> str:
        """Build prompt for LLM."""
        return f"""Create a personalized career transition plan for someone who is a {occupation}.

Current skills: {', '.join(skills)}
Interests: {', '.join(interests)}
Risk tolerance: {risk_tolerance}
Available learning time: {learning_hours} hours/week

Provide:
1. A brief summary (2-3 sentences)
2. Three transition tracks:
   - Fast Track (3-6 months, quick pivot)
   - Balanced Path (6-12 months, measured transition)
   - Deep Transformation (12-18 months, comprehensive reskilling)

For each track, include:
- 3-5 specific learning modules or skills to develop
- Realistic timeline and milestones
- Success factors

3. Wellbeing tips (3-5 items)
4. Additional resources

Format your response as JSON with this structure:
{{
  "summary": "...",
  "tracks": [
    {{
      "name": "Fast Track",
      "timeline": "3-6 months",
      "description": "...",
      "modules": [
        {{"title": "...", "description": "...", "affiliate_link": "coursera"}}
      ],
      "success_factors": ["...", "..."]
    }}
  ],
  "wellbeing_tips": ["...", "..."],
  "resources": [{{"title": "...", "url": "..."}}]
}}
"""

    def _parse_plan(self, content: str) -> PersonalPlan:
        """Parse LLM response into PersonalPlan."""
        import json

        # Extract JSON from response
        try:
            # Try to find JSON block
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            data = json.loads(json_str)
            return PersonalPlan(**data)
        except Exception as e:
            # Fallback to rules-based if parsing fails
            print(f"LLM parsing failed: {e}, falling back to rules")
            raise


class RulesBasedProvider(AIProvider):
    """Fallback rules-based plan generator."""

    # Template tracks
    TRACK_TEMPLATES = {
        "fast": {
            "name": "Fast Track",
            "timeline": "3-6 months",
            "description": "Quick pivot to adjacent, automation-resistant skills",
        },
        "balanced": {
            "name": "Balanced Path",
            "timeline": "6-12 months",
            "description": "Measured transition with skill building and portfolio development",
        },
        "deep": {
            "name": "Deep Transformation",
            "timeline": "12-18 months",
            "description": "Comprehensive reskilling for a new career direction",
        }
    }

    async def generate_plan(
        self,
        occupation: str,
        skills: List[str],
        interests: List[str],
        risk_tolerance: str,
        learning_hours: float
    ) -> PersonalPlan:
        """Generate plan using rules."""
        # Determine focus areas based on interests
        focus_areas = self._determine_focus_areas(interests)

        # Build tracks
        tracks = [
            self._build_fast_track(occupation, focus_areas),
            self._build_balanced_track(occupation, focus_areas),
            self._build_deep_track(occupation, focus_areas),
        ]

        summary = (
            f"Based on your background as a {occupation} and interests in "
            f"{', '.join(interests[:2])}, we've created three transition paths "
            f"that emphasize automation-resistant skills like creativity, "
            f"strategic thinking, and human connection."
        )

        wellbeing_tips = [
            "Set realistic milestones and celebrate small wins",
            "Connect with peers in transition communities",
            "Maintain work-life balance during learning periods",
            "Practice stress management and mindfulness",
            "Stay curious and embrace continuous learning"
        ]

        resources = [
            {"title": "AIDE Learn Platform", "url": "/learn"},
            {"title": "Future of Work Community", "url": "https://example.com/community"},
            {"title": "Career Transition Guide", "url": "https://example.com/guide"},
        ]

        return PersonalPlan(
            summary=summary,
            tracks=tracks,
            wellbeing_tips=wellbeing_tips,
            resources=resources
        )

    def _determine_focus_areas(self, interests: List[str]) -> List[str]:
        """Map interests to focus areas."""
        focus_map = {
            "technology": ["AI literacy", "Data analysis", "Digital tools"],
            "creative": ["Content creation", "Design thinking", "Storytelling"],
            "business": ["Strategy", "Entrepreneurship", "Innovation"],
            "social": ["Community building", "Coaching", "Facilitation"],
            "health": ["Wellness", "Mental health support", "Holistic care"],
        }

        areas = []
        for interest in interests:
            interest_lower = interest.lower()
            for key, values in focus_map.items():
                if key in interest_lower:
                    areas.extend(values)

        # Default if no matches
        if not areas:
            areas = ["Creative problem solving", "Digital literacy", "Communication"]

        return list(set(areas))[:5]  # Unique, max 5

    def _build_fast_track(self, occupation: str, focus_areas: List[str]) -> PlanTrack:
        """Build fast track."""
        modules = [
            {
                "title": f"{focus_areas[0]} Fundamentals",
                "description": f"Quick intro to {focus_areas[0]}",
                "affiliate_link": "https://coursera.org"
            },
            {
                "title": "AI Literacy Essentials",
                "description": "Understand AI capabilities and limitations",
                "affiliate_link": "https://udemy.com"
            },
            {
                "title": "Portfolio Builder Sprint",
                "description": "Create 3-5 portfolio pieces in your niche",
                "affiliate_link": "/learn"
            }
        ]

        return PlanTrack(
            **self.TRACK_TEMPLATES["fast"],
            modules=modules,
            success_factors=[
                "Complete at least 2 modules per month",
                "Build visible portfolio pieces",
                "Network with 5+ people in target field"
            ]
        )

    def _build_balanced_track(self, occupation: str, focus_areas: List[str]) -> PlanTrack:
        """Build balanced track."""
        modules = [
            {
                "title": f"Advanced {focus_areas[0]}",
                "description": f"Deep dive into {focus_areas[0]} applications",
                "affiliate_link": "https://coursera.org"
            },
            {
                "title": "Human-AI Collaboration",
                "description": "Learn to work alongside AI tools",
                "affiliate_link": "https://udemy.com"
            },
            {
                "title": "Professional Branding",
                "description": "Position yourself for the AI era",
                "affiliate_link": "/learn"
            },
            {
                "title": "Freelance Foundations",
                "description": "Start side income while transitioning",
                "affiliate_link": "https://skillshare.com"
            }
        ]

        return PlanTrack(
            **self.TRACK_TEMPLATES["balanced"],
            modules=modules,
            success_factors=[
                "Complete 1 major skill module per quarter",
                "Launch 1-2 side projects or freelance gigs",
                "Attend industry events and build network"
            ]
        )

    def _build_deep_track(self, occupation: str, focus_areas: List[str]) -> PlanTrack:
        """Build deep transformation track."""
        modules = [
            {
                "title": f"{focus_areas[0]} Mastery Program",
                "description": f"Comprehensive {focus_areas[0]} certification",
                "affiliate_link": "https://coursera.org"
            },
            {
                "title": "Business & Entrepreneurship",
                "description": "Build your own AI-era venture",
                "affiliate_link": "https://udemy.com"
            },
            {
                "title": "Technical Skills Suite",
                "description": "Core tech literacy for modern work",
                "affiliate_link": "/learn"
            },
            {
                "title": "Leadership & Strategy",
                "description": "Position for high-value roles",
                "affiliate_link": "https://linkedin.com/learning"
            },
            {
                "title": "Capstone Project",
                "description": "Major portfolio piece demonstrating new expertise",
                "affiliate_link": "/learn"
            }
        ]

        return PlanTrack(
            **self.TRACK_TEMPLATES["deep"],
            modules=modules,
            success_factors=[
                "Commit to structured learning program",
                "Build comprehensive portfolio",
                "Gain real-world experience through projects",
                "Develop strong professional network",
                "Consider formal certification or degree"
            ]
        )


class AIService:
    """
    Main AI service with provider selection and fallback.
    """

    def __init__(self):
        self.provider = self._initialize_provider()

    def _initialize_provider(self) -> AIProvider:
        """Initialize provider based on config."""
        provider_name = settings.ai_provider.lower()

        if provider_name == "openai" and settings.openai_api_key:
            try:
                return OpenAIProvider(settings.openai_api_key)
            except Exception as e:
                print(f"OpenAI init failed: {e}, falling back to rules")
                return RulesBasedProvider()

        # TODO: Add DeepInfra, Groq providers as needed

        # Default to rules-based
        print("Using rules-based plan generator")
        return RulesBasedProvider()

    async def generate_career_plan(
        self,
        occupation: str,
        skills: List[str],
        interests: List[str],
        risk_tolerance: str,
        learning_hours: float
    ) -> PersonalPlan:
        """
        Generate personalized career transition plan.

        Args:
            occupation: Current occupation title
            skills: List of current skills
            interests: List of interests/passions
            risk_tolerance: "low", "medium", "high"
            learning_hours: Hours per week available

        Returns:
            PersonalPlan with 3 tracks and resources
        """
        try:
            return await self.provider.generate_plan(
                occupation,
                skills,
                interests,
                risk_tolerance,
                learning_hours
            )
        except Exception as e:
            print(f"AI provider failed: {e}, using rules fallback")
            # Fallback to rules if provider fails
            fallback = RulesBasedProvider()
            return await fallback.generate_plan(
                occupation,
                skills,
                interests,
                risk_tolerance,
                learning_hours
            )


# Global service instance
ai_service = AIService()
