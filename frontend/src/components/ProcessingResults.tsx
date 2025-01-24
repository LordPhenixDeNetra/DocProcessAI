import React from 'react';
import { FileText, AlertTriangle } from 'lucide-react';
import {ProcessingResult} from "@/types";

interface ProcessingResultsProps {
    results: ProcessingResult;
}

export const ProcessingResults: React.FC<ProcessingResultsProps> = ({ results }) => {
    return (
        <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Résultats de l'analyse
            </h2>

            <div className="mt-4 space-y-4">
                {/* Type de document */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded">
                    <span className="text-gray-600">Type de document</span>
                    <span className="font-medium">{results.document_type}</span>
                </div>

                {/* Score de confiance */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded">
                    <span className="text-gray-600">Score de confiance</span>
                    <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full">
                            <div
                                className="h-full bg-blue-500 rounded-full"
                                style={{ width: `${results.confidence * 100}%` }}
                            />
                        </div>
                        <span className="font-medium">
              {(results.confidence * 100).toFixed(1)}%
            </span>
                    </div>
                </div>

                {/* Champs extraits */}
                <div className="border rounded">
                    <div className="p-4 bg-gray-50 border-b">
                        <h3 className="font-medium">Champs extraits</h3>
                    </div>
                    <div className="p-4 space-y-2">
                        {Object.entries(results.fields || {}).map(([key, value]) => (
                            <div key={key} className="flex justify-between items-center">
                                <span className="text-gray-600">{key}</span>
                                <span className="font-medium">{String(value)}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Messages de validation */}
                {((results.warnings?.length ?? 0) > 0 || (results.errors?.length ?? 0) > 0) && (
                    <div className="space-y-2">
                        {results.warnings?.map((warning, index) => (
                            <div key={index} className="flex items-center gap-2 text-yellow-700 bg-yellow-50 p-3 rounded">
                                <AlertTriangle className="h-5 w-5" />
                                {warning}
                            </div>
                        ))}
                        {results.errors?.map((error, index) => (
                            <div key={index} className="flex items-center gap-2 text-red-700 bg-red-50 p-3 rounded">
                                <AlertTriangle className="h-5 w-5" />
                                {error}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};