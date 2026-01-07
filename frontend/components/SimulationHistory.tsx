'use client';

import { useState, useEffect } from 'react';
import { FinancingAPI } from '@/services/api';
import type { SimulationResponse } from '@/types/financing';
import SimulationCard from './SimulationCard';
import { History, Loader2 } from 'lucide-react';

interface SimulationHistoryProps {
  onReuse: (simulation: SimulationResponse) => void;
  refreshTrigger?: number;
}

export default function SimulationHistory({ onReuse, refreshTrigger }: SimulationHistoryProps) {
  const [simulations, setSimulations] = useState<SimulationResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadHistory();
  }, [refreshTrigger]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await FinancingAPI.getHistory(3);
      setSimulations(data.simulations);
    } catch (err) {
      setError('Não foi possível carregar o histórico');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card-liquid p-8">
        <div className="flex items-center justify-center gap-3 text-liquid-gray-400">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>Carregando histórico...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card-liquid p-8">
        <div className="text-center text-liquid-gray-400">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (simulations.length === 0) {
    return (
      <div className="card-liquid p-8">
        <div className="text-center text-liquid-gray-400">
          <History className="w-12 h-12 mx-auto mb-3 text-liquid-gray-600" />
          <p className="font-medium text-white">Nenhuma simulação anterior</p>
          <p className="text-sm mt-1">Faça sua primeira simulação acima</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card-liquid p-6">
      <div className="flex items-center gap-2 mb-5">
        <History className="w-5 h-5 text-liquid-orange" />
        <h2 className="text-lg font-semibold text-white">
          Simulações Anteriores
        </h2>
        <span className="ml-auto text-sm text-liquid-gray-400">
          {simulations.length} {simulations.length === 1 ? 'simulação' : 'simulações'}
        </span>
      </div>
      
      <div className="space-y-3">
        {simulations.map((simulation) => (
          <SimulationCard
            key={simulation.simulation_id || simulation.timestamp}
            simulation={simulation}
            onReuse={() => onReuse(simulation)}
          />
        ))}
      </div>
    </div>
  );
}