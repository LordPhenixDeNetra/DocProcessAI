from typing import List, Dict
import re

class DataValidator:
    def validate_cv(self, cv_data: Dict) -> List[str]:
        errors = []

        # Vérification des sections obligatoires
        required_sections = ['contact', 'formation', 'experience']
        for section in required_sections:
            if section not in cv_data:
                errors.append(f"Section {section} manquante")

        # Validation des contacts
        if 'contact' in cv_data:
            contact_errors = self._validate_contact(cv_data['contact'])
            errors.extend(contact_errors)

        # Validation des dates
        if 'experience' in cv_data:
            date_errors = self._validate_dates(cv_data['experience'])
            errors.extend(date_errors)

        return errors





# class DataValidator:
#     def __init__(self):
#         self.email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
#         self.phone_patterns = {
#             'fr': r'^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$',
#             'en': r'^\+?1?\s*\(?(\d{3})\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
#         }
#
#     def validate_cv_data(self, data: Dict) -> Dict[str, List[str]]:
#         validation_results = {
#             'errors': [],
#             'warnings': []
#         }
#
#         # Validation des informations de contact
#         if 'contact' in data:
#             contact_errors = self._validate_contact_info(data['contact'])
#             validation_results['errors'].extend(contact_errors)
#
#         # Validation de l'éducation
#         if 'education' in data:
#             education_issues = self._validate_education(data['education'])
#             validation_results['errors'].extend(education_issues['errors'])
#             validation_results['warnings'].extend(education_issues['warnings'])
#
#         # Validation de l'expérience
#         if 'experience' in data:
#             experience_issues = self._validate_experience(data['experience'])
#             validation_results['errors'].extend(experience_issues['errors'])
#             validation_results['warnings'].extend(experience_issues['warnings'])
#
#         return validation_results
#
#     def _validate_contact_info(self, contact_data: Dict) -> List[str]:
#         errors = []
#
#         # Validation email
#         if 'email' in contact_data:
#             if not re.match(self.email_pattern, contact_data['email']):
#                 errors.append("Format d'email invalide")
#
#         # Validation téléphone
#         if 'phone' in contact_data:
#             valid_phone = False
#             for pattern in self.phone_patterns.values():
#                 if re.match(pattern, contact_data['phone']):
#                     valid_phone = True
#                     break
#             if not valid_phone:
#                 errors.append("Format de téléphone invalide")
#
#         return errors