from datetime import datetime
from dateutil.parser import parse
from typing import Optional, Tuple, List, Dict  # Ajout de Dict
import re

class DateExtractor:
    def __init__(self):
        # Patterns pour les dates européennes et américaines
        self.date_patterns = {
            'fr': {
                'range': r'(\d{2}/\d{2}/\d{4})\s*[-–]\s*(\d{2}/\d{2}/\d{4})',
                'single': r'\b(\d{2}/\d{2}/\d{4})\b',
                'month_year': r'(janvier|février|mars|...)\s+(\d{4})'
            },
            'en': {
                'range': r'(\d{2}-\d{2}-\d{4})\s*[-–]\s*(\d{2}-\d{2}-\d{4})',
                'single': r'\b(\d{2}-\d{2}-\d{4})\b',
                'month_year': r'(january|february|march|...)\s+(\d{4})'
            }
        }

    def extract_dates(self, text: str, lang: str = 'fr') -> List[Dict]:
        dates = []
        pattern = self.date_patterns[lang]

        # Cherche les périodes (plages de dates)
        for match in re.finditer(pattern['range'], text):
            start_date = self._parse_date(match.group(1))
            end_date = self._parse_date(match.group(2))
            if start_date and end_date:
                dates.append({
                    'start': start_date,
                    'end': end_date,
                    'type': 'range'
                })
        return dates

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        try:
            if date_str.lower() in ['présent', 'actuel', 'present', 'current']:
                return datetime.now()
            return parse(date_str, fuzzy=True)
        except:
            return None