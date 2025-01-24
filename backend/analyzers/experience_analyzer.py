import re
from datetime import datetime
from typing import List, Optional
from models.cv_models import Experience
from dateutil import parser

class ExperienceAnalyzer:
    def __init__(self):
        self.date_patterns = {
            'range': r'((?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)|(?:jan|fév|mar|avr|mai|juin|juil|août|sept|oct|nov|déc))\s*\d{4}\s*[-–]\s*(?:(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)|(?:jan|fév|mar|avr|mai|juin|juil|août|sept|oct|nov|déc)|présent|actuel)\s*\d{0,4}',
            'single': r'(?:depuis|depuis le)?\s*(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s*\d{4}'
        }
        self.company_patterns = [
            r'(?:chez|société|entreprise)\s+([A-Z][A-Za-z\s]+)',
            r'@\s*([A-Z][A-Za-z\s]+)'
        ]

    def analyze(self, text: str) -> List[Experience]:
        experiences = []
        sections = self._split_into_experience_sections(text)

        for section in sections:
            experience = self._parse_experience(section)
            if experience:
                experiences.append(experience)

        return experiences

    def _split_into_experience_sections(self, text: str) -> List[str]:
        # Séparer le texte en sections d'expérience
        sections = []
        current_section = []

        for line in text.split('\n'):
            if self._is_new_experience(line):
                if current_section:
                    sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)

        if current_section:
            sections.append('\n'.join(current_section))

        return sections

    def _is_new_experience(self, line: str) -> bool:
        # Vérifie si la ligne commence une nouvelle expérience
        if any(pattern in line.lower() for pattern in self.date_patterns.values()):
            return True
        return False

    def _parse_experience(self, text: str) -> Optional[Experience]:
        try:
            # Extraire les dates
            dates = self._extract_dates(text)
            if not dates:
                return None

            # Extraire l'entreprise
            entreprise = self._extract_company(text) or "Non spécifié"

            # Extraire le poste
            poste = self._extract_position(text) or "Non spécifié"

            # Extraire la description
            description = self._extract_description(text)

            return Experience(
                debut=dates['debut'],
                fin=dates.get('fin'),
                entreprise=entreprise,
                poste=poste,
                lieu=None,  # À implémenter si nécessaire
                description=description
            )
        except Exception:
            return None

    def _extract_dates(self, text: str) -> Optional[dict]:
        for pattern in self.date_patterns.values():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                dates_str = match.group(0)
                try:
                    if '-' in dates_str or '–' in dates_str:
                        start, end = re.split('[-–]', dates_str)
                        return {
                            'debut': parser.parse(start.strip()),
                            'fin': parser.parse(end.strip()) if 'présent' not in end.lower() else None
                        }
                    else:
                        return {'debut': parser.parse(dates_str.strip())}
                except:
                    continue
        return None

    def _extract_company(self, text: str) -> Optional[str]:
        for pattern in self.company_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    def _extract_position(self, text: str) -> Optional[str]:
        # Essayer de trouver le poste dans la première ligne
        first_line = text.split('\n')[0]
        # Enlever la partie date
        for pattern in self.date_patterns.values():
            first_line = re.sub(pattern, '', first_line)
        # Enlever l'entreprise
        for pattern in self.company_patterns:
            first_line = re.sub(pattern, '', first_line)

        position = first_line.strip()
        return position if position else None

    def _extract_description(self, text: str) -> List[str]:
        lines = text.split('\n')[1:]  # Skip first line (title)
        description = []
        for line in lines:
            line = line.strip()
            if line and not any(pattern in line.lower() for pattern in self.date_patterns.values()):
                description.append(line)
        return description