# analyzers/education_analyzer.py
import re
from datetime import datetime
from typing import List, Optional
from models.cv_models import Formation

class EducationAnalyzer:
    def __init__(self):
        self.date_patterns = [
            r'(19|20)\d{2}',  # Années complètes (ex: 2020)
            r'\d{2}\/\d{2}\/(\d{4})',  # Format DD/MM/YYYY
            r'\d{2}\-\d{2}\-(\d{4})',  # Format DD-MM-YYYY
            r'(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})'  # Format mois année
        ]
        self.diplome_patterns = [
            r'master\s+\w+',
            r'licence\s+\w+',
            r'bac\s*\+\s*\d',
            r'dut\s+\w+',
            r'bts\s+\w+',
        ]

    def analyze(self, text: str) -> List[Formation]:
        """
        Analyse le texte pour extraire les formations
        """
        formations = []
        # Diviser le texte en sections
        sections = text.split('\n\n')

        for section in sections:
            if self._is_education_section(section):
                formation = self._parse_formation(section)
                if formation:
                    formations.append(formation)

        return formations

    def _is_education_section(self, text: str) -> bool:
        """
        Vérifie si la section contient des informations sur l'éducation
        """
        education_keywords = [
            'formation', 'diplôme', 'études', 'bac+', 'master',
            'licence', 'dut', 'bts', 'école', 'université'
        ]
        return any(keyword in text.lower() for keyword in education_keywords)

    def _parse_date(self, text: str) -> Optional[datetime]:
        try:
            for pattern in self.date_patterns:
                match = re.search(pattern, text)
                if match:
                    year = match.group(match.lastindex or 1)
                    if len(year) == 2:
                        year = '20' + year
                    return datetime.strptime(year, '%Y')
            return None
        except Exception as e:
            print(f"Erreur de parsing de date: {str(e)}")
            return None

    def _parse_formation(self, text: str) -> Optional[Formation]:
        try:
            # Trouver toutes les dates
            dates = []
            for pattern in self.date_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    date = self._parse_date(match.group(0))
                    if date:
                        dates.append(date)

            # Trouver le diplôme
            diplome = None
            for pattern in self.diplome_patterns:
                match = re.search(pattern, text.lower())
                if match:
                    diplome = match.group(0)
                    break

            # Trouver l'établissement (ajout de cette fonctionnalité)
            etablissement_patterns = [
                r'université\s+[\w\s]+',
                r'école\s+[\w\s]+',
                r'institut\s+[\w\s]+',
                r'lycée\s+[\w\s]+'
            ]
            etablissement = None
            for pattern in etablissement_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    etablissement = match.group(0)
                    break

            if dates:
                dates.sort()
                return Formation(
                    debut=min(dates).date(),
                    fin=max(dates).date() if len(dates) > 1 else None,
                    diplome=diplome.title() if diplome else "Non spécifié",
                    etablissement=etablissement or "Non spécifié",
                    lieu=None,
                    description=None
                )
            return None
        except Exception as e:
            print(f"Erreur dans le parsing de formation: {str(e)}")
            return None