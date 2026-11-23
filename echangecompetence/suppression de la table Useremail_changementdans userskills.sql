BEGIN TRANSACTION;

CREATE TABLE "skills_userskills_new" (
    "skills" bigint NOT NULL REFERENCES "skills_skillsdate" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY ("user", "skills")
);

INSERT INTO "skills_userskills_new" ("skills", "user")
SELECT "skills", "user" FROM "skills_userskills";

DROP TABLE "skills_userskills";
ALTER TABLE "skills_userskills_new" RENAME TO "skills_userskills";

DROP TABLE IF EXISTS "skills_useremail";

COMMIT;