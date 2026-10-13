-- Reference data for running folder 06 against a local (H2) instance. Matches the ValidationServices-Local environment.
INSERT INTO validation_denylist ("value", value_type, active, created_at, updated_at) VALUES
 ('test', 'EMAIL', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
 ('example.com', 'DOMAIN', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
 ('713555', 'PHONE', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
 ('1200 Commerce Street', 'ADDRESS', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
 ('99999', 'ZIP_CODE', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
 ('Acme Corporation', 'ORGNAME', true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO store (store_key, store_name, phone_number, address_line_1, city, state, zip_code, country, is_selling_store, create_dttm, update_dttm) VALUES
 ('KEY-T999', 'Galleria', '(832) 467-1200', '6565 San Felipe Street', 'HOUSTON', 'TX', '77057', 'US', 'Y', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
