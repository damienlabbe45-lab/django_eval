BEGIN TRANSACTION;

ALTER TABLE skills_skills ADD COLUMN is_need integer;

UPDATE skills_skills
SET
    is_need = CASE WHEN name_skills LIKE 'aide pour %' THEN 1 ELSE 0 END,
    name_skills = CASE WHEN name_skills LIKE 'aide pour %' THEN SUBSTR(name_skills, 11) ELSE name_skills END;

ALTER TABLE skills_userskills RENAME COLUMN Skills_id TO skills;
ALTER TABLE skills_userskills RENAME COLUMN user_id TO user;

CREATE UNIQUE INDEX "UniqueNameSkillsOrNeed"
ON "skills_skills" ("name_skills", "is_need");

COMMIT;

VACUUM;