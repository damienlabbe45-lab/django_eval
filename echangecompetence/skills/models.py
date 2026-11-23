from django.db.models import CharField, Model, DateTimeField, BooleanField, ForeignKey, CASCADE, UniqueConstraint, CompositePrimaryKey

class Skills(Model):
    """models for the table skills_skills . this class represent the need and skills."""
    name_skills:CharField =CharField(max_length = 500)
    is_need = BooleanField()

    class Meta:
        constraints =[UniqueConstraint(fields=["name_skills","is_need"], name = "UniqueNameSkillsOrNeed" )]

    def __str__(self):
        return f"{"aide pour " if self.is_need else ""}{self.name_skills}"

class SkillsDate(Model):
    """models for the table SkillDate. this class represent the need and skills with this date"""
    skills = ForeignKey(Skills, on_delete=CASCADE)
    date_begin: DateTimeField = DateTimeField("date published")
    date_before: DateTimeField = DateTimeField("date published")
    boolean: BooleanField = BooleanField()
    
    class Meta:
        constraints =[UniqueConstraint(fields= ["skills", "date_begin", "date_before", "boolean"], name= "UniqueSkillsDate")]


class UserSkills(Model):
    """models for the table UserSkills. this class represent the association of skills or need with the user."""
    user = ForeignKey('auth.User', on_delete=CASCADE, db_column="user")
    skills= ForeignKey(SkillsDate, on_delete = CASCADE, db_column = "skills")
    pk = CompositePrimaryKey("user","skills")
