import { useState } from 'react';
import { searchFiles } from '../services/api';
import { Search, FileText } from 'lucide-react';

export default function SearchDashboard() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const res = await searchFiles(query);
      setResults(res.data || []);
    } catch (error) {
      console.error("Search error", error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-12 space-y-8">
      {/* Search Input */}
      <form onSubmit={handleSearch} className="relative flex items-center">
        <Search className="absolute left-4 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe the file or image you are looking for..."
          className="w-full pl-12 pr-24 py-4 rounded-xl border border-gray-200 shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none text-lg"
        />
        <button 
          type="submit" 
          disabled={isSearching}
          className="absolute right-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium"
        >
          {isSearching ? 'Searching...' : 'Search'}
        </button>
      </form>

      {/* Results List */}
      <div className="space-y-4">
        {results.map((item) => (
          <div key={item.id} className="p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center space-x-3">
                <FileText className="text-blue-500" />
                <h4 className="text-lg font-semibold text-gray-900">{item.file_name}</h4>
              </div>
              <span className="bg-blue-50 text-blue-700 text-xs px-3 py-1 rounded-full font-medium">
                Score: {item.scores.final_score.toFixed(2)}
              </span>
            </div>
            <p className="text-gray-600 text-sm mt-3">{item.snippet}</p>
            <div className="mt-4 flex space-x-4 text-xs text-gray-400">
              <span>Type: {item.file_type}</span>
              <span>Semantic: {item.scores.semantic_score.toFixed(2)}</span>
              <span>Keyword: {item.scores.filename_score.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}