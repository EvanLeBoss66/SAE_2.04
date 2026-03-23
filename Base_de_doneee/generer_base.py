import pandas as pd
from faker import Faker
import random
import os

fake = Faker('fr_FR')

BATCH_SIZE = 100_000
TOTAL_TENRAC = 1_000_000
NB_ORGANISMES = 5000
NB_ENTREPRISES = 1000
NB_PARTENAIRES = 1000
NB_PLATS = 500
NB_SAUCES = 200
NB_INGREDIENTS = 1000
NB_MACHINES = 2000

print(" Début de la génération de TOUTES les tables...")

ids_organisme = list(range(1, NB_ORGANISMES + 1))
ids_partenaires = list(range(1, NB_PARTENAIRES + 1))
ids_entreprises = list(range(1, NB_ENTREPRISES + 1))
ids_plats = list(range(1, NB_PLATS + 1))
ids_sauces = list(range(1, NB_SAUCES + 1))
ids_ingredients = list(range(1, NB_INGREDIENTS + 1))

print(" Génération des tables indépendantes (Niveau 1)...")

pd.DataFrame({'idGenre': [1, 2, 3], 'nom': ['Homme', 'Femme', 'Autre']}).to_csv('genre.csv', index=False, sep=';')
pd.DataFrame({'idGrade': range(1, 6), 'nom': [f"Grade {i}" for i in range(1, 6)]}).to_csv('grade.csv', index=False, sep=';')
pd.DataFrame({'idRang': range(1, 4), 'nom': [f"Rang {i}" for i in range(1, 4)]}).to_csv('rang.csv', index=False, sep=';')
pd.DataFrame({'idTitre': range(1, 4), 'nom': [f"Titre {i}" for i in range(1, 4)]}).to_csv('titre.csv', index=False, sep=';')
pd.DataFrame({'idDignite': range(1, 4), 'nom': [f"Dignité {i}" for i in range(1, 4)]}).to_csv('dignite.csv', index=False, sep=';')

pd.DataFrame({'idOrganisme': ids_organisme}).to_csv('organisme.csv', index=False, sep=';')
pd.DataFrame({'idEntreprise': ids_entreprises, 'raisonSociale': [fake.company() for _ in ids_entreprises], 'siret': [fake.siret() for _ in ids_entreprises]}).to_csv('entreprise.csv', index=False, sep=';')
pd.DataFrame({'idPartenaire': ids_partenaires, 'nom': [fake.company()[:50] for _ in ids_partenaires], 'adresse': [fake.address()[:70].replace('\n', ' ') for _ in ids_partenaires]}).to_csv('adressepartenaire.csv', index=False, sep=';')

pd.DataFrame({'idAllergenes': range(1, 51), 'nom': [f"Allergène {fake.word()}" for _ in range(1, 51)]}).to_csv('allergies.csv', index=False, sep=';')
pd.DataFrame({'idCroyance': range(1, 21), 'nom': [f"Croyance {fake.word()}" for _ in range(1, 21)]}).to_csv('croyance.csv', index=False, sep=';')
pd.DataFrame({'idConviction': range(1, 21), 'conviction': [f"Conviction {fake.word()}" for _ in range(1, 21)]}).to_csv('convictions.csv', index=False, sep=';')
pd.DataFrame({'idIngredient': ids_ingredients, 'nom': [f"Ingrédient {fake.word()}" for _ in ids_ingredients]}).to_csv('ingredient.csv', index=False, sep=';')
pd.DataFrame({'idPlat': ids_plats, 'intitule': [f"Plat {fake.word()}" for _ in ids_plats]}).to_csv('plat.csv', index=False, sep=';')
pd.DataFrame({'idSauce': ids_sauces, 'nom': [f"Sauce {fake.word()}" for _ in ids_sauces]}).to_csv('sauce.csv', index=False, sep=';')

print(" Génération des tables liées (Niveau 2)...")

pd.DataFrame({'idOrganisme': ids_organisme, 'dateCreation': [fake.date_between(start_date='-50y', end_date='today') for _ in ids_organisme]}).to_csv('ordre.csv', index=False, sep=';')
pd.DataFrame({'idOrganisme_1': ids_organisme, 'nom': [f"Club {fake.city()}" for _ in ids_organisme], 'idOrganisme': ids_organisme}).to_csv('club.csv', index=False, sep=';')

pd.DataFrame({'idIngredient': ids_ingredients[:300]}).to_csv('legume.csv', index=False, sep=';')

registres = []
for org in ids_organisme:
    registres.append({'idOrganisme': org, 'idRegistre': 1, 'dateOuverture': fake.date_between(start_date='-5y', end_date='-1y'), 'derniereModification': fake.date_between(start_date='-1y', end_date='today')})
pd.DataFrame(registres).to_csv('registre.csv', index=False, sep=';')

print(f" Génération de {TOTAL_TENRAC} Tenrac (Membres)...")

filename_tenrac = 'tenrac.csv'
if os.path.exists(filename_tenrac): os.remove(filename_tenrac)

for start in range(0, TOTAL_TENRAC, BATCH_SIZE):
    current_batch = min(BATCH_SIZE, TOTAL_TENRAC - start)
    noms_batch = [fake.last_name() for _ in range(current_batch)]
    prenoms_batch = [fake.first_name() for _ in range(current_batch)]
    
    df_tenrac = pd.DataFrame({
        'idOrganisme': [random.choice(ids_organisme) for _ in range(current_batch)],
        'idMembre': range(start + 1, start + current_batch + 1),
        'nom': noms_batch,
        'prenom': prenoms_batch,
        'courriel': [f"{prenoms_batch[j].lower()}.{noms_batch[j].lower()}{start + j}@example.com" for j in range(current_batch)],
        'adresse': [fake.street_address().replace('\n', ' ') for _ in range(current_batch)],
        'telephonePortable': [fake.phone_number() for _ in range(current_batch)],
        'telephoneFixe': [fake.phone_number() for _ in range(current_batch)],
        'codePostal': [fake.postcode() for _ in range(current_batch)],
        'idGenre': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'idTitre': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'idRang': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'idDignite': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'idGrade': [random.choice(range(1, 6)) for _ in range(current_batch)]
    })
    
    df_tenrac.to_csv(filename_tenrac, mode='a', index=False, header=not os.path.exists(filename_tenrac), sep=';')
    print(f" Avancement Tenrac : {start + current_batch}/{TOTAL_TENRAC}")

print(" Génération des Rendez-vous et de la Maintenance...")

certifs = []
for i in range(1, NB_MACHINES + 1):
    certifs.append({
        'idCertification': i,
        'dateDeCertification': fake.date_between(start_date='-1y', end_date='today'),
        'idOrganisme': random.choice(ids_organisme),
        'idMembre': random.randint(1, TOTAL_TENRAC)
    })
df_certif = pd.DataFrame(certifs)
df_certif.to_csv('certificationentretien.csv', index=False, sep=';')

rdv_list = []
for i in range(1, 5000):
    rdv_list.append({
        'idRdv': i,
        'heure': fake.time(),
        'date_': fake.date_between(start_date='-1y', end_date='today'),
        'idPartenaire': random.choice(ids_partenaires),
        'idOrganisme': random.choice(ids_organisme),
        'idMembre': random.randint(1, TOTAL_TENRAC)
    })
pd.DataFrame(rdv_list).to_csv('rdv.csv', index=False, sep=';')

print(" Génération des tables d'associations...")

accompagnements = set()
while len(accompagnements) < 1000:
    accompagnements.add((random.choice(ids_plats), random.choice(ids_sauces)))
pd.DataFrame(list(accompagnements), columns=['idPlat', 'idSauce']).to_csv('accompagne.csv', index=False, sep=';')

compositions = set()
while len(compositions) < 2000:
    compositions.add((random.choice(ids_plats), random.choice(ids_ingredients)))
pd.DataFrame(list(compositions), columns=['idPlat', 'idIngredient']).to_csv('compose.csv', index=False, sep=';')

print(" Tous les fichiers CSV ont été générés avec succès pour toutes les entités !")