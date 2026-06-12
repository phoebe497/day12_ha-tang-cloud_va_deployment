# Deployment Information

## Public URL
https://day12ha-tang-cloudvadeployment-production-84af.up.railway.app

## Platform
Railway

## Test Commands

### 1. Health Check (Liveness Probe)
```bash
curl https://day12ha-tang-cloudvadeployment-production-84af.up.railway.app/health
```
**Expected Response:**
```json
{
  "status": "ok",
  "version": "1.0.1",
  "environment": "production",
  "uptime_seconds": 124.5,
  "total_requests": 2,
  "checks": {
    "llm": "mock"
  },
  "timestamp": "2026-06-12T11:46:12.345678+00:00"
}
```

### 2. Readiness Check
```bash
curl https://day12ha-tang-cloudvadeployment-production-84af.up.railway.app/ready
```
**Expected Response:**
```json
{
  "ready": true
}
```

### 3. API Test (with X-API-Key authentication)
```bash
curl -X POST https://day12ha-tang-cloudvadeployment-production-84af.up.railway.app/ask \
  -H "X-API-Key: bfa6864068eb7a136d7f8d94d73abefa7089c1bb0fdc67643f9c3d61a2a72bf3" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```
**Expected Response:**
```json
{
  "question": "What is Docker?",
  "answer": "This is a mock response from the LLM for: What is Docker?",
  "model": "gpt-4o-mini",
  "timestamp": "2026-06-12T11:47:00.123456+00:00"
}
```

### 4. API Test without authentication (Should fail)
```bash
curl -X POST https://day12ha-tang-cloudvadeployment-production-84af.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```
**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Invalid or missing API key. Include header: X-API-Key: <key>"
}
```

---

## Environment Variables Set
- `PORT`: `8000` (được Railway tự động map cho cổng container)
- `ENVIRONMENT`: `production`
- `DEBUG`: `false`
- `AGENT_API_KEY`: `bfa6864068eb7a136d7f8d94d73abefa7089c1bb0fdc67643f9c3d61a2a72bf3`
- `JWT_SECRET`: `dev-jwt-secret-change-in-production`
- `DAILY_BUDGET_USD`: `10.0`
- `RATE_LIMIT_PER_MINUTE`: `20`

---

## Screenshots
- [Deployment dashboard](screenshots/Deployment%20dashboard.png)
- [Service running](screenshots/Service%20running.png)
- [Test results](screenshots/Test%20results.png)
