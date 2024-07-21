import React, { useState, useEffect } from 'react';

// Validation function to check input values
export const validateInput = (amount, interestRate, term) => {
    const errors = {};

    if (!amount || parseFloat(amount) <= 0) {
        errors.amount = 'Loan amount must be a positive number';
    }
    if (interestRate === '' || parseFloat(interestRate) < 0) {
        errors.interestRate = 'Interest rate must be 0 or a positive number';
    }
    if (!term || parseInt(term) <= 0 || !Number.isInteger(parseFloat(term))) {
        errors.term = 'Loan term must be a positive integer';
    }

    return errors;
};

const LoanCalculator = () => {
    // State variables for loan amount, interest rate, loan term, monthly payment, errors, and language
    const [amount, setAmount] = useState('');
    const [interestRate, setInterestRate] = useState('');
    const [term, setTerm] = useState('');
    const [monthlyPayment, setMonthlyPayment] = useState(null);
    const [errors, setErrors] = useState({});
    const [language, setLanguage] = useState('de');

    // Set default language to German on component mount
    useEffect(() => {
        setLanguage('de');
    }, []);

    // Function to convert input based on language
    const convertInput = (value) => {
        if (language === 'de') {
            return value.replace(',', '.');
        }
        return value;
    };

    // Function to handle input changes for amount and interest rate
    const handleAmountChange = (e) => {
        const value = e.target.value;
        setAmount(value);
    };

    const handleInterestRateChange = (e) => {
        const value = e.target.value;
        setInterestRate(value);
    };

    // Function to calculate monthly payment
    const calculatePayment = (e) => {
        e.preventDefault();

        // Convert inputs based on language
        const convertedAmount = convertInput(amount);
        const convertedInterestRate = convertInput(interestRate);

        // Validate input values
        const errors = validateInput(convertedAmount, convertedInterestRate, term);
        if (Object.keys(errors).length > 0) {
            setErrors(errors);
            return;
        }

        setErrors({});

        // Calculate monthly payment
        const principal = parseFloat(convertedAmount);
        const interest = parseFloat(convertedInterestRate) / 100 / 12;
        const payments = parseFloat(term);

        let monthly;
        if (interest === 0) {
            monthly = principal / payments;
        } else {
            const x = Math.pow(1 + interest, payments);
            monthly = (principal * x * interest) / (x - 1);
        }

        // Format the monthly payment based on the current language
        const formattedMonthly = new Intl.NumberFormat(language === 'de' ? 'de-DE' : 'en-US', {
            style: 'currency',
            currency: 'EUR'
        }).format(monthly);

        setMonthlyPayment(formattedMonthly);
    };

    // Labels for English and German languages
    const labels = {
        de: {
            title: 'Darlehensrechner',
            amount: 'Darlehensbetrag (€):',
            interestRate: 'Jahreszinssatz (%):',
            term: 'Laufzeit (Monate):',
            calculate: 'Berechnen',
            monthlyPayment: 'Monatliche Zahlung: ',
            errors: {
                amount: 'Der Darlehensbetrag muss eine positive Zahl sein',
                interestRate: 'Der Zinssatz muss 0 oder eine positive Zahl sein',
                term: 'Die Laufzeit muss eine positive Ganzzahl sein',
            },
        },
        en: {
            title: 'Loan Calculator',
            amount: 'Loan Amount (€):',
            interestRate: 'Annual Interest Rate (%):',
            term: 'Loan Term (months):',
            calculate: 'Calculate',
            monthlyPayment: 'Monthly Payment: ',
            errors: {
                amount: 'Loan amount must be a positive number',
                interestRate: 'Interest rate must be 0 or a positive number',
                term: 'Loan term must be a positive integer',
            },
        },
    };

    // Function to toggle the language between English and German
    const toggleLanguage = () => {
        setLanguage((prevLanguage) => (prevLanguage === 'de' ? 'en' : 'de'));
    };

    return (
        <div>
            <h1>{labels[language].title}</h1>
            <button className="language-toggle" onClick={toggleLanguage}>
                {language === 'de' ? 'Switch to English' : 'Auf Deutsch wechseln'}
            </button>
            <form onSubmit={calculatePayment}>
                <div>
                    <label>
                        {labels[language].amount}
                        <input
                            type="text"
                            value={amount}
                            onChange={handleAmountChange}
                            placeholder={language === 'de' ? '1.000,00' : '1000.00'}
                            required
                        />
                    </label>
                    {errors.amount && <p style={{ color: 'red' }}>{labels[language].errors.amount}</p>}
                </div>
                <div>
                    <label>
                        {labels[language].interestRate}
                        <input
                            type="text"
                            value={interestRate}
                            onChange={handleInterestRateChange}
                            placeholder={language === 'de' ? '5,00' : '5.00'}
                            required
                        />
                    </label>
                    {errors.interestRate && <p style={{ color: 'red' }}>{labels[language].errors.interestRate}</p>}
                </div>
                <div>
                    <label>
                        {labels[language].term}
                        <input
                            type="number"
                            value={term}
                            onChange={(e) => setTerm(e.target.value)}
                            required
                        />
                    </label>
                    {errors.term && <p style={{ color: 'red' }}>{labels[language].errors.term}</p>}
                </div>
                <button type="submit">{labels[language].calculate}</button>
            </form>
            {monthlyPayment !== null && (
                <div>
                    <h2>{labels[language].monthlyPayment}{monthlyPayment}</h2>
                </div>
            )}
        </div>
    );
};

export default LoanCalculator;
