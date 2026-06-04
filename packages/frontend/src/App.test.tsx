import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import App from './App';
import type { PredictResponse } from './types';

const oodResponse: PredictResponse = {
	prediction: 123.45,
	ood: true,
	anomaly_score: 0.72,
	warning: 'Warning: I am not sure about this [prediction]!',
};

const inRangeResponse: PredictResponse = {
	prediction: 87.65,
	ood: false,
	anomaly_score: 0,
	warning: null,
};

describe('App', () => {
	it('renders manual inputs and batch CSV controls', () => {
		render(<App onPredict={async () => inRangeResponse} />);

		expect(
			screen.getByRole('heading', { name: /E-commerce CLV Predictor/i }),
		).toBeInTheDocument();
		expect(screen.getByLabelText('Country')).toBeInTheDocument();
		expect(screen.getByLabelText('RecencyDays')).toBeInTheDocument();
		expect(screen.getByLabelText('CSV upload')).toBeInTheDocument();
	});

	it('shows prediction results and the OOD warning banner', async () => {
		const onPredict = vi.fn().mockResolvedValue(oodResponse);
		render(<App onPredict={onPredict} />);

		fireEvent.click(screen.getByRole('button', { name: /Predict CLV/i }));

		await waitFor(() => expect(onPredict).toHaveBeenCalledTimes(1));

		expect(await screen.findByText(/Predicted CLV/i)).toBeInTheDocument();
		expect(screen.getByText('$123.45')).toBeInTheDocument();
		expect(screen.getByRole('alert')).toHaveTextContent(
			'⚠️ Warning: I am not sure about this [prediction]!',
		);
	});

	it('loads a CSV file and displays the number of data rows', async () => {
		render(<App onPredict={async () => inRangeResponse} />);

		const file = new File(
			['Invoice,StockCode,Description\n1,ABC,Sample\n2,DEF,Sample'],
			'customers.csv',
			{ type: 'text/csv' },
		);

		fireEvent.change(screen.getByLabelText('CSV upload'), {
			target: { files: [file] },
		});

		expect(await screen.findByText('CSV rows loaded: 2')).toBeInTheDocument();
	});
});
