from django.db.models import CharField, Model, DateTimeField, BooleanField, ForeignKey, CASCADE

class Skills(Model):
    name_skills:CharField =CharField(max_length = 500)

    def __str__(self) -> str:
        return self.name_skills

class SkillsDate(Model):
    skills = ForeignKey(Skills, on_delete=CASCADE)
    date: DateTimeField = DateTimeField("date published")
    boolean: BooleanField = BooleanField()
    def __str__(self) -> str:
        return  f" {self.skills}   {self.date}"

class Useremail(Model):
    user =ForeignKey('auth.User', on_delete=CASCADE)
    email:CharField = CharField(max_length = 100)

    def __str__(self) -> str:
        return f"{self.user}   {self.email}"


class UserSkills(Model):
    user = ForeignKey(Useremail, on_delete= CASCADE)
    Skills:list[SkillsDate]
