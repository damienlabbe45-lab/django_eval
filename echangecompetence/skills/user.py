from django.contrib.auth.models import User

def create_user():
    """this functon create users different of the superuser or staff"""
    users = [('aervhuygjhg',"a@yahoo.fr",'azerfghjhgrefgh98Gt'),('Mia Hurting', 'a@free.com','Gè56çjGgv09!hgT'),
         ('Ane', 'ane@ane.com','hihanhihanhihanhihanhihan'),('GhuybFred%jh', 'ee@example.com', 'Ddfbth^jdbç6g'),
         ('PiRATE','ert@example.com', 'GHygddbdhfb'), ('Hyb^@hsgd','ert1@example.com', 'HuybFred'),
         ('Bhuj', 'az@example.fr', 'HUKnVgfc'), ('GHJUYB', 'SD@example.com', 'Nujhy@nbv'),
         ('TUTUJhbvhfh', 'vb@example.com', 'hshdhfnjdUJNGC98YB'), ('XCF9877609HGGNBFG', 'edfh@example.com', 'gFDDSDZER09è!!'),
         ('POIYTRVGGF', 'bn@example.com', 'CORRIGGE'), ('SECRET DEFENSE', 'khfsjg@uniq.com', 'oJ^6k+jGr5-,98dhGtfZjgç65WtèHYiùP8hGfV'),
         ('LEROUX', 'leroux@gmail.com', 'MoTDEP@SSE123456'), ('ces koi se truk?', 'kévindu20@gmail.com', 'Kévindu20'),
         ('Antoine Leverreux Cannibale', 'cannibale@example.com', 'BVGzt675@Hgvsve'), 
         ('Candide', 'candide@example.com', 'Oh on est fessé en cadence de 5'),('VIVALDI', 'moi@example.com', 'LES 4 SAISONS DE Moi'),
         ('Lefantôme Casper', 'lefantome@casper.com', 'HanteLesserveurs'), ('Will Treaty', 'montrouge@example.com', 'Par la loi des rodeurs')
         , ('GUIDE', 'joe@example.com', 'Où on mêne les 2 décades de trajet des calèches pour aller faire Brest-Toulouse alors que le tgv est à côté et fait le trajet en 56h')]
    for use in users:
        user = User.objects.create_user(
            username=use[0],
            email=use[1],
            password=use[2] 
            )
        user.save()

