"""
LABBAIK AI v6.0 - Analytics Module
==================================
Real-time visitor tracking and analytics.
"""

from .tracker import (
    AnalyticsTracker,
    get_analytics_tracker,
    track_page,
    get_visitor_stats,
    with_analytics
)

__all__ = [
    "AnalyticsTracker",
    "get_analytics_tracker",
    "track_page", 
    "get_visitor_stats",
    "with_analytics"
]
