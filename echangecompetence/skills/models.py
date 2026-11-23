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

class Useremail(Model):
    """models for the table Useremail. this class represent users of apply but this table is redundant with the class
    auth.User but it was possible if the develloper doesn't unterstand Django. this class my disapear if the author will."""
    user =ForeignKey('auth.User', on_delete=CASCADE)
    email:CharField = CharField(max_length = 100)

    class Meta:
        constraints = [UniqueConstraint(fields= ["user", "email"], name= "UniqueUserEmail")]

    def __str__(self):
        return f"{self.user.username} {self.email}"


class UserSkills(Model):
    """models for the table UserSkills. this class represent the association of skills or need with the user."""
    user = ForeignKey('Useremail', on_delete=CASCADE, db_column="user")
    skills= ForeignKey(SkillsDate, on_delete = CASCADE, db_column = "skills")
    pk = CompositePrimaryKey("user","skills")
