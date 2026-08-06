/** Core dashboard types for UI Foundation mock data. */

export interface DashboardMetrics {
  totalValue: number;
  dailyChange: number;
  dailyChangePercent: number;
  totalReturn: number;
  totalReturnPercent: number;
  investedPrincipal: number;
  unrealizedPnL: number;
  realizedPnL: number;
  cashReserve: number;
}

export interface PerformancePoint {
  date: string;
  value: number;
  principal?: number;
}

export interface AllocationItem {
  category: string;
  value: number;
  percentage: number;
  colorVar: string;
}

export interface Holding {
  id: string;
  assetName: string;
  assetCode: string;
  assetType: string;
  assetTypeLabel: string;
  quantity: number;
  averageCost: number;
  currentPrice: number;
  marketValue: number;
  dailyChange: number;
  dailyChangePercent: number;
  totalPnL: number;
  totalPnLPercent: number;
  dataTime: string;
  dataFreshness: DataFreshness;
  currency: string;
}

export type DataFreshness = "live" | "delayed" | "eod" | "stale";

export interface TransactionItem {
  id: string;
  type: TransactionTypeLabel;
  typeLabel: string;
  assetName: string;
  accountName: string;
  date: string;
  quantity?: number;
  amount: number;
  totalValue: number;
  needsReview: boolean;
}

export type TransactionTypeLabel =
  | "BUY"
  | "SELL"
  | "DEPOSIT"
  | "WITHDRAWAL"
  | "DIVIDEND"
  | "INTEREST"
  | "FEE"
  | "TAX"
  | "TRANSFER_IN"
  | "TRANSFER_OUT";

export interface PortfolioObservation {
  id: string;
  text: string;
  kind: "concentration" | "data-quality" | "allocation" | "risk";
}

export interface DataSourceStatus {
  provider: string;
  providerLabel: string;
  status: "healthy" | "degraded" | "down" | "unknown";
  lastChecked: string;
  lastError?: string;
  responseTimeMs?: number;
}

export type PeriodKey = "1A" | "3A" | "6A" | "YBB" | "1Y" | "ALL";

export type PrivacyMode = "visible" | "masked";

export interface PeriodReturn {
  amount: number;
  percentage: number;
}
