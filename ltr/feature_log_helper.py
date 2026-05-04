"""
Feature Logging Helper Module

This module provides convenient utilities for logging LTR features.
It simplifies the process of creating feature logging queries and 
processing the results.

Examples:
    # Create a feature logging query
    from ltr.feature_log_helper import create_feature_log_query
    
    query = create_feature_log_query(
        featureset='my_feature_set',
        keywords='rambo',
        ids=['1368', '7555', '1369']
    )
    results = client.query('tmdb', query)
    
    # Parse results and get features
    from ltr.feature_log_helper import extract_features_from_results
    
    docs_with_features = extract_features_from_results(results)
"""

import json


def create_feature_log_query(featureset, keywords, ids=None, additional_params=None):
    """
    Create a feature logging query for OpenSearch/Elasticsearch.
    
    This query uses the sltr (Scoring LTR) filter to compute features
    without affecting document scores. Results include computed feature
    values that can be used for training ranking models.
    
    Args:
        featureset (str): Name of the feature set to use
        keywords (str): Search keywords to pass as parameter to features
        ids (list, optional): List of document IDs to filter by.
                             If None, all documents matching the filter are returned.
        additional_params (dict, optional): Additional parameters to pass to features.
                                           Example: {'fuzzy_keywords': 'rambo~ fight~'}
    
    Returns:
        dict: Query structure ready to send to OpenSearch/Elasticsearch
    
    Example:
        >>> query = create_feature_log_query('my_feature_set', 'rambo')
        >>> # Query includes sltr filter + ltr_log extension for feature capture
        
        >>> query = create_feature_log_query(
        ...     'my_feature_set',
        ...     'rambo',
        ...     ids=['1368', '7555'],
        ...     additional_params={'fuzzy_keywords': 'rambo~'}
        ... )
    """
    
    # Build base params with keywords
    params = {"keywords": keywords}
    
    # Add any additional parameters
    if additional_params:
        params.update(additional_params)
    
    # Build the query structure
    query = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "sltr": {
                            "_name": "logged_features",
                            "featureset": featureset,
                            "params": params
                        }
                    }
                ]
            }
        },
        "ext": {
            "ltr_log": {
                "log_specs": {
                    "name": "ltr_features",
                    "named_query": "logged_features"
                }
            }
        },
        "size": 1000
    }
    
    # Add document ID filter if provided
    if ids is not None and len(ids) > 0:
        must_filter = {
            "terms": {
                "_id": [str(doc_id) for doc_id in ids]
            }
        }
        query["query"]["bool"]["must"] = [must_filter]
    
    return query


def extract_features_from_results(results):
    """
    Extract feature values from query results.
    
    Processes the OpenSearch/Elasticsearch response and extracts
    the computed feature values into a more convenient format.
    
    Args:
        results (list): List of result documents from client.query()
                       Each document should have _ltrlog field with feature data
    
    Returns:
        list: List of dicts with keys:
              - id: Document ID
              - features: List of feature values
              - original_doc: The full source document
    
    Example:
        >>> results = client.query('tmdb', query)
        >>> docs_with_features = extract_features_from_results(results)
        >>> for doc in docs_with_features:
        ...     print(doc['id'], doc['features'])
    """
    docs_with_features = []
    
    for doc in results:
        doc_id = doc.get('id') or doc.get('_id')
        
        features = []
        if '_ltrlog' in doc:
            for ltr_log_entry in doc['_ltrlog']:
                for feature_spec in ltr_log_entry.get('ltr_features', []):
                    value = feature_spec.get('value', 0.0)
                    features.append(value)
        
        docs_with_features.append({
            'id': doc_id,
            'features': features,
            'original_doc': doc
        })
    
    return docs_with_features


def print_query(query):
    """
    Pretty print a feature logging query.
    
    Args:
        query (dict): Query dictionary to print
    """
    print(json.dumps(query, indent=2))


def build_feature_logging_pipeline(client, index, featureset, keywords, ids):
    """
    Complete feature logging pipeline.
    
    Combines query creation, execution, and feature extraction into
    a single convenient function.
    
    Args:
        client: Search client (OpenSearch, Elasticsearch)
        index (str): Index name to search
        featureset (str): Feature set name
        keywords (str): Search keywords
        ids (list): Document IDs to log features for
    
    Returns:
        list: Documents with extracted feature values
    
    Example:
        >>> from ltr.client import OpenSearchClient
        >>> from ltr.feature_log_helper import build_feature_logging_pipeline
        >>> 
        >>> client = OpenSearchClient()
        >>> docs = build_feature_logging_pipeline(
        ...     client,
        ...     'tmdb',
        ...     'my_feature_set',
        ...     'rambo',
        ...     ['1368', '7555', '1369']
        ... )
    """
    query = create_feature_log_query(featureset, keywords, ids)
    results = client.query(index, query)
    docs_with_features = extract_features_from_results(results)
    return docs_with_features


def create_judgment_features_dict(docs_with_features):
    """
    Convert documents with features to a convenient lookup dict.
    
    Args:
        docs_with_features (list): Output from extract_features_from_results()
    
    Returns:
        dict: Mapping of doc_id -> features list
    
    Example:
        >>> docs = extract_features_from_results(results)
        >>> feature_dict = create_judgment_features_dict(docs)
        >>> # Now can easily get features: feature_dict['1368']
        >>> features_for_doc = feature_dict.get('1368', [])
    """
    return {doc['id']: doc['features'] for doc in docs_with_features}
