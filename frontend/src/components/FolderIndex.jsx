// src/components/FolderIndex.jsx
import { useState } from 'react';
import { indexFolder } from '../services/api';
import { FolderPlus } from 'lucide-react';

export default function FolderIndex() {
  const [folderPath, setFolderPath] = useState('');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleIndex = async (e) => {
    e.preventDefault();
    if (!folderPath.trim()) return;

    setIsLoading(true);
    setStatus('Scanning and embedding files... This may take a while.');
    
    try {
      const res = await indexFolder(folderPath);
      setStatus(`Success! Indexed ${res.details.indexed} new files. Skipped ${res.details.skipped} files.`);
      setFolderPath('');
    } catch (error) {
      setStatus(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-8 text-center">
      <FolderPlus className="mx-auto h-12 w-12 text-green-500 mb-4" />
      <h3 className="text-lg font-semibold text-gray-800">Index Local Folder</h3>
      <p className="text-sm text-gray-500 mb-4">Paste the absolute path to a folder on your machine.</p>
      
      <form onSubmit={handleIndex} className="flex flex-col space-y-4">
        <input
          type="text"
          value={folderPath}
          onChange={(e) => setFolderPath(e.target.value)}
          placeholder="e.g., C:\Users\Username\Documents\MyProject"
          className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-green-500 focus:outline-none"
          disabled={isLoading}
        />
        <button 
          type="submit"
          disabled={isLoading}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          {isLoading ? 'Processing...' : 'Start Indexing'}
        </button>
      </form>
      {status && <p className="mt-4 text-sm font-medium text-gray-700">{status}</p>}
    </div>
  );
}