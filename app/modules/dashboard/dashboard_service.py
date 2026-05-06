from sqlmodel import Session

from app.modules.activity_logs.activity_repository import ActivityLogRepository
from app.modules.archive_entries.archive_entry_repository import ArchiveEntryRepository
from app.modules.dashboard.dashboard_mapper import (
    build_dashboard_stats_response,
    map_dashboard_activity,
    map_featured_entry,
    map_recent_entry,
    map_timeline_item,
    map_top_rated_entry,
)
from app.modules.dashboard.dashboard_schemas import DashboardStatsResponse
from app.modules.personal_ratings.rating_repository import RatingRepository


class DashboardService:
    def __init__(self, session: Session):
        self.session = session
        self.archive_repository = ArchiveEntryRepository(session)
        self.rating_repository = RatingRepository(session)
        self.activity_repository = ActivityLogRepository(session)

    def get_dashboard_stats(self) -> DashboardStatsResponse:
        total_entries = self.archive_repository.count()
        average_rating = self._get_average_rating()
        top_ratings = self.rating_repository.list_top(n=5)
        recent_entries = self.archive_repository.get_recent(n=5)
        latest_entry = recent_entries[0] if recent_entries else None
        recent_activity = self.activity_repository.list_recent(n=10)

        return build_dashboard_stats_response(
            total_entries=total_entries,
            average_rating=average_rating,
            best_rated_entry=self._map_best_rated_entry(top_ratings),
            latest_entry=map_featured_entry(latest_entry),
            recent_entries=[map_recent_entry(entry) for entry in recent_entries],
            release_timeline=[
                map_timeline_item(release_year, total)
                for release_year, total in self.archive_repository.count_by_release_year()
            ],
            top_rated_entries=self._map_top_rated_entries(top_ratings),
            recent_activity=[map_dashboard_activity(log) for log in recent_activity],
        )

    def _get_average_rating(self) -> float | None:
        average = self.rating_repository.get_average_score()
        if average is None:
            return None

        return round(average, 1)

    def _map_best_rated_entry(self, top_ratings: list):
        if not top_ratings:
            return None

        rating = top_ratings[0]
        entry = self.archive_repository.get_by_id(rating.series_id)
        return map_featured_entry(entry, rating_score=float(rating.score)) if entry else None

    def _map_top_rated_entries(self, top_ratings: list):
        items = []
        for rating in top_ratings:
            entry = self.archive_repository.get_by_id(rating.series_id)
            if entry is not None:
                items.append(map_top_rated_entry(entry, rating_score=float(rating.score)))

        return items
