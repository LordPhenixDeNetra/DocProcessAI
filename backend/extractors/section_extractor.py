# from typing import Dict, Optional
#
# class CVSectionDetector:
#     def __init__(self):
#         self.section_patterns = {
#             'contact': [
#                 'contact', 'coordonnées', 'phone', 'email',
#                 'adresse', 'téléphone', 'contact information'
#             ],
#             'education': [
#                 'education', 'formation', 'études', 'diplôme',
#                 'baccalauréat', 'université', 'academic', 'cursus',
#                 'parcours', 'scolaire'
#             ],
#             'experience': [
#                 'expérience', 'professionnelle', 'career',
#                 'stage', 'emplois', 'work experience', 'employment'
#             ],
#             'skills': [
#                 'compétences', 'skills', 'expertise', 'technologies',
#                 'outils', 'technical', 'competencies'
#             ],
#             'languages': [
#                 'langues', 'language', 'linguistique',
#                 'language proficiency'
#             ],
#             'interests': [
#                 'centres d\'intérêt', 'hobbies', 'loisirs',
#                 'interests', 'activities', 'centres d\'intérêt'
#             ],
#             'profile': [
#                 'profil', 'about me', 'à propos', 'resume',
#                 'summary', 'profile'
#             ]
#         }
#
#     def detect_sections(self, text: str) -> Dict[str, str]:
#         sections = {}
#         lines = text.split('\n')
#         current_section = None
#         current_content = []
#
#         for line in lines:
#             detected_section = self._identify_section(line.strip().lower())
#             if detected_section:
#                 if current_section and current_content:
#                     sections[current_section] = '\n'.join(current_content).strip()
#                 current_section = detected_section
#                 current_content = []
#             elif current_section and line.strip():
#                 current_content.append(line)
#
#         # Ajouter la dernière section
#         if current_section and current_content:
#             sections[current_section] = '\n'.join(current_content).strip()
#
#         return sections
#
#     def _identify_section(self, line: str) -> Optional[str]:
#         """
#         Identifie la section à partir d'une ligne de texte
#         """
#         line = line.lower()
#         # Retirer les caractères spéciaux et la ponctuation
#         line = ''.join(c for c in line if c.isalnum() or c.isspace())
#
#         for section, patterns in self.section_patterns.items():
#             for pattern in patterns:
#                 # Nettoyer le pattern de la même manière
#                 clean_pattern = ''.join(c for c in pattern.lower() if c.isalnum() or c.isspace())
#                 if clean_pattern in line:
#                     return section
#
#         return None






from .base_extractor import BaseExtractor
from typing import Dict, Optional

class SectionExtractor(BaseExtractor):
    def __init__(self):
        self.section_patterns = {
            'contact': [
                'contact', 'coordonnées', 'coordonnees', 'informations personnelles'
            ],
            'formation': [
                'formation', 'éducation', 'education', 'diplômes', 'diplomes',
                'parcours académique', 'parcours scolaire'
            ],
            'experience': [
                'expérience', 'experience', 'parcours professionnel',
                'expériences professionnelles'
            ],
            'competences': [
                'compétences', 'competences', 'skills', 'savoir-faire',
                'qualifications'
            ],
            'langues': [
                'langues', 'languages', 'compétences linguistiques'
            ],
            'interets': [
                'centres d\'intérêt', "centres d'intérêt", 'loisirs', 'hobbies'
            ]
        }

    def extract(self, content: str) -> Dict[str, str]:
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            section = self._identify_section(line.strip())
            if section:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = section
                current_content = []
            elif current_section and line.strip():
                current_content.append(line)

        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _identify_section(self, line: str) -> Optional[str]:
        line = line.lower()
        for section_name, patterns in self.section_patterns.items():
            if any(pattern in line for pattern in patterns):
                return section_name
        return None