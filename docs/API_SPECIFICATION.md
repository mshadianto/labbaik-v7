# Labbaik AI - API Specification

## Base URL
```
Production: https://api.labbaik.ai/v1
Staging: https://staging-api.labbaik.ai/v1
```

## Authentication
```http
Authorization: Bearer <API_KEY>
X-Agent-ID: <AGENT_ID>
```

---

## 1. AGENT APIs

### Register Agent
```http
POST /agents/register
Content-Type: application/json

{
  "company_name": "PT Travel Berkah",
  "ppiu_number": "123456",
  "email": "admin@travelberkah.com",
  "phone": "+6281234567890",
  "address": "Jakarta, Indonesia"
}

Response:
{
  "agent_id": "AGT-001",
  "api_key": "sk_live_xxxxx",
  "status": "pending_verification"
}
```

### Get Agent Dashboard
```http
GET /agents/dashboard

Response:
{
  "total_jamaah": 150,
  "active_trips": 3,
  "upcoming_trips": 5,
  "revenue_this_month": 75000000,
  "commission_pending": 5000000
}
```

---

## 2. JAMAAH APIs

### Create Jamaah
```http
POST /jamaah
Content-Type: application/json

{
  "full_name": "Ahmad Fauzi",
  "passport_number": "A1234567",
  "passport_expiry": "2028-01-15",
  "phone": "+6281234567890",
  "email": "ahmad@email.com",
  "emergency_contact": {
    "name": "Siti Aminah",
    "phone": "+6289876543210",
    "relation": "spouse"
  },
  "medical_conditions": [],
  "group_id": "GRP-001"
}

Response:
{
  "jamaah_id": "JMH-001",
  "qr_code": "https://api.labbaik.ai/qr/JMH-001",
  "status": "registered"
}
```

### Get Jamaah Location
```http
GET /jamaah/{jamaah_id}/location

Response:
{
  "jamaah_id": "JMH-001",
  "last_location": {
    "lat": 21.4225,
    "lng": 39.8262,
    "accuracy": 10,
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "current_zone": "masjidil_haram",
  "battery_level": 75
}
```

### Bulk Create Jamaah
```http
POST /jamaah/bulk
Content-Type: application/json

{
  "group_id": "GRP-001",
  "jamaah": [
    { "full_name": "Ahmad Fauzi", ... },
    { "full_name": "Siti Aminah", ... }
  ]
}
```

---

## 3. GROUP APIs

### Create Group
```http
POST /groups
Content-Type: application/json

{
  "name": "Umrah Ramadhan 2024 - Batch 1",
  "departure_date": "2024-03-15",
  "return_date": "2024-03-25",
  "package_type": "premium",
  "guide_id": "GDE-001",
  "max_members": 45
}

Response:
{
  "group_id": "GRP-001",
  "invite_code": "BERKAH2024",
  "join_link": "https://app.labbaik.ai/join/BERKAH2024"
}
```

### Get Group Status
```http
GET /groups/{group_id}/status

Response:
{
  "group_id": "GRP-001",
  "name": "Umrah Ramadhan 2024",
  "total_members": 42,
  "checked_in": 40,
  "current_location": "madinah",
  "next_activity": {
    "name": "Ziarah ke Masjid Quba",
    "time": "2024-03-18T08:00:00Z"
  },
  "alerts": []
}
```

### Broadcast Message
```http
POST /groups/{group_id}/broadcast
Content-Type: application/json

{
  "message": "Berkumpul di lobby hotel jam 8 pagi",
  "channels": ["whatsapp", "push", "sms"],
  "priority": "high"
}
```

---

## 4. BOOKING APIs

### Search Hotels
```http
GET /hotels/search?city=MAKKAH&checkin=2024-03-15&checkout=2024-03-20&rooms=2&adults=4

Response:
{
  "hotels": [
    {
      "hotel_id": "HTL-001",
      "name": "Pullman Zamzam Makkah",
      "star_rating": 5,
      "distance_to_haram": "50m",
      "price_per_night": 2500000,
      "currency": "IDR",
      "amenities": ["wifi", "breakfast", "shuttle"],
      "images": ["https://..."],
      "availability": true
    }
  ],
  "total": 25,
  "page": 1
}
```

### Create Hotel Booking
```http
POST /bookings/hotel
Content-Type: application/json

{
  "hotel_id": "HTL-001",
  "checkin": "2024-03-15",
  "checkout": "2024-03-20",
  "rooms": [
    {
      "type": "double",
      "guests": ["JMH-001", "JMH-002"]
    }
  ],
  "special_requests": "High floor, Haram view"
}

Response:
{
  "booking_id": "BKG-001",
  "status": "confirmed",
  "total_price": 12500000,
  "confirmation_code": "PZM-123456"
}
```

### Search Transport
```http
GET /transport/search?from=MAKKAH&to=MADINAH&date=2024-03-18&passengers=4

Response:
{
  "options": [
    {
      "type": "train",
      "operator": "Haramain Railway",
      "departure": "08:00",
      "arrival": "10:30",
      "price": 350000,
      "class": "business"
    },
    {
      "type": "bus",
      "operator": "SAPTCO",
      "departure": "09:00",
      "arrival": "14:00",
      "price": 150000,
      "class": "vip"
    }
  ]
}
```

---

## 5. PERMIT APIs (Nusuk Integration)

### Check Umrah Availability
```http
GET /permits/umrah/availability?date=2024-03-15

Response:
{
  "date": "2024-03-15",
  "slots": [
    { "time": "06:00", "available": 500 },
    { "time": "12:00", "available": 750 },
    { "time": "18:00", "available": 300 }
  ]
}
```

### Book Umrah Permit
```http
POST /permits/umrah
Content-Type: application/json

{
  "jamaah_ids": ["JMH-001", "JMH-002"],
  "date": "2024-03-15",
  "preferred_time": "06:00"
}

Response:
{
  "permit_id": "PRM-001",
  "qr_codes": [
    { "jamaah_id": "JMH-001", "qr": "https://..." },
    { "jamaah_id": "JMH-002", "qr": "https://..." }
  ],
  "valid_from": "2024-03-15T06:00:00Z",
  "valid_until": "2024-03-15T12:00:00Z"
}
```

### Book Rawdah
```http
POST /permits/rawdah
Content-Type: application/json

{
  "jamaah_ids": ["JMH-001"],
  "date": "2024-03-20",
  "gender": "male"
}
```

---

## 6. AI APIs

### Chat with AI Assistant
```http
POST /ai/chat
Content-Type: application/json

{
  "message": "Apa doa saat tawaf?",
  "context": {
    "current_step": "tawaf",
    "language": "id"
  }
}

Response:
{
  "response": "Saat tawaf, disunnahkan membaca doa...",
  "suggested_doas": ["doa_021", "doa_022"],
  "audio_url": "https://api.labbaik.ai/audio/tawaf-doa.mp3"
}
```

### Get Crowd Prediction
```http
GET /ai/crowd-prediction?location=masjidil_haram&date=2024-03-15

Response:
{
  "predictions": [
    { "hour": 6, "level": "low", "percentage": 30 },
    { "hour": 12, "level": "high", "percentage": 85 },
    { "hour": 18, "level": "medium", "percentage": 60 }
  ],
  "best_time": "06:00",
  "recommendation": "Disarankan tawaf sebelum Dhuhr"
}
```

---

## 7. NOTIFICATION APIs

### Send WhatsApp
```http
POST /notifications/whatsapp
Content-Type: application/json

{
  "to": "+6281234567890",
  "template": "booking_confirmation",
  "params": {
    "name": "Ahmad",
    "booking_id": "BKG-001",
    "hotel": "Pullman Zamzam"
  }
}
```

### Send Push Notification
```http
POST /notifications/push
Content-Type: application/json

{
  "jamaah_ids": ["JMH-001", "JMH-002"],
  "title": "Waktunya Tawaf!",
  "body": "Crowd level rendah, waktu terbaik untuk tawaf",
  "data": {
    "action": "open_tawaf_guide"
  }
}
```

---

## 8. WEBHOOK Events

### Register Webhook
```http
POST /webhooks
Content-Type: application/json

{
  "url": "https://yourserver.com/labbaik-webhook",
  "events": [
    "booking.created",
    "booking.cancelled",
    "jamaah.checkin",
    "jamaah.sos",
    "permit.approved"
  ],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload Example
```json
{
  "event": "jamaah.sos",
  "timestamp": "2024-03-15T10:30:00Z",
  "data": {
    "jamaah_id": "JMH-001",
    "jamaah_name": "Ahmad Fauzi",
    "location": { "lat": 21.4225, "lng": 39.8262 },
    "emergency_type": "medical",
    "message": "Butuh bantuan medis"
  }
}
```

---

## 9. ERROR CODES

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Invalid API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Error | Server error |

---

## 10. RATE LIMITS

| Plan | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 10 | 1,000 |
| Starter | 60 | 10,000 |
| Professional | 300 | 100,000 |
| Enterprise | Unlimited | Unlimited |

---

## SDK & Libraries

### Python
```python
pip install labbaik-sdk

from labbaik import LabbaikClient

client = LabbaikClient(api_key="sk_live_xxx")
jamaah = client.jamaah.create(name="Ahmad", ...)
```

### JavaScript
```javascript
npm install @labbaik/sdk

import { Labbaik } from '@labbaik/sdk';

const client = new Labbaik({ apiKey: 'sk_live_xxx' });
const jamaah = await client.jamaah.create({ name: 'Ahmad', ... });
```

### PHP
```php
composer require labbaik/sdk

use Labbaik\Client;

$client = new Client('sk_live_xxx');
$jamaah = $client->jamaah->create(['name' => 'Ahmad', ...]);
```

---

## Support

- Documentation: https://docs.labbaik.ai
- API Status: https://status.labbaik.ai
- Email: api-support@labbaik.ai
