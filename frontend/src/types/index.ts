// src/types/index.ts
export interface DocumentField {
    value: string;
    confidence: number;
}

export interface ProcessingResult {
    document_type: string;
    confidence: number;
    fields: {
        [key: string]: DocumentField;
    };
    warnings?: string[];
    errors?: string[];
    metadata?: {
        filename: string;
        processedAt: string;
        fileSize: number;
    };
}