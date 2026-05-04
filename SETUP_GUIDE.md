# Setup Guide for hello-ltr OpenSearch Learning-to-Rank

This guide will help you set up the hello-ltr project after cloning from git. The repository is configured to track only the OpenSearch-related scripts and the core LTR library.

## What's Included in Git

The repository includes:
- ✅ **Core LTR Library**: `ltr/` directory with all modules
- ✅ **OpenSearch Notebooks**: `notebooks/opensearch/` including:
  - `ltr-tmdb.ipynb` - Main LTR tutorial with TMDB dataset
  - `ML_Models_Training_UPDATED.ipynb` - ML model training
  - Other learning notebooks and examples
- ✅ **Docker Configuration**: `notebooks/opensearch/docker-compose.yml`
- ✅ **Dependencies**: `requirements.txt` with all packages

## What's NOT Included (Can Be Deleted)

The following directories can be safely deleted and recreated:
- `notebooks/elasticsearch/` - Elasticsearch examples
- `notebooks/exercises/` - Practice exercises
- `tests/` - Test suite
- `utils/` - Utility scripts
- `rre/` - RRE (Relevant Results Engine) config

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hello-ltr
```

### 2. Create a Python Virtual Environment

```bash
# Use Python 3.10 or higher
python3 -m venv ltr3
source ltr3/bin/activate
```

On Windows:
```bash
python -m venv ltr3
ltr3\Scripts\activate
```

### 3. Install Dependencies

Install all required dependencies from requirements.txt:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Key Dependencies

The following are automatically installed and required:
- **opensearch-py** (2.2.0) - OpenSearch client
- **pandas** (2.0.3) - Data manipulation
- **numpy** (1.23.5) - Numerical computing
- **scikit-learn** (1.3.0) - ML algorithms
- **xgboost** (1.7.6) - Gradient boosting
- **jupyter** - Jupyter notebook server
- **plotly** (5.5.0) - Interactive visualizations
- **plotnine** (0.12.2) - Grammar of graphics plotting
- **matplotlib** (3.7.2) - Static plotting
- **elasticsearch** (7.16.2) - Elasticsearch support
- **requests** (2.27.1) - HTTP library

### 4. Verify Installation

```bash
# Activate the environment
source ltr3/bin/activate

# Verify key packages
python -c "import opensearchpy; import pandas; import jupyter; print('✓ All dependencies installed successfully!')"

# Check Jupyter
jupyter notebook --version
```

## Running OpenSearch Scripts

The primary content is in `notebooks/opensearch/` with TMDB (The Movie Database) learning-to-rank examples.

### Start OpenSearch Environment

First, ensure Docker is running, then:

```bash
cd notebooks/opensearch
docker compose up
```

This will launch:
- **OpenSearch** (port 9201) - Search engine with LTR plugin
- **OpenSearch Dashboards** (port 5602) - Web UI for OpenSearch
- **Jupyter Notebook** (port 8888) - Notebook server

Wait for all services to be ready (approximately 30-60 seconds).

### Access and Run Notebooks

Once services are running:

1. **Open Jupyter**:
   - Navigate to `http://localhost:8888` in your browser
   - Default password is set in docker-compose.yml

2. **Key Notebooks** in `notebooks/opensearch/tmdb/`:
   - **ltr-tmdb.ipynb** - Start here! Complete LTR workflow with TMDB data
   - **ML_Models_Training_UPDATED.ipynb** - Train ML ranking models
   - **evaluation.ipynb** - Evaluate model performance
   - **bayesian-optimization.ipynb** - Hyperparameter optimization
   - Other examples for reference

3. **Run Cells**:
   - Start with Phase 1 (data setup) - downloads TMDB dataset
   - Follow through Phases 2+ for feature engineering and ranking

### Verify OpenSearch is Ready

```bash
# From another terminal
curl -X GET https://localhost:9201 -u admin:admin -k
```

Should return status 200 and OpenSearch version info.

## Notebook Dependencies

Both primary notebooks (`ltr-tmdb.ipynb` and `ML_Models_Training_UPDATED.ipynb`) use:

**From ltr library**:
- `ltr.client.OpenSearchClient` - Connect to OpenSearch
- `ltr.index.rebuild` - Index documents
- `ltr.helpers.movies.indexable_movies` - Load movie data
- `ltr.judgments` - Handle relevance judgments
- `ltr.log.FeatureLogger` - Log feature values
- `ltr.ranklib` - RankLib integration
- `ltr.download` - Download datasets

**From external packages**:
- `pandas`, `numpy` - Data handling
- `sklearn` (scikit-learn) - ML algorithms (RandomForest, GradientBoosting, LinearRegression)
- `xgboost` - XGBoost models
- `plotly`, `matplotlib` - Visualizations
- `requests` - HTTP requests

All dependencies are in `requirements.txt`.

## Troubleshooting

### Missing Modules Error
```bash
# Ensure environment is activated
source ltr3/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Docker Services Won't Start
```bash
# Check Docker is running
docker ps

# Check docker-compose version
docker-compose --version

# View logs
cd notebooks/opensearch
docker compose logs
```

### Jupyter Can't Connect to OpenSearch
1. Verify OpenSearch is running: `docker ps`
2. Check network connectivity:
   ```bash
   curl -X GET https://localhost:9201 -u admin:admin -k
   ```
3. Restart services:
   ```bash
   cd notebooks/opensearch
   docker compose down
   docker compose up
   ```

### Port Already in Use
If ports 9201, 5602, or 8888 are already in use:
1. Check what's using them: `lsof -i :9201`
2. Stop those services or use different ports in docker-compose.yml
3. Alternatively, stop other services first

### Python Version Issues
This project requires Python 3.10+. Check your version:
```bash
python3 --version
```

If you have multiple Python versions, specify 3.10:
```bash
python3.10 -m venv ltr3
```

## Next Steps

1. **Activate virtual environment**: `source ltr3/bin/activate`
2. **Start Docker services**: `cd notebooks/opensearch && docker compose up`
3. **Access Jupyter**: Open http://localhost:8888 in browser
4. **Open ltr-tmdb.ipynb** and start with Phase 1
5. **Run cells sequentially** - each phase builds on the previous
6. **Experiment** with features, queries, and models

## Additional Resources

- OpenSearch LTR Docs: https://docs.opensearch.org/latest/search-plugins/search-relevance/
- LTR Plugin Docs: https://opensearch.org/docs/latest/search-plugins/search-relevance/ltr/
- Jupyter Docs: https://jupyter.org/
- Scikit-learn Docs: https://scikit-learn.org/

## Resetting the Environment

If you need to completely reset:

```bash
# Stop and remove containers
cd notebooks/opensearch
docker compose down -v

# Remove indexed data (optional)
rm -rf notebooks/opensearch/tmdb/data/

# Reinstall Python packages (optional)
rm -rf ltr3/
python3 -m venv ltr3
source ltr3/bin/activate
pip install -r requirements.txt
```

Then restart from "Running OpenSearch Scripts" section above.

