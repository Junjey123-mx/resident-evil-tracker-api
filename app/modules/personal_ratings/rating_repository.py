from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.modules.personal_ratings.rating_model import Rating


class RatingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: int) -> Optional[Rating]:
        return self.session.get(Rating, id)

    def get_by_series_id(self, series_id: int) -> Optional[Rating]:
        stmt = select(Rating).where(Rating.series_id == series_id)
        return self.session.exec(stmt).first()

    def list_by_series_ids(self, series_ids: list[int]) -> list[Rating]:
        if not series_ids:
            return []

        stmt = select(Rating).where(Rating.series_id.in_(series_ids))
        return list(self.session.exec(stmt).all())

    def list_all(self) -> list[Rating]:
        return list(self.session.exec(select(Rating)).all())

    def list_top(self, n: int = 5) -> list[Rating]:
        stmt = select(Rating).order_by(Rating.score.desc()).limit(n)
        return list(self.session.exec(stmt).all())

    def get_average_score(self) -> float | None:
        result = self.session.exec(select(func.avg(Rating.score)))
        avg = result.one()
        return float(avg) if avg is not None else None

    def count(self) -> int:
        result = self.session.exec(select(func.count()).select_from(Rating))
        return result.one()

    def create(self, data: dict) -> Rating:
        rating = Rating(**data)
        self.session.add(rating)
        self.session.flush()
        self.session.refresh(rating)
        return rating

    def update(self, id: int, data: dict) -> Optional[Rating]:
        rating = self.session.get(Rating, id)
        if rating is None:
            return None
        for attr, value in data.items():
            setattr(rating, attr, value)
        rating.updated_at = datetime.now(timezone.utc)
        self.session.add(rating)
        self.session.flush()
        self.session.refresh(rating)
        return rating

    def delete(self, id: int) -> bool:
        rating = self.session.get(Rating, id)
        if rating is None:
            return False
        self.session.delete(rating)
        self.session.flush()
        return True
