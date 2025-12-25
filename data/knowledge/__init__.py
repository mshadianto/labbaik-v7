"""
LABBAIK AI v6.0 - Knowledge Base Package
========================================
Exports all knowledge base modules for Umrah guidance.
"""

from .umrah_guide import (
    UMRAH_OVERVIEW,
    UMRAH_REQUIREMENTS,
    UMRAH_PREPARATION,
    UMRAH_RITUALS,
    IHRAM_GUIDE,
    TAWAF_GUIDE,
    SAI_GUIDE,
    TAHALLUL_GUIDE,
    get_all_guides,
    get_guide_by_topic,
    search_guides,
)

from .arabic_phrases import (
    ArabicPhrase,
    GREETING_PHRASES,
    IHRAM_PHRASES,
    TAWAF_PHRASES,
    SAI_PHRASES,
    TAHALLUL_PHRASES,
    MOSQUE_PHRASES,
    PRACTICAL_PHRASES,
    NUMBER_PHRASES,
    get_all_phrases,
    get_phrases_by_category,
    get_phrase_categories,
    search_phrases,
    get_phrase_count,
    ARABIC_PHRASES_TEXT,
)

from .faq import (
    FAQ,
    GENERAL_FAQ,
    PREPARATION_FAQ,
    RITUAL_FAQ,
    WOMEN_FAQ,
    HEALTH_FAQ,
    get_all_faqs,
    get_faqs_by_category,
    get_faq_categories,
    search_faqs,
    get_faq_count,
    FAQ_TEXT,
)


# =============================================================================
# COMBINED KNOWLEDGE BASE
# =============================================================================

def get_full_knowledge_base() -> str:
    """
    Get the complete knowledge base as a single text document.
    Useful for RAG indexing.
    
    Returns:
        Complete knowledge base text
    """
    sections = [
        "# PANDUAN UMRAH LENGKAP\n",
        UMRAH_OVERVIEW,
        "\n---\n",
        UMRAH_REQUIREMENTS,
        "\n---\n",
        "# PERSIAPAN UMRAH\n",
        UMRAH_PREPARATION,
        "\n---\n",
        "# TATA CARA IBADAH\n",
        UMRAH_RITUALS,
        "\n---\n",
        "# FRASA BAHASA ARAB\n",
        ARABIC_PHRASES_TEXT,
        "\n---\n",
        "# PERTANYAAN UMUM (FAQ)\n",
        FAQ_TEXT,
    ]
    
    return "\n".join(sections)


def get_knowledge_stats() -> dict:
    """
    Get statistics about the knowledge base.
    
    Returns:
        Dictionary with knowledge base statistics
    """
    all_guides = get_all_guides()
    all_phrases = get_all_phrases()
    all_faqs = get_all_faqs()
    
    return {
        "guides": {
            "total": len(all_guides),
            "topics": list(all_guides.keys()),
        },
        "arabic_phrases": {
            "total": len(all_phrases),
            "categories": get_phrase_categories(),
        },
        "faqs": {
            "total": len(all_faqs),
            "categories": get_faq_categories(),
        },
        "total_items": len(all_guides) + len(all_phrases) + len(all_faqs),
    }


# =============================================================================
# SEARCH FUNCTIONALITY
# =============================================================================

def search_knowledge_base(query: str, limit: int = 10) -> dict:
    """
    Search across all knowledge base content.
    
    Args:
        query: Search query
        limit: Maximum results per category
    
    Returns:
        Dictionary with search results from each category
    """
    results = {
        "guides": [],
        "phrases": [],
        "faqs": [],
    }
    
    # Search guides
    guide_results = search_guides(query)
    for topic, content in guide_results[:limit]:
        results["guides"].append({
            "topic": topic,
            "preview": content[:200] + "..." if len(content) > 200 else content
        })
    
    # Search phrases
    phrase_results = search_phrases(query)
    for phrase in phrase_results[:limit]:
        results["phrases"].append(phrase.to_dict())
    
    # Search FAQs
    faq_results = search_faqs(query)
    for faq in faq_results[:limit]:
        results["faqs"].append(faq.to_dict())
    
    return results


# =============================================================================
# TOPIC CATEGORIES
# =============================================================================

KNOWLEDGE_CATEGORIES = {
    "persiapan": {
        "name": "Persiapan Umrah",
        "icon": "📋",
        "description": "Dokumen, vaksin, dan persiapan sebelum berangkat",
    },
    "ritual": {
        "name": "Tata Cara Ibadah",
        "icon": "🕋",
        "description": "Rukun, wajib, dan sunnah umrah",
    },
    "doa": {
        "name": "Doa & Dzikir",
        "icon": "📿",
        "description": "Doa-doa selama umrah dan ziarah",
    },
    "bahasa": {
        "name": "Bahasa Arab",
        "icon": "🔤",
        "description": "Frasa-frasa penting dalam bahasa Arab",
    },
    "kesehatan": {
        "name": "Kesehatan",
        "icon": "🏥",
        "description": "Tips menjaga kesehatan selama umrah",
    },
    "wanita": {
        "name": "Khusus Wanita",
        "icon": "👩",
        "description": "Panduan khusus untuk jamaah wanita",
    },
}


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # From umrah_guide
    "UMRAH_OVERVIEW",
    "UMRAH_REQUIREMENTS",
    "UMRAH_PREPARATION",
    "UMRAH_RITUALS",
    "IHRAM_GUIDE",
    "TAWAF_GUIDE",
    "SAI_GUIDE",
    "TAHALLUL_GUIDE",
    "get_all_guides",
    "get_guide_by_topic",
    "search_guides",
    # From arabic_phrases
    "ArabicPhrase",
    "GREETING_PHRASES",
    "IHRAM_PHRASES",
    "TAWAF_PHRASES",
    "SAI_PHRASES",
    "TAHALLUL_PHRASES",
    "MOSQUE_PHRASES",
    "PRACTICAL_PHRASES",
    "NUMBER_PHRASES",
    "get_all_phrases",
    "get_phrases_by_category",
    "get_phrase_categories",
    "search_phrases",
    "get_phrase_count",
    "ARABIC_PHRASES_TEXT",
    # From faq
    "FAQ",
    "GENERAL_FAQ",
    "PREPARATION_FAQ",
    "RITUAL_FAQ",
    "WOMEN_FAQ",
    "HEALTH_FAQ",
    "get_all_faqs",
    "get_faqs_by_category",
    "get_faq_categories",
    "search_faqs",
    "get_faq_count",
    "FAQ_TEXT",
    # Combined functions
    "get_full_knowledge_base",
    "get_knowledge_stats",
    "search_knowledge_base",
    "KNOWLEDGE_CATEGORIES",
]
