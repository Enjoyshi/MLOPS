# MLOPS project

Dans ce projet vous aurez à mettre en production un modèle de machine learning de votre choix.

Le déploiement du modèle devra se faire automatique via un script simple. 

Il faudra que le modèle puisse gérer une certaine charge. Vous pourrez soit faire du batch processing / une API HTTP ou du streaming. 

Il faudra que le système soit capable de : 
 - soit de se réentraîner tout seul régulièrement grâce à des données nouvellement labelisée
 - soit de faire remonter des alertes si il existe des risques que le modèle ne marche plus (distributional shift)
 
Bonus : le modèle sera packagé dans un conteneur docker ou sera déployé via Kubernetes / kubeflow

## A) Choix du sujet

Nous avons choisi à faire du streaming à l'aide du Kafka. Notre système sera capable de faire remonter des alertes si il existe des risques que le modèle ne marche plus (distributional shift). Et l'entièreté du projet est dockerisé.

## B) Notre équipe

| Name             | Email (@epita.fr)         | Github account |
| ---------------- | ------------------------- | -------------- |
| Théo Perinet     | theo.perinet              | `TheoPeri`     |
| Hao Ye           | hao.ye                    | `Enjoyshi`     |

## C) Démarches

### C.1) Requirements
Pour exécuter le projet, il est nécessaire d'avoir installé :
* Python 3.9
* `python3-pip`
* `virtualenv`
* `docker`

Exécutez les commandes suivantes pour importer et construire le projet :
* Git clone le projet
* Run `python -m venv .venv` dans le dossier du projet. Faites attention à choisir la bonne version de python, par exemple `python3.9 -m venv .venv`
* Run `source ./.venv/bin/activate` pour activer l'environnement virtuel
* Run `pip install -r requirements.txt`

### C.2) Entraîner le modèle
```
python train/train_model.py
```

### C.3) Lancer le projet
```
docker compose up
```

### C.4) Frontend
```
http://localhost:8501
```


