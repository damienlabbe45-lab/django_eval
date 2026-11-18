from django.db.models import CharField, Model, DateTimeField, BooleanField, ForeignKey, CASCADE

class Skills(Model):
    name_skills:CharField =CharField(max_length = 500)

    def __str__(self):
        return self.name_skills

class SkillsDate(Model):
    skills = ForeignKey(Skills, on_delete=CASCADE)
    date_begin: DateTimeField = DateTimeField("date published")
    date_before: DateTimeField = DateTimeField("date published")
    boolean: BooleanField = BooleanField()

class Useremail(Model):
    user =ForeignKey('auth.User', on_delete=CASCADE)
    email:CharField = CharField(max_length = 100)

    def __str__(self):
        return f"{self.user.username} {self.email}"


class UserSkills(Model):
    user = ForeignKey('Useremail', on_delete=CASCADE)
    Skills= ForeignKey(SkillsDate, on_delete = CASCADE)
