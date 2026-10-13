# ValidationServices - Test Case Catalog

Generated from the Postman collection. One row per request.

**Total cases:** 235


## 00 Health

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| HLT-001 | Health endpoint reports UP | P1 | Smoke | 200 with status UP. |  |
| HLT-002 | Liveness probe reports UP | P2 | Smoke | 200 with status UP. |  |
| HLT-003 | Readiness probe reports UP | P2 | Smoke | 200 with status UP. |  |
| HLT-004 | Health details are not exposed | P3 | Security | 200 and no `components` / `details` block in the body. |  |

## 01 Name Validation

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| NAME-001 | Valid full name with title and suffix | P1 | Positive | 200, valid=true, title normalised to `Dr`, suffix `Jr`, no warning codes. |  |
| NAME-002 | Only required name parts (first + last) | P1 | Positive | 200, valid=true; middleName, title and suffix are null. |  |
| NAME-003 | userId is optional on this endpoint | P3 | Positive | 200, valid=true and userId echoed as null. |  |
| NAME-004 | Whitespace is trimmed and collapsed; all-caps / all-lower is re-cased | P2 | Normalization | First name `Mary Ann`, last name `Smith`. |  |
| NAME-005 | Caps-lock inverted input is re-cased | P2 | Normalization | `jANE dOE` becomes `Jane Doe`. |  |
| NAME-006 | Intentional mixed casing is preserved | P2 | Normalization | `DeShawn McDonald` is returned exactly as entered. |  |
| NAME-007 | Hyphen and typographic apostrophe are accepted and normalised | P2 | Normalization | Curly apostrophe folded to `'`; last name re-cased to `O'Brien-Smith`. |  |
| NAME-008 | Accented / international letters are accepted | P2 | Positive | 200, valid=true, accents preserved. |  |
| NAME-009 | Title and suffix are case-insensitive and lose a trailing period | P2 | Normalization | Title `Mrs`; suffix accepted (returned as `Iii` - see QA note). |  |
| NAME-010 | Every allowed title is accepted | P3 | Positive | 200, valid=true for a random title from MR, MS, MRS, DR, PROF, SIR, MADAM, MISS. |  |
| NAME-011 | Every allowed suffix is accepted | P3 | Positive | 200, valid=true for a random suffix from JR, SR, II, III, IV, V, ESQ, PHD, MD. |  |
| NAME-012 | Single-character first name is a warning, not a rejection | P2 | Warning | 200, valid=true, warningCodes=[SINGLE_CHARACTER_NAME]. |  |
| NAME-013 | Single-character middle initial is a warning | P2 | Warning | 200, valid=true, warningCodes=[SINGLE_CHARACTER_NAME], middle name `A`. |  |
| NAME-014 | Blank optional fields are treated as not provided | P3 | Positive | 200, valid=true; middleName, title and suffix null. |  |
| NAME-020 | Digit in first name is rejected | P1 | Negative | 422, valid=false, warningCodes=[INVALID_CHARACTERS]. |  |
| NAME-021 | Special character in last name is rejected | P1 | Negative | 422, warningCodes=[INVALID_CHARACTERS]. |  |
| NAME-022 | Digit in middle name is rejected | P2 | Negative | 422, warningCodes=[INVALID_CHARACTERS]. |  |
| NAME-023 | HTML / script markup in a name is rejected | P1 | Security | 422, warningCodes=[INVALID_CHARACTERS]; response is JSON, not rendered HTML. |  |
| NAME-024 | Spreadsheet formula prefix is rejected | P2 | Security | 422, warningCodes=[INVALID_CHARACTERS]. |  |
| NAME-025 | Emoji in a name is rejected | P2 | Negative | 422, warningCodes=[INVALID_CHARACTERS]. |  |
| NAME-026 | Unknown title is rejected | P1 | Negative | 422, warningCodes=[INVALID_TITLE]. |  |
| NAME-027 | Unknown suffix is rejected | P1 | Negative | 422, warningCodes=[INVALID_SUFFIX]. |  |
| NAME-028 | Dotted suffix `Ph.D.` is rejected (only `PhD` is allowed) | P3 | Negative | 422, warningCodes=[INVALID_SUFFIX]. |  |
| NAME-029 | Several problems are all reported | P2 | Negative | 422 with INVALID_CHARACTERS, SINGLE_CHARACTER_NAME and INVALID_TITLE. |  |
| NAME-040 | Missing firstName returns 400 | P1 | Contract | 400 with message `firstName: must not be blank`. |  |
| NAME-041 | Whitespace-only lastName returns 400 | P2 | Contract | 400 with message `lastName: must not be blank`. |  |
| NAME-042 | Missing requestId returns 400 | P2 | Contract | 400 with message `requestId: must not be null`. |  |
| NAME-043 | Non-numeric requestId returns 400 Malformed request body | P2 | Contract | 400 with message `Malformed request body` (requestId must be a number on this endpoint). |  |
| NAME-044 | Missing storeId, sourceSystem and brand are all reported | P2 | Contract | 400; message lists storeId, sourceSystem and brand. |  |
| NAME-045 | Empty JSON object returns 400 | P2 | Contract | 400; message lists every required field. |  |
| NAME-046 | Malformed JSON returns 400 without parser details | P2 | Contract | 400 with message `Malformed request body`. |  |

## 02 Email Validation

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| EMAIL-001 | Valid email address | P1 | Positive | 200, syntaxValid=true, message `Email is valid`, no warning codes. |  |
| EMAIL-002 | Email is trimmed and lower-cased | P1 | Normalization | normalizedEmail `jane.doe@acme.org`. |  |
| EMAIL-003 | Plus-addressing and allowed special characters | P2 | Positive | 200, syntaxValid=true. |  |
| EMAIL-004 | Sub-domains and hyphenated domain labels | P2 | Positive | 200, syntaxValid=true. |  |
| EMAIL-005 | Boundary: exactly 60 characters is accepted | P1 | Boundary | 200, syntaxValid=true (max length is 60). |  |
| EMAIL-006 | Boundary: 61 characters is rejected | P1 | Boundary | syntaxValid=false, warningCodes=[EMAIL_TOO_LONG]. |  |
| EMAIL-010 | Missing @ symbol | P1 | Negative | syntaxValid=false, warningCodes=[MISSING_AT]. |  |
| EMAIL-011 | Two @ symbols | P2 | Negative | warningCodes=[INVALID_AT_COUNT]. |  |
| EMAIL-012 | Empty local part | P2 | Negative | warningCodes=[EMPTY_LOCAL_PART]. |  |
| EMAIL-013 | Empty domain | P2 | Negative | warningCodes=[EMPTY_DOMAIN, MISSING_DOMAIN_DOT]. |  |
| EMAIL-014 | Domain without a dot | P2 | Negative | warningCodes=[MISSING_DOMAIN_DOT]. |  |
| EMAIL-015 | Consecutive dots in local part | P2 | Negative | warningCodes=[CONSECUTIVE_DOTS]. |  |
| EMAIL-016 | Consecutive dots in domain | P2 | Negative | warningCodes=[CONSECUTIVE_DOTS, INVALID_DOMAIN]. |  |
| EMAIL-017 | Local part starting with a dot | P2 | Negative | warningCodes=[INVALID_LOCAL_PART]. |  |
| EMAIL-018 | Local part ending with a dot | P2 | Negative | warningCodes=[INVALID_LOCAL_PART]. |  |
| EMAIL-019 | Whitespace inside the address | P2 | Negative | warningCodes=[WHITESPACE, INVALID_LOCAL_PART]. |  |
| EMAIL-020 | Domain label starting with a hyphen | P2 | Negative | warningCodes=[INVALID_DOMAIN]. |  |
| EMAIL-021 | Underscore in domain | P2 | Negative | warningCodes=[INVALID_DOMAIN]. |  |
| EMAIL-022 | Trailing dot in domain | P2 | Negative | warningCodes=[INVALID_DOMAIN]. |  |
| EMAIL-023 | Parentheses in local part | P2 | Negative | warningCodes=[INVALID_LOCAL_PART]. |  |
| EMAIL-024 | Non-ASCII (accented) local part is rejected | P3 | Negative | warningCodes=[INVALID_LOCAL_PART]. |  |
| EMAIL-025 | Markup in the address is rejected | P2 | Security | warningCodes=[INVALID_LOCAL_PART]. |  |
| EMAIL-026 | Over-length address without @ reports both problems | P2 | Negative | warningCodes=[EMAIL_TOO_LONG, MISSING_AT]. |  |
| EMAIL-040 | Missing email returns 400 | P1 | Contract | 400 with message `email: must not be blank`. |  |
| EMAIL-041 | Whitespace-only email returns 400 | P2 | Contract | 400 with message `email: must not be blank`. |  |
| EMAIL-042 | Missing userId returns 400 (required on this endpoint) | P2 | Contract | 400 with message `userId: must not be blank`. |  |
| EMAIL-043 | Missing requestId returns 400 | P2 | Contract | 400 with message `requestId: must not be null`. |  |
| EMAIL-044 | Non-numeric requestId returns 400 | P2 | Contract | 400 with message `Malformed request body`. |  |
| EMAIL-045 | Numeric string requestId is accepted and returned as a number | P3 | Contract | 200 and requestId returned as the number 1234567. |  |
| EMAIL-046 | Malformed JSON returns 400 | P2 | Contract | 400 with message `Malformed request body`. |  |

## 03 Phone Validation

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| PHONE-001 | Valid US number with punctuation | P1 | Positive | 200, syntaxValid=true, digits `7134829156`, display `713-482-9156`. |  |
| PHONE-002 | US number with +1 country prefix | P1 | Normalization | Leading 1 removed: digits `7134829156`. |  |
| PHONE-003 | US number, digits only | P2 | Positive | digits `7134829156`. |  |
| PHONE-004 | US number with dots and spaces | P2 | Normalization | digits `7134829156`. |  |
| PHONE-005 | Canadian number (NANP rules) | P1 | Positive | digits `4164829156`, display `416-482-9156`. |  |
| PHONE-006 | Country code is case-insensitive | P3 | Positive | Treated as US. |  |
| PHONE-007 | International (UK) number | P1 | Positive | digits `442079460958`; display is the plain digits; no NANP warnings. |  |
| PHONE-008 | Boundary: international with 7 digits (minimum) | P2 | Boundary | 200, syntaxValid=true. |  |
| PHONE-009 | Boundary: international with 15 digits (maximum) | P2 | Boundary | 200, syntaxValid=true. |  |
| PHONE-010 | 10-digit US number sent with a non-NANP country uses international rules | P3 | Positive | 200, digits `7134829156`, display without dashes, no NANP warnings. |  |
| PHONE-020 | 555 exchange is flagged | P1 | Warning | syntaxValid=true, includes FIVE_FIVE_FIVE_WARNING. |  |
| PHONE-021 | Toll-free area code is flagged | P1 | Warning | syntaxValid=true, includes TOLL_FREE_WARNING. |  |
| PHONE-022 | Toll-free with 555 exchange reports both | P2 | Warning | includes FIVE_FIVE_FIVE_WARNING and TOLL_FREE_WARNING. |  |
| PHONE-023 | Exchange starting with 1 is not a valid NANP number | P2 | Warning | includes INVALID_NANP_NUMBER. |  |
| PHONE-024 | Area code starting with 0 is not a valid NANP number | P2 | Warning | includes INVALID_NANP_NUMBER. |  |
| PHONE-025 | Generic sequence 1234567890 | P2 | Warning | includes INVALID_NANP_NUMBER and GENERIC_PATTERN_WARNING. |  |
| PHONE-026 | Generic sequence 9876543210 | P2 | Warning | includes GENERIC_PATTERN_WARNING. |  |
| PHONE-027 | Repeated subscriber digits (organisational pattern) | P2 | Warning | includes ORGANIZATIONAL_PATTERN_WARNING. |  |
| PHONE-028 | All digits identical | P2 | Warning | includes ORGANIZATIONAL_PATTERN_WARNING. |  |
| PHONE-029 | International number with all identical digits | P3 | Warning | includes ORGANIZATIONAL_PATTERN_WARNING. |  |
| PHONE-040 | US number with 9 digits | P1 | Negative | syntaxValid=false, warningCodes=[INVALID_LENGTH]. |  |
| PHONE-041 | US number with 11 digits not starting with 1 | P2 | Negative | warningCodes=[INVALID_LENGTH]. |  |
| PHONE-042 | US number with +1 and 11 national digits | P2 | Negative | warningCodes=[INVALID_LENGTH]. |  |
| PHONE-043 | Letters in the number (vanity number) | P1 | Negative | warningCodes=[NON_NUMERIC]. |  |
| PHONE-044 | Extension suffix is not accepted | P2 | Negative | warningCodes=[NON_NUMERIC]. |  |
| PHONE-045 | Hash / symbol separators are not accepted | P2 | Negative | warningCodes=[NON_NUMERIC]. |  |
| PHONE-046 | Boundary: international with 6 digits | P2 | Boundary | warningCodes=[INVALID_LENGTH]. |  |
| PHONE-047 | Boundary: international with 16 digits | P2 | Boundary | warningCodes=[INVALID_LENGTH]. |  |
| PHONE-060 | Missing phone returns 400 | P1 | Contract | 400 with message `phone: must not be blank`. |  |
| PHONE-061 | Missing countryCode returns 400 | P1 | Contract | 400 with message `countryCode: must not be blank`. |  |
| PHONE-062 | Whitespace-only phone returns 400 | P2 | Contract | 400 with message `phone: must not be blank`. |  |
| PHONE-063 | Missing userId returns 400 | P2 | Contract | 400 with message `userId: must not be blank`. |  |
| PHONE-064 | Phone sent as a JSON number is accepted | P3 | Contract | 200, digits `7134829156`. |  |
| PHONE-065 | Malformed JSON returns 400 | P2 | Contract | 400 with message `Malformed request body`. |  |

## 04 Address Validation

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| ADDR-001 | Valid US address is normalised to USPS format | P1 | Positive | 200, valid=true, line1 `1427 MAPLE HOLLOW LN`, line2 `APT 4B`, state `TX`, country `US`. |  |
| ADDR-002 | ZIP+4 without a hyphen is formatted | P2 | Normalization | postalCode `77494-1234`. |  |
| ADDR-003 | ZIP+4 with a space is formatted | P3 | Normalization | postalCode `77494-1234`. |  |
| ADDR-004 | Country alias `U.S.A.` resolves to US | P2 | Normalization | country `US`. |  |
| ADDR-005 | Street suffix, directional and unit abbreviations | P1 | Normalization | line1 `200 N MAIN ST STE 300`, city `ST LOUIS`, state `MO`. |  |
| ADDR-006 | PO Box is normalised | P2 | Normalization | line1 `PO BOX 4521`. |  |
| ADDR-007 | Ordinal street names are abbreviated | P3 | Normalization | line1 `500 5TH AVE`, state `IL`. |  |
| ADDR-008 | Valid Canadian address | P1 | Positive | line1 `100 QUEEN ST W`, state `ON`, postalCode `M5H 2N2`, country `CA`. |  |
| ADDR-009 | Canadian province alias (Québec) and ISO alpha-3 country | P2 | Normalization | state `QC`, postalCode `H3A 3G4`, country `CA`. |  |
| ADDR-010 | International (UK) address without a state | P2 | Positive | valid=true, no MISSING_STATE warning (state only required for US/CA), postalCode `SW1A 2AA`. |  |
| ADDR-011 | US territory (Puerto Rico) | P3 | Positive | state `PR`, postalCode `00901`. |  |
| ADDR-012 | Military (APO / AE) address | P3 | Positive | state `AE`, valid=true. |  |
| ADDR-020 | Address explicitly null is reported as missing (not invalid) | P1 | Positive | valid=true, missingAddress=true, normalizedAddress=null. The caller must persist NULL and never fall back to the store address. |  |
| ADDR-021 | Address omitted entirely | P2 | Positive | Same as ADDR-020. |  |
| ADDR-022 | All address fields blank / whitespace | P2 | Positive | Same as ADDR-020. |  |
| ADDR-030 | Address line 1 shorter than 3 characters | P2 | Warning | valid=true, warningCodes=[LINE1_TOO_SHORT]. |  |
| ADDR-031 | Missing city | P2 | Warning | valid=true, warningCodes=[MISSING_CITY]. |  |
| ADDR-032 | Missing state for a US address | P2 | Warning | valid=true, warningCodes=[MISSING_STATE]. |  |
| ADDR-033 | Missing postal code | P2 | Warning | valid=true, warningCodes=[MISSING_POSTAL_CODE]. |  |
| ADDR-034 | Missing line 1 | P2 | Warning | valid=true, warningCodes=[MISSING_LINE1]. |  |
| ADDR-035 | Missing country skips US state / ZIP checks | P2 | Warning | valid=true, warningCodes=[MISSING_COUNTRY]; state returned as `TEXAS` (not converted to `TX`). |  |
| ADDR-036 | Only a city is provided | P2 | Warning | valid=true, warnings MISSING_COUNTRY, MISSING_POSTAL_CODE and MISSING_LINE1. |  |
| ADDR-040 | Unknown US state | P1 | Negative | valid=false, syntaxValid=false, errorCodes=[INVALID_STATE]. |  |
| ADDR-041 | US ZIP with 4 digits | P1 | Negative | errorCodes=[INVALID_POSTAL_CODE]. |  |
| ADDR-042 | US ZIP containing letters | P2 | Negative | errorCodes=[INVALID_POSTAL_CODE]. |  |
| ADDR-043 | US-style ZIP on a Canadian address | P2 | Negative | errorCodes=[INVALID_POSTAL_CODE]. |  |
| ADDR-044 | Canadian province on a US address | P2 | Negative | errorCodes=[INVALID_STATE]. |  |
| ADDR-045 | Unknown country | P1 | Negative | errorCodes=[INVALID_COUNTRY], country `NARNIA`. |  |
| ADDR-046 | Several format errors are all reported | P2 | Negative | errorCodes=[INVALID_STATE, INVALID_POSTAL_CODE] and both messages. |  |
| ADDR-060 | Missing requestId returns 400 | P1 | Contract | 400 with message `requestId: must not be blank`. |  |
| ADDR-061 | requestId longer than 50 characters returns 400 | P2 | Boundary | 400 with message `requestId: size must be between 0 and 50`. |  |
| ADDR-062 | Missing userId returns 400 | P2 | Contract | 400 with message `userId: must not be blank`. |  |
| ADDR-063 | storeId is optional | P3 | Contract | 200, valid=true, storeId null. |  |
| ADDR-064 | line1 longer than 200 characters returns 400 | P2 | Boundary | 400 with message `address.line1: size must be between 0 and 200`. |  |
| ADDR-065 | postalCode longer than 20 characters returns 400 | P2 | Boundary | 400 with message `address.postalCode: size must be between 0 and 20`. |  |
| ADDR-066 | brand longer than 20 characters returns 400 | P2 | Boundary | 400 with message `brand: size must be between 0 and 20`. |  |
| ADDR-067 | Malformed JSON returns 400 | P2 | Contract | 400 with message `Malformed request body`. |  |

## 05 Profile Validation

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| PROF-001 | Clean profile is accepted and normalised | P1 | Positive | 200, decision ACCEPT, no errors or warnings, every contact and address isValidated=true. |  |
| PROF-002 | Minimal profile (name + one email) | P1 | Positive | 200, ACCEPT; userId null, addresses and phones empty lists. |  |
| PROF-003 | Phone is enough as the only contact method | P1 | Positive | 200, ACCEPT with phones[0].isValidated=true. |  |
| PROF-004 | Legacy field names (RequestID, UserID, email, phone) are accepted | P1 | Contract | 200, ACCEPT; requestId and userId echoed; emails/phones validated. |  |
| PROF-005 | Numeric RequestId is echoed back as text | P2 | Contract | 200 and requestId returned as a string equal to the number sent. |  |
| PROF-006 | Input is trimmed, re-cased and normalised | P1 | Normalization | Name `Jane Marie Doe`, email lower-cased, phone `7134829156`, type and sourceSystem/brand trimmed. |  |
| PROF-007 | International phone keeps a leading + | P2 | Positive | 200, ACCEPT, phones[0].value `+442079460958`, isValidated=true. |  |
| PROF-008 | Boundary: 4 addresses, 4 emails and 4 phones are accepted | P1 | Boundary | 200, ACCEPT with 4 normalised entries in each list. |  |
| PROF-009 | Client-supplied isValidated is ignored and recomputed | P1 | Business rule | emails[0].isValidated=true even though false was sent; phones[0].isValidated=false even though true was sent. |  |
| PROF-010 | Single-character middle initial is accepted without a warning | P2 | Positive | 200, ACCEPT, no warnings. |  |
| PROF-011 | Blank address slot is kept as null to preserve indexes | P3 | Positive | 200, ACCEPT, normalizedProfile.addresses = [null]. |  |
| PROF-012 | Blank email slot is not an error when a phone is valid | P3 | Positive | 200, ACCEPT, normalizedProfile.emails = [null]. |  |
| PROF-020 | Single-character first name | P1 | Warning | 200, ACCEPT_WITH_WARNINGS, NAME_SINGLE_CHARACTER on profile.firstName. |  |
| PROF-021 | Single-character last name | P2 | Warning | NAME_SINGLE_CHARACTER on profile.lastName. |  |
| PROF-022 | Digits in middle name are only a warning | P1 | Warning | ACCEPT_WITH_WARNINGS, MIDDLE_NAME_NUMERIC_CHARACTERS on profile.middleName. |  |
| PROF-023 | Phone with an organisational pattern is a warning and not validated | P1 | Warning | ACCEPT_WITH_WARNINGS (email is valid), PHONE_ORGANIZATIONAL_PATTERN, phones[0].isValidated=false. |  |
| PROF-024 | Generic sequential phone is a warning | P2 | Warning | PHONE_ORGANIZATIONAL_PATTERN on phones[0].value. |  |
| PROF-025 | Phone that is not a valid NANP number is a warning | P2 | Warning | PHONE_INVALID_NANP_NUMBER, phones[0].isValidated=false. |  |
| PROF-026 | Customer phone equal to storeContext.storePhone | P1 | Warning | PHONE_MATCHES_STORE warning, phones[0].isValidated=false. |  |
| PROF-027 | Address with an unknown state is a non-blocking warning | P1 | Warning | ADDRESS_INVALID on addresses[0] with message `Address is not valid: INVALID_STATE.`; isValidated=false. |  |
| PROF-028 | Address with several format errors | P2 | Warning | ADDRESS_INVALID message lists INVALID_STATE, INVALID_POSTAL_CODE. |  |
| PROF-029 | Incomplete address (no city) stays validated | P1 | Warning | ADDRESS_INCOMPLETE `City is missing.`; isValidated stays true. |  |
| PROF-030 | Incomplete address lists every missing part | P2 | Warning | ADDRESS_INCOMPLETE `Postal code is missing. City is missing.` |  |
| PROF-031 | Customer address equal to storeContext.storeAddress (with a suite number) | P1 | Warning | ADDRESS_MATCHES_STORE `Customer address matches the transacting store address.`; isValidated=false. |  |
| PROF-032 | Missing country is inferred as US from the state | P2 | Business rule | ACCEPT; normalised country `US`, state `TX`. |  |
| PROF-033 | Missing country is inferred as CA from the province | P2 | Business rule | ACCEPT; country `CA`, state `ON`, postalCode `M5H 2N2`. |  |
| PROF-034 | Missing country and state are inferred from the ZIP | P3 | Business rule | ACCEPT_WITH_WARNINGS; country `US`, ADDRESS_INCOMPLETE `State is missing.` |  |
| PROF-050 | Digits in last name reject the profile | P1 | Negative | REJECT, NAME_NUMERIC_CHARACTERS on profile.lastName. |  |
| PROF-051 | Special characters in first name reject the profile | P1 | Negative | REJECT, NAME_NUMERIC_CHARACTERS on profile.firstName. |  |
| PROF-052 | Invalid email syntax rejects the profile even when the phone is valid | P1 | Negative | REJECT, EMAIL_INVALID_SYNTAX on emails[0].value; emails[0].isValidated=false. |  |
| PROF-053 | Email with several syntax problems lists them all | P2 | Negative | EMAIL_INVALID_SYNTAX message lists whitespace, missing dot and invalid local part. |  |
| PROF-054 | Phone with wrong digit count | P1 | Negative | REJECT, PHONE_INVALID_FORMAT; value echoed as sent. |  |
| PROF-055 | Phone with letters | P2 | Negative | REJECT, PHONE_INVALID_FORMAT (invalid characters). |  |
| PROF-056 | International phone that is too short | P2 | Negative | REJECT, PHONE_INVALID_FORMAT. |  |
| PROF-057 | Toll-free phone is blocked | P1 | Negative | REJECT, PHONE_TOLL_FREE_BLOCKED; value `8882347890`. |  |
| PROF-058 | No email and no phone | P1 | Business rule | REJECT, CONTACT_METHOD_NOT_VALIDATED on contactMethods. |  |
| PROF-059 | Only blank contact slots | P2 | Business rule | REJECT, CONTACT_METHOD_NOT_VALIDATED; emails=[null], phones=[null]. |  |
| PROF-060 | Only phone matches the store phone, so no usable contact | P1 | Business rule | REJECT: PHONE_MATCHES_STORE warning plus CONTACT_METHOD_NOT_VALIDATED error. |  |
| PROF-061 | Invalid email and pattern phone leave no usable contact | P2 | Business rule | REJECT: EMAIL_INVALID_SYNTAX + CONTACT_METHOD_NOT_VALIDATED errors, PHONE_ORGANIZATIONAL_PATTERN warning. |  |
| PROF-062 | Every error is reported in field order | P1 | Negative | Errors in order: profile.firstName, profile.lastName, emails[0].value, phones[0].value, contactMethods. |  |
| PROF-063 | Issue path points at the right list index | P2 | Negative | REJECT, EMAIL_INVALID_SYNTAX on emails[1].value; emails[0] stays validated. |  |
| PROF-064 | Markup in a name is rejected and returned as JSON | P2 | Security | REJECT, NAME_NUMERIC_CHARACTERS; Content-Type application/json. |  |
| PROF-080 | Missing sourceSystem | P1 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: sourceSystem`. |  |
| PROF-081 | Missing requestId | P1 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: requestId`. |  |
| PROF-082 | Missing brand | P2 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: brand`. |  |
| PROF-083 | Missing profile block | P1 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: profile`. |  |
| PROF-084 | Missing profile.firstName | P2 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: profile.firstName`. |  |
| PROF-085 | Whitespace-only profile.lastName | P2 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: profile.lastName`. |  |
| PROF-086 | Empty JSON object lists every required field | P2 | Contract | 400 VALIDATION_REQUEST_INVALID.  |  |
| PROF-087 | requestId containing a space | P1 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: requestId must contain only printable characters without spaces`. |  |
| PROF-088 | Boundary: requestId of 101 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: requestId size must be between 0 and 100`. |  |
| PROF-089 | Boundary: requestId of 100 characters is accepted | P2 | Boundary | 200, ACCEPT; requestId echoed. |  |
| PROF-090 | Boundary: sourceSystem of 31 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: sourceSystem size must be between 0 and 30`. |  |
| PROF-091 | Boundary: brand of 21 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: brand size must be between 0 and 20`. |  |
| PROF-092 | Boundary: userId of 101 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: userId size must be between 0 and 100`. |  |
| PROF-093 | Boundary: first name of 101 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: profile.firstName size must be between 0 and 100`. |  |
| PROF-094 | Boundary: 5 emails | P1 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: emails size must be between 0 and 4`. |  |
| PROF-095 | Boundary: 5 phones | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: phones size must be between 0 and 4`. |  |
| PROF-096 | Boundary: 5 addresses | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: addresses size must be between 0 and 4`. |  |
| PROF-097 | Address line 1 longer than 200 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: addresses[0].line1 size must be between 0 and 200`. |  |
| PROF-098 | storeContext.storeId longer than 50 characters | P2 | Boundary | 400 VALIDATION_REQUEST_INVALID. Message: `Invalid field: storeContext.storeId size must be between 0 and 50`. |  |
| PROF-099 | Missing and invalid fields together: missing wins the message | P2 | Contract | 400 VALIDATION_REQUEST_INVALID. Message: `Missing required field: brand`. |  |
| PROF-100 | Malformed JSON | P1 | Contract | 400 VALIDATION_REQUEST_INVALID, message `Malformed request body`, details [{body, MALFORMED}]. |  |
| PROF-101 | Wrong JSON type (profile as a string) | P2 | Contract | 400 VALIDATION_REQUEST_INVALID, message `Malformed request body`. |  |
| PROF-102 | emails sent as an object instead of a list | P2 | Contract | 400 VALIDATION_REQUEST_INVALID, message `Malformed request body`. |  |
| PROF-103 | Empty request body | P2 | Contract | 400 VALIDATION_REQUEST_INVALID, message `Malformed request body`. |  |
| PROF-104 | Content-Type text/plain returns 415 | P1 | Contract | 415 UNSUPPORTED_MEDIA_TYPE, message `Content-Type must be application/json`. |  |
| PROF-105 | Accept: application/xml returns 406 with no body | P2 | Contract | 406, empty body, X-Correlation-ID header still returned. |  |
| PROF-110 | No X-Correlation-ID header: a UUID is generated | P1 | Traceability | 200 and response header X-Correlation-ID is a UUID. |  |
| PROF-111 | Boundary: 100-character correlation id is echoed | P2 | Traceability | Response header equals the 100-character id sent. |  |
| PROF-112 | Boundary: 101-character correlation id is replaced | P2 | Traceability | Response header is a new UUID, not the oversized id. |  |
| PROF-113 | Correlation id on a 400 matches header and body | P2 | Traceability | 400; body.correlationId and X-Correlation-ID both equal the id sent. |  |

## 06 Reference Data (denylist & store master)

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| REF-001 | Name equal to a store name is rejected | P2 | Reference data | 422, storeName=true, warningCodes include STORE_NAME. | refStoreName |
| REF-002 | Name equal to a denylisted organisation name is rejected | P2 | Reference data | 422, warningCodes include BUSINESS_NAME. | refOrgName |
| REF-003 | Denylisted email prefix is flagged (but syntaxValid stays true) | P2 | Reference data | 200, syntaxValid=true, message `Email is valid`, warningCodes include DENYLISTED_EMAIL. | refEmailPrefix |
| REF-004 | Denylisted email domain is flagged | P2 | Reference data | 200, syntaxValid=true, warningCodes include DENYLISTED_DOMAIN. | refEmailDomain |
| REF-005 | Phone matching a store phone | P2 | Reference data | 200, storePhone=true, warningCodes include STORE_PHONE_MATCH. | refStorePhone |
| REF-006 | Phone starting with a denylisted prefix | P2 | Reference data | 200, warningCodes include DENYLIST_MATCH. | refPhonePrefix |
| REF-007 | Address equal to a store-master address is a crossover | P2 | Reference data | valid=false, errorCodes include ADDRESS_STORE_CROSSOVER, storeAddressMatch=true, matchedStoreId set. | refStoreLine1, refStoreCity, refStoreState, refStorePostalCode |
| REF-008 | Store-master address with a suite number still matches | P2 | Reference data | ADDRESS_STORE_CROSSOVER (unit designators are ignored when matching). | refStoreLine1, refStoreCity, refStoreState, refStorePostalCode |
| REF-009 | Denylisted street address | P2 | Reference data | valid=false, syntaxValid=true, errorCodes include DENYLISTED_ADDRESS. | refAddressLine1 |
| REF-010 | Denylisted ZIP code | P2 | Reference data | valid=false, errorCodes include DENYLISTED_ZIP_CODE. | refZipCode |
| REF-011 | Profile: placeholder email is rejected | P2 | Reference data | REJECT: EMAIL_PLACEHOLDER and CONTACT_METHOD_NOT_VALIDATED. | refEmailPrefix |
| REF-012 | Profile: denylisted email domain is rejected | P2 | Reference data | REJECT: EMAIL_PLACEHOLDER on emails[0].value. | refEmailDomain |
| REF-013 | Profile: denylisted phone prefix is rejected | P2 | Reference data | REJECT: PHONE_DENYLISTED on phones[0].value. | refPhonePrefix |
| REF-014 | Profile: denylisted street address is rejected | P2 | Reference data | REJECT: ADDRESS_DENYLISTED on addresses[0].line1. | refAddressLine1 |
| REF-015 | Profile: denylisted ZIP code is rejected | P2 | Reference data | REJECT: ADDRESS_DENYLISTED on addresses[0].postalCode. | refZipCode |
| REF-016 | Profile: store-master address is a warning | P2 | Reference data | ACCEPT_WITH_WARNINGS: ADDRESS_MATCHES_STORE `Customer address matches store <id> address.` | refStoreLine1, refStoreCity, refStoreState, refStorePostalCode |
| REF-017 | Profile: store-master phone is a warning | P2 | Reference data | ACCEPT_WITH_WARNINGS: PHONE_MATCHES_STORE; phones[0].isValidated=false. | refStorePhone |
| REF-018 | Profile: name equal to a store name is a warning | P2 | Reference data | NAME_BUSINESS_OR_STORE warning on profile.firstName. | refStoreName |

## 07 Security & Resilience

| ID | Title | Priority | Type | Expected result | Reference data |
|---|---|---|---|---|---|
| SEC-001 | GET on a POST-only endpoint returns 405 | P2 | Security | 405 Method Not Allowed. |  |
| SEC-002 | 405 error body must not leak a stack trace | P1 | Security | No `trace` attribute or Java class names in the body. |  |
| SEC-003 | Unknown endpoint returns 404 without a stack trace | P2 | Security | 404 and no stack trace in the body. |  |
| SEC-004 | Unsupported Content-Type on a single-field endpoint returns 415 without a stack trace | P2 | Security | 415 and no stack trace in the body. |  |
| SEC-005 | SQL-injection style email is handled as plain text | P1 | Security | 200, syntaxValid=false; the service keeps working (see HLT-001). |  |
| SEC-006 | SQL-injection style phone is handled as plain text | P2 | Security | 200, warningCodes=[NON_NUMERIC]. |  |
| SEC-007 | SQL-injection style name is rejected | P2 | Security | 422, INVALID_CHARACTERS. |  |
| SEC-008 | Very long name (10,000 characters) does not crash the service | P2 | Resilience | A 2xx/4xx answer within the SLA, never 5xx. |  |
| SEC-009 | Service is still healthy after the security cases | P2 | Resilience | 200 with status UP. |  |
