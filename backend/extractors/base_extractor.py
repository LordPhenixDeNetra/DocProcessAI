from abc import ABC, abstractmethod
from typing import Any

class BaseExtractor(ABC):
    """Classe de base pour tous les extracteurs"""

    @abstractmethod
    def extract(self, content: bytes) -> Any:
        """Méthode abstraite que toutes les classes filles doivent implémenter"""
        pass

    def clean_text(self, text: str) -> str:
        """Méthode commune pour nettoyer le texte"""
        # Supprimer les espaces multiples
        text = ' '.join(text.split())
        # Supprimer les caractères spéciaux non désirés
        text = ''.join(char for char in text if char.isprintable())
        return text.strip()