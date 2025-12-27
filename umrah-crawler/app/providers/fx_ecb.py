"""
LABBAIK AI - ECB FX Fetcher V1.3
================================
Auto-fetch exchange rates from ECB (free, no API key).
EUR as base, cross-rate derivation for SAR/IDR/MYR.
"""

import re
import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Optional, Tuple

import httpx

logger = logging.getLogger(__name__)

# ECB daily rates (XML, free, no auth)
ECB_LATEST_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

# Fallback rates (approximate, updated periodically)
FALLBACK_RATES = {
    "USD": Decimal("1.08"),
    "SAR": Decimal("4.05"),
    "IDR": Decimal("17200"),
    "MYR": Decimal("4.75"),
    "GBP": Decimal("0.86"),
    "AED": Decimal("3.97"),
}


def parse_ecb_xml(xml_text: str) -> Dict[str, Decimal]:
    """
    Parse ECB XML response to extract rates.

    ECB format:
    <Cube currency='USD' rate='1.0843'/>
    <Cube currency='SAR' rate='4.0662'/>

    Returns:
        Dict of currency -> rate (EUR as base)
    """
    rates = {"EUR": Decimal("1.0")}

    # Simple regex parse (avoid XML library overhead)
    pattern = r"currency='([A-Z]{3})'\s+rate='([0-9.]+)'"
    for match in re.finditer(pattern, xml_text):
        currency = match.group(1)
        rate = match.group(2)
        try:
            rates[currency] = Decimal(rate)
        except Exception:
            continue

    return rates


async def fetch_ecb_rates() -> Tuple[Dict[str, Decimal], str]:
    """
    Fetch latest rates from ECB.

    Returns:
        (rates_dict, source) - source is 'ECB' or 'FALLBACK'
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(ECB_LATEST_URL, headers={
                "User-Agent": "labbaik-umrah/1.3",
                "Accept": "application/xml"
            })
            resp.raise_for_status()

            rates = parse_ecb_xml(resp.text)

            if len(rates) > 5:  # ECB typically has 30+ currencies
                logger.info(f"ECB: fetched {len(rates)} currency rates")
                return rates, "ECB"
            else:
                logger.warning("ECB: insufficient rates, using fallback")
                return FALLBACK_RATES, "FALLBACK"

    except Exception as e:
        logger.error(f"ECB fetch failed: {e}, using fallback")
        return FALLBACK_RATES, "FALLBACK"


def cross_rate(
    rates: Dict[str, Decimal],
    from_cur: str,
    to_cur: str
) -> Optional[Decimal]:
    """
    Calculate cross rate using EUR as intermediary.

    Example: USD -> SAR
    1. USD -> EUR = 1 / EUR_USD
    2. EUR -> SAR = EUR_SAR
    3. USD -> SAR = (1 / EUR_USD) * EUR_SAR

    Returns:
        Cross rate or None if currencies not found
    """
    from_cur = from_cur.upper()
    to_cur = to_cur.upper()

    if from_cur == to_cur:
        return Decimal("1.0")

    # Get EUR -> X rates
    eur_to_from = rates.get(from_cur)
    eur_to_to = rates.get(to_cur)

    if eur_to_from is None or eur_to_to is None:
        return None

    # from_cur -> EUR = 1 / (EUR -> from_cur)
    # EUR -> to_cur = eur_to_to
    # from_cur -> to_cur = (1 / eur_to_from) * eur_to_to
    return eur_to_to / eur_to_from


class FXService:
    """FX conversion service with ECB + fallback."""

    def __init__(self):
        self._rates: Dict[str, Decimal] = {}
        self._source: str = "NONE"
        self._last_fetch: Optional[datetime] = None

    async def refresh(self) -> bool:
        """Refresh rates from ECB."""
        self._rates, self._source = await fetch_ecb_rates()
        self._last_fetch = datetime.utcnow()
        return self._source == "ECB"

    @property
    def rates(self) -> Dict[str, Decimal]:
        return self._rates

    @property
    def source(self) -> str:
        return self._source

    @property
    def is_stale(self) -> bool:
        """Check if rates are older than 24 hours."""
        if not self._last_fetch:
            return True
        age_hours = (datetime.utcnow() - self._last_fetch).total_seconds() / 3600
        return age_hours > 24

    def convert(
        self,
        amount: float,
        from_cur: str,
        to_cur: str
    ) -> Optional[float]:
        """
        Convert amount between currencies.

        Args:
            amount: Amount to convert
            from_cur: Source currency (e.g., 'USD')
            to_cur: Target currency (e.g., 'SAR')

        Returns:
            Converted amount or None if conversion not possible
        """
        if amount is None:
            return None

        from_cur = from_cur.upper()
        to_cur = to_cur.upper()

        if from_cur == to_cur:
            return float(amount)

        rate = cross_rate(self._rates, from_cur, to_cur)
        if rate is None:
            logger.warning(f"No rate for {from_cur} -> {to_cur}")
            return None

        return float(Decimal(str(amount)) * rate)

    def to_sar(self, amount: float, currency: str) -> Optional[float]:
        """Convert any currency to SAR."""
        return self.convert(amount, currency, "SAR")

    def to_idr(self, amount: float, currency: str) -> Optional[float]:
        """Convert any currency to IDR."""
        return self.convert(amount, currency, "IDR")

    def format_dual(
        self,
        amount_sar: float,
        show_idr: bool = True
    ) -> str:
        """
        Format price in SAR with optional IDR equivalent.

        Args:
            amount_sar: Amount in SAR
            show_idr: Whether to show IDR equivalent

        Returns:
            Formatted string like "SAR 200 (~Rp 848.000)"
        """
        if amount_sar is None:
            return "N/A"

        sar_str = f"SAR {amount_sar:,.0f}"

        if show_idr:
            idr = self.convert(amount_sar, "SAR", "IDR")
            if idr:
                idr_str = f"Rp {idr:,.0f}".replace(",", ".")
                return f"{sar_str} (~{idr_str})"

        return sar_str


# Singleton instance
_fx_service: Optional[FXService] = None


async def get_fx_service() -> FXService:
    """Get or create FX service singleton."""
    global _fx_service
    if _fx_service is None:
        _fx_service = FXService()
        await _fx_service.refresh()
    elif _fx_service.is_stale:
        await _fx_service.refresh()
    return _fx_service


# Convenience functions
async def to_sar(amount: float, currency: str) -> Optional[float]:
    """Convert to SAR."""
    fx = await get_fx_service()
    return fx.to_sar(amount, currency)


async def to_idr(amount: float, currency: str) -> Optional[float]:
    """Convert to IDR."""
    fx = await get_fx_service()
    return fx.to_idr(amount, currency)


async def format_price_dual(amount_sar: float) -> str:
    """Format SAR with IDR equivalent."""
    fx = await get_fx_service()
    return fx.format_dual(amount_sar)
