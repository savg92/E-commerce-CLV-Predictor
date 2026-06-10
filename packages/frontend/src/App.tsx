import { useMemo, useState, type ChangeEvent, type FormEvent } from 'react';

import { createPredictClient } from './api';
import type { PredictRequest, PredictResponse } from './types';

export type AppProps = {
	onPredict?: (payload: PredictRequest) => Promise<PredictResponse>;
	onPredictBatch?: (payload: PredictRequest[]) => Promise<PredictResponse[]>;
};

const DEFAULT_FORM_STATE: PredictRequest = {
	Country: 'UK',
	RecencyDays: 10,
	TenureDays: 100,
	Frequency: 5,
	Monetary: 100,
	AvgBasketValue: 20,
	AvgBasketQuantity: 5,
	UniqueProducts: 10,
	AverageUnitPrice: 2,
};

const FIELD_CONFIG = [
	['Country', 'text'],
	['RecencyDays', 'number'],
	['TenureDays', 'number'],
	['Frequency', 'number'],
	['Monetary', 'number'],
	['AvgBasketValue', 'number'],
	['AvgBasketQuantity', 'number'],
	['UniqueProducts', 'number'],
	['AverageUnitPrice', 'number'],
] as const;

function parseCsv(fileText: string): PredictRequest[] {
	const lines = fileText
		.split(/\r?\n/)
		.map((line) => line.trim())
		.filter(Boolean);

	if (lines.length < 2) return [];

	const headers = lines[0].split(',').map((h) => h.trim());
	const dataLines = lines.slice(1);

	return dataLines.map((line) => {
		const values = line.split(',').map((v) => v.trim());
		const record: any = {};
		headers.forEach((header, index) => {
			const value = values[index];
			if (header === 'Country') {
				record[header] = value;
			} else {
				record[header] = Number(value);
			}
		});
		return record as PredictRequest;
	});
}

function readFileText(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = () => resolve(String(reader.result ?? ''));
		reader.onerror = () =>
			reject(reader.error ?? new Error('Unable to read CSV file'));
		reader.readAsText(file);
	});
}

export function App({ onPredict, onPredictBatch }: AppProps) {
	const [formState, setFormState] =
		useState<PredictRequest>(DEFAULT_FORM_STATE);
	const [result, setResult] = useState<PredictResponse | null>(null);
	const [batchResults, setBatchResults] = useState<PredictResponse[] | null>(
		null,
	);
	const [error, setError] = useState<string | null>(null);
	const [csvData, setCsvData] = useState<PredictRequest[] | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	const client = useMemo(
		() =>
			createPredictClient(
				import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
			),
		[],
	);

	const predict = onPredict ?? client.predict;
	const predictBatch = onPredictBatch ?? client.predictBatch;

	const updateField = (field: keyof PredictRequest, value: string) => {
		setFormState((current) => ({
			...current,
			[field]: field === 'Country' ? value : Number(value),
		}));
	};

	const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		setIsSubmitting(true);
		setError(null);
		setBatchResults(null);

		try {
			const prediction = await predict(formState);
			setResult(prediction);
		} catch (submissionError) {
			setError(
				submissionError instanceof Error
					? submissionError.message
					: 'Prediction failed',
			);
		} finally {
			setIsSubmitting(false);
		}
	};

	const handleCsvUpload = async (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files?.[0];
		if (!file) {
			setCsvData(null);
			return;
		}

		try {
			const text = await readFileText(file);
			const parsed = parseCsv(text);
			setCsvData(parsed);
		} catch (err) {
			setError('Failed to parse CSV file');
		}
	};

	const handleBatchPredict = async () => {
		if (!csvData || csvData.length === 0) return;

		setIsSubmitting(true);
		setError(null);
		setResult(null);

		try {
			const predictions = await predictBatch(csvData);
			setBatchResults(predictions);
		} catch (submissionError) {
			setError(
				submissionError instanceof Error
					? submissionError.message
					: 'Batch prediction failed',
			);
		} finally {
			setIsSubmitting(false);
		}
	};

	const batchStats = useMemo(() => {
		if (!batchResults || batchResults.length === 0) return null;

		const totalClv = batchResults.reduce((acc, r) => acc + r.prediction, 0);
		const oodCount = batchResults.filter((r) => r.ood).length;
		const avgClv = totalClv / batchResults.length;

		return {
			count: batchResults.length,
			avgClv,
			oodCount,
		};
	}, [batchResults]);

	return (
		<main className='dashboard-shell'>
			<section className='hero-card'>
				<p className='eyebrow'>Modern Fintech dashboard</p>
				<h1>E-commerce CLV Predictor</h1>
				<p className='hero-copy'>
					Enter a customer&apos;s RFM profile, preview batch CSV uploads, and
					surface prediction uncertainty clearly when the input drifts outside
					the training distribution.
				</p>
			</section>

			<div className='dashboard-grid'>
				<form
					className='card panel'
					onSubmit={handleSubmit}
				>
					<div className='section-heading'>
						<h2>Manual prediction</h2>
						<p>
							Provide the current RFM feature set for a single customer profile.
						</p>
					</div>

					<div className='field-grid'>
						{FIELD_CONFIG.map(([field, inputType]) => (
							<label
								key={field}
								className='field'
							>
								<span>{field}</span>
								<input
									aria-label={field}
									type={inputType}
									value={formState[field] as string | number}
									onChange={(event) => updateField(field, event.target.value)}
								/>
							</label>
						))}
					</div>

					<button
						className='primary-button'
						type='submit'
						disabled={isSubmitting}
					>
						{isSubmitting ? 'Predicting…' : 'Predict CLV'}
					</button>
				</form>

				<section
					className='card panel'
					aria-label='Batch CSV loader'
				>
					<div className='section-heading'>
						<h2>Batch CSV loader</h2>
						<p>
							Drop in a CSV file to preview the number of customers queued for
							batch prediction.
						</p>
					</div>

					<label
						className='dropzone'
						htmlFor='csv-upload'
					>
						<strong>Drop or select a CSV file</strong>
						<span>Supports the same RFM schema as the manual form.</span>
					</label>
					<input
						id='csv-upload'
						aria-label='CSV upload'
						className='csv-input'
						accept='.csv'
						type='file'
						onChange={handleCsvUpload}
					/>

					{csvData !== null ? (
						<div className='batch-actions'>
							<p className='muted'>CSV rows loaded: {csvData.length}</p>
							<button
								className='primary-button'
								type='button'
								onClick={handleBatchPredict}
								disabled={isSubmitting || csvData.length === 0}
							>
								{isSubmitting ? 'Processing Batch…' : 'Run Batch Prediction'}
							</button>
						</div>
					) : (
						<p className='muted'>No CSV uploaded yet.</p>
					)}
				</section>
			</div>

			<section
				className='card panel result-panel'
				aria-label='Prediction results'
			>
				<div className='section-heading'>
					<h2>Prediction summary</h2>
					<p>Review the model output, anomaly score, and safety message.</p>
				</div>

				{error ? (
					<div
						className='error-banner'
						role='alert'
					>
						{error}
					</div>
				) : null}

				{result ? (
					<>
						<div className='result-grid'>
							<div>
								<span className='result-label'>Predicted CLV</span>
								<strong className='result-value'>
									${result.prediction.toFixed(2)}
								</strong>
							</div>
							<div>
								<span className='result-label'>OOD score</span>
								<strong className='result-value'>
									{result.anomaly_score.toFixed(3)}
								</strong>
							</div>
						</div>

						{result.warning ? (
							<div
								className='warning-banner'
								role='alert'
							>
								⚠️ {result.warning}
							</div>
						) : (
							<p className='muted'>Prediction is within the training range.</p>
						)}
					</>
				) : batchStats ? (
					<div className='batch-results'>
						<div className='result-grid'>
							<div>
								<span className='result-label'>Batch Size</span>
								<strong className='result-value'>{batchStats.count}</strong>
							</div>
							<div>
								<span className='result-label'>Avg Predicted CLV</span>
								<strong className='result-value'>
									${batchStats.avgClv.toFixed(2)}
								</strong>
							</div>
							<div>
								<span className='result-label'>OOD Alerts</span>
								<strong className='result-value'>{batchStats.oodCount}</strong>
							</div>
						</div>
						{batchStats.oodCount > 0 && (
							<div
								className='warning-banner'
								role='alert'
							>
								⚠️ Warning: {batchStats.oodCount} customers in this batch
								triggered OOD alerts!
							</div>
						)}
					</div>
				) : (
					<p className='muted'>
						Run a prediction to see the model output and uncertainty banner.
					</p>
				)}
			</section>
		</main>
	);
}

export default App;
