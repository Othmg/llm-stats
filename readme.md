# FastAPI NumPy and SciPy Calculation Server

This project is an open-source API server built with FastAPI that allows LLM assistants and other clients to perform numerical calculations using NumPy functions as well as advanced statistical analyses using SciPy functions.

## Features

### NumPy Calculation Endpoint

- **Calculation Endpoint:** Provides a `/calculate` endpoint to perform numerical computations.
- **Supported Operations:**
  - **Basic operations:** `sum`, `mean`, `std`, `min`, `max`, `median`
  - **Advanced operations:** `prod`, `var`, `cumsum`, `cumprod`, `diff`, `abs`, `sqrt`, `log`, `log10`, `exp`, `floor`, `ceil`, `round`
  - **Trigonometric operations:** `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`, `square`
- **Error Handling:** Returns appropriate error messages if the requested calculation is unsupported or if the data is in an invalid format.

### SciPy Statistics Endpoint

- **Statistics Endpoint:** A dedicated `/calculate` endpoint (in a separate module) for statistical analysis.
- **Supported Statistical Operations:**
  - **Regression Analysis:** `linregress`
  - **T-tests:** `ttest_1samp`, `ttest_ind`, `ttest_rel`
  - **Correlation Tests:** `pearsonr`, `spearmanr`
  - **Chi-square Test:** `chisquare`
  - **ANOVA:** `f_oneway`
  - **Non-parametric Tests:** `mannwhitneyu`, `kruskal`, `wilcoxon`
  - **Variance Test:** `levene`
  - **Normality Tests:** `normaltest`, `shapiro`, `anderson`
  - **Other Statistical Tests:** `ks_2samp`, `fisher_exact`, `chi2_contingency`
  - **Descriptive Statistics:** `zscore`, `skew`, `kurtosis`, `describe`
- **Functionality:** Accepts a JSON payload with the specific statistical operation and the required data, then returns the analysis results in a JSON-friendly format.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Othmg/llm-stats.git
   cd your-repo-name