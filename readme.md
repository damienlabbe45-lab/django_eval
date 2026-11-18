# qu'est-ce que c'est comme projet

il s'agit d'un projet en django  pour démontrer mes compétences en django et en interface web. Ce projet n'est pas destiné à être mis à jour tout les ans.

# comment faire pour l'utiliser?

vous devez faire d'abord 

```git pull https://github.com/damienlabbe45-lab/django_eval```

dans un environnement virtuel python.

ensuite dans un terminal situé sur le même dossier et avec l'environnement virtuel activé, vous devez taper:

```pip install -r requirements.txt```

puis 

```py manage.py sqlmigrate skills 0001```

ensuite ```cd echangecompetence```

enfin 

```python manage.py runserver   0.0.0.0:80```

la dernière étape qui vous reste,est de juste d'aller sur votre navigateur internet et de mettre:

```http://127.0.0.1/skills/``` ou les nombres sont l'addresse ip. à noter que c'est pour tester et débugger , pas pour faire de la production.

je vous conseille de ensuite vous créez un script qui active directement l'environnement virtuel et fasse toutes ces étapes à votre place.

il vous restera à remplir la base de données de donnée à vous.

vous pouvez vous amusez à tout modifier, mais c'est à vos risques et périls.

# à quoi sert le code

le code actuel permet de représenter une application ou les utilisateurs s'entraident en fonctions de leurs compétences et besoins.