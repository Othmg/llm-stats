# FastAPI NumPy and SciPy Calculation Server

A public API server that enables numerical calculations and statistical analyses using NumPy and SciPy functions.

## API Usage

### Request Format
```json
{
    "service": "calculator | statistics",
    "calculation": "operation_name",
    "data": [1, 2, 3, 4, 5],
    "params": {
        "param1": value1,
        "param2": value2
    }
}
```

### Parameters
- The `params` field accepts any parameters that the underlying NumPy/SciPy functions require
- Refer to the official documentation for specific parameter requirements:
  - NumPy functions: [NumPy Documentation](https://numpy.org/doc/stable/reference/index.html)
  - SciPy statistics: [SciPy Stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

### Examples

1. Simple calculation (no parameters):
```bash
curl -X POST "https://www.api.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{
           "service": "calculator",
           "calculation": "mean",
           "data": [1, 2, 3, 4, 5]
         }'
```

2. Calculation with parameters (rounding to 2 decimals):
```bash
curl -X POST "https://www.api.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{
           "service": "calculator",
           "calculation": "round",
           "data": [1.2345, 2.5678],
           "params": {"decimals": 2}
         }'
```

3. Statistical test with parameters:
```bash
curl -X POST "https://www.api.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{
           "service": "statistics",
           "calculation": "ttest_1samp",
           "data": [1, 2, 3, 4, 5],
           "params": {"popmean": 0}
         }'
```

## Supported Functions

### Calculator Service (`service: "numpy_llm"`)
Basic statistical operations:
- `sum`, `mean`, `std`, `min`, `max`, `median`, `prod`, `var`
- Common parameters: `axis`, `dtype`, `keepdims`

Array operations:
- `cumsum`, `cumprod`, `diff`
- Common parameters: `n` (for diff)

Mathematical functions:
- `abs`, `sqrt`, `log`, `log10`, `exp`, `square`
- Common parameters: `out`, `where`

Rounding:
- `floor`, `ceil`, `round`
- Common parameters: `decimals` (for round)

Trigonometric:
- `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`

### Statistics Service (`service: "statistics"`)

#### Descriptive Statistics
- `describe` - Compute several descriptive statistics
- `skew` - Sample skewness
- `kurtosis` - Sample kurtosis
- `moment` - Calculate the nth moment about the mean
- `zscore` - Calculate the z-score of each value in the sample

#### Distribution Tests
- `normaltest` - Test for normal distribution (D'Agostino and Pearson's test)
- `shapiro` - Shapiro-Wilk test for normality
- `anderson` - Anderson-Darling test for data coming from a particular distribution
- `kstest` - Kolmogorov-Smirnov test for goodness of fit
- `jarque_bera` - Jarque-Bera goodness of fit test

#### Parametric Tests
- `ttest_1samp` - Calculate the T-test for the mean of ONE group of scores
  - params: `popmean` (float), `alternative` ('two-sided', 'less', 'greater')
- `ttest_ind` - Calculate the T-test for the means of two independent samples
  - params: `equal_var` (bool), `alternative` (str)
- `ttest_rel` - Calculate the T-test on TWO RELATED samples of scores
  - params: `alternative` (str)
- `f_oneway` - Perform one-way ANOVA
- `pearsonr` - Calculate Pearson correlation coefficient
  - params: `alternative` (str)

#### Non-parametric Tests
- `mannwhitneyu` - Mann-Whitney U test
  - params: `alternative` (str), `method` ('auto', 'asymptotic', 'exact')
- `wilcoxon` - Calculate the Wilcoxon signed-rank test
  - params: `alternative` (str), `correction` (bool)
- `kruskal` - Kruskal-Wallis H-test
- `friedmanchisquare` - Friedman test for repeated measurements
- `ranksums` - Wilcoxon rank-sum test
- `spearmanr` - Calculate Spearman correlation coefficient
  - params: `alternative` (str), `nan_policy` ('propagate', 'raise', 'omit')

#### Contingency Table Tests
- `chi2_contingency` - Chi-square test of independence
  - params: `correction` (bool), `lambda_` (float)
- `fisher_exact` - Fisher exact test on a 2x2 contingency table
  - params: `alternative` ('two-sided', 'less', 'greater')
- `barnard_exact` - Barnard's exact test on a 2x2 contingency table
- `boschloo_exact` - Boschloo's exact test on a 2x2 contingency table

#### Variance Tests
- `levene` - Levene test for equal variances
  - params: `center` ('mean', 'median', 'trimmed'), `proportiontocut` (float)
- `bartlett` - Bartlett's test for equal variances
- `fligner` - Fligner-Killeen test for equality of variances

#### Effect Size
- `pointbiserialr` - Calculate point biserial correlation coefficient
- `kendalltau` - Calculate Kendall's tau
  - params: `alternative` (str), `method` ('auto', 'asymptotic', 'exact')
- `linregress` - Calculate linear regression
  - params: `alternative` (str)

Common Parameters Across Many Functions:
- `alternative`: 'two-sided' (default), 'less', 'greater'
- `nan_policy`: 'propagate', 'raise', 'omit'
- `axis`: Integer or None (default)

For detailed parameter descriptions and return values, refer to the [SciPy Stats Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

Example using advanced parameters:
```bash
curl -X POST "https://www.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{
           "service": "statistics",
           "calculation": "spearmanr",
           "data": [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
           "params": {
             "alternative": "greater",
             "nan_policy": "omit"
           }
         }'
```

## Security and Limits
- Rate limit: 10 requests per minute per IP
- Maximum array size: 10,000 elements
- Maximum number size: within float64 range
- Timeout: 5 seconds per calculation
- Memory limit: 500MB per request

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llmNum.git
cd llmNum
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn api.main:app --reload
```

## Development

### Running Tests
```bash
pytest tests/
```

### Local Development
The API will be available at `http://localhost:8000`


## License
MIT License - feel free to use in your projects

## Contributing
Contributions welcome! Please feel free to submit a Pull Request.