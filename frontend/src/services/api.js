// src/services/api.js
import axios from "axios";

const API_URL = "http://localhost:8000/api";

// Keep your existing searchFiles function...
export const searchFiles = async (query, limit = 10) => {
    const response = await axios.get(`${API_URL}/search/`, {
        params: { q: query, limit },
    });
    return response.data;
};

// Add this new function
export const indexFolder = async (folderPath) => {
    const response = await axios.post(`${API_URL}/files/index-folder`, {
        folder_path: folderPath,
    });
    return response.data;
};
