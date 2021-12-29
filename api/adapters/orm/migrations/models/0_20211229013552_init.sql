-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "role" VARCHAR(16) NOT NULL,
    "phone" VARCHAR(255),
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "password" VARCHAR(255),
    "last_login" TIMESTAMPTZ,
    "phone_code" VARCHAR(16),
    "email_code" VARCHAR(255),
    "password_code" VARCHAR(255),
    "is_phone_verified" BOOL NOT NULL  DEFAULT False,
    "is_email_verified" BOOL NOT NULL  DEFAULT False,
    "is_active" BOOL NOT NULL  DEFAULT False,
    "is_onboarded" BOOL NOT NULL  DEFAULT False,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "company" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "owner_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "companym2mcontractor" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "company_id" UUID NOT NULL REFERENCES "company" ("pk") ON DELETE CASCADE,
    "contractor_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE,
    CONSTRAINT "uid_companym2mc_company_8a3ed3" UNIQUE ("company_id", "contractor_id")
);
CREATE TABLE IF NOT EXISTS "companym2memployer" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "company_id" UUID NOT NULL REFERENCES "company" ("pk") ON DELETE CASCADE,
    "employer_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE,
    CONSTRAINT "uid_companym2me_company_f55677" UNIQUE ("company_id", "employer_id")
);
CREATE TABLE IF NOT EXISTS "inviteusertocompany" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "invitation_code" VARCHAR(255) NOT NULL,
    "company_id" UUID REFERENCES "company" ("pk") ON DELETE CASCADE,
    "sender_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "recipientbankaccount" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "recipient_bank_account_type" VARCHAR(16) NOT NULL,
    "recipient_currency" VARCHAR(3) NOT NULL,
    "recipient_country_alpha3" VARCHAR(3) NOT NULL,
    "recipient_owner_company_id" UUID REFERENCES "company" ("pk") ON DELETE CASCADE,
    "recipient_owner_user_id" UUID REFERENCES "user" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "senderbankaccount" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "sender_bank_account_type" VARCHAR(16) NOT NULL,
    "sender_currency" VARCHAR(3) NOT NULL,
    "sender_country_alpha3" VARCHAR(3) NOT NULL,
    "sender_owner_company_id" UUID REFERENCES "company" ("pk") ON DELETE CASCADE,
    "sender_owner_user_id" UUID REFERENCES "user" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "operation" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "sender_amount" DECIMAL(9,2),
    "recipient_amount" DECIMAL(9,2),
    "status" VARCHAR(16) NOT NULL,
    "our_fee" DECIMAL(9,2),
    "provider_fee" DECIMAL(9,2),
    "operation_owner_company_id" UUID NOT NULL REFERENCES "company" ("pk") ON DELETE CASCADE,
    "operation_recipient_user_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE,
    "operation_sender_user_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE,
    "recipient_account_id" UUID REFERENCES "recipientbankaccount" ("pk") ON DELETE CASCADE,
    "sender_account_id" UUID REFERENCES "senderbankaccount" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "invoice" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "created_by_id" UUID NOT NULL REFERENCES "user" ("pk") ON DELETE CASCADE,
    "for_company_id" UUID NOT NULL REFERENCES "company" ("pk") ON DELETE CASCADE,
    "operation_id" UUID REFERENCES "operation" ("pk") ON DELETE CASCADE,
    "recipient_account_id" UUID NOT NULL REFERENCES "recipientbankaccount" ("pk") ON DELETE CASCADE,
    "sender_account_id" UUID REFERENCES "senderbankaccount" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "invoiceitem" (
    "pk" UUID NOT NULL  PRIMARY KEY,
    "created_date" TIMESTAMPTZ NOT NULL,
    "updated_date" TIMESTAMPTZ NOT NULL,
    "amount" DECIMAL(9,2) NOT NULL,
    "quantity" INT NOT NULL,
    "descripion" TEXT,
    "invoice_id" UUID NOT NULL REFERENCES "invoice" ("pk") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
