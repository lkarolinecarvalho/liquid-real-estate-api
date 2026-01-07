import type { SimulationResponse } from '@/types/financing';
import { RotateCcw, Calendar, Home, Clock } from 'lucide-react';

interface SimulationCardProps {
  simulation: SimulationResponse;
  onReuse: () => void;
}

export default function SimulationCard({ simulation, onReuse }: SimulationCardProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (isoDate: string) => {
    const date = new Date(isoDate);
    const now = new Date();
    const diffMinutes = Math.floor((now.getTime() - date.getTime()) / 60000);
    
    if (diffMinutes < 1) return 'agora mesmo';
    if (diffMinutes < 60) return `há ${diffMinutes} min`;
    if (diffMinutes < 1440) return `há ${Math.floor(diffMinutes / 60)}h`;
    return `há ${Math.floor(diffMinutes / 1440)} dias`;
  };

  return (
    <div className="bg-liquid-gray-800/50 border border-liquid-gray-700 rounded-lg p-4 hover:border-liquid-orange/50 hover:bg-liquid-gray-800 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 text-liquid-gray-400 text-sm mb-3">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(simulation.timestamp)}</span>
          </div>
          
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="flex items-center gap-1 text-liquid-gray-500 text-xs mb-1">
                <Home className="w-3 h-3" />
                <span>Valor</span>
              </div>
              <p className="font-semibold text-white">
                {formatCurrency(simulation.simulacao.valor_financiado)}
              </p>
            </div>
            
            <div>
              <div className="flex items-center gap-1 text-liquid-gray-500 text-xs mb-1">
                <Clock className="w-3 h-3" />
                <span>Prazo</span>
              </div>
              <p className="font-semibold text-white">
                {simulation.simulacao.prazo_meses} meses
              </p>
            </div>
            
            <div>
              <div className="text-liquid-gray-500 text-xs mb-1">Parcela</div>
              <p className="font-semibold text-liquid-orange">
                {formatCurrency(simulation.resultado.parcela_mensal)}
              </p>
            </div>
          </div>
        </div>
        
        <button
          onClick={onReuse}
          className="ml-4 flex items-center gap-2 px-3 py-2 text-sm font-medium text-liquid-orange hover:bg-liquid-orange/10 rounded-lg transition-colors border border-liquid-orange/20"
          title="Refazer esta simulação"
        >
          <RotateCcw className="w-4 h-4" />
          Refazer
        </button>
      </div>
      
      <div className="pt-3 border-t border-liquid-gray-700 flex items-center justify-between text-xs text-liquid-gray-500">
        <span>Taxa: {simulation.taxas.taxa_juros_anual.toFixed(2)}% a.a.</span>
        <span className="text-liquid-gray-600">ID: {simulation.simulation_id?.slice(0, 8)}...</span>
      </div>
    </div>
  );
}