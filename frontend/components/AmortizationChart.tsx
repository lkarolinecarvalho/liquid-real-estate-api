'use client';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import type { SimulationResponse } from '@/types/financing';

interface AmortizationChartProps {
  data: SimulationResponse;
}

export default function AmortizationChart({ data }: AmortizationChartProps) {
  // Preparar dados para o gráfico
  const chartData = data.tabela_amortizacao_resumida.map((parcela) => ({
    mes: parcela.mes,
    juros: parcela.juros,
    amortizacao: parcela.amortizacao,
    saldo: parcela.saldo_devedor,
  }));

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-liquid-gray-900 border border-liquid-gray-700 rounded-lg p-3 shadow-xl">
          <p className="text-sm font-semibold text-white mb-2">
            Mês {payload[0].payload.mes}
          </p>
          <div className="space-y-1">
            <p className="text-xs">
              <span className="text-red-400">Juros: </span>
              <span className="text-white font-semibold">
                {formatCurrency(payload[0].payload.juros)}
              </span>
            </p>
            <p className="text-xs">
              <span className="text-green-400">Amortização: </span>
              <span className="text-white font-semibold">
                {formatCurrency(payload[0].payload.amortizacao)}
              </span>
            </p>
            <p className="text-xs">
              <span className="text-liquid-gray-400">Saldo: </span>
              <span className="text-white font-semibold">
                {formatCurrency(payload[0].payload.saldo)}
              </span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card-liquid animate-fade-in animation-delay-200">
      <h3 className="text-lg font-bold mb-6 flex items-center">
        <span className="text-white">Evolução da</span>
        <span className="text-liquid-orange ml-2">Amortização</span>
      </h3>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={chartData}
            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorJuros" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#EF4444" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorAmortizacao" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" />
            <XAxis
              dataKey="mes"
              stroke="#6B7280"
              style={{ fontSize: '12px' }}
              tickFormatter={(value) => `${value}m`}
            />
            <YAxis
              stroke="#6B7280"
              style={{ fontSize: '12px' }}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{
                fontSize: '12px',
                paddingTop: '20px',
              }}
              iconType="circle"
            />
            <Area
              type="monotone"
              dataKey="juros"
              name="Juros"
              stroke="#EF4444"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorJuros)"
            />
            <Area
              type="monotone"
              dataKey="amortizacao"
              name="Amortização"
              stroke="#10B981"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorAmortizacao)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
        <div className="p-3 bg-liquid-gray-800 rounded-lg">
          <div className="flex items-center mb-1">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
            <span className="text-liquid-gray-400">Juros</span>
          </div>
          <p className="text-white font-semibold">
            {formatCurrency(data.resultado.juros_totais)}
          </p>
        </div>
        <div className="p-3 bg-liquid-gray-800 rounded-lg">
          <div className="flex items-center mb-1">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="text-liquid-gray-400">Amortização</span>
          </div>
          <p className="text-white font-semibold">
            {formatCurrency(data.simulacao.valor_financiado)}
          </p>
        </div>
      </div>
    </div>
  );
}