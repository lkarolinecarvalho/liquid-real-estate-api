'use client';

import { TrendingUp, TrendingDown, AlertCircle, CheckCircle } from 'lucide-react';
import type { SimulationResponse } from '@/types/financing';

interface ResultsPanelProps {
  data: SimulationResponse;
}

export default function ResultsPanel({ data }: ResultsPanelProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const getViabilidadeBadge = () => {
    switch (data.analise.viabilidade) {
      case 'ALTA':
        return <span className="badge-green">Viabilidade Alta</span>;
      case 'MODERADA':
        return <span className="badge-yellow">Viabilidade Moderada</span>;
      case 'BAIXA':
        return <span className="badge-red">Viabilidade Baixa</span>;
    }
  };

  const getComparativoBadge = () => {
    switch (data.comparativo.classificacao) {
      case 'ABAIXO_DA_MEDIA':
        return (
          <span className="flex items-center text-green-400 text-sm">
            <TrendingDown className="w-4 h-4 mr-1" />
            Abaixo da Média
          </span>
        );
      case 'NA_MEDIA':
        return (
          <span className="flex items-center text-liquid-gray-400 text-sm">
            <CheckCircle className="w-4 h-4 mr-1" />
            Na Média
          </span>
        );
      case 'ACIMA_DA_MEDIA':
        return (
          <span className="flex items-center text-yellow-400 text-sm">
            <TrendingUp className="w-4 h-4 mr-1" />
            Acima da Média
          </span>
        );
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Stats principais */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="stat-card">
          <p className="text-sm text-liquid-gray-400 mb-1">Parcela Mensal</p>
          <p className="text-3xl font-bold text-liquid-orange">
            {formatCurrency(data.resultado.parcela_mensal)}
          </p>
          <p className="text-xs text-liquid-gray-500 mt-2">
            {data.simulacao.tipo_amortizacao === 'PRICE' ? 'Fixo' : 'Primeira parcela'}
          </p>
        </div>

        <div className="stat-card">
          <p className="text-sm text-liquid-gray-400 mb-1">Total a Pagar</p>
          <p className="text-2xl font-bold text-white">
            {formatCurrency(data.resultado.total_pago)}
          </p>
          <p className="text-xs text-liquid-gray-500 mt-2">
            Em {data.simulacao.prazo_meses} meses
          </p>
        </div>

        <div className="stat-card">
          <p className="text-sm text-liquid-gray-400 mb-1">Juros Totais</p>
          <p className="text-2xl font-bold text-red-400">
            {formatCurrency(data.resultado.juros_totais)}
          </p>
          <p className="text-xs text-liquid-gray-500 mt-2">
            {data.resultado.percentual_juros.toFixed(1)}% do total
          </p>
        </div>
      </div>

      {/* Taxas aplicadas */}
      <div className="card-liquid">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <span className="text-white">Taxas</span>
          <span className="text-liquid-orange ml-2">Aplicadas</span>
        </h3>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Indicador Usado:</span>
            <span className="badge-orange">{data.taxas.indicador.indicador_usado}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Fonte:</span>
            <span className="text-white text-sm">{data.taxas.indicador.fonte}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Taxa Anual:</span>
            <span className="text-liquid-orange font-bold">{data.taxas.taxa_juros_anual.toFixed(2)}%</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Taxa Mensal:</span>
            <span className="text-white font-semibold">{data.taxas.taxa_juros_mensal.toFixed(4)}%</span>
          </div>
        </div>
      </div>

      {/* Comparativo */}
      <div className="card-liquid">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <span className="text-white">Comparativo</span>
          <span className="text-liquid-orange ml-2">Nacional</span>
        </h3>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Status:</span>
            {getComparativoBadge()}
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Taxa Média Brasil:</span>
            <span className="text-white">{data.comparativo.taxa_media_nacional.toFixed(2)}%</span>
          </div>
          
          <div className="p-3 bg-liquid-gray-800 rounded-lg">
            <p className="text-sm text-liquid-gray-300">{data.comparativo.mensagem}</p>
          </div>
        </div>
      </div>

      {/* Análise de Viabilidade */}
      <div className="card-liquid">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <span className="text-white">Análise de</span>
          <span className="text-liquid-orange ml-2">Viabilidade</span>
        </h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Classificação:</span>
            {getViabilidadeBadge()}
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Renda Mínima Sugerida:</span>
            <span className="text-liquid-orange font-bold">
              {formatCurrency(data.analise.renda_minima_sugerida)}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-liquid-gray-400">Comprometimento Ideal:</span>
            <span className="text-white">{data.analise.comprometimento_renda_sugerido}%</span>
          </div>
          
          {data.analise.alertas.length > 0 && (
            <div className="mt-4 space-y-2">
              <p className="text-sm font-semibold text-liquid-gray-300 flex items-center">
                <AlertCircle className="w-4 h-4 mr-2 text-liquid-orange" />
                Recomendações:
              </p>
              {data.analise.alertas.map((alerta, index) => (
                <div key={index} className="p-3 bg-liquid-gray-800 rounded-lg border-l-4 border-liquid-orange">
                  <p className="text-sm text-liquid-gray-300">{alerta}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Detalhes das Parcelas */}
      <div className="card-liquid">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <span className="text-white">Detalhes das</span>
          <span className="text-liquid-orange ml-2">Parcelas</span>
        </h3>
        
        <div className="space-y-4">
          <div className="p-4 bg-liquid-gray-800 rounded-lg">
            <p className="text-xs text-liquid-gray-400 mb-2">Primeira Parcela</p>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-liquid-gray-400">Parcela:</span>
                <span className="ml-2 text-white font-semibold">
                  {formatCurrency(data.resultado.primeira_parcela.valor)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Juros:</span>
                <span className="ml-2 text-red-400">
                  {formatCurrency(data.resultado.primeira_parcela.juros)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Amortização:</span>
                <span className="ml-2 text-green-400">
                  {formatCurrency(data.resultado.primeira_parcela.amortizacao)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Saldo:</span>
                <span className="ml-2 text-liquid-gray-300">
                  {formatCurrency(data.resultado.primeira_parcela.saldo_devedor)}
                </span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-liquid-gray-800 rounded-lg">
            <p className="text-xs text-liquid-gray-400 mb-2">Última Parcela</p>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-liquid-gray-400">Parcela:</span>
                <span className="ml-2 text-white font-semibold">
                  {formatCurrency(data.resultado.ultima_parcela.valor)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Juros:</span>
                <span className="ml-2 text-red-400">
                  {formatCurrency(data.resultado.ultima_parcela.juros)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Amortização:</span>
                <span className="ml-2 text-green-400">
                  {formatCurrency(data.resultado.ultima_parcela.amortizacao)}
                </span>
              </div>
              <div>
                <span className="text-liquid-gray-400">Saldo:</span>
                <span className="ml-2 text-green-400 font-semibold">
                  R$ 0,00
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}