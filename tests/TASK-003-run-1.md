---
task: TASK-003
run: 1
verdict: PASS
tested_sha: a8b6f11
merge_commit: a8b6f11
updated: 2026-09-24 10:09
---

# TASK-003 Test Run 1

- Tested: `main` @ `a8b6f11` (contains `merge_commit` a8b6f11)
- Build/tests: `./mvnw -q verify` PASS (53 tests)

| AC | Result | Evidence |
|----|--------|----------|
| AC-001 | PASS | `GET http://localhost:18081/api/v1/articles` → 200 `total=3` items newest-first, each has `slug`, `title`, `excerpt`, `publishedAt`. `?page=1&size=2` → 200 2 items `total=3`. `?page=2&size=2` → 200 remaining 1 (`chon-moi-cau-chep-mua-lanh`). |
| AC-002 | PASS | `GET /api/v1/articles/bao-quan-moi-cau-sau-khi-mo-bao` → 200 `title`, `content`, `imageUrl=/placeholders/article.svg`, `prevSlug=chon-moi-cau-chep-mua-lanh` (older), `nextSlug=chuan-bi-can-cau-buoi-som` (newer). Newest `nextSlug=null`; oldest `prevSlug=null`. `GET /api/v1/articles/khong-ton-tai` → 404 `{"detail":"Article not found","status":404,"title":"Not Found"}`. |
| AC-003 | PASS | `GET /api/v1/pages/{about,contact,shipping,privacy,warranty,terms,shopping-guide}` each 200 `{slug,title,body}` matching design §7 titles. `GET /api/v1/pages/khong-ton-tai` → 404 `{"detail":"Page not found","status":404}`. |
| AC-004 | PASS | `GET /api/v1/shop/settings` → 200 `{"shopName":"Mồi Câu Shop","hotline":"0123 456 789","email":"shop@example.com","zaloUrl":"https://zalo.me/0123456789","freeShipFromVnd":200000}` (design §7 defaults; no `SHOP_*` override). |
| AC-005 | PASS | `POST /api/v1/contact` `{"name":"An","email":"an@example.com","phone":"0900000001","message":"Hỏi hàng"}` → 202 `{"accepted":true}`. Blank name, name len 81, phone len 31, message len 2001 → 400 ProblemDetail `{"status":400,"title":"Bad Request","detail":"Invalid request content."}`. No mail/smtp lines in app log (validate-and-ack only). |

Exploratory:
- `size=60` → 200; `size=61` → 400 `Validation failure`; `page=0` → 400.
- Invalid email / empty `{}` → 400 ProblemDetail.
- TASK-002 regression: `/api/v1/categories` 200 two-level tree; `/api/v1/products?size=5` 200 `total=18`.
- TASK-001 regression: `/actuator/health` 200 UP; `/api/v1/does-not-exist` 404 ProblemDetail, no stack.
- Flyway V1–V5 applied; 3 articles, 7 pages.
- shop-service left clean on `main`; port 18081 free after stop.

Bug (FAIL): n/a
