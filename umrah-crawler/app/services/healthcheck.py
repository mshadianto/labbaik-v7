"""
LABBAIK AI - Health Check & Observability V1.3
===============================================
Monitor system health, provider coverage, and alert on issues.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class Severity(str, Enum):
    """Alert severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class MetricType(str, Enum):
    """Types of metrics tracked."""
    OFFERS_24H = "offers_24h"
    TRANSPORT_24H = "transport_24h"
    HOTELS_ENRICHED = "hotels_enriched"
    FX_AGE_HOURS = "fx_age_hours"
    SCRAPE_FAIL_PCT = "scrape_fail_pct"
    API_LATENCY_MS = "api_latency_ms"
    PROVIDER_COVERAGE = "provider_coverage"


@dataclass
class AlertRule:
    """Alert rule configuration."""
    name: str
    metric: str
    operator: str  # '<', '>', '<=', '>=', '='
    threshold: float
    severity: Severity = Severity.WARNING
    enabled: bool = True


@dataclass
class Alert:
    """Triggered alert."""
    rule_name: str
    metric: str
    current_value: float
    threshold: float
    severity: Severity
    message: str
    triggered_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Metric:
    """Recorded metric value."""
    provider: str
    metric: str
    value: float
    metadata: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


# Default alert rules
DEFAULT_ALERT_RULES: List[AlertRule] = [
    AlertRule(
        name="low_offers_24h",
        metric=MetricType.OFFERS_24H.value,
        operator="<",
        threshold=50,
        severity=Severity.WARNING
    ),
    AlertRule(
        name="no_transport_24h",
        metric=MetricType.TRANSPORT_24H.value,
        operator="<",
        threshold=1,
        severity=Severity.CRITICAL
    ),
    AlertRule(
        name="fx_stale",
        metric=MetricType.FX_AGE_HOURS.value,
        operator=">",
        threshold=48,
        severity=Severity.WARNING
    ),
    AlertRule(
        name="high_scrape_failures",
        metric=MetricType.SCRAPE_FAIL_PCT.value,
        operator=">",
        threshold=50,
        severity=Severity.CRITICAL
    ),
    AlertRule(
        name="slow_api",
        metric=MetricType.API_LATENCY_MS.value,
        operator=">",
        threshold=5000,
        severity=Severity.WARNING
    ),
]


class HealthCheckService:
    """
    Health check and monitoring service.

    Tracks metrics, evaluates alert rules, and reports system health.
    """

    def __init__(self):
        self._metrics: List[Metric] = []
        self._alerts: List[Alert] = []
        self._alert_rules = list(DEFAULT_ALERT_RULES)
        self._last_check: Optional[datetime] = None

    def add_rule(self, rule: AlertRule):
        """Add custom alert rule."""
        self._alert_rules.append(rule)

    def record_metric(
        self,
        provider: str,
        metric: str,
        value: float,
        metadata: Dict = None
    ):
        """
        Record a metric value.

        Args:
            provider: Provider/system name
            metric: Metric name
            value: Metric value
            metadata: Optional additional data
        """
        m = Metric(
            provider=provider,
            metric=metric,
            value=value,
            metadata=metadata or {}
        )
        self._metrics.append(m)

        # Keep only last 24h of metrics in memory
        cutoff = datetime.utcnow() - timedelta(hours=24)
        self._metrics = [
            x for x in self._metrics
            if x.timestamp > cutoff
        ]

        logger.debug(f"Metric: {provider}/{metric} = {value}")

    def get_metric(self, metric: str, provider: str = None) -> Optional[float]:
        """
        Get latest value for a metric.

        Args:
            metric: Metric name
            provider: Optional provider filter

        Returns:
            Latest metric value or None
        """
        relevant = [
            m for m in self._metrics
            if m.metric == metric and (provider is None or m.provider == provider)
        ]

        if not relevant:
            return None

        # Return most recent
        relevant.sort(key=lambda x: x.timestamp, reverse=True)
        return relevant[0].value

    def check_alerts(self) -> List[Alert]:
        """
        Evaluate all alert rules against current metrics.

        Returns:
            List of triggered alerts
        """
        triggered = []

        for rule in self._alert_rules:
            if not rule.enabled:
                continue

            value = self.get_metric(rule.metric)
            if value is None:
                continue

            if self._evaluate_rule(value, rule.operator, rule.threshold):
                alert = Alert(
                    rule_name=rule.name,
                    metric=rule.metric,
                    current_value=value,
                    threshold=rule.threshold,
                    severity=rule.severity,
                    message=self._format_alert_message(rule, value)
                )
                triggered.append(alert)
                logger.warning(f"Alert: {alert.message}")

        self._alerts = triggered
        self._last_check = datetime.utcnow()
        return triggered

    def _evaluate_rule(
        self,
        value: float,
        operator: str,
        threshold: float
    ) -> bool:
        """Evaluate if a rule condition is met."""
        ops = {
            "<": lambda v, t: v < t,
            ">": lambda v, t: v > t,
            "<=": lambda v, t: v <= t,
            ">=": lambda v, t: v >= t,
            "=": lambda v, t: v == t,
        }
        op_func = ops.get(operator)
        if op_func:
            return op_func(value, threshold)
        return False

    def _format_alert_message(self, rule: AlertRule, value: float) -> str:
        """Format human-readable alert message."""
        return (
            f"[{rule.severity.value}] {rule.name}: "
            f"{rule.metric} = {value:.2f} "
            f"({rule.operator} {rule.threshold})"
        )

    async def run_daily_check(self) -> Dict:
        """
        Run comprehensive daily health check.

        This would typically query the database for actual counts.
        For now, we simulate with in-memory metrics.

        Returns:
            Health check report dict
        """
        # In production, these would be actual DB queries:
        # SELECT COUNT(*) FROM offers WHERE fetched_at > now() - '24h'
        # SELECT COUNT(*) FROM transport_schedule WHERE fetched_at > now() - '24h'
        # etc.

        # Simulate metrics (replace with actual DB queries)
        offers_24h = self.get_metric(MetricType.OFFERS_24H.value) or 0
        transport_24h = self.get_metric(MetricType.TRANSPORT_24H.value) or 0
        hotels_enriched = self.get_metric(MetricType.HOTELS_ENRICHED.value) or 0
        fx_age = self.get_metric(MetricType.FX_AGE_HOURS.value) or 0

        # Record current values
        self.record_metric("system", MetricType.OFFERS_24H.value, offers_24h)
        self.record_metric("system", MetricType.TRANSPORT_24H.value, transport_24h)
        self.record_metric("system", MetricType.HOTELS_ENRICHED.value, hotels_enriched)
        self.record_metric("system", MetricType.FX_AGE_HOURS.value, fx_age)

        # Check alerts
        alerts = self.check_alerts()

        return {
            "ok": len([a for a in alerts if a.severity == Severity.CRITICAL]) == 0,
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "offers_24h": offers_24h,
                "transport_24h": transport_24h,
                "hotels_enriched": hotels_enriched,
                "fx_age_hours": fx_age,
            },
            "alerts": [
                {
                    "name": a.rule_name,
                    "severity": a.severity.value,
                    "message": a.message,
                }
                for a in alerts
            ],
            "alert_count": {
                "info": len([a for a in alerts if a.severity == Severity.INFO]),
                "warning": len([a for a in alerts if a.severity == Severity.WARNING]),
                "critical": len([a for a in alerts if a.severity == Severity.CRITICAL]),
            }
        }

    def get_status_summary(self) -> Dict:
        """Get current status summary."""
        alerts = self._alerts or []
        critical = [a for a in alerts if a.severity == Severity.CRITICAL]
        warnings = [a for a in alerts if a.severity == Severity.WARNING]

        if critical:
            status = "CRITICAL"
            message = f"{len(critical)} critical issue(s)"
        elif warnings:
            status = "WARNING"
            message = f"{len(warnings)} warning(s)"
        else:
            status = "HEALTHY"
            message = "All systems operational"

        return {
            "status": status,
            "message": message,
            "last_check": self._last_check.isoformat() if self._last_check else None,
            "alerts_count": len(alerts),
        }


# Singleton
_health_service: Optional[HealthCheckService] = None


def get_health_service() -> HealthCheckService:
    """Get or create HealthCheckService singleton."""
    global _health_service
    if _health_service is None:
        _health_service = HealthCheckService()
    return _health_service


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def daily_healthcheck() -> Dict:
    """Run daily health check."""
    service = get_health_service()
    return await service.run_daily_check()


def write_metric(provider: str, metric: str, value: float, metadata: Dict = None):
    """Write a metric."""
    service = get_health_service()
    service.record_metric(provider, metric, value, metadata)


def check_alerts() -> List[Alert]:
    """Check all alert rules."""
    service = get_health_service()
    return service.check_alerts()


def get_status() -> Dict:
    """Get current status summary."""
    service = get_health_service()
    return service.get_status_summary()


# =============================================================================
# PROVIDER-SPECIFIC METRICS
# =============================================================================

def record_provider_scrape(
    provider: str,
    success: bool,
    items_count: int = 0,
    latency_ms: float = 0,
    error: str = None
):
    """
    Record a provider scrape attempt.

    Args:
        provider: Provider name (e.g., 'HARAMAIN', 'SAPTCO')
        success: Whether scrape succeeded
        items_count: Number of items scraped
        latency_ms: Request latency
        error: Error message if failed
    """
    service = get_health_service()

    # Record latency
    service.record_metric(
        provider=provider,
        metric=MetricType.API_LATENCY_MS.value,
        value=latency_ms
    )

    # Record success/failure
    service.record_metric(
        provider=provider,
        metric="scrape_success",
        value=1.0 if success else 0.0,
        metadata={"error": error} if error else {}
    )

    # Record item count
    if success and items_count > 0:
        service.record_metric(
            provider=provider,
            metric="items_scraped",
            value=float(items_count)
        )


def record_fx_update(source: str, currencies_count: int, age_hours: float = 0):
    """
    Record FX rate update.

    Args:
        source: 'ECB', 'MANUAL', 'FALLBACK'
        currencies_count: Number of currencies updated
        age_hours: Age of rates in hours
    """
    service = get_health_service()

    service.record_metric(
        provider="fx",
        metric="fx_update",
        value=float(currencies_count),
        metadata={"source": source}
    )

    service.record_metric(
        provider="system",
        metric=MetricType.FX_AGE_HOURS.value,
        value=age_hours
    )
