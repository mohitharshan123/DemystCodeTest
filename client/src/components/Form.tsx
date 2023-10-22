import React, { ChangeEvent, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { fetchBalanceSheet } from '../apis';
import BalanceSheet from './BalanceSheet';
import { applyForLoan } from '../apis';

export type BalanceSheetFormData = {
    business_name: string,
    year_established: number,
    loan_amount: number,
    provider_name: "Xero" | "MYOB"
}

export type BalanceSheetResponseData = {
    business_name: string,
    year_established: number,
    loan_amount: number,
    provider_name: "Xero" | "MYOB"
}

const Form = () => {
    const [formData, setFormData] = useState<BalanceSheetFormData>({
        business_name: '',
        year_established: 2016,
        loan_amount: 0,
        provider_name: "Xero"
    });

    const { data: balanceSheetData, mutateAsync: retrieveBalanceSheet, isSuccess, reset: resetBalanceSheet } = useMutation({ mutationFn: fetchBalanceSheet })
    const { data: loanApplicationResponse, mutateAsync: apply, reset: resetLoanStatus } = useMutation({ mutationFn: applyForLoan })

    const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isSuccess) {
            await apply(formData);
            resetBalanceSheet();
        } else {
            await retrieveBalanceSheet(formData);
            resetLoanStatus();
        }
    };

    return (
        <div className='flex flex-col space-y-4'>
            {loanApplicationResponse?.data &&
                <div className={`bg-${loanApplicationResponse?.data?.status === "Approved" ? "green-400" : "red-400"}`}>
                    {loanApplicationResponse?.data?.status}
                </div>
            }
            <form className="w-full max-w-sm mx-auto mt-6 p-4 bg-white rounded shadow-lg" onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">
                        Business Name:
                    </label>
                    <input
                        type="text"
                        name="business_name"
                        value={formData.business_name}
                        onChange={handleInputChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="year" className="block text-gray-700 text-sm font-bold mb-2">
                        Year established:
                    </label>
                    <input
                        type="number"
                        id="year"
                        name="year_established"
                        min="1900"
                        max="2099"
                        step="1"
                        value={formData.year_established}
                        onChange={handleInputChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="loanAmount" className="block text-gray-700 text-sm font-bold mb-2">
                        Loan amount:
                    </label>
                    <input
                        type="text"
                        name="loan_amount"
                        value={formData.loan_amount}
                        onChange={handleInputChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="provider" className="block text-gray-700 text-sm font-bold mb-2">
                        Accounting Provider:
                    </label>
                    <select
                        name="provider_name"
                        value={formData.provider_name}
                        onChange={handleInputChange}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    >
                        <option value="Xero">Xero</option>
                        <option value="MYOB">MYOB</option>
                    </select>
                </div>

                <div className="text-center">
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        {isSuccess ? "Apply" : "Fetch balance sheet"}
                    </button>
                </div>
            </form>
            {balanceSheetData?.data?.balance_sheet?.length && <BalanceSheet balanceSheet={balanceSheetData.data?.balance_sheet} />}
        </div>
    );
};

export default Form;
