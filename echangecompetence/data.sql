INSERT OR IGNORE INTO skills_skills(name_skills) 
VALUES("word"), 
("excel"), 
("python"),
("java"), 
("sql"), 
("arroser les plantes"), 
("peindre les murs"), 
("créer un univers de roleplay"), 
("créer des fiches de personnage de roleplay"),
("créé une base de données");


INSERT OR IGNORE INTO skills_skillsdate(date_begin, date_before, boolean, skills_id)
VALUES ('2025-06-22', '2027-07-15', FALSE, 1),
('2026-06-22', '2027-07-15', True, 1),
('2026-08-22', '2027-07-15', True, 1),
('2025-04-22', '2026-07-15', FALSE, 5),
('2026-04-22', '2026-07-15', TRUE, 5),
('2026-04-22', '2026-02-15', TRUE, 5),
('2025-05-22', '2026-09-15', TRUE, 8),
('2025-05-22', '2026-03-15', False, 8),
('2026-05-22', '2026-09-15', TRUE, 8),
('2025-05-22', '2026-09-15', TRUE, 6),
('2026-05-22', '2026-09-15', FALSE, 6),
('2025-05-22', '2026-02-15', TRUE, 6),