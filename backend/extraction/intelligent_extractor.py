# extraction/intelligent_extractor.py
import re
from dataclasses import dataclass
from typing import Dict

@dataclass
class ExtractedData:
    document_type: str
    fields: Dict[str, str]
    confidence: float

class IntelligentExtractor:
    def __init__(self):
        self.rules = self._load_extraction_rules()

    def _load_extraction_rules(self) -> Dict:
        return {
            'invoice': {
                'invoice_number': r'(?i)facture\s*(?:n[o°]?)?\s*[:# ]*([A-Z0-9-]+)',
                'date': r'(?i)date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
                'amount': r'(?i)total\s*(?:ttc|ht)?\s*:?\s*(\d+[.,]\d{2})',
                'vat': r'(?i)tva\s*:?\s*(\d+[.,]\d{2})'
            },
            'form': {
                'name': r'(?i)nom\s*:?\s*([A-Za-z\s]+)',
                'email': r'[\w\.-]+@[\w\.-]+\.\w+',
                'phone': r'(?:\+\d{2,3}|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
            }
        }

    def extract(self, text: str) -> ExtractedData:
        # Détection du type de document
        doc_type = self._detect_document_type(text)

        # Extraction basée sur les règles
        extracted_fields = {}
        rules = self.rules.get(doc_type, {})
        for field_name, pattern in rules.items():
            match = re.search(pattern, text)
            if match:
                extracted_fields[field_name] = match.group(1)

        # Calcul du score de confiance
        confidence = self._calculate_confidence(extracted_fields, rules)

        return ExtractedData(
            document_type=doc_type,
            fields=extracted_fields,
            confidence=confidence
        )

    def _detect_document_type(self, text: str) -> str:
        keywords = {
            'invoice': ['facture', 'tva', 'total ttc', 'règlement'],
            'form': ['formulaire', 'inscription', 'coordonnées']
        }

        scores = {doc_type: 0 for doc_type in keywords}
        for doc_type, kw_list in keywords.items():
            for kw in kw_list:
                if re.search(f'(?i){kw}', text):
                    scores[doc_type] += 1

        return max(scores.items(), key=lambda x: x[1])[0]

    def _calculate_confidence(self,
                              extracted_fields: Dict,
                              rules: Dict) -> float:
        if not rules:
            return 0.0

        fields_found = len(extracted_fields)
        total_fields = len(rules)

        return round(fields_found / total_fields * 100, 2)






# import re
# from dataclasses import dataclass
# from typing import Dict, List, Optional
# from transformers import pipeline
#
# @dataclass
# class ExtractedData:
#     document_type: str
#     fields: Dict[str, str]
#     confidence: float
#
# class IntelligentExtractor:
#     def __init__(self):
#         self.ner_pipeline = pipeline("token-classification",
#                                      model="jean-baptiste/camembert-ner")
#         self.rules = self._load_extraction_rules()
#
#     def _load_extraction_rules(self) -> Dict:
#         return {
#             'invoice': {
#                 'invoice_number': r'(?i)facture\s*(?:n[o°]?)?\s*[:# ]*([A-Z0-9-]+)',
#                 'date': r'(?i)date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
#                 'amount': r'(?i)total\s*(?:ttc|ht)?\s*:?\s*(\d+[.,]\d{2})',
#                 'vat': r'(?i)tva\s*:?\s*(\d+[.,]\d{2})'
#             },
#             'form': {
#                 'name': r'(?i)nom\s*:?\s*([A-Za-z\s]+)',
#                 'email': r'[\w\.-]+@[\w\.-]+\.\w+',
#                 'phone': r'(?:\+\d{2,3}|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
#             }
#         }
#
#     def extract(self, text: str) -> ExtractedData:
#         # Détection du type de document
#         doc_type = self._detect_document_type(text)
#
#         # Extraction basée sur les règles
#         extracted_fields = {}
#         rules = self.rules.get(doc_type, {})
#         for field_name, pattern in rules.items():
#             match = re.search(pattern, text)
#             if match:
#                 extracted_fields[field_name] = match.group(1)
#
#         # Extraction basée sur NER pour les champs manquants
#         ner_results = self.ner_pipeline(text)
#         for result in ner_results:
#             if result['entity'] in ['PER', 'ORG', 'LOC']:
#                 field_name = f"ner_{result['entity'].lower()}"
#                 if field_name not in extracted_fields:
#                     extracted_fields[field_name] = result['word']
#
#         # Calcul du score de confiance
#         confidence = self._calculate_confidence(extracted_fields, rules)
#
#         return ExtractedData(
#             document_type=doc_type,
#             fields=extracted_fields,
#             confidence=confidence
#         )
#
#     def _detect_document_type(self, text: str) -> str:
#         keywords = {
#             'invoice': ['facture', 'tva', 'total ttc', 'règlement'],
#             'form': ['formulaire', 'inscription', 'coordonnées']
#         }
#
#         scores = {doc_type: 0 for doc_type in keywords}
#         for doc_type, kw_list in keywords.items():
#             for kw in kw_list:
#                 if re.search(f'(?i){kw}', text):
#                     scores[doc_type] += 1
#
#         return max(scores.items(), key=lambda x: x[1])[0]
#
#     def _calculate_confidence(self,
#                               extracted_fields: Dict,
#                               rules: Dict) -> float:
#         if not rules:
#             return 0.0
#
#         fields_found = len(extracted_fields)
#         total_fields = len(rules)
#
#         return round(fields_found / total_fields * 100, 2)