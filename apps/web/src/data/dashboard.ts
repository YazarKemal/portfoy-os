import type {
  AllocationItem,
  DashboardMetrics,
  DataSourceStatus,
  Holding,
  PerformancePoint,
  PeriodReturn,
  PortfolioObservation,
  TransactionItem,
} from "@/types/dashboard";

/** Demo veri — bütün değerler kurgusaldır, yatırım tavsiyesi değildir. */

export const DEMO_METRICS: DashboardMetrics = {
  totalValue: 428650.4,
  dailyChange: 2184.3,
  dailyChangePercent: 0.51,
  totalReturn: 38420.7,
  totalReturnPercent: 9.85,
  investedPrincipal: 390229.7,
  unrealizedPnL: 31780.2,
  realizedPnL: 6640.5,
  cashReserve: 54200.0,
};

export const DEMO_PERIOD_RETURNS: Record<string, PeriodReturn> = {
  "1A": { amount: 3850.1, percentage: 0.91 },
  "3A": { amount: 15449.6, percentage: 3.74 },
  "6A": { amount: 33220.2, percentage: 8.4 },
  YBB: { amount: 38420.7, percentage: 9.85 },
  "1Y": { amount: 38420.7, percentage: 9.85 },
  ALL: { amount: 38420.7, percentage: 9.85 },
};

export const PERIOD_CUTOFFS: Record<string, string> = {
  "1A": "2026-07-04",
  "3A": "2026-05-04",
  "6A": "2026-02-04",
  YBB: "2026-01-01",
  "1Y": "2025-08-04",
  ALL: "",
};

export const DEMO_PERFORMANCE: PerformancePoint[] = [
  { date: "2026-01-05", value: 390229.7, principal: 390229.7 },
  { date: "2026-01-20", value: 392100.5, principal: 390229.7 },
  { date: "2026-02-05", value: 395430.2, principal: 390229.7 },
  { date: "2026-02-20", value: 398800.9, principal: 390229.7 },
  { date: "2026-03-05", value: 401200.6, principal: 390229.7 },
  { date: "2026-03-20", value: 404650.3, principal: 390229.7 },
  { date: "2026-04-05", value: 407800.1, principal: 390229.7 },
  { date: "2026-04-20", value: 410300.4, principal: 390229.7 },
  { date: "2026-05-05", value: 413200.8, principal: 390229.7 },
  { date: "2026-05-20", value: 416500.0, principal: 390229.7 },
  { date: "2026-06-05", value: 419100.2, principal: 390229.7 },
  { date: "2026-06-20", value: 422300.7, principal: 390229.7 },
  { date: "2026-07-05", value: 424800.3, principal: 390229.7 },
  { date: "2026-07-20", value: 426900.5, principal: 390229.7 },
  { date: "2026-08-04", value: 428650.4, principal: 390229.7 },
];

export function filterPerformanceByPeriod(
  data: PerformancePoint[],
  cutoff: string,
): PerformancePoint[] {
  if (!cutoff) return data;
  const filtered = data.filter((d) => d.date >= cutoff);
  if (filtered.length < 2) return data.slice(-2);
  return filtered;
}

export const DEMO_ALLOCATION: AllocationItem[] = [
  { category: "Fon", value: 182430.8, percentage: 42.6, colorVar: "--chart-1" },
  { category: "Değerli Maden", value: 98520.6, percentage: 23.0, colorVar: "--chart-2" },
  { category: "Döviz", value: 65200.3, percentage: 15.2, colorVar: "--chart-3" },
  { category: "Mevduat / Nakit", value: 54200.0, percentage: 12.6, colorVar: "--chart-4" },
  { category: "Hisse", value: 28298.7, percentage: 6.6, colorVar: "--chart-5" },
];

export const DEMO_HOLDINGS: Holding[] = [
  {
    id: "h1",
    assetName: "BGP Para Piyasası Fonu",
    assetCode: "BPP",
    assetType: "fon",
    assetTypeLabel: "Fon",
    quantity: 10_000,
    averageCost: 12.062568,
    currentPrice: 13.062568,
    marketValue: 130_625.68,
    dailyChange: 125.42,
    dailyChangePercent: 0.1,
    totalPnL: 10_000.0,
    totalPnLPercent: 8.29,
    dataTime: "5 Ağu 2026, 18:30",
    dataFreshness: "eod",
    currency: "TRY",
  },
  {
    id: "h2",
    assetName: "Altın Fonu",
    assetCode: "ALT",
    assetType: "fon",
    assetTypeLabel: "Fon",
    quantity: 800,
    averageCost: 57.2564,
    currentPrice: 64.7564,
    marketValue: 51_805.12,
    dailyChange: 320.5,
    dailyChangePercent: 0.62,
    totalPnL: 6_000.0,
    totalPnLPercent: 13.1,
    dataTime: "5 Ağu 2026, 18:30",
    dataFreshness: "eod",
    currency: "TRY",
  },
  {
    id: "h3",
    assetName: "Fiziki Altın (Gram)",
    assetCode: "XAU",
    assetType: "değerli-maden",
    assetTypeLabel: "Değerli Maden",
    quantity: 30,
    averageCost: 3_000.68666667,
    currentPrice: 3_284.02,
    marketValue: 98_520.6,
    dailyChange: 850.04,
    dailyChangePercent: 0.87,
    totalPnL: 8_500.0,
    totalPnLPercent: 9.44,
    dataTime: "3 Ağu 2026, 17:30",
    dataFreshness: "stale",
    currency: "TRY",
  },
  {
    id: "h4",
    assetName: "Hisse Senedi",
    assetCode: "HSS",
    assetType: "hisse",
    assetTypeLabel: "Hisse",
    quantity: 1_000,
    averageCost: 24.2987,
    currentPrice: 28.2987,
    marketValue: 28_298.7,
    dailyChange: 600.0,
    dailyChangePercent: 2.17,
    totalPnL: 4_000.0,
    totalPnLPercent: 16.46,
    dataTime: "5 Ağu 2026, 18:15",
    dataFreshness: "eod",
    currency: "TRY",
  },
  {
    id: "h5",
    assetName: "USD Döviz",
    assetCode: "USD",
    assetType: "döviz",
    assetTypeLabel: "Döviz",
    quantity: 1_800,
    averageCost: 34.40005556,
    currentPrice: 36.22238889,
    marketValue: 65_200.3,
    dailyChange: 288.34,
    dailyChangePercent: 0.44,
    totalPnL: 3_280.2,
    totalPnLPercent: 5.3,
    dataTime: "5 Ağu 2026, 19:15",
    dataFreshness: "live",
    currency: "TRY",
  },
  {
    id: "h6",
    assetName: "Nakit Rezerv (TRY)",
    assetCode: "TRY",
    assetType: "mevduat",
    assetTypeLabel: "Mevduat / Nakit",
    quantity: 54_200,
    averageCost: 1.0,
    currentPrice: 1.0,
    marketValue: 54_200.0,
    dailyChange: 0.0,
    dailyChangePercent: 0.0,
    totalPnL: 0.0,
    totalPnLPercent: 0.0,
    dataTime: "5 Ağu 2026, 09:00",
    dataFreshness: "live",
    currency: "TRY",
  },
];

export const DEMO_TRANSACTIONS: TransactionItem[] = [
  {
    id: "t1",
    type: "BUY",
    typeLabel: "Alım",
    assetName: "BGP Para Piyasası Fonu",
    accountName: "Yatırım Hesabı",
    date: "5 Ağu 2026",
    quantity: 150.5,
    amount: 1578.74,
    totalValue: 1578.74,
    needsReview: false,
  },
  {
    id: "t2",
    type: "DIVIDEND",
    typeLabel: "Temettü",
    assetName: "Hisse Senedi",
    accountName: "Yatırım Hesabı",
    date: "3 Ağu 2026",
    amount: 340.0,
    totalValue: 340.0,
    needsReview: false,
  },
  {
    id: "t3",
    type: "SELL",
    typeLabel: "Satım",
    assetName: "Altın Fonu",
    accountName: "Yatırım Hesabı",
    date: "29 Tem 2026",
    quantity: 50.0,
    amount: 3216.0,
    totalValue: 3216.0,
    needsReview: true,
  },
  {
    id: "t4",
    type: "DEPOSIT",
    typeLabel: "Para Yatırma",
    assetName: "—",
    accountName: "Yatırım Hesabı",
    date: "25 Tem 2026",
    amount: 10000.0,
    totalValue: 10000.0,
    needsReview: false,
  },
  {
    id: "t5",
    type: "FEE",
    typeLabel: "Ücret",
    assetName: "—",
    accountName: "Yatırım Hesabı",
    date: "22 Tem 2026",
    amount: 18.5,
    totalValue: 18.5,
    needsReview: false,
  },
];

export const DEMO_OBSERVATIONS: PortfolioObservation[] = [
  {
    id: "o1",
    text: "Portföyünüzün %42'si Fon kategorisinde.",
    kind: "concentration",
  },
  {
    id: "o2",
    text: "1 fiyat kaynağı 24 saatten eski.",
    kind: "data-quality",
  },
  {
    id: "o3",
    text: "Nakit rezerviniz toplam değerin %12,6'sı.",
    kind: "allocation",
  },
];

export const DEMO_DATA_SOURCES: DataSourceStatus[] = [
  {
    provider: "tefas",
    providerLabel: "TEFAS",
    status: "healthy",
    lastChecked: "5 Ağu 2026, 18:45",
    responseTimeMs: 245,
  },
  {
    provider: "manual",
    providerLabel: "Manuel Giriş",
    status: "healthy",
    lastChecked: "5 Ağu 2026, 19:15",
    responseTimeMs: 0,
  },
  {
    provider: "altin-fiyat",
    providerLabel: "Altın Fiyat API",
    status: "degraded",
    lastChecked: "4 Ağu 2026, 23:30",
    lastError: "Gateway timeout — veri gecikmeli",
    responseTimeMs: 4523,
  },
];

export const DEMO_DATA_FRESHNESS_SUMMARY = {
  status: "partial" as const,
  label: "Veriler kısmen güncel",
  description: "1 kaynak 24 saati aşkın süredir güncellenmedi.",
  lastFullUpdate: "5 Ağu 2026, 18:45",
};
