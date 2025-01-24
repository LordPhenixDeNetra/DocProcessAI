from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class Formation:
    debut: date
    fin: Optional[date]
    diplome: str
    etablissement: str
    lieu: Optional[str]
    description: Optional[str]

@dataclass
class Experience:
    debut: date
    fin: Optional[date]
    entreprise: str
    poste: str
    lieu: Optional[str]
    description: List[str]

@dataclass
class Langue:
    nom: str
    niveau: str  # ex: "Courant", "Intermédiaire", "Débutant"

@dataclass
class CompetenceTechnique:
    categorie: str  # ex: "Programmation", "Bases de données"
    competences: List[str]

@dataclass
class CVData:
    # Informations personnelles
    nom: str
    prenom: str
    email: str
    telephone: str
    adresse: Optional[str]
    linkedin: Optional[str]

    # Parcours
    formations: List[Formation]
    experiences: List[Experience]

    # Compétences
    competences_techniques: List[CompetenceTechnique]
    langues: List[Langue]

    # Autres
    certifications: Optional[List[str]]
    centres_interet: Optional[List[str]]