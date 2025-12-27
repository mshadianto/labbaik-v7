"""
LABBAIK AI - Geo Clustering & Dedup V1.2
========================================
Deduplicate hotels with different names but same location.
"""

import math
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from difflib import SequenceMatcher

from .name_norm import normalize_name, similarity_score


@dataclass
class GeoPoint:
    """Geographic point."""
    lat: float
    lon: float

    def is_valid(self) -> bool:
        """Check if coordinates are valid."""
        return (
            self.lat is not None and
            self.lon is not None and
            -90 <= self.lat <= 90 and
            -180 <= self.lon <= 180
        )


@dataclass
class HotelCluster:
    """A cluster of similar/duplicate hotels."""
    cluster_id: str
    city: str
    representative_id: str
    representative_name: str
    members: List[dict] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    confidence: float = 0.0


def haversine_distance(
    lat1: float, lon1: float,
    lat2: float, lon2: float
) -> float:
    """
    Calculate distance between two points in meters.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in meters
    """
    R = 6371000  # Earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) *
        math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def address_similarity(addr1: str, addr2: str) -> float:
    """
    Calculate address similarity score.

    Args:
        addr1: First address
        addr2: Second address

    Returns:
        Similarity score 0.0 to 1.0
    """
    if not addr1 or not addr2:
        return 0.0

    # Normalize addresses
    a1 = normalize_name(addr1)
    a2 = normalize_name(addr2)

    if a1 == a2:
        return 1.0

    # Check if one contains the other
    if a1 in a2 or a2 in a1:
        return 0.85

    return SequenceMatcher(None, a1, a2).ratio()


def is_duplicate_candidate(
    hotel_a: dict,
    hotel_b: dict,
    name_threshold: float = 0.75,
    geo_threshold_m: float = 100,
    address_threshold: float = 0.7
) -> Tuple[bool, List[str], float]:
    """
    Check if two hotels are potential duplicates.

    Args:
        hotel_a: First hotel dict
        hotel_b: Second hotel dict
        name_threshold: Min name similarity (0-1)
        geo_threshold_m: Max distance in meters
        address_threshold: Min address similarity (0-1)

    Returns:
        (is_duplicate, reasons, confidence)
    """
    reasons = []
    scores = []

    # 1. Name similarity
    name_a = hotel_a.get("name", "")
    name_b = hotel_b.get("name", "")
    name_sim = similarity_score(name_a, name_b)

    if name_sim >= name_threshold:
        reasons.append(f"Name similarity: {name_sim:.2f}")
        scores.append(name_sim)

    # 2. Geo distance
    lat_a = hotel_a.get("lat") or hotel_a.get("latitude")
    lon_a = hotel_a.get("lon") or hotel_a.get("longitude")
    lat_b = hotel_b.get("lat") or hotel_b.get("latitude")
    lon_b = hotel_b.get("lon") or hotel_b.get("longitude")

    geo_match = False
    if all([lat_a, lon_a, lat_b, lon_b]):
        try:
            distance = haversine_distance(
                float(lat_a), float(lon_a),
                float(lat_b), float(lon_b)
            )
            if distance <= geo_threshold_m:
                geo_match = True
                geo_score = 1.0 - (distance / geo_threshold_m)
                reasons.append(f"Distance: {distance:.0f}m")
                scores.append(geo_score)
        except (ValueError, TypeError):
            pass

    # 3. Address similarity
    addr_a = hotel_a.get("address", "")
    addr_b = hotel_b.get("address", "")
    addr_sim = address_similarity(addr_a, addr_b)

    if addr_sim >= address_threshold:
        reasons.append(f"Address similarity: {addr_sim:.2f}")
        scores.append(addr_sim)

    # Decision logic
    is_dup = False
    confidence = 0.0

    if len(scores) >= 2:
        # Multiple signals match
        confidence = sum(scores) / len(scores)
        if confidence >= 0.7:
            is_dup = True
    elif name_sim >= 0.9:
        # Very high name match alone
        is_dup = True
        confidence = name_sim
    elif geo_match and name_sim >= 0.6:
        # Close location + reasonable name match
        is_dup = True
        confidence = 0.8

    return is_dup, reasons, confidence


def find_clusters(
    hotels: List[dict],
    city: str,
    name_threshold: float = 0.75,
    geo_threshold_m: float = 100
) -> List[HotelCluster]:
    """
    Find clusters of duplicate hotels.

    Args:
        hotels: List of hotel dicts with name, lat, lon, address
        city: City name (MAKKAH/MADINAH)
        name_threshold: Min name similarity
        geo_threshold_m: Max distance in meters

    Returns:
        List of HotelCluster objects
    """
    clusters = []
    used: Set[str] = set()

    for i, hotel_a in enumerate(hotels):
        hotel_id_a = hotel_a.get("hotel_id") or hotel_a.get("id") or str(i)

        if hotel_id_a in used:
            continue

        # Start new cluster
        cluster_members = [hotel_a]
        cluster_reasons = []
        used.add(hotel_id_a)

        # Find matches
        for j, hotel_b in enumerate(hotels[i + 1:], start=i + 1):
            hotel_id_b = hotel_b.get("hotel_id") or hotel_b.get("id") or str(j)

            if hotel_id_b in used:
                continue

            is_dup, reasons, confidence = is_duplicate_candidate(
                hotel_a, hotel_b,
                name_threshold=name_threshold,
                geo_threshold_m=geo_threshold_m
            )

            if is_dup:
                cluster_members.append(hotel_b)
                cluster_reasons.extend(reasons)
                used.add(hotel_id_b)

        # Only create cluster if there are duplicates
        if len(cluster_members) > 1:
            # Choose representative (prefer one with more data)
            def data_score(h):
                score = 0
                if h.get("lat") and h.get("lon"):
                    score += 2
                if h.get("address"):
                    score += 1
                if h.get("amenities"):
                    score += 1
                if h.get("star_rating"):
                    score += 1
                return score

            rep = max(cluster_members, key=data_score)
            rep_id = rep.get("hotel_id") or rep.get("id")

            cluster = HotelCluster(
                cluster_id=f"cluster_{rep_id}",
                city=city.upper(),
                representative_id=rep_id,
                representative_name=rep.get("name", ""),
                members=cluster_members,
                reasons=list(set(cluster_reasons)),
                confidence=sum(1 for _ in cluster_members) / len(cluster_members)
            )
            clusters.append(cluster)

    return clusters


def merge_hotel_data(hotels: List[dict]) -> dict:
    """
    Merge data from multiple duplicate hotels.

    Args:
        hotels: List of duplicate hotel dicts

    Returns:
        Merged hotel dict with best data from each
    """
    if not hotels:
        return {}

    if len(hotels) == 1:
        return hotels[0].copy()

    # Start with first hotel
    merged = hotels[0].copy()

    for hotel in hotels[1:]:
        # Prefer non-empty values
        for key, value in hotel.items():
            if value and not merged.get(key):
                merged[key] = value

        # Collect all provider IDs
        if "provider_ids" not in merged:
            merged["provider_ids"] = {}

        provider = hotel.get("provider", "unknown")
        provider_id = hotel.get("provider_id") or hotel.get("hotel_id")
        if provider_id:
            merged["provider_ids"][provider] = provider_id

        # Merge amenities
        if hotel.get("amenities"):
            existing = merged.get("amenities", "")
            new = hotel.get("amenities", "")
            merged["amenities"] = f"{existing} {new}".strip()

    # Mark as merged
    merged["is_merged"] = True
    merged["merged_count"] = len(hotels)

    return merged


def get_cluster_summary(cluster: HotelCluster) -> dict:
    """
    Get summary info for a cluster.

    Args:
        cluster: HotelCluster object

    Returns:
        Summary dict
    """
    return {
        "cluster_id": cluster.cluster_id,
        "city": cluster.city,
        "representative": {
            "id": cluster.representative_id,
            "name": cluster.representative_name,
        },
        "member_count": len(cluster.members),
        "member_names": [m.get("name") for m in cluster.members],
        "reasons": cluster.reasons,
        "confidence": cluster.confidence,
        "action": "review" if cluster.confidence < 0.8 else "auto_merge",
    }


def deduplicate_hotels(
    hotels: List[dict],
    city: str,
    auto_merge: bool = True,
    confidence_threshold: float = 0.8
) -> Tuple[List[dict], List[HotelCluster]]:
    """
    Deduplicate hotel list.

    Args:
        hotels: List of hotel dicts
        city: City name
        auto_merge: Whether to auto-merge high-confidence duplicates
        confidence_threshold: Min confidence for auto-merge

    Returns:
        (deduplicated_hotels, clusters)
    """
    clusters = find_clusters(hotels, city)

    if not auto_merge:
        return hotels, clusters

    # Get IDs to remove (merged into representative)
    merged_ids: Set[str] = set()
    merged_hotels = []

    for cluster in clusters:
        if cluster.confidence >= confidence_threshold:
            # Merge this cluster
            merged = merge_hotel_data(cluster.members)
            merged_hotels.append(merged)

            # Mark member IDs for removal
            for member in cluster.members:
                member_id = member.get("hotel_id") or member.get("id")
                if member_id != cluster.representative_id:
                    merged_ids.add(member_id)

    # Build deduplicated list
    result = []
    seen_ids: Set[str] = set()

    for hotel in hotels:
        hotel_id = hotel.get("hotel_id") or hotel.get("id")

        if hotel_id in merged_ids:
            continue

        if hotel_id in seen_ids:
            continue

        # Check if this is a merged representative
        merged_version = next(
            (m for m in merged_hotels if m.get("hotel_id") == hotel_id),
            None
        )

        if merged_version:
            result.append(merged_version)
        else:
            result.append(hotel)

        seen_ids.add(hotel_id)

    return result, clusters
