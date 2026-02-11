<div align="center">
    <img src="https://github.com/user-attachments/assets/4f74dcb8-b636-48c9-b1fd-8dcd3b8c84fb" alt="Logo" height="120" width="210">
</div>

<div align="center">
<h1>Prédiction du prix des billets d'avion</h1>
</div>

L'objectif de ce projet est de prédire le prix des billets d'avion en fonction de diverses caractéristiques telles que la date de réservation, la durée du vol, le nombre d'escales, etc. Nous allons effectuer une analyse exploratoire des données (EDA) pour comprendre les relations entre les différentes variables et le prix des billets. Ensuite, nous construirons un modèle prédictif pour estimer le prix des billets en fonction des caractéristiques disponibles.

Le dataset `Clean_Dataset.csv` provient de Kaggle, et est disponible [ICI](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction).

## Installation

### Prérequis

- Python 3.12 ou supérieur
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gestionnaire de paquets)

### Étapes

1. Cloner le dépôt :

```bash
git clone https://github.com/<votre-utilisateur>/Projet_flight_price.git
cd Projet_flight_price
```

2. Installer les dépendances avec uv :

```bash
uv sync
```

3. Lancer le notebook pour entraîner le modèle :

```bash
uv run jupyter notebook flight-price.ipynb
```

4. Lancer le dashboard Streamlit :

```bash
uv run streamlit run dashboard.py
```