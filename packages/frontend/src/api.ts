import type { PredictRequest, PredictResponse } from './types';

export function createPredictClient(baseUrl: string) {
	return async (payload: PredictRequest): Promise<PredictResponse> => {
		const response = await fetch(`${baseUrl.replace(/\/$/, '')}/predict`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		});

		if (!response.ok) {
			const errorText = await response.text();
			throw new Error(
				errorText || `Request failed with status ${response.status}`,
			);
		}

		return (await response.json()) as PredictResponse;
	};
}
