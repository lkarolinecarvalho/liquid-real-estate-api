'use client';

import { useState } from 'react';
import type { SimulationRequest } from '@/types/financing';

interface SimulatorFormProps {
  onSubmit: (data: SimulationRequest) => void;
  isLoading: boolean;
}

const ESTADOS_BRASIL = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
];

export default function SimulatorForm({ onSubmit, isLoading }: SimulatorFormProps) {
  const [formData, setFormData] = useState<SimulationRequest>({
    valor_imovel: 500000,
    entrada: 100000,
    prazo_meses: 360,
    tipo_amortizacao: 'PRICE',
    regiao: 'SP',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const percentualEntrada = ((formData.entrada / formData.valor_imovel) * 100).toFixed(1);
  const valorFinanciado = formData.valor_imovel - formData.entrada;
  

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="card-liquid">
        <h2 className="text-xl font-bold mb-6 flex items-center">
          <span className="text-white">Dados do</span>
          <span className="text-liquid-orange ml-2">Financiamento</span>
        </h2>

        {/* Valor do Imóvel */}
        <div>
          <label className="label-liquid">
            Valor do Imóvel
          </label>
          <input
            type="number"
            className="input-liquid"
            value={formData.valor_imovel || ''}
            onChange={(e) => setFormData({ 
              ...formData, 
              valor_imovel: e.target.value === '' ? 0 : Number(e.target.value) 
            })}
            min="10000"
            max="100000000"
            step="1000"
            required
          />
          <p className="text-xs text-liquid-gray-400 mt-1">
            {formatCurrency(formData.valor_imovel)}
          </p>
        </div>

        {/* Entrada */}
        <div className="mt-4">
          <label className="label-liquid">
            Valor da Entrada ({percentualEntrada}%)
          </label>
          <input
            type="number"
            className="input-liquid"
            value={formData.entrada === 0 ? '' : formData.entrada}
            onChange={(e) => setFormData({ 
              ...formData, 
              entrada: e.target.value === '' ? 0 : Number(e.target.value) 
            })}
            min="0"
            max={formData.valor_imovel}
            step="1000"
            required
          />
          <p className="text-xs text-liquid-gray-400 mt-1">
            {formatCurrency(formData.entrada)}
          </p>
        </div>

        {/* Valor Financiado */}
        <div className="mt-4 p-4 bg-liquid-gray-800 rounded-lg border border-liquid-gray-700">
          <p className="text-sm text-liquid-gray-400">Valor a Financiar</p>
          <p className="text-2xl font-bold text-liquid-orange">
            {formatCurrency(valorFinanciado)}
          </p>
        </div>

        {/* Prazo */}
        <div className="mt-4">
          <label className="label-liquid">
            Prazo (meses)
          </label>
          <input
            type="number"
            className="input-liquid"
            value={formData.prazo_meses || ''}
            onChange={(e) => setFormData({ 
              ...formData, 
              prazo_meses: e.target.value === '' ? 0 : Number(e.target.value) 
            })}
            min="12"
            max="480"
            step="12"
            required
          />
          <p className="text-xs text-liquid-gray-400 mt-1">
            {(formData.prazo_meses / 12).toFixed(1)} anos
          </p>
        </div>

        {/* Tipo de Amortização */}
        <div className="mt-4">
          <label className="label-liquid">
            Sistema de Amortização
          </label>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => setFormData({ ...formData, tipo_amortizacao: 'PRICE' })}
              className={`p-4 rounded-lg border-2 transition-all ${
                formData.tipo_amortizacao === 'PRICE'
                  ? 'border-liquid-orange bg-liquid-orange/10'
                  : 'border-liquid-gray-700 bg-liquid-gray-800 hover:border-liquid-gray-600'
              }`}
            >
              <p className="font-semibold">PRICE</p>
              <p className="text-xs text-liquid-gray-400 mt-1">Parcelas fixas</p>
            </button>
            <button
              type="button"
              onClick={() => setFormData({ ...formData, tipo_amortizacao: 'SAC' })}
              className={`p-4 rounded-lg border-2 transition-all ${
                formData.tipo_amortizacao === 'SAC'
                  ? 'border-liquid-orange bg-liquid-orange/10'
                  : 'border-liquid-gray-700 bg-liquid-gray-800 hover:border-liquid-gray-600'
              }`}
            >
              <p className="font-semibold">SAC</p>
              <p className="text-xs text-liquid-gray-400 mt-1">Parcelas decrescentes</p>
            </button>
          </div>
        </div>

        {/* Estado */}
        <div className="mt-4">
          <label className="label-liquid">
            Estado (UF)
          </label>
          <select
            className="input-liquid"
            value={formData.regiao}
            onChange={(e) => setFormData({ ...formData, regiao: e.target.value })}
            required
          >
            {ESTADOS_BRASIL.map((uf) => (
              <option key={uf} value={uf}>
                {uf}
              </option>
            ))}
          </select>
        </div>

        {/* Botão Submit */}
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary mt-6"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Calculando...
            </span>
          ) : (
            'Simular Financiamento'
          )}
        </button>
      </div>
    </form>
  );
}