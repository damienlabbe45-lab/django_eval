PRAGMA foreign_keys = OFF;

BEGIN TRANSACTION;

CREATE TABLE "new__skills_userskills" (
    "Skills_id" bigint NOT NULL REFERENCES "skills_skillsdate" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" bigint NOT NULL REFERENCES "skills_useremail" ("id") DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY ("user_id", "Skills_id")
);

INSERT INTO "new__skills_userskills" ("Skills_id", "user_id")
SELECT DISTINCT "Skills_id", "user_id"
FROM "skills_userskills";

DROP TABLE "skills_userskills";

ALTER TABLE "new__skills_userskills" RENAME TO "skills_userskills";

COMMIT;

PRAGMA foreign_keys = ON;
PRAGMA foreign_key_check;