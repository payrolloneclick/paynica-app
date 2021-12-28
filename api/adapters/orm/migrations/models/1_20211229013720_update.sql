-- upgrade --
ALTER TABLE "user" ALTER COLUMN "phone_code" TYPE VARCHAR(8) USING "phone_code"::VARCHAR(8);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "phone_code" TYPE VARCHAR(16) USING "phone_code"::VARCHAR(16);
