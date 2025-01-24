// src/components/TestDocuments.tsx
import React from 'react';

const TEST_DOCUMENTS = [
    {
        name: 'facture_test.pdf',
        content: new File(['test content'], 'facture_test.pdf', { type: 'application/pdf' }),
        expectedType: 'invoice'
    },
    {
        name: 'contrat_test.jpg',
        content: new File(['test content'], 'contrat_test.jpg', { type: 'image/jpeg' }),
        expectedType: 'contract'
    }
];

export const TestDocuments: React.FC = () => {
    return (
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-4">Documents de Test</h2>
            <div className="space-y-2">
                {TEST_DOCUMENTS.map((doc) => (
                    <div key={doc.name} className="flex items-center gap-4">
                        <span>{doc.name}</span>
                        <button
                            onClick={() => {
                                // Simuler un drag and drop ou un clic sur input file
                                const input = document.querySelector('input[type="file"]') as HTMLInputElement;
                                if (input) {
                                    const dataTransfer = new DataTransfer();
                                    dataTransfer.items.add(doc.content);
                                    input.files = dataTransfer.files;
                                    input.dispatchEvent(new Event('change', { bubbles: true }));
                                }
                            }}
                            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            Tester
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};