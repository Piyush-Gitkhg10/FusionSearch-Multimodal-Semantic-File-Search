import { useState } from 'react';
import { uploadFile } from '../services/api';
import { UploadCloud } from 'lucide-react';

export default function FileUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setMessage('');
    try {
      await uploadFile(file);
      setMessage(`Successfully uploaded ${file.name}`);
    } catch (error) {
      setMessage(`Upload failed. Please try again. ${error}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-gray-100 mt-8 text-center">
      <UploadCloud className="mx-auto h-12 w-12 text-blue-500 mb-4" />
      <h3 className="text-lg font-semibold text-gray-800">Upload a File</h3>
      <p className="text-sm text-gray-500 mb-4">Supports Text, Code, and Images</p>
      
      <label className="cursor-pointer bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors">
        {isUploading ? 'Uploading...' : 'Browse Files'}
        <input type="file" className="hidden" onChange={handleUpload} disabled={isUploading} />
      </label>
      {message && <p className="mt-4 text-sm font-medium text-gray-700">{message}</p>}
    </div>
  );
}