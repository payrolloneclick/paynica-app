-- upgrade --
CREATE TABLE IF NOT EXISTS "ormuser" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "email" VARCHAR(255) NOT NULL,
    "role" VARCHAR(16) NOT NULL,
    "phone" VARCHAR(255),
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "password" VARCHAR(255),
    "last_login" TIMESTAMPTZ,
    "phone_code" VARCHAR(8),
    "email_code" VARCHAR(255),
    "password_code" VARCHAR(255),
    "is_phone_verified" BOOL NOT NULL  DEFAULT False,
    "is_email_verified" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "is_onboarded" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "ormcompany" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "name" VARCHAR(255) NOT NULL,
    "owner_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ormcompanym2mcontractor" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "company_id" UUID NOT NULL REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "contractor_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_ormcompanym_company_a29512" UNIQUE ("company_id", "contractor_id")
);
CREATE TABLE IF NOT EXISTS "ormcompanym2memployer" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "company_id" UUID NOT NULL REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "employer_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_ormcompanym_company_6c2e6c" UNIQUE ("company_id", "employer_id")
);
CREATE TABLE IF NOT EXISTS "orminviteusertocompany" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "email" VARCHAR(255) NOT NULL,
    "invitation_code" VARCHAR(255) NOT NULL,
    "company_id" UUID REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "sender_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ormrecipientbankaccount" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "recipient_bank_account_type" VARCHAR(16) NOT NULL,
    "recipient_currency" VARCHAR(3) NOT NULL,
    "recipient_country_alpha3" VARCHAR(3) NOT NULL,
    "recipient_owner_company_id" UUID REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "recipient_owner_user_id" UUID REFERENCES "ormuser" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ormsenderbankaccount" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "sender_bank_account_type" VARCHAR(16) NOT NULL,
    "sender_currency" VARCHAR(3) NOT NULL,
    "sender_country_alpha3" VARCHAR(3) NOT NULL,
    "sender_owner_company_id" UUID REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "sender_owner_user_id" UUID REFERENCES "ormuser" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ormoperation" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "sender_bank_account_type" VARCHAR(16) NOT NULL,
    "sender_currency" VARCHAR(3) NOT NULL,
    "sender_country_alpha3" VARCHAR(3) NOT NULL,
    "recipient_bank_account_type" VARCHAR(16) NOT NULL,
    "recipient_currency" VARCHAR(3) NOT NULL,
    "recipient_country_alpha3" VARCHAR(3) NOT NULL,
    "sender_amount" DECIMAL(9,2),
    "recipient_amount" DECIMAL(9,2),
    "status" VARCHAR(16) NOT NULL,
    "our_fee" DECIMAL(9,2),
    "provider_fee" DECIMAL(9,2),
    "operation_owner_company_id" UUID NOT NULL REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "operation_recipient_user_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE,
    "operation_sender_user_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE,
    "recipient_account_id" UUID REFERENCES "ormrecipientbankaccount" ("id") ON DELETE CASCADE,
    "sender_account_id" UUID REFERENCES "ormsenderbankaccount" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orminvoice" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "created_by_id" UUID NOT NULL REFERENCES "ormuser" ("id") ON DELETE CASCADE,
    "for_company_id" UUID NOT NULL REFERENCES "ormcompany" ("id") ON DELETE CASCADE,
    "operation_id" UUID REFERENCES "ormoperation" ("id") ON DELETE CASCADE,
    "recipient_account_id" UUID NOT NULL REFERENCES "ormrecipientbankaccount" ("id") ON DELETE CASCADE,
    "sender_account_id" UUID REFERENCES "ormsenderbankaccount" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "orminvoiceitem" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ,
    "amount" DECIMAL(9,2) NOT NULL,
    "quantity" INT NOT NULL,
    "descripion" TEXT,
    "invoice_id" UUID NOT NULL REFERENCES "orminvoice" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
