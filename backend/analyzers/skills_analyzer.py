from typing import Dict, List, Optional
from models.cv_models import CompetenceTechnique, Langue

class SkillsAnalyzer:
    def __init__(self):
        self.skill_categories = {
            'programmation': ['python', 'java', 'javascript', 'c++', 'php'],
            'frameworks': ['django', 'flask', 'spring', 'react', 'angular'],
            'bases_de_donnees': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle'],
            'outils': ['git', 'docker', 'kubernetes', 'jenkins', 'jira'],
            'systemes': ['linux', 'windows', 'macos', 'unix'],
        }

        self.language_levels = {
            'débutant': ['débutant', 'basic', 'a1', 'a2'],
            'intermédiaire': ['intermédiaire', 'intermediate', 'b1', 'b2'],
            'avancé': ['avancé', 'advanced', 'courant', 'fluent', 'c1', 'c2'],
            'natif': ['natif', 'native', 'langue maternelle', 'mother tongue']
        }

    def analyze(self, text: str) -> Dict:
        sections = self._split_sections(text.lower())

        return {
            'techniques': self._analyze_technical_skills(sections.get('competences', '')),
            'langues': self._analyze_languages(sections.get('langues', '')),
            'certifications': self._analyze_certifications(sections.get('certifications', ''))
        }

    def _split_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        current_section = None
        current_content = []

        for line in text.split('\n'):
            if self._is_section_header(line):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = self._get_section_type(line)
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _is_section_header(self, line: str) -> bool:
        keywords = ['compétences', 'skills', 'langues', 'languages', 'certifications']
        return any(keyword in line.lower() for keyword in keywords)

    def _get_section_type(self, line: str) -> str:
        line = line.lower()
        if any(word in line for word in ['compétences', 'skills']):
            return 'competences'
        elif any(word in line for word in ['langues', 'languages']):
            return 'langues'
        elif 'certifications' in line:
            return 'certifications'
        return 'autre'

    def _analyze_technical_skills(self, text: str) -> List[CompetenceTechnique]:
        result = []
        for category, keywords in self.skill_categories.items():
            found_skills = []
            for skill in keywords:
                if skill in text:
                    found_skills.append(skill)
            if found_skills:
                result.append(CompetenceTechnique(
                    categorie=category,
                    competences=found_skills
                ))
        return result

    def _analyze_languages(self, text: str) -> List[Langue]:
        languages = []
        known_languages = ['français', 'anglais', 'espagnol', 'allemand', 'italien', 'chinois', 'arabe']

        for lang in known_languages:
            if lang in text:
                niveau = self._determine_language_level(text)
                languages.append(Langue(nom=lang, niveau=niveau))

        return languages

    def _determine_language_level(self, text: str) -> str:
        for level, keywords in self.language_levels.items():
            if any(keyword in text for keyword in keywords):
                return level
        return "non spécifié"

    def _analyze_certifications(self, text: str) -> List[str]:
        certifications = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                certifications.append(line)
        return certifications