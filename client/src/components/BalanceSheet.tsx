import React from "react";

export type BalanceSheet = Array<{ year: number, month: number, profit_or_loss: number, assets_value: number }>

const BalanceSheet: React.FC<{ balanceSheet: BalanceSheet }> = ({ balanceSheet }) => (
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
    {balanceSheet.map(sheet => (
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="font-bold text-xl mb-2">{sheet.year}</div>
        <div className="text-sm mb-2">
          <p>Month: {sheet.month}</p>
          <p>Profit/Loss: Rs: {sheet.profit_or_loss.toFixed(2)}</p>
          <p>Assets Value: Rs: {sheet.assets_value.toFixed(2)}</p>
        </div>
      </div>
    ))}
  </div>
);

export default BalanceSheet;
