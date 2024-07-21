import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoanCalculator, { validateInput } from './LoanCalculator';

// Helper function to set input values
const setInputValue = (label, value) => {
  const input = screen.getByLabelText(label);
  fireEvent.change(input, { target: { value } });
};

// Helper function to match text content with potential broken elements
const matchTextContent = (content, text) => {
  return content.includes(text);
};

test('validates loan amount', () => {
  render(<LoanCalculator />);
  setInputValue('Darlehensbetrag (€):', '-1000');
  fireEvent.click(screen.getByText('Berechnen'));
  expect(screen.getByText('Der Darlehensbetrag muss eine positive Zahl sein')).toBeInTheDocument();
});

test('validates interest rate', () => {
  render(<LoanCalculator />);
  setInputValue('Jahreszinssatz (%):', '-5');
  fireEvent.click(screen.getByText('Berechnen'));
  expect(screen.getByText('Der Zinssatz muss 0 oder eine positive Zahl sein')).toBeInTheDocument();
});

test('validates loan term', () => {
  render(<LoanCalculator />);
  setInputValue('Laufzeit (Monate):', '0');
  fireEvent.click(screen.getByText('Berechnen'));
  expect(screen.getByText('Die Laufzeit muss eine positive Ganzzahl sein')).toBeInTheDocument();
});

test('calculates monthly payment correctly in German', () => {
  render(<LoanCalculator />);
  setInputValue('Darlehensbetrag (€):', '10000,00');
  setInputValue('Jahreszinssatz (%):', '5,00');
  setInputValue('Laufzeit (Monate):', '60');
  fireEvent.click(screen.getByText('Berechnen'));
  expect(screen.getByText((content, element) => matchTextContent(content, 'Monatliche Zahlung:') && matchTextContent(content, '188,71 €'))).toBeInTheDocument();
});

test('calculates monthly payment correctly with zero interest in German', () => {
  render(<LoanCalculator />);
  setInputValue('Darlehensbetrag (€):', '12000,00');
  setInputValue('Jahreszinssatz (%):', '0,00');
  setInputValue('Laufzeit (Monate):', '24');
  fireEvent.click(screen.getByText('Berechnen'));
  expect(screen.getByText((content, element) => matchTextContent(content, 'Monatliche Zahlung:') && matchTextContent(content, '500,00 €'))).toBeInTheDocument();
});

test('toggles between German and English and calculates correctly in English', () => {
  render(<LoanCalculator />);

  // Check initial labels and button text in German
  expect(screen.getByText('Darlehensrechner')).toBeInTheDocument();
  expect(screen.getByText('Darlehensbetrag (€):')).toBeInTheDocument();
  expect(screen.getByText('Jahreszinssatz (%):')).toBeInTheDocument();
  expect(screen.getByText('Laufzeit (Monate):')).toBeInTheDocument();
  expect(screen.getByText('Berechnen')).toBeInTheDocument();
  expect(screen.getByText('Switch to English')).toBeInTheDocument();

  // Switch to English
  fireEvent.click(screen.getByText('Switch to English'));

  // Check labels and button text in English
  expect(screen.getByText('Loan Calculator')).toBeInTheDocument();
  expect(screen.getByText('Loan Amount (€):')).toBeInTheDocument();
  expect(screen.getByText('Annual Interest Rate (%):')).toBeInTheDocument();
  expect(screen.getByText('Loan Term (months):')).toBeInTheDocument();
  expect(screen.getByText('Calculate')).toBeInTheDocument();
  expect(screen.getByText('Auf Deutsch wechseln')).toBeInTheDocument();

  // Enter values and calculate in English
  setInputValue('Loan Amount (€):', '10000.00');
  setInputValue('Annual Interest Rate (%):', '5.00');
  setInputValue('Loan Term (months):', '60');
  fireEvent.click(screen.getByText('Calculate'));
  expect(screen.getByText((content, element) => matchTextContent(content, 'Monthly Payment:') && matchTextContent(content, '€188.71'))).toBeInTheDocument();

  // Switch back to German and check initial labels and button text in German again
  fireEvent.click(screen.getByText('Auf Deutsch wechseln'));
  expect(screen.getByText('Darlehensrechner')).toBeInTheDocument();
  expect(screen.getByText('Darlehensbetrag (€):')).toBeInTheDocument();
  expect(screen.getByText('Jahreszinssatz (%):')).toBeInTheDocument();
  expect(screen.getByText('Laufzeit (Monate):')).toBeInTheDocument();
  expect(screen.getByText('Berechnen')).toBeInTheDocument();
  expect(screen.getByText('Switch to English')).toBeInTheDocument();
});

test('validation function works correctly', () => {
  expect(validateInput('-1000', '5', '60')).toEqual({
    amount: 'Loan amount must be a positive number',
  });
  expect(validateInput('1000', '-5', '60')).toEqual({
    interestRate: 'Interest rate must be 0 or a positive number',
  });
  expect(validateInput('1000', '5', '0')).toEqual({
    term: 'Loan term must be a positive integer',
  });
  expect(validateInput('1000', '5', '60')).toEqual({});
});
