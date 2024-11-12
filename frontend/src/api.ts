// api.ts
import axios from 'axios';
import { Planet, Star, Satellite } from './types';

axios.defaults.baseURL = 'http://127.0.0.1:8888/api/v1';
axios.defaults.headers.common['x-api-token'] = '1234'; // Replace with actual API token

// Generic fetchData function that explicitly returns `Promise<T>`
export const fetchData = async <T>(endpoint: string, params?: Record<string, any>): Promise<T> => {
    const { data } = await axios.get<T>(endpoint, { params });
    return data;
};

export const createData = async <T>(endpoint: string, params: Record<string, any>): Promise<T> => {
    const { data } = await axios.post<T>(endpoint, null, { params });
    return data;
};

export const updateData = async <T>(endpoint: string, params: Record<string, any>): Promise<T> => {
    const { data } = await axios.patch<T>(endpoint, null, { params });
    return data;
};

export const deleteData = async (endpoint: string, params: Record<string, any>): Promise<void> => {
    await axios.delete(endpoint, { params });
};
