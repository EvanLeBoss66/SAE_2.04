import pandas as pd
import random
import os
from faker import Faker

fake = Faker('fr_FR')

lot, total = 100000, 1000000
nb_org, nb_ent, nb_par, nb_plt, nb_sau, nb_ing, nb_mac = 5000, 1000, 1000, 500, 200, 1000, 2000
org_ids, ent_ids, par_ids, plt_ids, sau_ids, ing_ids = [list(range(1, n+1)) for n in (nb_org, nb_ent, nb_par, nb_plt, nb_sau, nb_ing)]
paires = set()

chevaliers = []
maitres = []

# Sauvegarde
def sv(df, nom): 
    df.to_csv(nom, index=False, sep=';')
    print(nom, len(df))

# References
sv(pd.DataFrame({'ID_GENRE':[1,2,3], 'GENRE':['Homme','Femme','Autre']}), 'genre.csv')
sv(pd.DataFrame({'ID_GRADE':range(1,6), 'GRADE':[f'Grade {x}' for x in range(1,6)]}), 'grade.csv')
sv(pd.DataFrame({'ID_RANG':range(1,4), 'RANG':['Rang 1','Rang 2','Rang 3']}), 'rang.csv')
sv(pd.DataFrame({'ID_TITRE':range(1,4), 'TITRE':['Titre 1','Titre 2','Titre 3']}), 'titre.csv')
sv(pd.DataFrame({'ID_DIGNITE':range(1,4), 'DIGNITE':['Dignite 1','Dignite 2','Dignite 3']}), 'dignite.csv')
sv(pd.DataFrame({'ID_ROLE':range(1,6), 'ROLE':[f'Role {x}' for x in range(1,6)]}), 'role.csv')

# Organismes
sv(pd.DataFrame({'ID_ORGANISME':org_ids}), 'organisme.csv')
sv(pd.DataFrame({'ID_ENTREPRISE':ent_ids, 'RAISONSOCIALE':[fake.company()[:50] for _ in ent_ids], 'SIRET':[fake.siret() for _ in ent_ids]}), 'entreprise.csv')
sv(pd.DataFrame({'ID_PARTENAIRE':par_ids, 'NOM':[fake.company()[:50] for _ in par_ids], 'ADRESSE':[fake.address()[:70].replace('\n',' ') for _ in par_ids]}), 'adresse_partenaire.csv')

# Métier
sv(pd.DataFrame({'ID_ALLERGENE':range(1,51), 'NOM':[fake.word()[:50] for _ in range(50)]}), 'allergies.csv')
sv(pd.DataFrame({'ID_CROYANCE':range(1,21), 'NOM':[fake.word()[:50] for _ in range(20)]}), 'croyance.csv')
sv(pd.DataFrame({'ID_CONVICTION':range(1,21), 'CONVICTION':[fake.word()[:50] for _ in range(20)]}), 'convictions.csv')
sv(pd.DataFrame({'ID_INGREDIENT':ing_ids, 'NOM':[fake.word()[:50] for _ in ing_ids]}), 'ingredient.csv')
sv(pd.DataFrame({'ID_PLAT':plt_ids, 'INTITULE':[fake.word()[:50] for _ in plt_ids]}), 'plat.csv')
sv(pd.DataFrame({'ID_SAUCE':sau_ids, 'NOM':[fake.word()[:50] for _ in sau_ids]}), 'sauce.csv')
sv(pd.DataFrame({'ID_INGREDIENT':ing_ids[:300]}), 'legume.csv')

# Ordres et Registres
sv(pd.DataFrame({'ID_ORGANISME':org_ids, 'DATE_DE_CREATION':[fake.date_between('-50y', 'today') for _ in org_ids]}), 'ordre.csv')
sv(pd.DataFrame({'ID_ORGANISME_1':org_ids, 'NOM':[fake.city()[:50] for _ in org_ids], 'ID_ORGANISME':org_ids}), 'club.csv')

regs = [{'ID_ORGANISME':o, 'ID_REGISTRE':1, 'DATE_OUVERTURE':fake.date_between('-5y', '-1y'), 'DERNIERE_MODIFICATION':fake.date_between('-1y', 'today')} for o in org_ids]
sv(pd.DataFrame(regs), 'registre.csv')

fcsv = 'tenrac.csv'
if os.path.exists(fcsv): os.remove(fcsv)

for deb in range(0, total, lot):
    nb = min(lot, total - deb)
    noms, prenoms = [fake.last_name()[:50] for _ in range(nb)], [fake.first_name()[:50] for _ in range(nb)]
    orgs, ids = [random.choice(org_ids) for _ in range(nb)], list(range(deb+1, deb+nb+1))
    paires.update(zip(orgs[:2000], ids[:2000]))
    
    genres = [random.randint(1,3) for _ in range(nb)]
    titres = [random.randint(1,3) for _ in range(nb)]
    rangs = [random.randint(1,3) for _ in range(nb)]
    dignites = [random.randint(1,3) for _ in range(nb)]
    grades = [random.randint(1,5) for _ in range(nb)]

    for i in range(nb):
        paire = (orgs[i], ids[i])
        if grades[i] >= 4:
            chevaliers.append(paire)
        if dignites[i] == 1:
            maitres.append(paire)

    pd.DataFrame({
        'ID_ORGANISME': orgs, 'ID_MEMBRE': ids, 'NOM': noms, 'PRENOM': prenoms,
        'COURRIEL': [f"{prenoms[i].lower()}.{noms[i].lower()}{deb+i}@example.com" for i in range(nb)],
        'ADRESSE': [fake.street_address()[:50].replace('\n',' ') for _ in range(nb)],
        'TELEPHONE_PORTABLE': [fake.phone_number()[:20] for _ in range(nb)],
        'TELEPHONE_FIXE': [fake.phone_number()[:20] for _ in range(nb)],
        'ID_GENRE': genres, 'ID_TITRE': titres,
        'ID_RANG': rangs, 'ID_DIGNITE': dignites,
        'ID_GRADE': grades
    }).to_csv(fcsv, mode='a', index=False, header=(deb==0), sep=';')

ech = list(paires)

chevaliers = list(set(chevaliers).intersection(set(ech)))
maitres = list(set(maitres).intersection(set(ech)))

ec, timp = ech[:min(20000, len(ech))], ech[:min(10000, len(ech))]
sv(pd.DataFrame({'ID_CARTE': range(1, len(ec)+1), 'DATE_DE_DELIVRANCE': [fake.date_between('-2y', 'today') for _ in ec], 'DATE_FIN_VALIDITE': [fake.date_between('today', '+2y') for _ in ec], 'ID_ENTREPRISE': [random.choice(ent_ids) for _ in ec], 'ID_ORGANISME': [x[0] for x in ec], 'ID_MEMBRE': [x[1] for x in ec]}), 'carte.csv')
sv(pd.DataFrame({'ID_ORGANISME':[x[0] for x in timp], 'ID_MEMBRE':[x[1] for x in timp], 'POSITION_':[fake.word()[:50] for _ in timp]}), 'tenrac_important.csv')

certs = []
for i in range(1, nb_mac + 1):
    le_maitre = random.choice(maitres) if maitres else random.choice(timp)
    certs.append({
        'ID_CERTIFICATION': f'CERT_{i}',
        'DATE_DE_CERTIFICATION': fake.date_between('-1y', 'today'),
        'ID_ORGANISME': le_maitre[0],
        'ID_MEMBRE': le_maitre[1]
    })
sv(pd.DataFrame(certs), 'certification_entretien.csv')

tent = [{'ID_CERTIFICATION': c['ID_CERTIFICATION'], 'ID_TYPE': tid, 'TYPE': f'Type {tid}', 'NOM': fake.word()[:50], 'PERIODICITE': 'Mensuelle'} for c in certs for tid in (1, 2)]
sv(pd.DataFrame(tent), 'type_entretien.csv')
machs = [{'ID_MACHINE': i, 'NOM': f"Machine {fake.word()[:42]}", 'ID_CERTIFICATION': certs[i-1]['ID_CERTIFICATION']} for i in range(1, nb_mac+1)]
sv(pd.DataFrame(machs), 'machine.csv')
sv(pd.DataFrame([{'ID_MACHINE': m['ID_MACHINE'], 'ID_MODELE': 1, 'NOM': fake.word()[:50], 'MARQUE': fake.company()[:50], 'ID_CERTIFICATION': m['ID_CERTIFICATION'], 'ID_TYPE': random.choice([t['ID_TYPE'] for t in tent if t['ID_CERTIFICATION'] == m['ID_CERTIFICATION']])} for m in machs]), 'modele.csv')
sv(pd.DataFrame([{'ID_RDV': i, 'HEURE': fake.time(), 'DATE_': fake.date_between('-1y', 'today'), 'ID_PARTENAIRE': random.choice(par_ids), 'ID_ORGANISME': random.choice(timp)[0], 'ID_MEMBRE': random.choice(timp)[1]} for i in range(1, 10001)]), 'rdv.csv')

def g(n, mx, fn, cols):
    t = set()
    while len(t) < mx: t.add(fn())
    sv(pd.DataFrame(list(t), columns=cols), n)

reunions_data = set()
for rdv_id in range(1, 10001):
    chef = random.choice(chevaliers) if chevaliers else random.choice(ech)
    reunions_data.add((chef[0], chef[1], rdv_id))
    for _ in range(random.randint(1, 4)):
        random_m = random.choice(ech)
        reunions_data.add((random_m[0], random_m[1], rdv_id))

sv(pd.DataFrame(list(reunions_data), columns=['ID_ORGANISME','ID_MEMBRE','ID_RDV']), 'reunion.csv')

g('coopere.csv', 2000, lambda: (random.choice(org_ids), random.choice(par_ids)), ['ID_ORGANISME','ID_PARTENAIRE'])
g('compose.csv', 2000, lambda: (random.choice(plt_ids), random.choice(ing_ids)), ['ID_PLAT','ID_INGREDIENT'])
g('deguste.csv', 5000, lambda: (random.randint(1, 10000), random.choice(plt_ids)), ['ID_RDV','ID_PLAT'])
g('constitue.csv', 2000, lambda: (random.choice(sau_ids), random.choice(ing_ids)), ['ID_SAUCE','ID_INGREDIENT'])
g('utilise.csv', 5000, lambda: (random.randint(1, 10000), random.randint(1, nb_mac)), ['ID_RDV','ID_MACHINE'])
g('donne.csv', 1000, lambda: (random.choice(ing_ids), random.randint(1, 50)), ['ID_INGREDIENT','ID_ALLERGENE'])
g('accompagne.csv', 1000, lambda: (random.choice(plt_ids), random.choice(sau_ids)), ['ID_PLAT','ID_SAUCE'])
g('allergique_a_.csv', 5000, lambda: (*random.choice(ech), random.randint(1, 50)), ['ID_ORGANISME','ID_MEMBRE','ID_ALLERGENE'])
g('heurt.csv', 1000, lambda: (random.choice(ing_ids), random.randint(1, 20)), ['ID_INGREDIENT','ID_CROYANCE'])
g('croit.csv', 5000, lambda: (*random.choice(ech), random.randint(1, 20)), ['ID_ORGANISME','ID_MEMBRE','ID_CROYANCE'])
g('a_des.csv', 5000, lambda: (*random.choice(ech), random.randint(1, 20)), ['ID_ORGANISME','ID_MEMBRE','ID_CONVICTION'])
g('transgresse.csv', 1000, lambda: (random.choice(ing_ids), random.randint(1, 20)), ['ID_INGREDIENT','ID_CONVICTION'])

arch = set((r['ID_ORGANISME'], r['ID_REGISTRE'], t['ID_CERTIFICATION'], t['ID_TYPE']) for r in regs for t in [random.choice(tent) for _ in range(3)])
sv(pd.DataFrame(list(arch), columns=['ID_ORGANISME','ID_REGISTRE','ID_CERTIFICATION','ID_TYPE']), 'archive.csv')

g('a_un.csv', 3000, lambda: (*random.choice(timp), random.randint(1, 5)), ['ID_ORGANISME','ID_MEMBRE','ID_ROLE'])

print('Fini !')