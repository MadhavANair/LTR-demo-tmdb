"""
Example script demonstrating BM25 vs LTR evaluation.

This script shows:
1. Single query comparison between BM25 and LTR
2. Batch evaluation on multiple test cases
3. Analysis and visualization of results
4. Model comparison across different LTR models
"""

import sys
sys.path.insert(0, '/home/madhav/Projects/hello-ltr')

from ltr.search import (
    esBm25Query, esLtrQuery, batch_evaluate, 
    compare_results, evaluate_accuracy
)
import pandas as pd


def example_single_comparison(client):
    """
    Example 1: Compare BM25 vs LTR on a single query
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Query Comparison")
    print("="*80)
    
    query = "batman"
    ground_truth = "Batman Begins"
    
    # Execute BM25 search
    bm25_query = esBm25Query(query, size=10)
    bm25_results = client.query('tmdb', bm25_query)
    
    # Execute LTR search
    ltr_query = esLtrQuery(query, 'my_model_v2', featureset='my_feature_set', size=10)
    ltr_results = client.query('tmdb', ltr_query)
    
    # Compare results with verbose output
    comparison = compare_results(
        query, 
        ground_truth, 
        bm25_results, 
        ltr_results,
        verbose=True
    )
    
    return comparison


def example_batch_evaluation(client):
    """
    Example 2: Batch evaluation on multiple test cases
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Batch Evaluation")
    print("="*80)
    
    # Define test cases
    test_cases = [
        {'query': 'batman', 'ground_truth': 'Batman Begins'},
        {'query': 'rambo', 'ground_truth': 'First Blood'},
        {'query': 'matrix', 'ground_truth': 'The Matrix'},
        {'query': 'terminator', 'ground_truth': 'The Terminator'},
        {'query': 'alien', 'ground_truth': 'Alien'},
        {'query': 'superman', 'ground_truth': 'Superman'},
        {'query': 'iron man', 'ground_truth': 'Iron Man'},
    ]
    
    # Run batch evaluation
    results, metrics = batch_evaluate(
        client,
        test_cases,
        model_name='my_model_v2',
        featureset='my_feature_set',
        index='tmdb',
        verbose=True
    )
    
    return results, metrics


def example_per_query_analysis(results):
    """
    Example 3: Analyze individual query results
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Per-Query Analysis")
    print("="*80)
    
    # Create DataFrame for easier analysis
    df = pd.DataFrame([
        {
            'Query': r['query'],
            'Ground Truth': r['ground_truth'],
            'BM25 Result': r['bm25_title'],
            'BM25 Score': round(r['bm25_score'], 4) if r['bm25_score'] else 0,
            'BM25 Correct': '✓' if r['bm25_correct'] else '✗',
            'LTR Result': r['ltr_title'],
            'LTR Score': round(r['ltr_score'], 4) if r['ltr_score'] else 0,
            'LTR Correct': '✓' if r['ltr_correct'] else '✗',
            'LTR Improved': '✓' if r['improvement'] else '',
        }
        for r in results
    ])
    
    print("\nComparison Table:")
    print(df.to_string(index=False))
    
    # Show cases where LTR improved
    improvements = [r for r in results if r['improvement']]
    if improvements:
        print(f"\n\nCases where LTR improved ({len(improvements)}):")
        for r in improvements:
            print(f"  Query: '{r['query']}'")
            print(f"    BM25: {r['bm25_title']} (incorrect)")
            print(f"    LTR:  {r['ltr_title']} (correct)")
    
    return df


def example_model_comparison(client, test_cases):
    """
    Example 4: Compare multiple LTR models
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Model Comparison")
    print("="*80)
    
    models_to_test = ['my_model_v1', 'my_model_v2']
    model_results = []
    
    for model in models_to_test:
        print(f"\nEvaluating model: {model}")
        
        try:
            results, metrics = batch_evaluate(
                client,
                test_cases,
                model_name=model,
                featureset='my_feature_set',
                verbose=False
            )
            
            model_results.append({
                'Model': model,
                'BM25 Accuracy': f"{metrics['bm25_accuracy']:.2%}",
                'LTR Accuracy': f"{metrics['ltr_accuracy']:.2%}",
                'Absolute Improvement': metrics['absolute_improvement'],
                'Percentage Improvement': f"{metrics['percentage_improvement']:+.2f}%",
                'Cases Improved': metrics['improvements_count']
            })
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    if model_results:
        df_models = pd.DataFrame(model_results)
        print("\n\nModel Comparison Results:")
        print(df_models.to_string(index=False))
    
    return model_results


def example_metrics_summary(metrics):
    """
    Example 5: Display detailed metrics summary
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Metrics Summary")
    print("="*80)
    
    print(f"""
Overall Performance:
  Total Queries Evaluated:  {metrics['total_queries']}
  
BM25 Baseline:
  Correct Answers:         {metrics['bm25_correct']}/{metrics['total_queries']}
  Accuracy:                {metrics['bm25_accuracy']:.2%}
  
LTR Model Performance:
  Correct Answers:         {metrics['ltr_correct']}/{metrics['total_queries']}
  Accuracy:                {metrics['ltr_accuracy']:.2%}
  
Improvement Analysis:
  Additional Correct:      {metrics['absolute_improvement']} queries
  Percentage Improvement:  {metrics['percentage_improvement']:+.2f}%
  Cases where LTR Won:     {metrics['improvements_count']}
  
Key Takeaway:
  LTR model is {metrics['percentage_improvement']:.1f}% better than BM25
  at selecting the correct movie as the top result.
""")


def main():
    """
    Run all examples
    """
    print("\n" + "="*80)
    print("BM25 vs LTR EVALUATION EXAMPLES")
    print("="*80)
    
    # Import the OpenSearch client
    try:
        from opensearchpy import OpenSearch
    except ImportError:
        from opensearch_py import OpenSearch
    
    # Initialize client
    client = OpenSearch([{'host': 'localhost', 'port': 9201}])
    
    # Check connection
    try:
        info = client.info()
        print(f"\nConnected to OpenSearch successfully")
        print(f"Cluster: {info['cluster_name']}")
    except Exception as e:
        print(f"Error connecting to OpenSearch: {str(e)}")
        print("Make sure OpenSearch is running on localhost:9201")
        return
    
    # Example 1: Single comparison
    try:
        comparison = example_single_comparison(client)
    except Exception as e:
        print(f"Example 1 error: {str(e)}")
    
    # Example 2: Batch evaluation
    try:
        results, metrics = example_batch_evaluation(client)
        
        # Example 3: Per-query analysis
        try:
            df = example_per_query_analysis(results)
        except Exception as e:
            print(f"Example 3 error: {str(e)}")
        
        # Example 5: Metrics summary
        try:
            example_metrics_summary(metrics)
        except Exception as e:
            print(f"Example 5 error: {str(e)}")
        
    except Exception as e:
        print(f"Example 2 error: {str(e)}")
    
    # Example 4: Model comparison
    try:
        test_cases = [
            {'query': 'batman', 'ground_truth': 'Batman Begins'},
            {'query': 'rambo', 'ground_truth': 'First Blood'},
            {'query': 'matrix', 'ground_truth': 'The Matrix'},
        ]
        model_results = example_model_comparison(client, test_cases)
    except Exception as e:
        print(f"Example 4 error: {str(e)}")
    
    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80)


if __name__ == "__main__":
    main()
