export type PredictRequest = {
	Country: string;
	RecencyDays: number;
	TenureDays: number;
	Frequency: number;
	Monetary: number;
	AvgBasketValue: number;
	AvgBasketQuantity: number;
	UniqueProducts: number;
	AverageUnitPrice: number;
};

export type PredictResponse = {
	prediction: number;
	ood: boolean;
	anomaly_score: number;
	warning?: string | null;
};
