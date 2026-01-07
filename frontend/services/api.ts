import axios, { AxiosError } from 'axios';
import type { SimulationRequest, SimulationResponse, ApiError } from '@/types/financing';

export type { SimulationResponse, SimulationRequest, ApiError } from '@/types/financing';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://62dv6tdqh1.execute-api.us-east-1.amazonaws.com';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export class FinancingAPI {
  static async simulate(data: SimulationRequest): Promise<SimulationResponse> {
    try {
      const response = await apiClient.post<SimulationResponse>('/financing/simulate', data);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<ApiError>;
        
        if (axiosError.response?.data?.error) {
          throw new Error(axiosError.response.data.error.message);
        }
        
        if (axiosError.code === 'ECONNABORTED') {
          throw new Error('Tempo limite excedido. Tente novamente.');
        }
        
        if (!axiosError.response) {
          throw new Error('Não foi possível conectar à API. Verifique sua conexão.');
        }
      }
      
      throw new Error('Erro inesperado ao processar simulação.');
    }
  }

  static async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('API indisponível');
    }
  }

  static async getHistory(limit: number = 3): Promise<HistoryResponse> {
    try {
      const response = await apiClient.get(`/financing/history?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar histórico:', error);
      throw new Error('Não foi possível carregar o histórico');
    }
  }
}

export default apiClient;
export interface HistoryResponse {
  total: number;
  simulations: SimulationResponse[];
}