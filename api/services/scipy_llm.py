from typing import List, Any, Union
import numpy as np
from scipy import stats
from api.services.base_service import BaseService


class StatisticsService(BaseService):
    ALLOWED_FUNCTIONS = {
        # Basic statistics
        "skew": stats.skew,
        "kurtosis": stats.kurtosis,
        "mode": stats.mode,
        "percentile": np.percentile,
        "zscore": stats.zscore,
        "describe": stats.describe,
        # Normality tests
        "normaltest": stats.normaltest,
        "shapiro": stats.shapiro,
        "anderson": stats.anderson,
        # Parametric tests
        "ttest_1samp": lambda a, popmean: stats.ttest_1samp(a, popmean=popmean),
        "ttest_ind": lambda a, b: stats.ttest_ind(a, b),
        "f_oneway": stats.f_oneway,
        "levene": stats.levene,
        # Non-parametric tests
        "mannwhitneyu": lambda x, y: stats.mannwhitneyu(x, y),
        "kruskal": stats.kruskal,
        "wilcoxon": stats.wilcoxon,
        # Correlation tests
        "pearsonr": lambda a, b: stats.pearsonr(a, b),
        "spearmanr": lambda a, b: stats.spearmanr(a, b),
        # Categorical tests
        "chi2_contingency": lambda table: stats.chi2_contingency(table),
        "fisher_exact": lambda table: stats.fisher_exact(table),
        # Regression
        "linregress": lambda x, y: stats.linregress(x, y)._asdict(),
        # Distribution tests
        "ks_2samp": lambda a, b: stats.ks_2samp(a, b),
    }

    # Special cases that require specific parameter handling
    SPECIAL_CASES = {
        "multi_sample": ["f_oneway", "kruskal"],
        "two_sample": [
            "ttest_ind",
            "mannwhitneyu",
            "ks_2samp",
            "pearsonr",
            "spearmanr",
        ],
        "contingency": ["chi2_contingency", "fisher_exact"],
        "regression": ["linregress"],
    }

    @classmethod
    def _handle_special_calculation(cls, calculation: str, data: dict):
        if calculation in cls.SPECIAL_CASES["regression"]:
            return cls.ALLOWED_FUNCTIONS[calculation](data.get("x"), data.get("y"))

        elif calculation in cls.SPECIAL_CASES["two_sample"]:
            return cls.ALLOWED_FUNCTIONS[calculation](data.get("a"), data.get("b"))

        elif calculation in cls.SPECIAL_CASES["multi_sample"]:
            # Handle multiple samples for ANOVA and Kruskal-Wallis
            samples = [data.get(f"sample_{i}") for i in range(len(data))]
            return cls.ALLOWED_FUNCTIONS[calculation](*samples)

        elif calculation in cls.SPECIAL_CASES["contingency"]:
            # Handle contingency table input
            table = np.array(data.get("table"))
            return cls.ALLOWED_FUNCTIONS[calculation](table)

        raise ValueError(f"Unhandled special case for calculation: {calculation}")

    @classmethod
    def perform_calculation(cls, calculation: str, data: List[Any], **params):
        # Convert data to numpy array
        array = np.array(data)

        # Get the scipy stats function
        func = getattr(stats, calculation)

        # Call function with data and any additional params
        result = func(array, **params)

        # Handle tuple returns (many scipy functions return multiple values)
        if hasattr(result, "_fields"):  # Named tuple
            return {field: getattr(result, field) for field in result._fields}
        elif isinstance(result, tuple):
            return list(result)
        return result

    @classmethod
    def _convert_result(cls, result):
        if isinstance(result, np.generic):
            return result.item()
        elif isinstance(result, np.ndarray):
            return result.tolist()
        elif isinstance(result, tuple):
            return list(result)
        return result
