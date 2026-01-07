'use client';

import { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import Header from '@/components/Header';
import SimulatorForm from '@/components/SimulatorForm';
import ResultsPanel from '@/components/ResultsPanel';
import AmortizationChart from '@/components/AmortizationChart';
import SimulationHistory from '@/components/SimulationHistory';
import { FinancingAPI } from '@/services/api';
import type { SimulationRequest, SimulationResponse } from '@/types/financing';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SimulationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [historyRefresh, setHistoryRefresh] = useState(0);
  const [formKey, setFormKey] = useState(0);

  const handleSimulate = async (data: SimulationRequest) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await FinancingAPI.simulate(data);
      setResult(response);
      
      // Atualiza o histórico após nova simulação
      setHistoryRefresh(prev => prev + 1);
      
      // Scroll suave para os resultados
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao processar simulação');
      console.error('Erro na simulação:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReuseSimulation = (simulation: SimulationResponse) => {
    // Rola para o topo
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Carrega os dados da simulação anterior
    setResult(simulation);
    setFormKey(prev => prev + 1);
  };

  return (
    <>
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-white">Simulador de</span>
            <br />
            <span className="text-gradient-orange">Financiamento Imobiliário</span>
          </h1>
          <p className="text-liquid-gray-400 text-lg max-w-2xl mx-auto">
            Simule seu financiamento com taxas reais e indicadores econômicos atualizados.
            Calcule parcelas, juros e compare com a média nacional.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-8 p-4 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start animate-fade-in">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-red-400 font-semibold">Erro na Simulação</p>
              <p className="text-red-300 text-sm mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Formulário - 1 coluna */}
          <div className="lg:col-span-1">
            <SimulatorForm 
              key={formKey}
              onSubmit={handleSimulate} 
              isLoading={isLoading}
              initialData={result ? {
                valor_imovel: result.simulacao.valor_imovel,
                entrada: result.simulacao.entrada,
                prazo_meses: result.simulacao.prazo_meses,
                tipo_amortizacao: result.simulacao.tipo_amortizacao as 'PRICE' | 'SAC',
                regiao: 'SP'
              } : undefined}
            />

          </div>

          {/* Resultados - 2 colunas */}
          <div className="lg:col-span-2">
            {isLoading && (
              <div className="card-liquid h-96 flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-block w-16 h-16 border-4 border-liquid-orange border-t-transparent rounded-full animate-spin mb-4"></div>
                  <p className="text-liquid-gray-400">Processando simulação...</p>
                  <p className="text-sm text-liquid-gray-500 mt-2">
                    Consultando indicadores econômicos e calculando financiamento
                  </p>
                </div>
              </div>
            )}

            {!isLoading && !result && !error && (
              <div className="card-liquid h-96 flex items-center justify-center">
                <div className="text-center max-w-md">
                  <div className="w-20 h-20 bg-liquid-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={1.5}
                      stroke="currentColor"
                      className="w-10 h-10 text-liquid-orange"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M15.75 15.75V18m-7.5-6.75h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V13.5zm0 2.25h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V18zm2.498-6.75h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V13.5zm0 2.25h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V18zm2.504-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zm0 2.25h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V18zm2.498-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zM8.25 6h7.5v2.25h-7.5V6zM12 2.25c-1.892 0-3.758.11-5.593.322C5.307 2.7 4.5 3.65 4.5 4.757V19.5a2.25 2.25 0 002.25 2.25h10.5a2.25 2.25 0 002.25-2.25V4.757c0-1.108-.806-2.057-1.907-2.185A48.507 48.507 0 0012 2.25z"
                      />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">
                    Preencha o formulário
                  </h3>
                  <p className="text-liquid-gray-400">
                    Complete os dados ao lado para simular seu financiamento imobiliário
                    com taxas atualizadas e análise detalhada.
                  </p>
                </div>
              </div>
            )}

            {result && (
              <div id="results" className="space-y-8">
                <ResultsPanel data={result} />
                <AmortizationChart data={result} />
              </div>
            )}

            <div className="mt-8">
              <SimulationHistory
                onReuse={handleReuseSimulation}
                refreshTrigger={historyRefresh}
              />
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-16 text-center text-liquid-gray-500 text-sm">
          <p>
            Simulação baseada em indicadores econômicos reais (SELIC/IPCA) do Banco Central e IBGE.
          </p>
          <p className="mt-2">
            Desenvolvido com{' '}
            <span className="text-liquid-orange">♥</span> usando Next.js, TypeScript e AWS Lambda
          </p>
        </div>
      </main>
    </>
  );
}