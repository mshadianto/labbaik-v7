"""
LABBAIK AI - Pricing & Currency Service
=======================================
Multi-currency conversion and price formatting.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Tuple
from datetime import datetime, date
from dataclasses import dataclass


@dataclass
class FXRate:
    """Exchange rate data."""
    base: str
    quote: str
    rate: Decimal
    asof_date: date
    source: str = "manual"


# Default exchange rates (updated periodically)
# Base rates to SAR (Saudi Riyal)
DEFAULT_FX_RATES: Dict[str, Decimal] = {
    "SAR": Decimal("1.0"),
    "USD": Decimal("3.75"),      # 1 USD = 3.75 SAR
    "EUR": Decimal("4.10"),      # 1 EUR = 4.10 SAR
    "GBP": Decimal("4.75"),      # 1 GBP = 4.75 SAR
    "IDR": Decimal("0.000235"),  # 1 IDR = 0.000235 SAR
    "MYR": Decimal("0.85"),      # 1 MYR = 0.85 SAR
    "SGD": Decimal("2.80"),      # 1 SGD = 2.80 SAR
    "AED": Decimal("1.02"),      # 1 AED = 1.02 SAR
    "EGP": Decimal("0.076"),     # 1 EGP = 0.076 SAR
    "PKR": Decimal("0.0135"),    # 1 PKR = 0.0135 SAR
    "BDT": Decimal("0.032"),     # 1 BDT = 0.032 SAR
    "INR": Decimal("0.045"),     # 1 INR = 0.045 SAR
    "TRY": Decimal("0.11"),      # 1 TRY = 0.11 SAR
}

# IDR rate for display (1 SAR = X IDR)
SAR_TO_IDR_RATE = Decimal("4250")  # 1 SAR = 4,250 IDR


class PricingService:
    """Currency conversion and pricing utilities."""

    def __init__(self):
        self.fx_rates = DEFAULT_FX_RATES.copy()
        self._last_updated = datetime.now()

    def update_rate(self, currency: str, rate_to_sar: Decimal) -> None:
        """Update exchange rate for a currency."""
        self.fx_rates[currency.upper()] = rate_to_sar
        self._last_updated = datetime.now()

    def get_fx_rate(self, base: str, quote: str = "SAR") -> Optional[Decimal]:
        """
        Get exchange rate from base to quote currency.

        Args:
            base: Source currency code
            quote: Target currency code (default SAR)

        Returns:
            Exchange rate or None if not available
        """
        base = base.upper()
        quote = quote.upper()

        if base == quote:
            return Decimal("1.0")

        # Direct rate to SAR
        if quote == "SAR" and base in self.fx_rates:
            return self.fx_rates[base]

        # Inverse rate from SAR
        if base == "SAR" and quote in self.fx_rates:
            return Decimal("1.0") / self.fx_rates[quote]

        # Cross rate via SAR
        if base in self.fx_rates and quote in self.fx_rates:
            base_to_sar = self.fx_rates[base]
            sar_to_quote = Decimal("1.0") / self.fx_rates[quote]
            return base_to_sar * sar_to_quote

        return None

    def to_sar(self, amount: float, currency: str) -> Optional[float]:
        """
        Convert amount to SAR.

        Args:
            amount: Amount in source currency
            currency: Source currency code

        Returns:
            Amount in SAR or None if conversion failed
        """
        if amount is None:
            return None

        currency = currency.upper()

        if currency == "SAR":
            return float(amount)

        rate = self.get_fx_rate(currency, "SAR")
        if rate is None:
            return None

        result = Decimal(str(amount)) * rate
        return float(result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    def to_idr(self, amount: float, currency: str) -> Optional[float]:
        """
        Convert amount to IDR.

        Args:
            amount: Amount in source currency
            currency: Source currency code

        Returns:
            Amount in IDR or None if conversion failed
        """
        # First convert to SAR
        sar_amount = self.to_sar(amount, currency)
        if sar_amount is None:
            return None

        # Then convert SAR to IDR
        result = Decimal(str(sar_amount)) * SAR_TO_IDR_RATE
        return float(result.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    def from_sar(self, amount_sar: float, target_currency: str) -> Optional[float]:
        """
        Convert SAR amount to target currency.

        Args:
            amount_sar: Amount in SAR
            target_currency: Target currency code

        Returns:
            Amount in target currency or None
        """
        if amount_sar is None:
            return None

        target = target_currency.upper()

        if target == "SAR":
            return float(amount_sar)

        if target == "IDR":
            result = Decimal(str(amount_sar)) * SAR_TO_IDR_RATE
            return float(result.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

        rate = self.get_fx_rate("SAR", target)
        if rate is None:
            return None

        result = Decimal(str(amount_sar)) * rate
        return float(result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# Singleton instance
_pricing_service: Optional[PricingService] = None


def get_pricing_service() -> PricingService:
    """Get singleton PricingService instance."""
    global _pricing_service
    if _pricing_service is None:
        _pricing_service = PricingService()
    return _pricing_service


# Convenience functions
def get_fx_rate(base: str, quote: str = "SAR") -> Optional[Decimal]:
    """Get exchange rate."""
    return get_pricing_service().get_fx_rate(base, quote)


def to_sar(amount: float, currency: str) -> Optional[float]:
    """Convert to SAR."""
    return get_pricing_service().to_sar(amount, currency)


def to_idr(amount: float, currency: str) -> Optional[float]:
    """Convert to IDR."""
    return get_pricing_service().to_idr(amount, currency)


def format_price(
    amount: float,
    currency: str = "SAR",
    show_symbol: bool = True,
    show_decimals: bool = True
) -> str:
    """
    Format price for display.

    Args:
        amount: Price amount
        currency: Currency code
        show_symbol: Whether to show currency symbol
        show_decimals: Whether to show decimal places

    Returns:
        Formatted price string
    """
    if amount is None:
        return "-"

    currency = currency.upper()

    # Currency symbols
    symbols = {
        "SAR": "SAR",
        "IDR": "Rp",
        "USD": "$",
        "EUR": "EUR",
        "GBP": "GBP",
        "MYR": "RM",
        "SGD": "S$",
        "AED": "AED",
    }

    symbol = symbols.get(currency, currency)

    # Format number
    if currency == "IDR":
        # Indonesian format: no decimals, thousand separator with dot
        formatted = f"{int(amount):,}".replace(",", ".")
    else:
        if show_decimals:
            formatted = f"{amount:,.2f}"
        else:
            formatted = f"{int(amount):,}"

    if show_symbol:
        if currency == "IDR":
            return f"{symbol} {formatted}"
        else:
            return f"{formatted} {symbol}"
    else:
        return formatted


def format_price_range(
    min_price: float,
    max_price: float,
    currency: str = "SAR"
) -> str:
    """
    Format price range for display.

    Args:
        min_price: Minimum price
        max_price: Maximum price
        currency: Currency code

    Returns:
        Formatted price range string
    """
    if min_price is None and max_price is None:
        return "-"

    if min_price == max_price or max_price is None:
        return format_price(min_price, currency)

    if min_price is None:
        return f"up to {format_price(max_price, currency)}"

    return f"{format_price(min_price, currency, show_symbol=False)} - {format_price(max_price, currency)}"


def format_price_dual(
    amount: float,
    source_currency: str = "SAR"
) -> str:
    """
    Format price in both SAR and IDR.

    Args:
        amount: Price amount
        source_currency: Source currency

    Returns:
        Formatted string with both currencies
    """
    sar_amount = to_sar(amount, source_currency)
    if sar_amount is None:
        return format_price(amount, source_currency)

    idr_amount = to_idr(amount, source_currency)

    sar_str = format_price(sar_amount, "SAR")
    idr_str = format_price(idr_amount, "IDR") if idr_amount else ""

    if idr_str:
        return f"{sar_str} ({idr_str})"
    return sar_str


def calculate_price_per_night(
    total_price: float,
    nights: int,
    currency: str = "SAR"
) -> Tuple[float, str]:
    """
    Calculate and format price per night.

    Args:
        total_price: Total price
        nights: Number of nights
        currency: Currency code

    Returns:
        Tuple of (per_night_amount, formatted_string)
    """
    if nights <= 0:
        nights = 1

    per_night = total_price / nights
    formatted = format_price(per_night, currency)

    return per_night, f"{formatted}/malam"


def compare_prices(
    price1: float,
    price2: float,
    currency1: str = "SAR",
    currency2: str = "SAR"
) -> Dict:
    """
    Compare two prices and calculate savings.

    Args:
        price1: First price (original/higher)
        price2: Second price (sale/lower)
        currency1: Currency of price1
        currency2: Currency of price2

    Returns:
        Dict with comparison details
    """
    # Convert both to SAR for comparison
    sar1 = to_sar(price1, currency1) or 0
    sar2 = to_sar(price2, currency2) or 0

    if sar1 == 0:
        return {
            "savings_sar": 0,
            "savings_idr": 0,
            "savings_percent": 0,
            "is_cheaper": False,
        }

    savings_sar = sar1 - sar2
    savings_percent = (savings_sar / sar1) * 100 if sar1 > 0 else 0
    savings_idr = to_idr(savings_sar, "SAR") or 0

    return {
        "original_sar": sar1,
        "sale_sar": sar2,
        "savings_sar": round(savings_sar, 2),
        "savings_idr": round(savings_idr),
        "savings_percent": round(savings_percent, 1),
        "is_cheaper": savings_sar > 0,
        "formatted_savings": format_price_dual(savings_sar, "SAR") if savings_sar > 0 else "-",
    }
