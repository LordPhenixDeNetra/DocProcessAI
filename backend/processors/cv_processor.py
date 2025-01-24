# import re
# from typing import Any, Dict, List
# from models.cv_models import CVData
# from extractors.base_extractor import BaseExtractor
# from extractors.pdf_extractor import PDFExtractor
# from extractors.image_extractor import ImageExtractor
# from extractors.doc_extractor import DocExtractor
# from analyzers.contact_analyzer import ContactAnalyzer
# from analyzers.education_analyzer import EducationAnalyzer
# from analyzers.experience_analyzer import ExperienceAnalyzer
# from analyzers.skills_analyzer import SkillsAnalyzer
# from analyzers.interest_analyzer import InterestAnalyzer
#
# class CVProcessor:
#     def __init__(self):
#         # Initialisation des extracteurs
#         self.extractors: Dict[str, BaseExtractor] = {
#             'pdf': PDFExtractor(),
#             'image': ImageExtractor(),
#             'doc': DocExtractor()
#         }
#
#         # Initialisation des analyseurs
#         self.analyzers = {
#             'contact': ContactAnalyzer(),
#             'education': EducationAnalyzer(),
#             'experience': ExperienceAnalyzer(),
#             'skills': SkillsAnalyzer(),
#             'interests': InterestAnalyzer()
#         }
#
#     async def process_cv(self, file_content: bytes, filename: str) -> Dict[str, Any]:
#         """
#         Traite un CV et retourne les données structurées
#         """
#         try:
#             # Déterminer le type de fichier
#             file_type = self._get_file_type(filename)
#
#             # Extraire le texte
#             extractor = self.extractors.get(file_type)
#             if not extractor:
#                 raise ValueError(f"Format de fichier non supporté: {file_type}")
#
#             text = await extractor.extract(file_content)
#
#             # Analyser chaque section
#             contact_data = self.analyzers['contact'].analyze(text)
#             education_data = self.analyzers['education'].analyze(text)
#             experience_data = self.analyzers['experience'].analyze(text)
#             skills_data = self.analyzers['skills'].analyze(text)
#             interests_data = self.analyzers['interests'].analyze(text)
#
#             # Construire la réponse
#             cv_data = {
#                 'informations_personnelles': contact_data,
#                 'formations': education_data,
#                 'experiences': experience_data,
#                 'competences': skills_data,
#                 'centres_interet': interests_data,
#                 'metadata': {
#                     'filename': filename,
#                     'file_type': file_type,
#                     'text_length': len(text)
#                 }
#             }
#
#             # Calculer un score de confiance global
#             cv_data['score_confiance'] = self._calculate_confidence(cv_data)
#
#             return cv_data
#
#         except Exception as e:
#             raise ValueError(f"Erreur lors du traitement du CV: {str(e)}")
#
#     def _get_file_type(self, filename: str) -> str:
#         """
#         Détermine le type de fichier à partir de son extension
#         """
#         ext = filename.lower().split('.')[-1]
#         if ext in ['pdf']:
#             return 'pdf'
#         elif ext in ['jpg', 'jpeg', 'png']:
#             return 'image'
#         elif ext in ['doc', 'docx']:
#             return 'doc'
#         raise ValueError(f"Extension non supportée: {ext}")
#
#     def _calculate_confidence(self, cv_data: Dict[str, Any]) -> float:
#         """
#         Calcule un score de confiance global pour l'analyse du CV
#         """
#         scores = []
#
#         # Vérifier les informations personnelles
#         if cv_data['informations_personnelles']:
#             required_fields = ['nom', 'email', 'telephone']
#             score = sum(1 for field in required_fields
#                         if field in cv_data['informations_personnelles']) / len(required_fields)
#             scores.append(score)
#
#         # Vérifier les formations
#         if cv_data['formations']:
#             scores.append(1.0)
#
#         # Vérifier les expériences
#         if cv_data['experiences']:
#             scores.append(1.0)
#
#         # Vérifier les compétences
#         if cv_data['competences'].get('techniques'):
#             scores.append(1.0)
#
#         # Calculer la moyenne
#         return round((sum(scores) / len(scores)) * 100, 2) if scores else 0.0
#
#     def get_missing_information(self, cv_data: Dict[str, Any]) -> List[str]:
#         """
#         Identifie les informations manquantes dans le CV
#         """
#         missing = []
#
#         # Vérifier les sections obligatoires
#         if not cv_data['informations_personnelles'].get('email'):
#             missing.append("Email manquant")
#         if not cv_data['informations_personnelles'].get('telephone'):
#             missing.append("Numéro de téléphone manquant")
#
#         # Vérifier les sections principales
#         if not cv_data['formations']:
#             missing.append("Section formation manquante")
#         if not cv_data['experiences']:
#             missing.append("Section expérience manquante")
#         if not cv_data['competences'].get('techniques'):
#             missing.append("Compétences techniques manquantes")
#
#         return missing


# from typing import Dict, Any, List, Optional
# import re
# from extractors.pdf_extractor import PDFExtractor
# from extractors.image_extractor import ImageExtractor
# from extractors.doc_extractor import DocExtractor
# from extractors.section_extractor import SectionExtractor
# from preprocessing.document_processor import DocumentProcessor
#
# class CVProcessor:
#     def __init__(self):
#         self.pdf_extractor = PDFExtractor()
#         self.image_extractor = ImageExtractor()
#         self.doc_extractor = DocExtractor()
#         self.section_extractor = SectionExtractor()
#         self.document_processor = DocumentProcessor()
#
#         self.supported_formats = {
#             'pdf': ['application/pdf'],
#             'image': ['image/jpeg', 'image/png', 'image/jpg'],
#             'word': ['application/msword',
#                      'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
#         }
#
#     def _get_file_type(self, filename: str) -> str:
#         ext = filename.lower().split('.')[-1]
#         if ext == 'pdf':
#             return 'pdf'
#         elif ext in ['jpg', 'jpeg', 'png']:
#             return 'image'
#         elif ext in ['doc', 'docx']:
#             return 'word'
#         raise ValueError(f"Format de fichier non supporté: {ext}")
#
#     async def process_cv(self, content: bytes, filename: str) -> Dict[str, Any]:
#         try:
#             # Identifier le type de fichier et prétraiter
#             file_type = self._get_file_type(filename)
#             processed_content = self.document_processor.preprocess(content, file_type)
#
#             # Extraire le texte selon le type de fichier
#             if file_type == 'pdf':
#                 text = self.pdf_extractor.extract(processed_content)
#             elif file_type == 'image':
#                 text = self.image_extractor.extract(processed_content)
#             elif file_type == 'word':
#                 text = self.doc_extractor.extract(processed_content)
#
#             # Extraire les sections
#             sections = self.section_extractor.extract(text)
#
#             # Structurer les résultats
#             result = {
#                 'informations_personnelles': self._extract_personal_info(text),
#                 'formations': self._extract_education(sections.get('formation', '')),
#                 'experiences': self._extract_experience(sections.get('experience', '')),
#                 'competences': self._extract_skills(sections.get('competences', '')),
#                 'langues': self._extract_languages(sections.get('langues', '')),
#                 'centres_interet': self._extract_interests(sections.get('interets', '')),
#                 'metadata': {
#                     'filename': filename,
#                     'file_type': file_type,
#                     'text_length': len(text)
#                 }
#             }
#
#             # Calculer le score de confiance
#             result['score_confiance'] = self._calculate_confidence(result)
#
#             return result
#
#         except Exception as e:
#             raise Exception(f"Erreur lors du traitement du CV: {str(e)}")
#
#     def _extract_personal_info(self, text: str) -> Dict:
#         info = {}
#         patterns = {
#             'email': r'[\w\.-]+@[\w\.-]+\.\w+',
#             'telephone': r'(?:(?:\+|00)221|0)\s*[76][0-9](?:[\s.-]*\d{2}){3}',
#             'nom': r'(?i)(?:nom\s*:|nom\s+et\s+prénom\s*:?|je\s+m\'appelle\s+)([A-Z\s]+)',
#             'adresse': r'(?i)(?:adresse\s*:|demeurant\s+à\s+|domicilié\s+à\s+)([\w\s,]+)'
#         }
#
#         for key, pattern in patterns.items():
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             if matches:
#                 info[key] = matches[0].strip()
#
#         return info
#
#     def _extract_education(self, text: str) -> List:
#         formations = []
#         formation_pattern = (
#                 r'(?P<diplome>master|licence|baccalauréat|bac|dut|bts|ingénieur)' +
#                 r'[^\n]*?' +
#                 r'(?P<etablissement>université|école|lycée|institut)[^\n]*?' +
#                 r'(?P<date>\d{4}(?:\s*[-–]\s*(?:\d{4}|présent|actuel))?)'
#         )
#
#         matches = re.finditer(formation_pattern, text, re.IGNORECASE)
#         for match in matches:
#             dates = match.group('date').split('-')
#             formations.append({
#                 'diplome': match.group('diplome').strip().capitalize(),
#                 'etablissement': match.group('etablissement').strip(),
#                 'debut': dates[0].strip(),
#                 'fin': dates[1].strip() if len(dates) > 1 else None,
#                 'lieu': None,
#                 'description': None
#             })
#
#         return formations
#
#     def _extract_experience(self, text: str) -> List:
#         experiences = []
#         experience_pattern = (
#                 r'(?P<poste>[^-\n]*)' +
#                 r'(?P<dates>\d{4}\s*[-–]\s*(?:\d{4}|présent|actuel))' +
#                 r'(?:[^\n]*?)' +
#                 r'(?:chez|à|au)?\s*(?P<entreprise>[A-Z][^,\n]*)'
#         )
#
#         matches = re.finditer(experience_pattern, text, re.IGNORECASE)
#         for match in matches:
#             dates = match.group('dates').split('-')
#             experiences.append({
#                 'poste': match.group('poste').strip(),
#                 'entreprise': match.group('entreprise').strip(),
#                 'debut': dates[0].strip(),
#                 'fin': dates[1].strip() if len(dates) > 1 else 'présent',
#                 'description': self._extract_description(text, match.end())
#             })
#
#         return experiences
#
#     def _extract_skills(self, text: str) -> Dict:
#         skills = {
#             'techniques': [],
#             'categories': {
#                 'programmation': [],
#                 'frameworks': [],
#                 'outils': [],
#                 'bases_de_donnees': []
#             }
#         }
#
#         skill_patterns = {
#             'programmation': r'(?:python|java|javascript|c\+\+|php|html|css)',
#             'frameworks': r'(?:react|angular|vue|django|flask|spring|laravel)',
#             'outils': r'(?:git|docker|kubernetes|jenkins|aws|azure)',
#             'bases_de_donnees': r'(?:sql|mysql|postgresql|mongodb|oracle)'
#         }
#
#         for category, pattern in skill_patterns.items():
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             if matches:
#                 skills['categories'][category] = list(set(matches))
#                 skills['techniques'].extend(matches)
#
#         return skills
#
#     def _extract_languages(self, text: str) -> List:
#         languages = []
#         language_pattern = (
#                 r'(?P<langue>français|anglais|espagnol|arabe|allemand)' +
#                 r'\s*:?\s*' +
#                 r'(?P<niveau>courant|intermédiaire|débutant|bilingue|natif)'
#         )
#
#         matches = re.finditer(language_pattern, text, re.IGNORECASE)
#         for match in matches:
#             languages.append({
#                 'nom': match.group('langue').lower(),
#                 'niveau': match.group('niveau').lower()
#             })
#
#         return languages
#
#     def _extract_interests(self, text: str) -> Dict:
#         interests = {
#             'sports': [],
#             'culture': [],
#             'autres': []
#         }
#
#         interest_patterns = {
#             'sports': r'(?:football|basketball|tennis|natation|sport)',
#             'culture': r'(?:lecture|cinéma|musique|théâtre|art|voyage)'
#         }
#
#         for category, pattern in interest_patterns.items():
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             if matches:
#                 interests[category] = list(set(matches))
#
#         return interests
#
#     def _extract_description(self, text: str, start_pos: int, max_length: int = 200) -> Optional[str]:
#         description = text[start_pos:start_pos + max_length]
#         lines = [line.strip() for line in description.split('\n')]
#         clean_lines = [line for line in lines if line and not re.match(r'\d{4}|stage|expérience', line, re.IGNORECASE)]
#         return ' '.join(clean_lines) if clean_lines else None
#
#     def _calculate_confidence(self, result: Dict) -> float:
#         total_sections = 6
#         found_sections = 0
#
#         if result['informations_personnelles']:
#             found_sections += 1
#         if result['formations']:
#             found_sections += 1
#         if result['experiences']:
#             found_sections += 1
#         if result['competences']['techniques']:
#             found_sections += 1
#         if result['langues']:
#             found_sections += 1
#         if any(result['centres_interet'].values()):
#             found_sections += 1
#
#         return round((found_sections / total_sections) * 100, 2)
#
#     def get_missing_information(self, result: Dict) -> List[str]:
#         missing = []
#
#         if not result['informations_personnelles'].get('email'):
#             missing.append("Email manquant")
#         if not result['informations_personnelles'].get('telephone'):
#             missing.append("Numéro de téléphone manquant")
#         if not result['formations']:
#             missing.append("Section formation manquante")
#         if not result['experiences']:
#             missing.append("Section expérience manquante")
#         if not result['competences']['techniques']:
#             missing.append("Compétences techniques manquantes")
#
#         return missing


from typing import Dict, Any, List, Optional
import re
import logging
from extractors.pdf_extractor import PDFExtractor
from extractors.image_extractor import ImageExtractor
from extractors.doc_extractor import DocExtractor
from extractors.section_extractor import SectionExtractor
from preprocessing.document_processor import DocumentProcessor
import utils
import json

# Configurer le logging pour surveiller le traitement
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class CVProcessor:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.image_extractor = ImageExtractor()
        self.doc_extractor = DocExtractor()
        self.section_extractor = SectionExtractor()
        self.document_processor = DocumentProcessor()

        self.supported_formats = {
            'pdf': ['application/pdf'],
            'image': ['image/jpeg', 'image/png', 'image/jpg'],
            'word': ['application/msword',
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        }

    def _get_file_type(self, filename: str) -> str:
        ext = filename.lower().split('.')[-1]
        if ext == 'pdf':
            return 'pdf'
        elif ext in ['jpg', 'jpeg', 'png']:
            return 'image'
        elif ext in ['doc', 'docx']:
            return 'word'
        raise ValueError(f"Format de fichier non supporté: {ext}")

    async def process_cv(self, content: bytes, filename: str) -> Dict[str, Any]:
        try:
            logging.info(f"Traitement du fichier: {filename}")
            # Identifier le type de fichier et prétraiter
            file_type = self._get_file_type(filename)
            processed_content = self.document_processor.preprocess(content, file_type)

            # Extraire le texte selon le type de fichier
            if file_type == 'pdf':
                text = self.pdf_extractor.extract(processed_content)
            elif file_type == 'image':
                text = self.image_extractor.extract(processed_content)
            elif file_type == 'word':
                text = self.doc_extractor.extract(processed_content)

            if not text:
                raise ValueError("Impossible d'extraire du texte du fichier")

            logging.info(f"Extraction de texte réussie, longueur: {len(text)} caractères")

            # Extraire les sections
            sections = self.section_extractor.extract(text)

            # Structurer les résultats
            result = {
                'informations_personnelles': self._extract_personal_info(text),
                'formations': self._extract_education(sections.get('formation', '')),
                'experiences': self._extract_experience(sections.get('experience', '')),
                'competences': self._extract_skills(sections.get('competences', '')),
                'langues': self._extract_languages(sections.get('langues', '')),
                'centres_interet': self._extract_interests(sections.get('interets', '')),
                'metadata': {
                    'filename': filename,
                    'file_type': file_type,
                    'text_length': len(text)
                }
            }

            # Calculer le score de confiance
            result['score_confiance'] = self._calculate_confidence(result)

            missing_info = self.get_missing_information(result)
            if missing_info:
                logging.warning(f"Informations manquantes: {missing_info}")

            return result

        except Exception as e:
            logging.error(f"Erreur lors du traitement du CV: {e}")
            raise Exception(f"Erreur lors du traitement du CV: {str(e)}")

    def _extract_personal_info(self, text: str) -> Dict:
        info = {}
        patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            # 'telephone': r'(?:(?:\+|00)221|0)\s*[76][0-9](?:[\s.-]*\d{2}){3}',
            'telephone': r'\+?\d{1,4}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}',
            'nom': r'(?i)(?:nom\s*:|nom\s+et\s+prénom\s*:?|je\s+m\'appelle\s+)([A-Z\s]+)',
            'adresse': r'(?i)(?:adresse\s*:|demeurant\s+à\s+|domicilié\s+à\s+)([\w\s,]+)'
        }

        for key, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                info[key] = matches[0].strip()

        return info

    def _extract_education(self, text: str) -> List:
        formations = []
        formation_pattern = (
            r'(?P<diplome>master|licence|baccalauréat|bac|dut|bts|ingénieur)'
            r'[^\n]*?'
            r'(?P<etablissement>université|école|lycée|institut)[^\n]*?'
            r'(?P<date>\d{4}(?:\s*[-–]\s*(?:\d{4}|présent|actuel))?)'
        )

        matches = re.finditer(formation_pattern, text, re.IGNORECASE)
        for match in matches:
            if match:  # Vérifiez si une correspondance est trouvée
                dates = match.group('date').split('-') if match.group('date') else []
                formations.append({
                    'diplome': match.group('diplome').strip().capitalize(),
                    'etablissement': match.group('etablissement').strip(),
                    'debut': dates[0].strip() if dates else None,
                    'fin': dates[1].strip() if len(dates) > 1 else None,
                    'lieu': None,
                    'description': None
                })

        return formations

    #
    # def _extract_experience(self, text: str) -> List:
    #     experiences = []
    #     experience_pattern = (
    #         r'(?P<poste>[^-\n]*)'
    #         r'(?P<dates>\d{4}\s*[-–]\s*(?:\d{4}|présent|actuel))'
    #         r'(?:[^\n]*?)'
    #         r'(?:chez|à|au)?\s*(?P<entreprise>[A-Z][^,\n]*)'
    #     )
    #
    #     matches = re.finditer(experience_pattern, text, re.IGNORECASE)
    #     for match in matches:
    #         if match:  # Vérifiez si une correspondance est trouvée
    #             dates = match.group('dates').split('-') if match.group('dates') else []
    #             experiences.append({
    #                 'poste': match.group('poste').strip() if match.group('poste') else None,
    #                 'entreprise': match.group('entreprise').strip() if match.group('entreprise') else None,
    #                 'debut': dates[0].strip() if dates else None,
    #                 'fin': dates[1].strip() if len(dates) > 1 else 'présent',
    #                 'description': self._extract_description(text, match.end())
    #             })
    #
    #     return experiences
    #

    def _extract_experience(self, text: str) -> List[Dict[str, Optional[str]]]:
        """
        Extrait les expériences professionnelles à partir d'un texte.
        """
        experiences = []

        # Pattern amélioré
        experience_pattern = (
            r"(?P<poste>[^\n,]+)"                # Poste
            r"(?:,\s*|\s+chez\s+|\s+à\s+)"       # Séparateur
            r"(?P<entreprise>[^\n,]+)"           # Entreprise
            r"(?:,\s*|\s*\|\s*|\s+)"             # Séparateur
            r"(?P<dates>\d{4}\s*[-–]\s*(?:\d{4}|présent|actuel))"  # Dates
        )

        # Trouver les correspondances
        matches = re.finditer(experience_pattern, text, re.IGNORECASE)

        for match in matches:
            dates = match.group("dates").split("-")
            debut = dates[0].strip() if dates else None
            fin = dates[1].strip() if len(dates) > 1 else "présent"

            experiences.append({
                "poste": match.group("poste").strip(),
                "entreprise": match.group("entreprise").strip(),
                "debut": debut,
                "fin": fin,
                "description": self._extract_description(text, match.end())
            })

        return experiences

    def _extract_description(self, text: str, start_pos: int, max_length: int = 300) -> Optional[str]:
        """
        Extrait une description associée à un poste à partir d'une position donnée dans le texte.
        """
        description = text[start_pos:start_pos + max_length]
        lines = [line.strip() for line in description.split("\n")]
        clean_lines = [
            line for line in lines
            if line and not re.match(r"^\s*-\s*$|^\d{4}", line, re.IGNORECASE)
        ]
        return " ".join(clean_lines).strip() if clean_lines else None


    def _extract_skills(self, text: str) -> Dict:
        skills = {
            'techniques': [],
            'categories': {
                'programmation': [],
                'frameworks': [],
                'outils': [],
                'bases_de_donnees': []
            }
        }

        skill_patterns = {
            'programmation': r'(?:python|java|javascript|c\+\+|php|html|css)',
            'frameworks': r'(?:react|angular|vue|django|flask|spring|laravel)',
            'outils': r'(?:git|docker|kubernetes|jenkins|aws|azure)',
            'bases_de_donnees': r'(?:sql|mysql|postgresql|mongodb|oracle)'
        }

        for category, pattern in skill_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                skills['categories'][category] = list(set(matches))
                skills['techniques'].extend(matches)

        return skills

    def _load_languages(self) -> List[str]:
        """
        Charge la liste des langues à partir d'un fichier JSON ou autre source.
        """
        with open("utils/languages.json", "r") as file:
            data = json.load(file)
        return data["languages"]

    def _load_info_to_extract(self, key) -> List[str]:
        """
        Charge la liste des donnees à partir du fichier JSON ou autre source.
        """
        with open("utils/data_to_extract.json", "r") as file:
            data = json.load(file)
        return data[key]

    # def _extract_languages(self, text: str) -> List:
    #     languages = []
    #     language_pattern = (
    #             r'(?P<langue>français|anglais|espagnol|arabe|allemand)' +
    #             r'\s*:?\s*' +
    #             r'(?P<niveau>courant|intermédiaire|débutant|bilingue|natif)'
    #     )
    #
    #     matches = re.finditer(language_pattern, text, re.IGNORECASE)
    #     for match in matches:
    #         languages.append({
    #             'nom': match.group('langue').lower(),
    #             'niveau': match.group('niveau').lower()
    #         })
    #
    #     return languages

    def _extract_languages(self, text: str) -> List[Dict[str, str]]:
        """
        Extrait les langues et leurs niveaux à partir d'un texte donné.
        """
        languages = []

        # Charger les langues dynamiquement
        # language_list = self._load_languages()
        language_list = self._load_info_to_extract('languages')

        # Construire dynamiquement le pattern regex
        language_pattern = (
            rf"(?P<langue>{'|'.join(map(re.escape, language_list))})"  # Échapper les langues pour éviter les conflits regex
            r"\s*:?\s*"
            r"(?P<niveau>courant|intermédiaire|débutant|bilingue|natif)"
        )

        # Trouver toutes les correspondances
        matches = re.finditer(language_pattern, text, re.IGNORECASE)
        for match in matches:
            languages.append({
                "nom": match.group("langue").lower(),
                "niveau": match.group("niveau").lower()
            })

        return languages


    def _extract_interests(self, text: str) -> Dict:

        """
        Extrait les langues et leurs niveaux à partir d'un texte donné.
        """
        # sports = []

        # Charger les langues dynamiquement
        sport_list = self._load_info_to_extract("sports")

        interests = {
            'sports': [],
            'culture': [],
            'autres': []
        }

        interest_patterns = {
            # 'sports': r'(?:football|basketball|tennis|natation|sport)',
            'sports': rf"(?P<langue>{'|'.join(map(re.escape, sport_list))})",  # Échapper les langues pour éviter les conflits regex
            'culture': r'(?:lecture|cinéma|musique|théâtre|art|voyage)'
        }

        for category, pattern in interest_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                interests[category] = list(set(matches))

        return interests

    #
    # def _extract_description(self, text: str, start_pos: int, max_length: int = 200) -> Optional[str]:
    #     description = text[start_pos:start_pos + max_length]
    #     lines = [line.strip() for line in description.split('\n')]
    #     clean_lines = [line for line in lines if line and not re.match(r'\d{4}|stage|expérience', line, re.IGNORECASE)]
    #     return ' '.join(clean_lines) if clean_lines else None
    #

    def _calculate_confidence(self, result: Dict) -> float:
        total_sections = 6
        found_sections = 0

        if result['informations_personnelles']:
            found_sections += 1
        if result['formations']:
            found_sections += 1
        if result['experiences']:
            found_sections += 1
        if result['competences']['techniques']:
            found_sections += 1
        if result['langues']:
            found_sections += 1
        if any(result['centres_interet'].values()):
            found_sections += 1

        return round((found_sections / total_sections) * 100, 2)


    def get_missing_information(self, result: Dict) -> List[str]:
        missing = []

        if not result['informations_personnelles'].get('email'):
            missing.append("Email manquant")
        if not result['informations_personnelles'].get('telephone'):
            missing.append("Numéro de téléphone manquant")
        if not result['formations']:
            missing.append("Section formation manquante")
        if not result['experiences']:
            missing.append("Section expérience manquante")
        if not result['competences']['techniques']:
            missing.append("Compétences techniques manquantes")

        return missing
