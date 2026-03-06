# Security & Data Safety Audit (Fast Pass)

- Date: 2026-03-05
- Scope: backend, admin-dashboard, news-engine
- Method: static review + targeted command checks (`npm test`, `npm run lint`, `npm audit`)

## Severity Rubric
- Critical: exploitable now, high blast radius (account takeover, secret compromise, privilege takeover).
- High: serious weakness with practical exploit path or major control bypass.
- Medium: meaningful weakness that needs remediation but lower immediacy.
- Low: hygiene/quality risk that can amplify incidents.
- Informational: non-blocking context.

## Attack Surface Map
- External API surface: Express routes under `/api/*` and `/health`.
- Privileged operations:
  - User management: `/api/users/*`
  - AI provider/API key management: `/api/ai-settings`
  - WordPress publishing and credential validation: `/api/wordpress/*`
  - Manual pipeline execution: `/api/cron/trigger`
- Data stores:
  - PostgreSQL tables including `users`, `websites`, `ai_settings`, `news_logs`.
- Automation/egress:
  - Python pipeline invokes external providers and WordPress; backend can trigger it via `child_process.exec`.

## Findings

### Critical

#### C1. Live X session cookies are committed to git
- Component: news-engine / repository hygiene
- Evidence:
  - `news-engine/x_cookies.json` contains `auth_token`, `ct0`, `kdt`, `att` cookie values (`news-engine/x_cookies.json:1`).
  - `.gitignore` does not ignore this file (`.gitignore:1`).
- Exploit/impact:
  - Session hijack risk for X account tied to scraper automation.
  - Potential unauthorized posting/scraping/account abuse until token expiry/revocation.
- Likelihood: High
- Fix recommendation:
  1. Revoke/rotate impacted X session immediately.
  2. Remove tracked sensitive artifact and purge from git history.
  3. Add ignore rules for runtime artifacts (`x_cookies.json`, debug screenshots, quota state if sensitive).
  4. Add pre-commit secret scanning.
- Verification steps:
  1. `git ls-files | rg 'x_cookies.json'` returns no result.
  2. Confirm new session/cookie generated outside repo or in secrets store.
  3. Secret scanner passes on current HEAD.
- Owner: News Engine
- Effort: 2-4 hours

#### C2. No RBAC on privileged backend routes (auth only)
- Component: backend authorization
- Evidence:
  - Routes use `router.use(requireAuth)` without role checks for user CRUD (`backend/src/routes/users.js:8-23`).
  - Same pattern for cron settings/trigger (`backend/src/routes/cron.js:16`, `backend/src/routes/cron.js:79-153`).
  - Same pattern for AI settings (`backend/src/routes/aiSettings.js:11`, `backend/src/routes/aiSettings.js:50-110`).
- Exploit/impact:
  - Any authenticated account can create/delete users, rotate AI keys, and trigger long-running automation.
  - Full privilege escalation from low-privilege account.
- Likelihood: High
- Fix recommendation:
  1. Implement `requireRole` middleware (e.g., `Super Admin`, `Admin`, `Editor` policy matrix).
  2. Enforce route-level authorization on all privileged endpoints.
  3. Add deny-by-default policy for unknown role claims.
- Verification steps:
  1. Integration tests: non-admin receives `403` on `/api/users`, `/api/ai-settings`, `/api/cron/trigger`.
  2. Admin role can still perform approved operations.
- Owner: Backend API
- Effort: 1-2 days

#### C3. Website credentials are exposed to authenticated users via API responses
- Component: backend data exposure
- Evidence:
  - Website model queries `SELECT *` (`backend/src/models/Website.js:12`, `backend/src/models/Website.js:28`).
  - Controller returns full row in list/get/create/update (`backend/src/controllers/websiteController.js:30`, `backend/src/controllers/websiteController.js:43`, `backend/src/controllers/websiteController.js:57`, `backend/src/controllers/websiteController.js:79`).
  - Table includes `platform_password` and `platform_user` (`backend/src/models/Website.js:35`).
- Exploit/impact:
  - Any authenticated user can retrieve WordPress credentials and pivot into external CMS accounts.
- Likelihood: High
- Fix recommendation:
  1. Introduce response DTOs that exclude secrets by default.
  2. Store platform credentials encrypted at rest; decrypt only at publish-time.
  3. Restrict credential read/write to admin role only.
- Verification steps:
  1. `/api/websites` response no longer contains `platform_password`.
  2. Publish flow still works with decrypt-at-use logic.
  3. Non-admin cannot access credential fields.
- Owner: Backend API
- Effort: 2-3 days

### High

#### H1. Password hashing uses unsalted SHA-256
- Component: backend auth
- Evidence:
  - Password hash implementation is raw SHA-256 (`backend/src/utils/security.js:9-10`).
  - Login compares deterministic hash directly (`backend/src/controllers/authController.js:24-26`).
- Exploit/impact:
  - Fast offline cracking if hashes are leaked.
- Likelihood: Medium-High
- Fix recommendation:
  1. Migrate to `bcrypt`/`argon2id` with strong work factor.
  2. Implement backward-compatible login migration path (rehash on successful login).
- Verification steps:
  1. New users stored with adaptive hash prefix (`$2b$` or argon format).
  2. Existing SHA users successfully migrate on next login.
- Owner: Backend API
- Effort: 1-2 days

#### H2. Insecure auth defaults + weak token storage pattern
- Component: backend + dashboard auth/session
- Evidence:
  - JWT secret fallback is hardcoded (`backend/src/middlewares/auth.js:7`).
  - Frontend stores access token in JS-readable cookie without secure attributes (`admin-dashboard/src/auth/context/jwt/utils.js:5-11`, `admin-dashboard/src/auth/context/jwt/utils.js:14-15`).
- Exploit/impact:
  - Predictable secret risk in misconfigured environments.
  - Token theft via XSS or third-party script compromise.
- Likelihood: Medium-High
- Fix recommendation:
  1. Fail startup if `JWT_SECRET` missing in non-test environments.
  2. Move auth token to HttpOnly/Secure/SameSite cookie issued server-side.
- Verification steps:
  1. App refuses startup with missing secret.
  2. Browser storage no longer exposes bearer token to JS.
- Owner: Backend API + Dashboard
- Effort: 2-4 days

#### H3. Legacy module with hardcoded credentials patterns and raw SQL interpolation is still imported
- Component: news-engine publication path
- Evidence:
  - `app_test.py` imports from `db_for_app.py` (`news-engine/publication/app_test.py:10`).
  - `db_for_app.py` contains hardcoded credential placeholders and raw SQL string interpolation (`news-engine/publication/db_for_app.py:3-6`, `news-engine/publication/db_for_app.py:62`, `news-engine/publication/db_for_app.py:116`).
- Exploit/impact:
  - Increases chance of accidental secret commit and SQL injection if helper functions are reused.
- Likelihood: Medium
- Fix recommendation:
  1. Replace `db_for_app.py` usage with minimal dedicated uploader module.
  2. Remove dead/legacy credential-bearing code from import path.
  3. Parameterize all SQL.
- Verification steps:
  1. `rg "db_for_app"` shows no runtime import.
  2. Security scan finds no raw SQL interpolation in active modules.
- Owner: News Engine
- Effort: 1-2 days

### Medium

#### M1. CORS config uses wildcard origin with credentials enabled
- Component: backend transport policy
- Evidence:
  - `origin: process.env.CORS_ORIGIN || '*'` with `credentials: true` (`backend/src/app.js:23-26`).
- Exploit/impact:
  - Misconfiguration may fail closed in browsers but creates inconsistent and risky cross-origin policy.
- Likelihood: Medium
- Fix recommendation:
  1. Replace wildcard with explicit allowlist.
  2. Validate `Origin` dynamically against known domains.
- Verification steps:
  1. Unauthorized origins rejected.
  2. Approved dashboard origin works in browser.
- Owner: Backend API
- Effort: 2-4 hours

#### M2. Frontend production dependency set has known vulnerabilities
- Component: admin-dashboard dependencies
- Evidence:
  - `npm audit --omit=dev --json` reports 8 vulns (4 high, 1 moderate, 3 low), including `serialize-javascript` and `minimatch` transitive paths.
- Exploit/impact:
  - Supply-chain risk; impact depends on runtime execution paths.
- Likelihood: Medium
- Fix recommendation:
  1. Upgrade affected dependency chain; remove deprecated `next-cookie` if possible.
  2. Add audit gate in CI with approved temporary exceptions only.
- Verification steps:
  1. `npm audit --omit=dev` returns zero high/critical for dashboard.
- Owner: Dashboard
- Effort: 0.5-1 day

### Low

#### L1. Security confidence is low due to minimal automated coverage and unstable lint baseline
- Component: repo-wide quality posture
- Evidence:
  - Backend tests: only one health test exists and passes.
  - Dashboard lint currently reports 654 issues (464 errors, 190 warnings).
- Exploit/impact:
  - Regressions and security fixes are harder to validate safely.
- Likelihood: High
- Fix recommendation:
  1. Add focused security integration tests first (auth/authz/secret redaction).
  2. Freeze current lint debt baseline and enforce no-new-errors policy.
- Verification steps:
  1. New security tests run in CI and fail on regression.
- Owner: Backend + Dashboard
- Effort: 2-4 days (initial baseline)

### Informational
- Backend production dependency audit currently returns zero prod vulnerabilities.
- Backend health test passes locally.

## 30-Day Remediation Backlog

### Quick Wins (same day)
1. Revoke X session tokens and remove `x_cookies.json` from tracking/history.
2. Add ignore rules for runtime artifacts and screenshots.
3. Block non-admin access to `/api/users`, `/api/ai-settings`, `/api/cron/*` with temporary middleware.
4. Remove JWT fallback secret in non-test runtime.
5. Redact `platform_password` from website API responses.

### Short-Term (1 week)
1. Implement full RBAC policy and tests.
2. Migrate password hashing to bcrypt/argon2id with phased backward compatibility.
3. Encrypt website and AI secrets at rest; decrypt only when needed.
4. Replace client-readable bearer cookie model with server-issued HttpOnly session/token cookie.
5. Remove `db_for_app.py` from runtime path and delete legacy insecure helpers.
6. Reduce dashboard dependency vulnerabilities to zero high/critical.

### Hardening (2-4 weeks)
1. Centralized secret management (vault/KMS) and key rotation runbook.
2. Security CI gates: secret scanning, dependency auditing, authz tests.
3. Add structured audit logs for privileged endpoints (`users`, `ai-settings`, `cron`, `wordpress`).
4. Add rate limits and abuse controls on trigger and auth endpoints.

## Gate-to-Release Checklist (Must-Fix Before Production Changes)
- [ ] C1 fixed: repository contains no live credential/session artifacts.
- [ ] C2 fixed: RBAC enforced for all privileged routes; unauthorized tests pass.
- [ ] C3 fixed: secrets/credentials are not exposed via API responses.
- [ ] H1 fixed: no new SHA-256 password writes; migration path active.
- [ ] H2 fixed: no insecure JWT fallback in production; token inaccessible to JS.
- [ ] M2 partially fixed: no high/critical prod dependency vulnerabilities in dashboard.

## Residual Risk Statement
If fixes are deferred, current exposure includes privilege escalation by any authenticated user, potential external CMS/X account compromise, and weak credential protections. The system should be treated as non-compliant for internet-facing production use until Critical findings are remediated.

## Unknowns / Follow-Up Required
1. Whether the committed X cookies are still active at audit-read time.
2. Current production role model requirements beyond Admin/Editor labels.
3. Whether `platform_password` values are currently plaintext for all rows or mixed encrypted/plaintext.
4. Runtime deployment hardening (WAF/rate-limit/proxy headers) was not fully audited in this pass.
