# Quick Reference: BM25 vs LTR Evaluation

## TL;DR - Get Started in 30 Seconds

```python
from ltr.search import batch_evaluate

# Your test cases
test_cases = [
    {'query': 'batman', 'ground_truth': 'Batman Begins'},
    {'query': 'rambo', 'ground_truth': 'First Blood'},
    {'query': 'matrix', 'ground_truth': 'The Matrix'},
]

# Run evaluation
results, metrics = batch_evaluate(
    client, 
    test_cases,
    model_name='my_model_v2',
    verbose=True
)

# Check results
print(f"BM25 Accuracy: {metrics['bm25_accuracy']:.2%}")
print(f"LTR Accuracy: {metrics['ltr_accuracy']:.2%}")
print(f"Improvement: {metrics['percentage_improvement']:+.2f}%")
```

## Available Functions

### Query Building
```python
from ltr.search import esBm25Query, esLtrQuery

# BM25 baseline search
bm25_query = esBm25Query('batman', fields=['title', 'overview'], size=10)
results = client.query('tmdb', bm25_query)

# LTR rescoring search
ltr_query = esLtrQuery('batman', 'my_model_v2', featureset='my_feature_set', size=10)
results = client.query('tmdb', ltr_query)
```

### Evaluation
```python
from ltr.search import (
    batch_evaluate,           # Batch test multiple queries
    compare_results,          # Compare single query
    evaluate_accuracy,        # Get metrics from results
    normalize_title,          # Normalize titles for comparison
    get_top_result            # Extract top result from results
)

# Batch - RECOMMENDED
results, metrics = batch_evaluate(client, test_cases, model_name='my_model_v2')

# Single comparison
comparison = compare_results('batman', 'Batman Begins', 
                           bm25_results, ltr_results, verbose=True)

# Manual evaluation
metrics = evaluate_accuracy(comparison_results, verbose=True)
```

## Metrics You Get

| Output | Meaning | Example |
|--------|---------|---------|
| `bm25_accuracy` | % correct for BM25 | 0.40 (40%) |
| `ltr_accuracy` | % correct for LTR | 0.80 (80%) |
| `absolute_improvement` | # additional correct | 4 |
| `percentage_improvement` | % improvement over BM25 | 100.0 |
| `improvements_count` | # queries where LTR beat BM25 | 4 |

## Common Tasks

### Compare Two Models
```python
for model in ['my_model_v1', 'my_model_v2']:
    results, metrics = batch_evaluate(client, test_cases, model_name=model)
    print(f"{model}: {metrics['ltr_accuracy']:.2%}")
```

### Analyze Failed Cases
```python
failures = [r for r in results if not r['ltr_correct']]
for f in failures:
    print(f"Query: {f['query']}")
    print(f"  Expected: {f['ground_truth']}")
    print(f"  Got: {f['ltr_title']}")
```

### Create Comparison Table
```python
import pandas as pd

df = pd.DataFrame([
    {
        'Query': r['query'],
        'Ground Truth': r['ground_truth'],
        'BM25': r['bm25_title'],
        'BM25 ✓': '✓' if r['bm25_correct'] else '✗',
        'LTR': r['ltr_title'],
        'LTR ✓': '✓' if r['ltr_correct'] else '✗',
        'Improved': '✓' if r['improvement'] else '',
    }
    for r in results
])
```

## Important Notes

⚠️ **LTR Works in Two Stages**
1. Stage 1: BM25 retrieval (initial filtering)
2. Stage 2: LTR rescoring (reranking top results)

⚠️ **Ensure Model is Uploaded**
- Model must be in Elasticsearch/OpenSearch before evaluation
- Feature set must match model requirements

⚠️ **Test Cases Format**
```python
test_cases = [
    {
        'query': 'search term',
        'ground_truth': 'expected movie title'
    },
    ...
]
```

## Typical Results Interpretation

| LTR vs BM25 | Interpretation |
|-------------|----------------|
| LTR > BM25 ✅ | Model successfully improves over baseline |
| LTR = BM25 ⚠️ | Model performs same as baseline - needs tuning |
| LTR < BM25 ❌ | Model performs worse - training issue |

## Files Reference

| File | Purpose |
|------|---------|
| `ltr/search.py` | Core evaluation functions |
| `ltr/EVALUATION_EXAMPLE.md` | Detailed guide |
| `ltr/evaluation_examples.py` | Runnable examples |
| `ltr/BM25_LTR_IMPLEMENTATION.md` | Technical details |

## Real Example

```python
from ltr.search import batch_evaluate

# Test cases
test_cases = [
    {'query': 'batman begins', 'ground_truth': 'Batman Begins'},
    {'query': 'first blood', 'ground_truth': 'First Blood'},
    {'query': 'the matrix', 'ground_truth': 'The Matrix'},
    {'query': 'terminator 2', 'ground_truth': 'Terminator 2: Judgment Day'},
    {'query': 'alien', 'ground_truth': 'Alien'},
]

# Evaluate
results, metrics = batch_evaluate(
    client, 
    test_cases,
    model_name='my_model_v2',
    verbose=True
)

# Results output:
# ================================================================================
# EVALUATION SUMMARY
# ================================================================================
# Total Queries: 5
# 
# BM25 Results:
#   Correct: 3/5
#   Accuracy: 60.00%
# 
# LTR Results:
#   Correct: 5/5
#   Accuracy: 100.00%
# 
# Comparison:
#   Absolute Improvement: 2 queries
#   Percentage Improvement: +66.67%
#   Cases where LTR improved: 2
# ================================================================================
```

## Troubleshooting

**Q: Getting zero results**
```python
# Check BM25 query works
bm25_query = esBm25Query('batman', size=10)
bm25_results = client.query('tmdb', bm25_query)
print(f"Found: {len(bm25_results)} results")
```

**Q: Model not found error**
```python
# Verify model exists in OpenSearch
# Via REST API: GET _ltr/_featureset/my_feature_set/_models
```

**Q: Incorrect results**
```python
# Run with verbose=True to see per-query details
results, metrics = batch_evaluate(client, test_cases, verbose=True)
```

## Next Steps

1. Prepare test dataset (at least 5-10 queries)
2. Upload LTR model to OpenSearch
3. Run batch_evaluate()
4. Review metrics and per-query results
5. Iterate on model if needed
6. Compare different model versions
