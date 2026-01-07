export interface SimulationRequest {
  valor_imovel: number;
  entrada: number;
  prazo_meses: number;
  tipo_amortizacao: 'PRICE' | 'SAC';
  regiao: string;
}

export interface IndicadorEconomico {
  indicador_usado: 'SELIC' | 'IPCA' | 'TAXA_BASE';
  valor_indicador: number;
  fonte: string;
  data_referencia: string;
}

export interface TaxasAplicadas {
  indicador: IndicadorEconomico;
  taxa_juros_anual: number;
  taxa_juros_mensal: number;
  formula_aplicada: string;
}

export interface DadosSimulacao {
  valor_imovel: number;
  entrada: number;
  valor_financiado: number;
  prazo_meses: number;
  tipo_amortizacao: 'PRICE' | 'SAC';
}

export interface DetalheParcela {
  valor: number;
  juros: number;
  amortizacao: number;
  saldo_devedor: number;
}

export interface ResultadoFinanciamento {
  parcela_mensal: number;
  total_pago: number;
  juros_totais: number;
  percentual_juros: number;
  primeira_parcela: DetalheParcela;
  ultima_parcela: DetalheParcela;
}

export interface Comparativo {
  taxa_media_nacional: number;
  diferenca_percentual: number;
  classificacao: 'ACIMA_DA_MEDIA' | 'NA_MEDIA' | 'ABAIXO_DA_MEDIA';
  mensagem: string;
}

export interface Analise {
  comprometimento_renda_sugerido: number;
  renda_minima_sugerida: number;
  viabilidade: 'ALTA' | 'MODERADA' | 'BAIXA';
  alertas: string[];
}

export interface ParcelaAmortizacao {
  mes: number;
  parcela: number;
  juros: number;
  amortizacao: number;
  saldo_devedor: number;
}

export interface SimulationResponse {
  request_id: string;
  timestamp: string;
  simulacao: DadosSimulacao;
  taxas: TaxasAplicadas;
  resultado: ResultadoFinanciamento;
  comparativo: Comparativo;
  analise: Analise;
  tabela_amortizacao_resumida: ParcelaAmortizacao[];
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: any;
    request_id?: string;
    timestamp?: string;
  };
}