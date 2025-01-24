import re
from typing import Dict

class ContactAnalyzer:
    def __init__(self):
        self.patterns = {
            'email': r'[\w\.-]+@[\w\.-]+\.\w+',
            'telephone': r'(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}',
            'linkedin': r'linkedin.com/in/[\w-]+',
        }

    def analyze(self, text: str) -> Dict[str, str]:
        result = {}

        # Extraire email
        email_match = re.search(self.patterns['email'], text)
        if email_match:
            result['email'] = email_match.group(0)

        # Extraire téléphone
        tel_match = re.search(self.patterns['telephone'], text)
        if tel_match:
            result['telephone'] = tel_match.group(0)

        # Extraire LinkedIn
        linkedin_match = re.search(self.patterns['linkedin'], text)
        if linkedin_match:
            result['linkedin'] = linkedin_match.group(0)

        # TODO: Extraire nom et prénom (nécessite une analyse plus complexe)

        return result