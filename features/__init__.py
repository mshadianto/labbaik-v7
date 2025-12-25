"""
LABBAIK AI v6.0 - Enhanced Features Package
============================================
New features inspired by PilgrimPal and other leading
Hajj/Umrah apps, optimized for Streamlit.

Features included:
1. Crowd Prediction - Masjid crowd level predictions
2. SOS Emergency - One-tap emergency with WhatsApp
3. Group Tracking - Real-time location sharing
4. 3D Manasik - Interactive ritual simulation
5. Smart Comparison - AI-powered package comparison
6. Analytics Dashboard - Enhanced visitor analytics
7. WhatsApp Service - WAHA integration for notifications
8. Doa Player - Voice-guided doa/dzikir
"""

# Crowd Prediction
from features.crowd_prediction import (
    CrowdPredictor,
    render_crowd_widget,
    render_24h_forecast,
    render_weekly_heatmap,
    render_crowd_prediction_page,
)

# SOS Emergency
from features.sos_emergency import (
    SOSService,
    EmergencyType,
    EmergencyContact,
    render_sos_button,
    render_sos_setup,
    render_sos_activated,
    render_sos_page,
    EMERGENCY_CONTACTS_SAUDI,
)

# Group Tracking
from features.group_tracking import (
    GroupTrackingService,
    TravelGroup,
    GroupMember,
    MemberStatus,
    render_group_tracking_page,
    render_tracking_mini_widget,
    render_member_card,
    create_demo_group,
)

# 3D Manasik
from features.manasik_3d import (
    render_3d_kaaba,
    render_manasik_page,
    render_manasik_mini_widget,
    render_ritual_step_card,
    RITUALS_DATA,
    RitualStep,
)

# Smart Comparison
from features.smart_comparison import (
    render_smart_comparison_page,
    render_package_card,
    render_comparison_table,
    get_sample_packages,
    match_packages,
    PackageDetails,
    UserPreferences,
)

# WhatsApp Service (WAHA)
try:
    from features.whatsapp_service import (
        WAHAClient,
        WhatsAppService,
        MessageTemplates,
        render_whatsapp_status,
        render_whatsapp_test,
        render_whatsapp_settings,
        send_sos_via_whatsapp,
    )
except ImportError:
    pass

# Doa Player
try:
    from features.doa_player import (
        Doa,
        DoaCategory,
        UMRAH_DOAS,
        render_doa_card,
        render_doa_list,
        render_doa_player_page,
        render_doa_mini_widget,
    )
except ImportError:
    pass

# PWA Support
try:
    from features.pwa_support import (
        init_pwa,
        render_install_button,
        render_pwa_settings_page,
        render_offline_indicator,
        PWA_MANIFEST,
        OFFLINE_HTML,
    )
except ImportError:
    pass

__all__ = [
    # Crowd Prediction
    "CrowdPredictor",
    "render_crowd_widget",
    "render_24h_forecast",
    "render_weekly_heatmap",
    "render_crowd_prediction_page",
    
    # SOS Emergency
    "SOSService",
    "EmergencyType",
    "EmergencyContact",
    "render_sos_button",
    "render_sos_setup",
    "render_sos_activated",
    "render_sos_page",
    "EMERGENCY_CONTACTS_SAUDI",
    
    # Group Tracking
    "GroupTrackingService",
    "TravelGroup",
    "GroupMember",
    "MemberStatus",
    "render_group_tracking_page",
    "render_tracking_mini_widget",
    "render_member_card",
    "create_demo_group",
    
    # 3D Manasik
    "render_3d_kaaba",
    "render_manasik_page",
    "render_manasik_mini_widget",
    "render_ritual_step_card",
    "RITUALS_DATA",
    "RitualStep",
    
    # Smart Comparison
    "render_smart_comparison_page",
    "render_package_card",
    "render_comparison_table",
    "get_sample_packages",
    "match_packages",
    "PackageDetails",
    "UserPreferences",
    
    # WhatsApp Service
    "WAHAClient",
    "WhatsAppService",
    "MessageTemplates",
    "render_whatsapp_status",
    "render_whatsapp_test",
    "render_whatsapp_settings",
    "send_sos_via_whatsapp",
    
    # Doa Player
    "Doa",
    "DoaCategory",
    "UMRAH_DOAS",
    "render_doa_card",
    "render_doa_list",
    "render_doa_player_page",
    "render_doa_mini_widget",
    
    # PWA Support
    "init_pwa",
    "render_install_button",
    "render_pwa_settings_page",
    "render_offline_indicator",
    "PWA_MANIFEST",
    "OFFLINE_HTML",
]

# Version
__version__ = "6.0.0"
