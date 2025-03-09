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

### Calculator Service (`service: "calculator"`)
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
Distribution tests:
- `normaltest`, `shapiro`, `anderson`

Parametric tests:
- `ttest_1samp` (params: `popmean`)
- `ttest_ind` (params: `equal_var`, `alternative`)
- `ttest_rel`

Non-parametric tests:
- `mannwhitneyu` (params: `alternative`, `method`)
- `wilcoxon` (params: `alternative`, `correction`)
- `kruskal`

Correlation:
- `pearsonr`
- `spearmanr` (params: `alternative`, `nan_policy`)

Other:
- `chisquare` (params: `f_exp`, `ddof`)
- `levene` (params: `center`, `proportiontocut`)

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

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License
MIT License - feel free to use in your projects

## Contributing
Contributions welcome! Please feel free to submit a Pull Request.