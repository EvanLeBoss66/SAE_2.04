CREATE TABLE Rang(
   idRang NUMBER(1,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idRang)
);

CREATE TABLE Dignite(
   idDignite NUMBER(1,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idDignite)
);

CREATE TABLE AdressePartenaire(
   idPartenaire NUMBER(10),
   nom CHAR(50),
   adresse CHAR(70) NOT NULL,
   PRIMARY KEY(idPartenaire)
);

CREATE TABLE Titre(
   idTitre NUMBER(1,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idTitre)
);

CREATE TABLE Entreprise(
   idEntreprise NUMBER(10,0),
   raisonSociale VARCHAR2(50),
   siret VARCHAR2(50),
   PRIMARY KEY(idEntreprise)
);

CREATE TABLE Grade(
   idGrade NUMBER(1,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idGrade)
);

CREATE TABLE Organisme(
   idOrganisme NUMBER(10,0),
   PRIMARY KEY(idOrganisme)
);

CREATE TABLE Plat(
   idPlat NUMBER(10,0),
   intitule VARCHAR2(50),
   PRIMARY KEY(idPlat)
);

CREATE TABLE Sauce(
   idSauce NUMBER(10,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idSauce)
);

CREATE TABLE Allergies(
   idAllergenes NUMBER(10,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idAllergenes)
);

CREATE TABLE Croyance(
   idCroyance NUMBER(10,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idCroyance)
);

CREATE TABLE Ingredient(
   idIngredient NUMBER(10,0),
   nom VARCHAR2(50),
   PRIMARY KEY(idIngredient)
);

CREATE TABLE Genre(
   idGenre NUMBER(1,0),
   nom VARCHAR2(11),
   PRIMARY KEY(idGenre)
);

CREATE TABLE Convictions(
   idConviction NUMBER(10,0),
   conviction VARCHAR2(50),
   PRIMARY KEY(idConviction)
);

CREATE TABLE Ordre(
   idOrganisme NUMBER(10,0),
   dateCreation DATE,
   PRIMARY KEY(idOrganisme),
   FOREIGN KEY(idOrganisme) REFERENCES Organisme(idOrganisme)
);

CREATE TABLE Club(
   idOrganisme_1 NUMBER(10,0),
   nom VARCHAR2(50),
   idOrganisme NUMBER(10,0),
   PRIMARY KEY(idOrganisme_1),
   FOREIGN KEY(idOrganisme_1) REFERENCES Organisme(idOrganisme),
   FOREIGN KEY(idOrganisme) REFERENCES Ordre(idOrganisme)
);

CREATE TABLE Legume(
   idIngredient NUMBER(10,0),
   PRIMARY KEY(idIngredient),
   FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient)
);

CREATE TABLE Registre(
   idOrganisme NUMBER(10,0),
   idRegistre NUMBER(10),
   dateOuverture VARCHAR2(50),
   derniereModification VARCHAR2(50),
   PRIMARY KEY(idOrganisme, idRegistre),
   FOREIGN KEY(idOrganisme) REFERENCES Club(idOrganisme_1)
);

CREATE TABLE Tenrac(
   idOrganisme NUMBER(10,0),
   idMembre NUMBER(10,0),
   nom VARCHAR2(50),
   prenom VARCHAR2(50),
   courriel VARCHAR2(50),
   adresse VARCHAR2(50),
   telephonePortable VARCHAR2(50),
   telephoneFixe VARCHAR2(50),
   codePostal VARCHAR2(10),
   idGenre NUMBER(1,0) NOT NULL,
   idTitre NUMBER(1,0),
   idRang NUMBER(1,0),
   idDignite NUMBER(1,0),
   idGrade NUMBER(1,0) NOT NULL,
   PRIMARY KEY(idOrganisme, idMembre),
   FOREIGN KEY(idOrganisme) REFERENCES Club(idOrganisme_1),
   FOREIGN KEY(idGenre) REFERENCES Genre(idGenre),
   FOREIGN KEY(idTitre) REFERENCES Titre(idTitre),
   FOREIGN KEY(idRang) REFERENCES Rang(idRang),
   FOREIGN KEY(idDignite) REFERENCES Dignite(idDignite),
   FOREIGN KEY(idGrade) REFERENCES Grade(idGrade)
);

CREATE TABLE Rdv(
   idRdv NUMBER(10,0),
   heure DATE NOT NULL,
   date_ DATE NOT NULL,
   idPartenaire NUMBER(10) NOT NULL,
   idOrganisme NUMBER(10,0) NOT NULL,
   idMembre NUMBER(10,0) NOT NULL,
   PRIMARY KEY(idRdv),
   FOREIGN KEY(idPartenaire) REFERENCES AdressePartenaire(idPartenaire),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre)
);

CREATE TABLE CertificationEntretien(
   idCertification NUMBER(10,0),
   dateDeCertification VARCHAR2(50),
   idOrganisme NUMBER(10,0) NOT NULL,
   idMembre NUMBER(10,0) NOT NULL,
   PRIMARY KEY(idCertification),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre)
);

CREATE TABLE TypeEntretien(
   idCertification NUMBER(10,0),
   idType NUMBER(10,0),
   type VARCHAR2(50),
   nom VARCHAR2(50),
   periodicite VARCHAR2(50),
   PRIMARY KEY(idCertification, idType),
   FOREIGN KEY(idCertification) REFERENCES CertificationEntretien(idCertification)
);

CREATE TABLE Carte(
   idCarte NUMBER(10,0),
   dateDeDelivrance DATE,
   dateFinValidite DATE,
   idEntreprise NUMBER(10,0) NOT NULL,
   idOrganisme NUMBER(10,0) NOT NULL,
   idMembre NUMBER(10,0) NOT NULL,
   PRIMARY KEY(idCarte),
   FOREIGN KEY(idEntreprise) REFERENCES Entreprise(idEntreprise),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre)
);

CREATE TABLE Machine(
   idMachine NUMBER(10,0),
   nom VARCHAR2(50),
   idCertification NUMBER(10,0) NOT NULL,
   PRIMARY KEY(idMachine),
   UNIQUE(idCertification),
   FOREIGN KEY(idCertification) REFERENCES CertificationEntretien(idCertification)
);

CREATE TABLE Modele(
   idMachine NUMBER(10,0),
   idModele NUMBER(10,0),
   nom VARCHAR2(50),
   marque VARCHAR2(50),
   idCertification NUMBER(10,0) NOT NULL,
   idType NUMBER(10,0) NOT NULL,
   PRIMARY KEY(idMachine, idModele),
   FOREIGN KEY(idMachine) REFERENCES Machine(idMachine),
   FOREIGN KEY(idCertification, idType) REFERENCES TypeEntretien(idCertification, idType)
);

CREATE TABLE Identifiant(
   idOrganisme NUMBER(10,0),
   idMachine NUMBER(10,0),
   idModele NUMBER(10,0),
   numeroSerie NUMBER(10,0),
   dateAacquisition VARCHAR2(50),
   dateFinGarantie VARCHAR2(50),
   PRIMARY KEY(idOrganisme, idMachine, idModele, numeroSerie),
   FOREIGN KEY(idOrganisme) REFERENCES Club(idOrganisme_1),
   FOREIGN KEY(idMachine, idModele) REFERENCES Modele(idMachine, idModele)
);

CREATE TABLE Coopere(
   idOrganisme NUMBER(10,0),
   idPartenaire NUMBER(10),
   PRIMARY KEY(idOrganisme, idPartenaire),
   FOREIGN KEY(idOrganisme) REFERENCES Ordre(idOrganisme),
   FOREIGN KEY(idPartenaire) REFERENCES AdressePartenaire(idPartenaire)
);

CREATE TABLE Reunion(
   idOrganisme NUMBER(10,0),
   idMembre NUMBER(10,0),
   idRdv NUMBER(10,0),
   PRIMARY KEY(idOrganisme, idMembre, idRdv),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre),
   FOREIGN KEY(idRdv) REFERENCES Rdv(idRdv)
);

CREATE TABLE Compose(
   idPlat NUMBER(10,0),
   idIngredient NUMBER(10,0),
   PRIMARY KEY(idPlat, idIngredient),
   FOREIGN KEY(idPlat) REFERENCES Plat(idPlat),
   FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient)
);

CREATE TABLE Deguste(
   idRdv NUMBER(10,0),
   idPlat NUMBER(10,0),
   PRIMARY KEY(idRdv, idPlat),
   FOREIGN KEY(idRdv) REFERENCES Rdv(idRdv),
   FOREIGN KEY(idPlat) REFERENCES Plat(idPlat)
);

CREATE TABLE Constitue(
   idSauce NUMBER(10,0),
   idIngredient NUMBER(10,0),
   PRIMARY KEY(idSauce, idIngredient),
   FOREIGN KEY(idSauce) REFERENCES Sauce(idSauce),
   FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient)
);

CREATE TABLE Utilise(
   idRdv NUMBER(10,0),
   idMachine NUMBER(10,0),
   PRIMARY KEY(idRdv, idMachine),
   FOREIGN KEY(idRdv) REFERENCES Rdv(idRdv),
   FOREIGN KEY(idMachine) REFERENCES Machine(idMachine)
);

CREATE TABLE Accompagne(
   idPlat NUMBER(10,0),
   idSauce NUMBER(10,0),
   PRIMARY KEY(idPlat, idSauce),
   FOREIGN KEY(idPlat) REFERENCES Plat(idPlat),
   FOREIGN KEY(idSauce) REFERENCES Sauce(idSauce)
);

CREATE TABLE Allergique_a(
   idOrganisme NUMBER(10,0),
   idMembre NUMBER(10,0),
   idAllergenes NUMBER(10,0),
   PRIMARY KEY(idOrganisme, idMembre, idAllergenes),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre),
   FOREIGN KEY(idAllergenes) REFERENCES Allergies(idAllergenes)
);

CREATE TABLE Heurt(
   idIngredient NUMBER(10,0),
   idCroyance NUMBER(10,0),
   PRIMARY KEY(idIngredient, idCroyance),
   FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient),
   FOREIGN KEY(idCroyance) REFERENCES Croyance(idCroyance)
);

CREATE TABLE Croit(
   idOrganisme NUMBER(10,0),
   idMembre NUMBER(10,0),
   idCroyance NUMBER(10,0),
   PRIMARY KEY(idOrganisme, idMembre, idCroyance),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre),
   FOREIGN KEY(idCroyance) REFERENCES Croyance(idCroyance)
);

CREATE TABLE Archive(
   idOrganisme NUMBER(10,0),
   idRegistre NUMBER(10),
   idCertification NUMBER(10,0),
   idType NUMBER(10,0),
   PRIMARY KEY(idOrganisme, idRegistre, idCertification, idType),
   FOREIGN KEY(idOrganisme, idRegistre) REFERENCES Registre(idOrganisme, idRegistre),
   FOREIGN KEY(idCertification, idType) REFERENCES TypeEntretien(idCertification, idType)
);

CREATE TABLE ADes(
   idOrganisme NUMBER(10,0),
   idMembre NUMBER(10,0),
   idConviction NUMBER(10,0),
   PRIMARY KEY(idOrganisme, idMembre, idConviction),
   FOREIGN KEY(idOrganisme, idMembre) REFERENCES Tenrac(idOrganisme, idMembre),
   FOREIGN KEY(idConviction) REFERENCES Convictions(idConviction)
);

CREATE TABLE Transgresse(
   idIngredient NUMBER(10,0),
   idConviction NUMBER(10,0),
   PRIMARY KEY(idIngredient, idConviction),
   FOREIGN KEY(idIngredient) REFERENCES Legume(idIngredient),
   FOREIGN KEY(idConviction) REFERENCES Convictions(idConviction)
);

CREATE TABLE Donne(
   idAllergenes NUMBER(10,0),
   idIngredient NUMBER(10,0),
   PRIMARY KEY(idAllergenes, idIngredient),
   FOREIGN KEY(idAllergenes) REFERENCES Allergies(idAllergenes),
   FOREIGN KEY(idIngredient) REFERENCES Ingredient(idIngredient)
);
