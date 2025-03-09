# FastAPI NumPy and SciPy Calculation Server

A public API server built with FastAPI that enables numerical calculations and statistical analyses using NumPy and SciPy.

## API Services

### numpy Service (`service: "numpy_llm"`)
- **Basic Operations:**
  - `sum`: Sum of array elements
  - `mean`: Arithmetic mean
  - `std`: Standard deviation
  - `min`: Minimum value
  - `max`: Maximum value
  - `median`: Median value
  - `prod`: Product of array elements
  - `var`: Variance
  
- **Array Operations:**
  - `cumsum`: Cumulative sum
  - `cumprod`: Cumulative product
  - `diff`: Calculate discrete difference
  
- **Mathematical Functions:**
  - `abs`: Absolute value
  - `sqrt`: Square root
  - `log`: Natural logarithm
  - `log10`: Base-10 logarithm
  - `exp`: Exponential
  - `square`: Square each element
  
- **Rounding:**
  - `floor`: Floor of each element
  - `ceil`: Ceiling of each element
  - `round`: Round to given decimals

- **Trigonometric:**
  - `sin`: Sine
  - `cos`: Cosine
  - `tan`: Tangent
  - `arcsin`: Inverse sine
  - `arccos`: Inverse cosine
  - `arctan`: Inverse tangent

### scipy Service (`service: "scipy_llm"`)
- **Distribution Tests:**
  - `normaltest`: Test for normal distribution
  - `shapiro`: Shapiro-Wilk test
  - `anderson`: Anderson-Darling test
  
- **Parametric Tests:**
  - `ttest_1samp`: One-sample t-test
  - `ttest_ind`: Independent two-sample t-test
  - `ttest_rel`: Paired t-test
  - `f_oneway`: One-way ANOVA
  
- **Non-parametric Tests:**
  - `mannwhitneyu`: Mann-Whitney U test
  - `kruskal`: Kruskal-Wallis H-test
  - `wilcoxon`: Wilcoxon signed-rank test
  
- **Correlation Analysis:**
  - `pearsonr`: Pearson correlation coefficient
  - `spearmanr`: Spearman rank correlation
  
- **Other Tests:**
  - `chisquare`: Chi-square test
  - `fisher_exact`: Fisher exact test
  - `levene`: Levene test for variance equality
  - `ks_2samp`: Two-sample Kolmogorov-Smirnov test
  
- **Descriptive Statistics:**
  - `describe`: Summary statistics
  - `zscore`: Z-score standardization
  - `skew`: Sample skewness
  - `kurtosis`: Sample kurtosis

## API Usage

### Request Format
```json
{
    "service": "calculator | statistics",
    "calculation": "operation_name",
    "data": [1, 2, 3, 4, 5]
}
```

### Example Requests

```bash
# Calculate mean
curl -X POST "https://www.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{"service":"calculator","calculation":"mean","data":[1,2,3,4,5]}'

# Perform t-test
curl -X POST "https://www.statsforllm.com/calculate" \
     -H "Content-Type: application/json" \
     -d '{"service":"statistics","calculation":"ttest_1samp","data":[1,2,3,4,5]}'
```

## Limits and Security
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

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License
MIT License - feel free to use in your projects

## Contributing
Contributions welcome! Please feel free to submit a Pull Request.