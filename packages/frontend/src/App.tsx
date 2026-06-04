import { useMemo, useState, type ChangeEvent, type FormEvent } from 'react';

import { createPredictClient } from './api';
import type { PredictRequest, PredictResponse } from './types';

export type AppProps = {
	onPredict?: (payload: PredictRequest) => Promise<PredictResponse>;
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

function parseCsvRowCount(fileText: string): number {
	const lines = fileText
		.split(/\r?\n/)
		.map((line) => line.trim())
		.filter(Boolean);

	return Math.max(lines.length - 1, 0);
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

export function App({ onPredict }: AppProps) {
	const [formState, setFormState] =
		useState<PredictRequest>(DEFAULT_FORM_STATE);
	const [result, setResult] = useState<PredictResponse | null>(null);
	const [error, setError] = useState<string | null>(null);
	const [csvRows, setCsvRows] = useState<number | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	const predict = useMemo(
		() =>
			onPredict ??
			createPredictClient(
				import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
			),
		[onPredict],
	);

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
			setCsvRows(null);
			return;
		}

		const text = await readFileText(file);
		setCsvRows(parseCsvRowCount(text));
	};

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

					{csvRows !== null ? (
						<p className='muted'>CSV rows loaded: {csvRows}</p>
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
