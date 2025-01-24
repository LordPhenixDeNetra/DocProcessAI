import redis
from minio import Minio
from typing import Optional
import json
import hashlib

class StorageManager:
    def __init__(self):
        # Redis pour le cache
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )

        # MinIO pour le stockage des documents
        self.minio_client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )

        self.bucket_name = "documents"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)

    def _generate_cache_key(self, file_content: bytes) -> str:
        # Création d'une clé unique basée sur le contenu
        return hashlib.sha256(file_content).hexdigest()

    def store_document(self, content: bytes, metadata: dict) -> str:
        # Générer un identifiant unique
        doc_id = self._generate_cache_key(content)

        # Stocker dans MinIO
        self.minio_client.put_object(
            self.bucket_name,
            f"{doc_id}/original",
            content,
            length=len(content)
        )

        # Mettre en cache les métadonnées
        self.redis_client.setex(
            f"doc:{doc_id}:metadata",
            3600,  # expire après 1 heure
            json.dumps(metadata)
        )

        return doc_id

    def get_document(self, doc_id: str) -> Optional[dict]:
        # Vérifier le cache d'abord
        cached_metadata = self.redis_client.get(f"doc:{doc_id}:metadata")
        if cached_metadata:
            metadata = json.loads(cached_metadata)

            # Récupérer le document depuis MinIO
            try:
                data = self.minio_client.get_object(
                    self.bucket_name,
                    f"{doc_id}/original"
                ).read()

                return {
                    "content": data,
                    "metadata": metadata
                }
            except:
                return None

        return None

    def update_metadata(self, doc_id: str, metadata: dict):
        # Mettre à jour les métadonnées en cache
        self.redis_client.setex(
            f"doc:{doc_id}:metadata",
            3600,
            json.dumps(metadata)
        )