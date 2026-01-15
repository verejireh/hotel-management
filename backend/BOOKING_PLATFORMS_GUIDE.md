# Booking Platforms 시트 가이드

## 컬럼 구조

`booking_platforms` 시트에는 다음 4개의 컬럼이 있습니다:

1. **id** - 플랫폼 고유 ID (자동 생성 또는 수동 입력)
2. **name** - 플랫폼 이름 (필수)
3. **api_key** - API 키 (선택사항, 향후 자동 연동용)
4. **webhook_url** - 웹훅 URL (선택사항, 향후 자동 연동용)

## 예시 데이터

### 기본 예시 (최소 정보)

| id | name | api_key | webhook_url |
|----|------|---------|-------------|
| 1 | Airbnb | | |
| 2 | Agoda | | |
| 3 | Hotels.com | | |
| 4 | Rakuten Travel | | |
| 5 | Booking.com | | |
| 6 | Expedia | | |

### 상세 예시 (API 연동 준비)

| id | name | api_key | webhook_url |
|----|------|---------|-------------|
| 1 | Airbnb | airbnb_api_key_12345 | https://your-server.com/webhooks/airbnb |
| 2 | Agoda | agoda_api_key_67890 | https://your-server.com/webhooks/agoda |
| 3 | Hotels.com | hotels_api_key_abcde | https://your-server.com/webhooks/hotels |
| 4 | Rakuten Travel | rakuten_api_key_fghij | https://your-server.com/webhooks/rakuten |

## 사용 방법

1. **최소 설정**: 플랫폼 이름만 입력해도 예약 관리가 가능합니다.
   - 예약 생성 시 `platform_id`로 이 테이블의 `id`를 참조합니다.

2. **향후 확장**: 
   - `api_key`: 각 플랫폼의 API를 통한 자동 예약 동기화용
   - `webhook_url`: 각 플랫폼에서 예약이 생성/변경될 때 알림을 받을 웹훅 URL

## 예약 생성 시 사용

예약을 생성할 때 `platform_id` 필드에 이 테이블의 `id` 값을 사용합니다.

예를 들어:
- Airbnb에서 온 예약 → `platform_id = "1"`
- Agoda에서 온 예약 → `platform_id = "2"`

이렇게 하면 어떤 플랫폼에서 예약이 들어왔는지 추적할 수 있습니다.







