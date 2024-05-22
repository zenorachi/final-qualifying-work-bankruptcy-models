# Final qualifying work | Predicting bankruptcy

## Project Description

This project aims to predict bankruptcy of a company using financial ratios and machine learning models. The project uses the public API of the Federal Tax Service of Russia to obtain financial reports of a company based on its INN (Taxpayer Identification Number). The financial ratios are then calculated using the obtained financial reports. Finally, three different models are used to predict the bankruptcy of the company:
1. Altman's Two-Factor Model
2. Altman's Four-Factor Model
3. Modified Altman's Model
4. Fulmer's Model

### Altman's Two-Factor Model
The Altman's Two-Factor Model uses two financial ratios to predict the bankruptcy of a company: working capital/total assets and retained earnings/total assets. To calculate the financial ratios, a CSV file needs to be filled with the liquidity coefficients of the company. The CSV file is located in the repository and needs to be updated with the latest liquidity coefficients of the company.
> **Hint**: The two-factor Altman Z-score model requires filling out a CSV file that contains a company's liquidity ratios. This file is located in the project repository and should be updated with the latest liquidity ratios of the company.

### Altman's Four-Factor Model
The Altman's Four-Factor Model uses four financial ratios to predict the bankruptcy of a company: working capital/total assets, retained earnings/total assets, earnings before interest and taxes/total assets, and market value of equity/book value of total liabilities. The financial ratios are calculated using the obtained financial reports.

### Modified Altman's Model
The Modified Altman's Model uses three financial ratios to predict the bankruptcy of a company: working capital/total assets, retained earnings/total assets, and earnings before interest and taxes/total assets. The financial ratios are calculated using the obtained financial reports.

### Fulmer's Model
Fulmer's Model uses a combination of financial ratios and non-financial variables to predict the bankruptcy of a company. The financial ratios are calculated using the obtained financial reports, while the non-financial variables are obtained from other sources.

## Conclusion
Overall, this project provides a comprehensive analysis of the financial health of a company and helps in predicting its bankruptcy using different machine learning models.
