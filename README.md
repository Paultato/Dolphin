# Projet Dolphin

## Membres du groupe
* MARIN Issam
* LEGRAND Antoine
* BANUS Paul

## Installation
`pip install virtualenv`

`virtualenv env`

`pip install -r requirements.txt`

`source env/bin/activate`

Pour ajouter des paquets pip au projet, installer avec pip (dans virtualenv) les paquets puis ajouter le paquet et sa version dans le fichier `requirements.txt`

Pour sortir de virtualenv : `deactivate`

Lancement de MySQL (MAC) : `brew services start mysql`

Arrêt de MySQL (MAC) : `brew services stop mysql`

Pour initialiser la base de données : `mysql -u root` `SOURCE init.sql;`

## Technologies utilisées

* python 3
* pip
* MySQL
* peewee
* virtualenv