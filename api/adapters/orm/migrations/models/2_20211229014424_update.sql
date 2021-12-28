-- upgrade --
ALTER TABLE "operation" ADD "sender_currency" VARCHAR(3) NOT NULL;
ALTER TABLE "operation" ADD "sender_bank_account_type" VARCHAR(16) NOT NULL;
ALTER TABLE "operation" ADD "recipient_bank_account_type" VARCHAR(16) NOT NULL;
ALTER TABLE "operation" ADD "recipient_currency" VARCHAR(3) NOT NULL;
ALTER TABLE "operation" ADD "sender_country_alpha3" VARCHAR(3) NOT NULL;
ALTER TABLE "operation" ADD "recipient_country_alpha3" VARCHAR(3) NOT NULL;
-- downgrade --
ALTER TABLE "operation" DROP COLUMN "sender_currency";
ALTER TABLE "operation" DROP COLUMN "sender_bank_account_type";
ALTER TABLE "operation" DROP COLUMN "recipient_bank_account_type";
ALTER TABLE "operation" DROP COLUMN "recipient_currency";
ALTER TABLE "operation" DROP COLUMN "sender_country_alpha3";
ALTER TABLE "operation" DROP COLUMN "recipient_country_alpha3";
