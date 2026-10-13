# ValidationServices - Postman QA Suite

Postman collection for the CustomerHub **ValidationServices** API (`/api/v1/data-quality`), ready for QA to run by
hand in Postman or unattended in CI with Newman.

**235 requests, about 2,200 automated assertions**, covering name, email, phone, address and profile validation,
plus health checks, request contract, boundary, security and traceability cases.

## Files

| File | What it is |
|---|---|
| `CustomerHub-ValidationServices.postman_collection.json` | The collection (Postman v2.1) |
| `environments/ValidationServices-Local.postman_environment.json` | Local run (`http://localhost:8080`), reference data pre-filled to match `local-seed.sql` |
| `environments/ValidationServices-DEV.postman_environment.json` | DEV: set `baseUrl` and the `ref*` values |
| `environments/ValidationServices-TEST.postman_environment.json` | TEST: set `baseUrl` and the `ref*` values |
| `TEST-CASES.md` | Test case catalog: ID, title, priority, type, expected result |
| `local-seed.sql` | Denylist and store rows used by the Local environment |

## Collection layout

| Folder | Endpoint | Cases |
|---|---|---|
| 00 Health | `/actuator/health`, liveness, readiness | 4 |
| 01 Name Validation | `POST /validate-name` | 31 |
| 02 Email Validation | `POST /validate-email` | 30 |
| 03 Phone Validation | `POST /validate-phone` | 34 |
| 04 Address Validation | `POST /validate-address` | 37 |
| 05 Profile Validation | `POST /validate-profile` (ACCEPT / WARNINGS / REJECT / contract) | 72 |
| 06 Reference Data | Denylist and store-master rules on every endpoint | 18 |
| 07 Security & Resilience | 404 / 405 / 415, stack-trace leaks, injection input, stability | 9 |

Each request has a description with its test ID, priority (P1 critical path, P2 standard, P3 edge case), type,
objective and expected result.

## How to use

1. In Postman: **Import** the collection and the three environment files.
2. Pick an environment. For DEV and TEST, replace the placeholder `baseUrl` with the real service host
   (no trailing slash).
3. To run folder 06, fill the `ref*` variables with values that exist in that database (see below). Requests whose
   variables are empty are skipped, so the rest of the run is not affected.
4. Run **00 Health** first, then the whole collection from the Runner.

### Reference data variables (folder 06)

| Variable | Value to use |
|---|---|
| `refStoreName` | A `store_name` from the `store` table |
| `refStorePhone` | A `phone_number` from the `store` table |
| `refStoreLine1`, `refStoreCity`, `refStoreState`, `refStorePostalCode` | Address of one active selling store (`is_selling_store = 'Y'`) |
| `refOrgName` | An active `ORGNAME` row in `validation_denylist` |
| `refEmailPrefix` | An active `EMAIL` row without `@` (for example `test`) |
| `refEmailDomain` | An active `DOMAIN` row (for example `example.com`) |
| `refPhonePrefix` | An active `PHONE` row (digits prefix) |
| `refAddressLine1` | An active `ADDRESS` row |
| `refZipCode` | An active `ZIP_CODE` row (5-digit US ZIP) |

### Running locally

```bash
cd ValidationServices
./gradlew bootJar
java -jar build/libs/ValidationServices-0.0.1-SNAPSHOT.jar \
  --spring.profiles.active=local \
  --spring.jpa.defer-datasource-initialization=true \
  --spring.sql.init.mode=always \
  --spring.sql.init.data-locations=file:/path/to/local-seed.sql
```

### Running in CI with Newman

```bash
npm install -g newman newman-reporter-htmlextra
newman run CustomerHub-ValidationServices.postman_collection.json \
  -e environments/ValidationServices-TEST.postman_environment.json \
  --env-var baseUrl=https://<test-host> \
  -r cli,junit,htmlextra \
  --reporter-junit-export results/junit.xml \
  --reporter-htmlextra-export results/report.html
```

## Built-in checks

* Every request sends a fresh `X-Correlation-ID` (`qa-<uuid>`) and fresh request IDs, so runs never collide.
  Profile calls can be traced in the database with
  `SELECT * FROM validation_audit WHERE correlation_id = '<id>';`
* Every response is checked for: time under `slaMs` (default 2000 ms), no 5xx error, JSON content type.

## Verified results

The full collection was run with Newman against the service built from the CDH-238 code, started locally
with `local-seed.sql`: all 235 requests ran and 2,201 of 2,204 assertions passed. The 3 failures are a real
defect (below), not test errors.

## Issues found while building the suite

| # | Finding | Cases |
|---|---|---|
| 1 | **Security:** `server.error.include-stacktrace: always` in the dev, qa and prod profiles returns full Java stack traces on 404, 405 and 415 errors. It should be `never`. | SEC-002, SEC-003, SEC-004 (fail until fixed) |
| 2 | A denylisted email on `/validate-email` still returns `syntaxValid: true` and "Email is valid"; only `warningCodes` shows the problem. | REF-003, REF-004 |
| 3 | `/validate-name` has no maximum length on name fields (the profile endpoint limits them to 100). | SEC-008 |
| 4 | Roman numeral suffixes come back as `Iii` instead of `III`, and `Ph.D.` is rejected (only `PhD` passes). | NAME-009, NAME-028 |
| 5 | `/validate-address` does not infer a missing country, so US state and ZIP are not checked (`/validate-profile` does infer it). | ADDR-035 |
