# ValidationServices - Postman QA Suite

Postman collection for the CustomerHub **ValidationServices** API (`/api/v1/data-quality`), ready for QA to run by
hand in Postman or unattended in CI with Newman.

**250 requests, about 2,300 automated assertions**, covering name, email, phone, address and profile validation,
plus health checks, request contract, boundary, security and traceability cases.

Every request body is fully filled in with example customer data, so any request can be sent or copied as is.

## Files

| File | What it is |
|---|---|
| `CustomerHub-ValidationServices.postman_collection.json` | The collection (Postman v2.1) |
| `environments/ValidationServices-Local.postman_environment.json` | Local run (`http://localhost:8080`), folder 06 switched on |
| `environments/ValidationServices-DEV.postman_environment.json` | DEV: set `baseUrl` |
| `environments/ValidationServices-TEST.postman_environment.json` | TEST: set `baseUrl` |
| `TEST-CASES.md` | Test case catalog: ID, title, priority, type, expected result |
| `local-seed.sql` | Denylist and store rows used by folder 06 when running locally |

## Collection layout

| Folder | Endpoint | Cases |
|---|---|---|
| 00 Health | `/actuator/health`, liveness, readiness | 4 |
| 01 Name Validation | `POST /validate-name` | 46 |
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
3. Folder 06 is skipped in DEV and TEST until you turn it on (see below).
4. Run **00 Health** first, then the whole collection from the Runner.

### Example customers

| Customer | Caller (brand / store / channel) | Used for |
|---|---|---|
| Michael James Thompson, 1427 Maple Hollow Ln Apt 4B, Katy TX 77494, (713) 482-9156, michael.thompson@gmail.com | TMW / 1102 / POS | Default customer for most cases |
| Sarah Johnson, sarah.johnson@outlook.com | JAB / 0457 / ECOM | Minimal online profile |
| David Lee Martinez, 3150 N Lake Shore Dr Unit 12C, Chicago IL 60657, (312) 846-2290 | KG / 2215 / CSR | Phone-only profile |
| Aisha Nicole Brown, 5419 Vickery Blvd, Dallas TX 75206, (214) 593-8841, aisha.brown@gmail.com | JAB / 0619 / POS | Country inferred from state |
| Liam Patrick O'Connor, 58 Glenview Ave, Toronto ON M4R 1P6, (416) 487-3320, liam.oconnor@rogers.com | MOORES / 7031 / POS | Canadian addresses and phones |
| Oliver George Smith, 14 Elm Park Gardens, London SW10 9NY, +44 20 7946 0958, oliver.smith@btinternet.com | TMW / 9001 / ECOM | International addresses and phones |
| Emily Chen | TMW / 0882 / POS | Address normalisation |

Request IDs are fixed per test: `QA-PROF-001` style on address and profile, `1500010` style numbers on name, email
and phone.

### Reference data (folder 06)

These cases need rows that exist in the database. Their bodies use the values in `local-seed.sql`:

| Value in the bodies | What it must be in your database |
|---|---|
| `Galleria` | A `store_name` in the `store` table |
| `(832) 467-1200` | A `phone_number` in the `store` table |
| `6565 San Felipe Street`, Houston, TX, 77057 | Address of an active selling store (`is_selling_store = 'Y'`) |
| `Acme Corporation` | An active `ORGNAME` row in `validation_denylist` |
| `test` (as in `test@gmail.com`) | An active `EMAIL` row |
| `example.com` | An active `DOMAIN` row |
| `(713) 555-4829` | A number starting with an active `PHONE` prefix (`713555`) |
| `1200 Commerce Street` | An active `ADDRESS` row |
| `99999` | An active `ZIP_CODE` row |

To run them in DEV or TEST, change these values in the folder 06 bodies to ones that exist there, then set
`runReferenceDataTests` to `true` in the environment.

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
with `local-seed.sql`: all 250 requests ran and 2,294 of 2,297 assertions passed. The 3 failures are a real
defect (below), not test errors.

## Issues found while building the suite

| # | Finding | Cases |
|---|---|---|
| 1 | **Security:** `server.error.include-stacktrace: always` in the dev, qa and prod profiles returns full Java stack traces on 404, 405 and 415 errors. It should be `never`. | SEC-002, SEC-003, SEC-004 (fail until fixed) |
| 2 | A denylisted email on `/validate-email` still returns `syntaxValid: true` and "Email is valid"; only `warningCodes` shows the problem. | REF-003, REF-004 |
| 3 | `/validate-name` has no maximum length on name fields (the profile endpoint limits them to 100). | SEC-008 |
| 4 | Roman numeral suffixes come back as `Iii` instead of `III`, and `Ph.D.` is rejected (only `PhD` passes). | NAME-009, NAME-028 |
| 5 | `/validate-address` does not infer a missing country, so US state and ZIP are not checked (`/validate-profile` does infer it). | ADDR-035 |
