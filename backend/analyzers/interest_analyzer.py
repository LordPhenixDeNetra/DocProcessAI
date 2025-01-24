from typing import List, Dict

class InterestAnalyzer:
    def __init__(self):
        # Catégories de centres d'intérêt
        self.categories = {
            'sports': [
                'football', 'basketball', 'tennis', 'natation', 'running',
                'fitness', 'yoga', 'cyclisme', 'randonnée', 'sport'
            ],
            'culture': [
                'lecture', 'cinéma', 'théâtre', 'musique', 'art',
                'photographie', 'littérature', 'musée', 'concert'
            ],
            'voyages': [
                'voyage', 'découverte', 'tourisme', 'exploration',
                'backpacking', 'road-trip'
            ],
            'tech_science': [
                'technologie', 'science', 'robotique', 'intelligence artificielle',
                'développement', 'programmation', 'innovation'
            ],
            'associatif': [
                'bénévolat', 'association', 'humanitaire', 'social',
                'engagement', 'communauté'
            ]
        }

    def analyze(self, text: str) -> Dict[str, List[str]]:
        """
        Analyse la section centres d'intérêt du CV.
        Retourne un dictionnaire avec les intérêts catégorisés.
        """
        try:
            # Convertir en minuscules pour la recherche
            text = text.lower()

            # Résultat par catégorie
            result = {
                'sports': [],
                'culture': [],
                'voyages': [],
                'tech_science': [],
                'associatif': [],
                'autres': []  # Pour les intérêts non catégorisés
            }

            # Extraire les sections pertinentes
            sections = self._extract_interest_section(text)

            # Analyser chaque ligne
            for line in sections:
                categorized = False
                # Chercher dans chaque catégorie
                for category, keywords in self.categories.items():
                    for keyword in keywords:
                        if keyword in line:
                            interest = self._clean_interest(line)
                            if interest and interest not in result[category]:
                                result[category].append(interest)
                                categorized = True
                                break

                # Si non catégorisé et semble être un intérêt valide
                if not categorized and len(line.strip()) > 2:
                    interest = self._clean_interest(line)
                    if interest and interest not in result['autres']:
                        result['autres'].append(interest)

            # Nettoyer le résultat (enlever les catégories vides)
            return {k: v for k, v in result.items() if v}

        except Exception as e:
            print(f"Erreur dans l'analyse des centres d'intérêt: {str(e)}")
            return {}

    def _extract_interest_section(self, text: str) -> List[str]:
        """
        Extrait la section des centres d'intérêt du texte.
        """
        sections = []
        interest_keywords = ['centres d\'intérêt', 'loisirs', 'hobbies', 'intérêts', 'activités']

        lines = text.split('\n')
        is_interest_section = False

        for line in lines:
            # Détecter le début de la section
            if any(keyword in line.lower() for keyword in interest_keywords):
                is_interest_section = True
                continue

            # Si on est dans la section d'intérêts et la ligne n'est pas vide
            if is_interest_section and line.strip():
                # Vérifier si on commence une nouvelle section principale
                if self._is_new_main_section(line):
                    break
                sections.append(line.strip())

        return sections

    def _is_new_main_section(self, line: str) -> bool:
        """
        Vérifie si la ligne indique le début d'une nouvelle section principale du CV.
        """
        main_sections = ['expérience', 'formation', 'compétences', 'education',
                         'langues', 'références', 'contact']
        return any(section in line.lower() for section in main_sections)

    def _clean_interest(self, text: str) -> str:
        """
        Nettoie et formate un centre d'intérêt.
        """
        # Enlever les puces et caractères spéciaux au début
        text = text.strip('•-*►→⚫⚪●○♦♢■□▪▫\t ')
        # Capitaliser la première lettre
        text = text.strip()
        return text.capitalize() if text else ''

    def get_main_interests(self, text: str) -> List[str]:
        """
        Retourne une liste simple des principaux centres d'intérêt.
        """
        analyzed = self.analyze(text)
        main_interests = []
        for category_interests in analyzed.values():
            main_interests.extend(category_interests)
        return main_interests