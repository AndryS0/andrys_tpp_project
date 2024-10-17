// src/components/Calculator.tsx
import React, { useState } from 'react';
import axios, {AxiosError} from 'axios';

interface ApiResponse {
    answer: number;
}

const backendUrl = 'http://127.0.0.1:8888'; // Update with actual backend URL
const xApiToken = "1234"

const Calculator: React.FC = () => {
    const [expression, setExpression] = useState<string>('');
    const [result, setResult] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null); // Reset previous errors

        try {
            const response = await axios.get<ApiResponse>(
                `${backendUrl}/api/v1/calc?expression=${encodeURIComponent(expression)}`,
                {headers: {'x-api-token': xApiToken}}
            );
            setResult(response.data.answer);
        } catch (err) {
            if (err instanceof AxiosError) {
                setError(`Failed to calculate expression: ${err?.response?.data?.detail}. Please try again.`);
            } else {
                setError("Failed to calculate expression. Please, try another one.")
            }
        }
    };

    return (
        <div className="calculator-container">
            <h1>Fancy Calculator</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={expression}
                    onChange={(e) => setExpression(e.target.value)}
                    placeholder="Enter expression (e.g., 2 + 2)"
                    className="calculator-input"
                />
                <button type="submit" className="calculator-button">Calculate</button>
            </form>

            {result !== null && <div className="calculator-result">Result: {result}</div>}
            {error && <div className="calculator-error">{error}</div>}
        </div>
    );
};

export default Calculator;
