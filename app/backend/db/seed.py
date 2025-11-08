"""
Seed database with initial occupation data.
"""
import csv
import sys
from pathlib import Path
from sqlmodel import Session, select
from app.backend.db.session import engine, init_db
from app.backend.models.occupation import Occupation


def seed_occupations(session: Session, csv_path: Path) -> int:
    """
    Seed occupations from CSV file.

    Args:
        session: Database session
        csv_path: Path to occupations CSV file

    Returns:
        Number of occupations created
    """
    # Check if data already exists
    existing_count = len(session.exec(select(Occupation)).all())
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} occupations. Skipping seed.")
        return 0

    created_count = 0
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            occupation = Occupation(
                soc_code=row['soc_code'],
                title=row['title'],
                sector=row['sector'],
                median_salary=float(row['median_salary']),
                baseline_risk=float(row['baseline_risk']),
                ai_velocity=float(row['ai_velocity']),
                remote_feasibility=float(row['remote_feasibility']),
                creativity_weight=float(row['creativity_weight']),
                social_weight=float(row['social_weight']),
                physical_weight=float(row.get('physical_weight', 0.0)),
                description=row.get('description')
            )
            session.add(occupation)
            created_count += 1

    session.commit()
    print(f"✅ Created {created_count} occupations")
    return created_count


def main():
    """Main seed function."""
    print("🌱 Initializing database...")
    init_db()

    csv_path = Path(__file__).parent.parent.parent.parent / "data" / "occupations.csv"

    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        sys.exit(1)

    print(f"📂 Loading occupations from {csv_path}")

    with Session(engine) as session:
        count = seed_occupations(session, csv_path)

    print(f"🎉 Seed complete! Created {count} occupations")


if __name__ == "__main__":
    main()
