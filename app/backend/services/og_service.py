"""
OG (Open Graph) image generation service.

Creates shareable social media images with user results.
"""
import os
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from app.backend.core.config import settings


class OGImageService:
    """Generate Open Graph images for sharing."""

    # Image dimensions for social sharing
    WIDTH = 1200
    HEIGHT = 630

    # Brand colors
    BG_COLOR = (15, 17, 21)  # Charcoal #0F1115
    TEXT_COLOR = (247, 247, 245)  # Off-white #F7F7F5
    ACCENT_COLOR = (90, 169, 255)  # Electric blue #5AA9FF
    MINT_COLOR = (100, 251, 210)  # Neon mint #64FBD2

    def __init__(self):
        """Initialize service."""
        # Create output directory if needed
        self.output_dir = Path(__file__).parent.parent / "static" / "og_images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_result_card(
        self,
        user_id: int,
        occupation: str,
        band: str,
        eta_years: int,
        dividend_y10: float
    ) -> str:
        """
        Generate OG image for user results.

        Args:
            user_id: User ID for filename
            occupation: Occupation title
            band: Risk band (Low/Medium/High)
            eta_years: Years to automation
            dividend_y10: 10-year dividend projection

        Returns:
            URL path to generated image
        """
        # Create image
        img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.BG_COLOR)
        draw = ImageDraw.Draw(img)

        try:
            # Try to load custom fonts (may not exist in Docker)
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except Exception:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Logo/title area
        draw.text(
            (60, 60),
            "LIFE AFTER AI",
            fill=self.ACCENT_COLOR,
            font=subtitle_font
        )

        # Occupation
        occupation_text = self._truncate_text(occupation, 30)
        draw.text(
            (60, 150),
            occupation_text,
            fill=self.TEXT_COLOR,
            font=title_font
        )

        # Risk band with color
        band_color = self._get_band_color(band)
        draw.text(
            (60, 260),
            f"Automation Risk: {band}",
            fill=band_color,
            font=body_font
        )

        # ETA
        draw.text(
            (60, 320),
            f"Timeline: ~{eta_years} years",
            fill=self.TEXT_COLOR,
            font=body_font
        )

        # Dividend projection
        draw.text(
            (60, 400),
            f"Potential AIDE (10y): ${dividend_y10:,.0f}/year",
            fill=self.MINT_COLOR,
            font=body_font
        )

        # Footer CTA
        draw.text(
            (60, 530),
            "Get your personalized plan at lifeafterai.com",
            fill=(150, 150, 150),
            font=small_font
        )

        # Decorative elements (simple gradient bars)
        for i in range(5):
            alpha = int(255 * (1 - i / 5))
            color = (*self.ACCENT_COLOR, alpha) if i % 2 == 0 else (*self.MINT_COLOR, alpha)
            # Note: PIL doesn't support alpha in basic mode, so we skip this
            # In production, use RGBA mode and composite

        # Save image
        filename = f"result_{user_id}_{occupation[:20].replace(' ', '_')}.png"
        filepath = self.output_dir / filename
        img.save(filepath, 'PNG', optimize=True)

        # Return URL path
        return f"/static/og_images/{filename}"

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text with ellipsis."""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

    def _get_band_color(self, band: str) -> tuple:
        """Get color for risk band."""
        if band == "Low":
            return (100, 251, 210)  # Mint
        elif band == "Medium":
            return (255, 193, 7)  # Amber
        else:  # High
            return (255, 87, 34)  # Red-orange


# Global service instance
og_service = OGImageService()
