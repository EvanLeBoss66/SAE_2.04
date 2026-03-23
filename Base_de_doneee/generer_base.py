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

print("Debut de la generation de TOUTES les tables...")

ids_organisme = list(range(1, NB_ORGANISMES + 1))
ids_partenaires = list(range(1, NB_PARTENAIRES + 1))
ids_entreprises = list(range(1, NB_ENTREPRISES + 1))
ids_plats = list(range(1, NB_PLATS + 1))
ids_sauces = list(range(1, NB_SAUCES + 1))
ids_ingredients = list(range(1, NB_INGREDIENTS + 1))

# CORRECTION : utiliser un set pour éviter les doublons de paires (ID_ORGANISME, ID_MEMBRE)
echantillon_membres_set = set()

print("Generation des tables independantes (Niveau 1)...")

pd.DataFrame({'ID_GENRE': [1, 2, 3], 'GENRE': ['Homme', 'Femme', 'Autre']}).to_csv('genre.csv', index=False, sep=';')
pd.DataFrame({'ID_GRADE': range(1, 6), 'GRADE': [f"Grade {i}" for i in range(1, 6)]}).to_csv('grade.csv', index=False, sep=';')
pd.DataFrame({'ID_RANG': range(1, 4), 'RANG': [f"Rang {i}" for i in range(1, 4)]}).to_csv('rang.csv', index=False, sep=';')
pd.DataFrame({'ID_TITRE': range(1, 4), 'TITRE': [f"Titre {i}" for i in range(1, 4)]}).to_csv('titre.csv', index=False, sep=';')
pd.DataFrame({'ID_DIGNITE': range(1, 4), 'DIGNITE': [f"Dignite {i}" for i in range(1, 4)]}).to_csv('dignite.csv', index=False, sep=';')
pd.DataFrame({'ID_ROLE': range(1, 6), 'ROLE': [f"Role {i}" for i in range(1, 6)]}).to_csv('role.csv', index=False, sep=';')

pd.DataFrame({'ID_ORGANISME': ids_organisme}).to_csv('organisme.csv', index=False, sep=';')
pd.DataFrame({'ID_ENTREPRISE': ids_entreprises, 'RAISONSOCIALE': [fake.company()[:50] for _ in ids_entreprises], 'SIRET': [fake.siret() for _ in ids_entreprises]}).to_csv('entreprise.csv', index=False, sep=';')
pd.DataFrame({'ID_PARTENAIRE': ids_partenaires, 'NOM': [fake.company()[:50] for _ in ids_partenaires], 'ADRESSE': [fake.address()[:70].replace('\n', ' ') for _ in ids_partenaires]}).to_csv('adresse_partenaire.csv', index=False, sep=';')

pd.DataFrame({'ID_ALLERGENE': range(1, 51), 'NOM': [fake.word()[:50] for _ in range(1, 51)]}).to_csv('allergies.csv', index=False, sep=';')
pd.DataFrame({'ID_CROYANCE': range(1, 21), 'NOM': [fake.word()[:50] for _ in range(1, 21)]}).to_csv('croyance.csv', index=False, sep=';')
pd.DataFrame({'ID_CONVICTION': range(1, 21), 'CONVICTION': [fake.word()[:50] for _ in range(1, 21)]}).to_csv('convictions.csv', index=False, sep=';')
pd.DataFrame({'ID_INGREDIENT': ids_ingredients, 'NOM': [fake.word()[:50] for _ in ids_ingredients]}).to_csv('ingredient.csv', index=False, sep=';')
pd.DataFrame({'ID_PLAT': ids_plats, 'INTITULE': [fake.word()[:50] for _ in ids_plats]}).to_csv('plat.csv', index=False, sep=';')
pd.DataFrame({'ID_SAUCE': ids_sauces, 'NOM': [fake.word()[:50] for _ in ids_sauces]}).to_csv('sauce.csv', index=False, sep=';')

print("Generation des tables liees (Niveau 2)...")

pd.DataFrame({'ID_ORGANISME': ids_organisme, 'DATE_DE_CREATION': [fake.date_between(start_date='-50y', end_date='today') for _ in ids_organisme]}).to_csv('ordre.csv', index=False, sep=';')
pd.DataFrame({'ID_ORGANISME_1': ids_organisme, 'NOM': [fake.city()[:50] for _ in ids_organisme], 'ID_ORGANISME': ids_organisme}).to_csv('club.csv', index=False, sep=';')

pd.DataFrame({'ID_INGREDIENT': ids_ingredients[:300]}).to_csv('legume.csv', index=False, sep=';')

registres = []
for org in ids_organisme:
    registres.append({
        'ID_ORGANISME': org,
        'ID_REGISTRE': 1,
        'DATE_OUVERTURE': fake.date_between(start_date='-5y', end_date='-1y'),
        'DERNIERE_MODIFICAITON': fake.date_between(start_date='-1y', end_date='today')
    })
pd.DataFrame(registres).to_csv('registre.csv', index=False, sep=';')

print(f"Generation de {TOTAL_TENRAC} Tenrac (Membres)...")

filename_tenrac = 'tenrac.csv'
if os.path.exists(filename_tenrac):
    os.remove(filename_tenrac)

for start in range(0, TOTAL_TENRAC, BATCH_SIZE):
    current_batch = min(BATCH_SIZE, TOTAL_TENRAC - start)
    noms_batch = [fake.last_name()[:50] for _ in range(current_batch)]
    prenoms_batch = [fake.first_name()[:50] for _ in range(current_batch)]
    orgs_batch = [random.choice(ids_organisme) for _ in range(current_batch)]
    membres_id_batch = list(range(start + 1, start + current_batch + 1))

    # CORRECTION : on stocke les paires uniques dans un set (pas de doublon possible)
    for o, m in zip(orgs_batch[:1500], membres_id_batch[:1500]):
        echantillon_membres_set.add((o, m))

    df_tenrac = pd.DataFrame({
        'ID_ORGANISME': orgs_batch,
        'ID_MEMBRE': membres_id_batch,
        'NOM': noms_batch,
        'PRENOM': prenoms_batch,
        'COURRIEL': [f"{prenoms_batch[j].lower()}.{noms_batch[j].lower()}{start + j}@example.com"[:50] for j in range(current_batch)],
        'ADRESSE': [fake.street_address()[:50].replace('\n', ' ') for _ in range(current_batch)],
        'TELEPHONE_PORTABLE': [fake.phone_number()[:20] for _ in range(current_batch)],
        'TELEPHONE_FIXE': [fake.phone_number()[:20] for _ in range(current_batch)],
        'ID_GENRE': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'ID_TITRE': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'ID_RANG': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'ID_DIGNITE': [random.choice([1, 2, 3]) for _ in range(current_batch)],
        'ID_GRADE': [random.choice(range(1, 6)) for _ in range(current_batch)]
    })

    df_tenrac.to_csv(filename_tenrac, mode='a', index=False, header=not os.path.exists(filename_tenrac), sep=';')
    print(f"Avancement Tenrac : {start + current_batch}/{TOTAL_TENRAC}")

# CORRECTION : convertir le set en liste après la boucle, toutes les paires sont uniques
echantillon_membres = list(echantillon_membres_set)
print(f"Nombre de membres uniques dans l'echantillon : {len(echantillon_membres)}")

print("Generation des Tables enfant du Tenrac (Importants, Cartes)...")

# CORRECTION : taille basée sur la liste finale (unique), pas sur une valeur arbitraire
taille_voulu = min(10000, len(echantillon_membres))
echantillon_carte = echantillon_membres[:taille_voulu]

pd.DataFrame({
    'ID_CARTE': range(1, taille_voulu + 1),
    'DATE_DE_DELIVRANCE': [fake.date_between(start_date='-2y', end_date='today') for _ in range(taille_voulu)],
    'DATE_FIN_VALIDITE': [fake.date_between(start_date='today', end_date='+2y') for _ in range(taille_voulu)],
    'ID_ENTREPRISE': [random.choice(ids_entreprises) for _ in range(taille_voulu)],
    'ID_ORGANISME': [m[0] for m in echantillon_carte],
    'ID_MEMBRE': [m[1] for m in echantillon_carte]
}).to_csv('carte.csv', index=False, sep=';')

nb_importants = min(5000, len(echantillon_membres))
# CORRECTION : echantillon_membres est déjà unique (issu du set), pas besoin de set() supplémentaire
tenrac_imp = echantillon_membres[:nb_importants]

pd.DataFrame({
    'ID_ORGANISME': [m[0] for m in tenrac_imp],
    'ID_MEMBRE': [m[1] for m in tenrac_imp],
    'POSITION_': [fake.word()[:50] for _ in tenrac_imp]
}).to_csv('tenrac_important.csv', index=False, sep=';')

print("Generation des Rendez-vous et de la Maintenance...")

certifs = []
for i in range(1, NB_MACHINES + 1):
    membre_imp = random.choice(tenrac_imp)
    certifs.append({
        'ID_CERTIFICATION': f"CERT_{i}",
        'DATE_DE_CERTIFICATION': str(fake.date_between(start_date='-1y', end_date='today')),
        'ID_ORGANISME': membre_imp[0],
        'ID_MEMBRE': membre_imp[1]
    })
df_certif = pd.DataFrame(certifs)
df_certif.to_csv('certification_entretien.csv', index=False, sep=';')

type_entretien = []
for cert in certifs:
    for type_id in range(1, 3):
        type_entretien.append({
            'ID_CERTIFICATION': cert['ID_CERTIFICATION'],
            'ID_TYPE': type_id,
            'TYPE': f"Type {type_id}"[:50],
            'NOM': fake.word()[:50],
            'PERIODICITE': "Mensuelle"
        })
pd.DataFrame(type_entretien).to_csv('type_entretien.csv', index=False, sep=';')

machines_list = []
for i in range(1, NB_MACHINES + 1):
    machines_list.append({
        'ID_MACHINE': i,
        'NOM': f"Machine {fake.word()}"[:50],
        'ID_CERTIFICATION': certifs[i-1]['ID_CERTIFICATION']
    })
pd.DataFrame(machines_list).to_csv('machine.csv', index=False, sep=';')

modeles = []
for mach in machines_list:
    cert_ent_lies = [te for te in type_entretien if te['ID_CERTIFICATION'] == mach['ID_CERTIFICATION']]
    te_choisi = random.choice(cert_ent_lies)
    modeles.append({
        'ID_MACHINE': mach['ID_MACHINE'],
        'ID_MODELE': 1,
        'NOM': fake.word()[:50],
        'MARQUE': fake.company()[:50],
        'ID_CERTIFICATION': mach['ID_CERTIFICATION'],
        'ID_TYPE': te_choisi['ID_TYPE']
    })
pd.DataFrame(modeles).to_csv('modele.csv', index=False, sep=';')

rdv_list = []
for i in range(1, 10001):
    membre_imp = random.choice(tenrac_imp)
    rdv_list.append({
        'ID_RDV': i,
        'HEURE': fake.time(),
        'DATE_': fake.date_between(start_date='-1y', end_date='today'),
        'ID_PARTENAIRE': random.choice(ids_partenaires),
        'ID_ORGANISME': membre_imp[0],
        'ID_MEMBRE': membre_imp[1]
    })
pd.DataFrame(rdv_list).to_csv('rdv.csv', index=False, sep=';')

print("Generation des tables d'associations...")

coop_list = set()
while len(coop_list) < 2000:
    coop_list.add((random.choice(ids_organisme), random.choice(ids_partenaires)))
pd.DataFrame(list(coop_list), columns=['ID_ORGANISME', 'ID_PARTENAIRE']).to_csv('coopere.csv', index=False, sep=';')

reu_list = set()
while len(reu_list) < 5000:
    rdv_id = random.randint(1, 10000)
    membre_tenrac = random.choice(echantillon_membres)
    reu_list.add((membre_tenrac[0], membre_tenrac[1], rdv_id))
pd.DataFrame(list(reu_list), columns=['ID_ORGANISME', 'ID_MEMBRE', 'ID_RDV']).to_csv('reunion.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_plats), random.choice(ids_ingredients)) for _ in range(2000))), columns=['ID_PLAT', 'ID_INGREDIENT']).to_csv('compose.csv', index=False, sep=';')

pd.DataFrame(list(set((random.randint(1, 10000), random.choice(ids_plats)) for _ in range(5000))), columns=['ID_RDV', 'ID_PLAT']).to_csv('deguste.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_sauces), random.choice(ids_ingredients)) for _ in range(2000))), columns=['ID_SAUCE', 'ID_INGREDIENT']).to_csv('constitue.csv', index=False, sep=';')

pd.DataFrame(list(set((random.randint(1, 10000), random.randint(1, NB_MACHINES)) for _ in range(5000))), columns=['ID_RDV', 'ID_MACHINE']).to_csv('utilise.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_ingredients[:300]), random.randint(1, 50)) for _ in range(1000))), columns=['ID_INGREDIENT', 'ID_ALLERGENE']).to_csv('donne.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_plats), random.choice(ids_sauces)) for _ in range(1000))), columns=['ID_PLAT', 'ID_SAUCE']).to_csv('accompagne.csv', index=False, sep=';')

allergies_tenrac = set()
while len(allergies_tenrac) < 5000:
    membre = random.choice(echantillon_membres)
    allergies_tenrac.add((membre[0], membre[1], random.randint(1, 50)))
pd.DataFrame(list(allergies_tenrac), columns=['ID_ORGANISME', 'ID_MEMBRE', 'ID_ALLERGENE']).to_csv('allergique_a_.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_ingredients[:300]), random.randint(1, 20)) for _ in range(1000))), columns=['ID_INGREDIENT', 'ID_CROYANCE']).to_csv('heurt.csv', index=False, sep=';')

croyances_tenrac = set()
while len(croyances_tenrac) < 5000:
    membre = random.choice(echantillon_membres)
    croyances_tenrac.add((membre[0], membre[1], random.randint(1, 20)))
pd.DataFrame(list(croyances_tenrac), columns=['ID_ORGANISME', 'ID_MEMBRE', 'ID_CROYANCE']).to_csv('croit.csv', index=False, sep=';')

convictions_tenrac = set()
while len(convictions_tenrac) < 5000:
    membre = random.choice(echantillon_membres)
    convictions_tenrac.add((membre[0], membre[1], random.randint(1, 20)))
pd.DataFrame(list(convictions_tenrac), columns=['ID_ORGANISME', 'ID_MEMBRE', 'ID_CONVICTION']).to_csv('a_des.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(ids_ingredients[:300]), random.randint(1, 20)) for _ in range(1000))), columns=['ID_INGREDIENT', 'ID_CONVICTION']).to_csv('transgresse.csv', index=False, sep=';')

archive_list = set()
for org_reg in registres:
    for _ in range(3):
        mach_ent_liaison = random.choice(type_entretien)
        archive_list.add((org_reg['ID_ORGANISME'], org_reg['ID_REGISTRE'], mach_ent_liaison['ID_CERTIFICATION'], mach_ent_liaison['ID_TYPE']))
pd.DataFrame(list(archive_list), columns=['ID_ORGANISME', 'ID_REGISTRE', 'ID_CERTIFICATION', 'ID_TYPE']).to_csv('archive.csv', index=False, sep=';')

pd.DataFrame(list(set((random.choice(tenrac_imp)[0], random.choice(tenrac_imp)[1], random.randint(1, 5)) for _ in range(3000))), columns=['ID_ORGANISME', 'ID_MEMBRE', 'ID_ROLE']).to_csv('a_un.csv', index=False, sep=';')

print("Tous les fichiers CSV ont ete generes avec succes pour toutes les entites du nouveau SQL !")