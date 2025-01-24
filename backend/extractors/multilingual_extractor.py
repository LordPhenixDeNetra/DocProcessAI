from typing import Dict, List
import re

class MultilingualExtractor:
    def __init__(self):
        self.patterns = {
            'fr': {
                'email': r'[\w\.-]+@[\w\.-]+\.\w+',
                'phone': r'(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}',
                'education': {
                    'diplomes': [
                        'baccalauréat', 'licence', 'master',
                        'doctorat', 'bts', 'dut'
                    ],
                    'institutions': [
                        'université', 'école', 'lycée', 'institut'
                    ]
                },
                'experience': {
                    'postes': [
                        'stage', 'alternance', 'cdd', 'cdi',
                        'chef de projet', 'développeur', 'ingénieur'
                    ]
                }
            },
            'en': {
                'email': r'[\w\.-]+@[\w\.-]+\.\w+',
                'phone': r'\+?1?\s*\(?(\d{3})\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                'education': {
                    'diplomas': [
                        'bachelor', 'master', 'phd', 'degree',
                        'certificate'
                    ],
                    'institutions': [
                        'university', 'college', 'school', 'institute'
                    ]
                },
                'experience': {
                    'positions': [
                        'internship', 'full-time', 'part-time',
                        'project manager', 'developer', 'engineer'
                    ]
                }
            }
        }

    def detect_language(self, text: str) -> str:
        # Compte les occurrences de mots-clés dans chaque langue
        scores = {'fr': 0, 'en': 0}

        for lang in ['fr', 'en']:
            # Vérifier les mots-clés d'éducation
            for keyword in (self.patterns[lang]['education']['diplomas'] +
                            self.patterns[lang]['education']['institutions']):
                if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                    scores[lang] += 1

            # Vérifier les mots-clés d'expérience
            for keyword in self.patterns[lang]['experience']['positions']:
                if re.search(r'\b' + keyword + r'\b', text, re.IGNORECASE):
                    scores[lang] += 1

        return max(scores.items(), key=lambda x: x[1])[0]

    def extract_info(self, text: str, lang: str = None) -> Dict:
        if not lang:
            lang = self.detect_language(text)

        extracted_info = {
            'contact': self._extract_contact(text, lang),
            'education': self._extract_education(text, lang),
            'experience': self._extract_experience(text, lang),
            'detected_language': lang
        }

        return extracted_info

    def _extract_contact(self, text: str, lang: str) -> Dict:
        contact_info = {}

        # Extraire email
        email_match = re.search(self.patterns[lang]['email'], text)
        if email_match:
            contact_info['email'] = email_match.group(0)

        # Extraire téléphone
        phone_match = re.search(self.patterns[lang]['phone'], text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)

        return contact_info