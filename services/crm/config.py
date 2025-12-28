"""
LABBAIK AI - CRM Configuration
===============================
Configuration loader for CRM module.
"""

import os
import yaml
import logging
from typing import Dict, Any, List, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "config",
    "travel_crm.yaml"
)


@lru_cache(maxsize=1)
def load_crm_config() -> Dict[str, Any]:
    """Load CRM configuration from YAML."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load CRM config: {e}")
        return {}


def get_crm_config() -> Dict[str, Any]:
    """Get CRM section of config."""
    return load_crm_config().get("crm", {})


def get_booking_config() -> Dict[str, Any]:
    """Get booking section of config."""
    return load_crm_config().get("booking", {})


def get_payment_config() -> Dict[str, Any]:
    """Get payment section of config."""
    return load_crm_config().get("payment", {})


def get_documents_config() -> Dict[str, Any]:
    """Get documents section of config."""
    return load_crm_config().get("documents", {})


def get_broadcast_config() -> Dict[str, Any]:
    """Get broadcast section of config."""
    return load_crm_config().get("broadcast", {})


def get_analytics_config() -> Dict[str, Any]:
    """Get analytics section of config."""
    return load_crm_config().get("analytics", {})


def get_competitors_config() -> Dict[str, Any]:
    """Get competitors section of config."""
    return load_crm_config().get("competitors", {})


# Helper functions for common lookups
def get_lead_sources() -> List[Dict[str, Any]]:
    """Get lead source options."""
    return get_crm_config().get("lead_sources", [])


def get_lead_statuses() -> List[Dict[str, Any]]:
    """Get lead status options."""
    return get_crm_config().get("lead_statuses", [])


def get_lead_priorities() -> List[Dict[str, Any]]:
    """Get lead priority options."""
    return get_crm_config().get("lead_priorities", [])


def get_activity_types() -> List[Dict[str, Any]]:
    """Get activity type options."""
    return get_crm_config().get("activity_types", [])


def get_booking_statuses() -> List[Dict[str, Any]]:
    """Get booking status options."""
    return get_booking_config().get("statuses", [])


def get_payment_statuses() -> List[Dict[str, Any]]:
    """Get payment status options."""
    return get_booking_config().get("payment_statuses", [])


def get_payment_methods() -> List[Dict[str, Any]]:
    """Get payment method options."""
    return get_payment_config().get("methods", [])


def get_banks() -> List[Dict[str, Any]]:
    """Get bank options."""
    return get_payment_config().get("banks", [])


def get_installment_options() -> List[Dict[str, Any]]:
    """Get installment options."""
    return get_payment_config().get("installment_options", [])


def get_required_documents() -> List[Dict[str, Any]]:
    """Get required documents list."""
    return get_documents_config().get("required", [])


def get_optional_documents() -> List[Dict[str, Any]]:
    """Get optional documents list."""
    return get_documents_config().get("optional", [])


def get_broadcast_templates() -> List[Dict[str, Any]]:
    """Get broadcast message templates."""
    return get_broadcast_config().get("templates", [])


def get_status_label(status_code: str, status_type: str = "lead") -> str:
    """Get status label from code."""
    if status_type == "lead":
        statuses = get_lead_statuses()
    elif status_type == "booking":
        statuses = get_booking_statuses()
    elif status_type == "payment":
        statuses = get_payment_statuses()
    else:
        return status_code

    for s in statuses:
        if s.get("code") == status_code:
            return s.get("label", status_code)
    return status_code


def get_status_color(status_code: str, status_type: str = "lead") -> str:
    """Get status color from code."""
    if status_type == "lead":
        statuses = get_lead_statuses()
    elif status_type == "booking":
        statuses = get_booking_statuses()
    elif status_type == "payment":
        statuses = get_payment_statuses()
    else:
        return "#95a5a6"

    for s in statuses:
        if s.get("code") == status_code:
            return s.get("color", "#95a5a6")
    return "#95a5a6"
