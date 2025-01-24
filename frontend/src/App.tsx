// import React from 'react';
import { useState } from 'react';
import { DocumentUploader } from './components/DocumentUploader';
import { ProcessingResults } from './components/ProcessingResults';
import { TestDocuments } from './components/TestDocuments';
import { ProcessingResult } from './types';
import './App.css';

function App() {
    const [processingResults, setProcessingResults] = useState<ProcessingResult | null>(null);

    const handleDocumentProcessed = (results: ProcessingResult) => {
        setProcessingResults(results);
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-4xl mx-auto space-y-8">
                <header className="text-center">
                    <h1 className="text-3xl font-bold text-gray-800">
                        Traitement Intelligent de Documents
                    </h1>
                    <p className="mt-2 text-gray-600">
                        Uploadez vos documents pour analyse automatique
                    </p>
                </header>

                <DocumentUploader onDocumentProcessed={handleDocumentProcessed} />

                {processingResults && (
                    <ProcessingResults results={processingResults} />
                )}

                {process.env.NODE_ENV === 'development' && (
                    <TestDocuments />
                )}

                <footer className="text-center text-gray-500 text-sm mt-8">
                    <p>Formats supportés : PDF, JPG, PNG</p>
                    <p>Taille maximale : 10MB</p>
                </footer>
            </div>
        </div>
    );
}

export default App;




// import React from 'react';
// import { DocumentUploader } from './components/DocumentUploader';
// import { ProcessingResults } from './components/ProcessingResults';
// import './App.css';
//
// function App() {
//     const [processingResults, setProcessingResults] = React.useState<any>(null);
//
//     const handleDocumentProcessed = (results: any) => {
//         setProcessingResults(results);
//     };
//
//     return (
//         <div className="min-h-screen bg-gray-100 p-8">
//             <div className="max-w-4xl mx-auto space-y-8">
//                 <header className="text-center">
//                     <h1 className="text-3xl font-bold text-gray-800">
//                         Traitement Intelligent de Documents
//                     </h1>
//                     <p className="mt-2 text-gray-600">
//                         Uploadez vos documents pour analyse automatique
//                     </p>
//                 </header>
//
//                 <DocumentUploader onDocumentProcessed={handleDocumentProcessed} />
//
//                 {processingResults && (
//                     <ProcessingResults results={processingResults} />
//                 )}
//             </div>
//         </div>
//     );
// }
//
// export default App;