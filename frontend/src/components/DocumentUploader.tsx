import React, { useState } from 'react';
import { Upload, AlertCircle } from 'lucide-react';
import {ProcessingResult} from "@/types";

interface DocumentUploaderProps {
    onDocumentProcessed: (results: ProcessingResult) => void;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({
                                                                      onDocumentProcessed
                                                                  }) => {
    const [dragging, setDragging] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setDragging(true);
    };

    const handleDragLeave = () => {
        setDragging(false);
    };

    const processFile = async (file: File) => {
        setProcessing(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/documents/analyze', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-API-Key': 'votre-clé-api-secrète',
                },
            });

            if (!response.ok) {
                throw new Error('Erreur lors du traitement du document');
            }

            const results = await response.json();
            onDocumentProcessed(results);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Une erreur est survenue');
        } finally {
            setProcessing(false);
            setDragging(false);
        }
    };

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        setDragging(false);

        const file = e.dataTransfer.files[0];
        if (file) {
            await processFile(file);
        }
    };

    const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            await processFile(file);
        }
    };

    return (
        <div className="space-y-4">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`
          border-2 border-dashed rounded-lg p-8 text-center
          transition-colors duration-200
          ${dragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${processing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
            >
                <div className="flex flex-col items-center">
                    {processing ? (
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
                    ) : (
                        <Upload className="h-12 w-12 text-gray-400" />
                    )}

                    <p className="mt-4 text-sm text-gray-600">
                        {processing
                            ? 'Traitement en cours...'
                            : 'Glissez un document ou cliquez pour sélectionner'}
                    </p>

                    {!processing && (
                        <label className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md
                            cursor-pointer hover:bg-blue-600 transition-colors">
                            Sélectionner un fichier
                            <input
                                type="file"
                                className="hidden"
                                onChange={handleFileInput}
                                accept=".pdf,.jpg,.jpeg,.png"
                                disabled={processing}
                            />
                        </label>
                    )}
                </div>
            </div>

            {error && (
                <div className="flex items-center gap-2 text-red-500 bg-red-50 p-4 rounded">
                    <AlertCircle className="h-5 w-5" />
                    <p>{error}</p>
                </div>
            )}
        </div>
    );
};