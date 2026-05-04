# Git Configuration Summary

## Overview

The hello-ltr repository has been reconfigured to include OpenSearch-related scripts while excluding other optional notebooks and directories.

## What's Tracked in Git

### ✅ Included Files

**Core Library**:
- `ltr/` - Complete Learning-to-Rank library with all modules
  - `ltr/client/` - OpenSearch, Elasticsearch, Solr clients
  - `ltr/clickmodels/` - Click models for relevance estimation
  - `ltr/helpers/` - Helper utilities
  - All Python modules and utilities

**OpenSearch Content** (`notebooks/opensearch/`):
- `notebooks/opensearch/docker-compose.yml` - Docker configuration
- `notebooks/opensearch/README.md` - Documentation
- `notebooks/opensearch/.docker/` - Docker build configurations
- **All Jupyter Notebooks**:
  - `ltr-tmdb.ipynb` ⭐ PRIMARY - Main LTR tutorial with TMDB dataset
  - `ML_Models_Training_UPDATED.ipynb` ⭐ PRIMARY - ML model training
  - `evaluation.ipynb` - Model evaluation
  - `bayesian-optimization.ipynb` - Hyperparameter tuning
  - `lambda-mart-in-python.ipynb` - LambdaMART algorithm
  - `opensearch-ltr-basics-project.ipynb` - LTR basics
  - `sandbox.ipynb` - Experimentation notebook
- `notebooks/opensearch/tmdb/` - All supporting files
  - `ltr.py` - Helper functions
  - `export_randomforest_ensemble.py` - Model export
  - `tmdb_settings.json` - OpenSearch index settings
  - `data/tmdb.json` - TMDB dataset
  - `data/xgboost_*.json` - Pre-trained models
- `notebooks/opensearch/osc-blog/` - Blog-related examples

**Configuration Files**:
- `.gitignore` - Updated ignore rules
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition
- `docker-compose.yml` - Docker Compose configuration
- `README.md` - Project documentation
- `SETUP_GUIDE.md` - Setup instructions

---

## What's NOT Tracked (Can Be Deleted)

### ❌ Excluded Directories

**Deleted Notebook Collections**:
- `notebooks/elasticsearch/` - Elasticsearch examples (can be recreated)
- `notebooks/exercises/` - Practice exercises (can be recreated)

**Not Tracked in Repository**:
- `notebooks/solr/` - Solr examples (can be recreated)
- `tests/` - Test suite (optional)
- `utils/` - Utility scripts (optional)
- `rre/` - RRE configuration (optional)

**Temporary/Cache Directories**:
- `.claw/` - Build cache
- `.sandbox-home/`, `.sandbox-tmp/` - Sandbox environments
- `ltr3/` - Virtual environment (created locally)
- `venv/`, `tests_venv/` - Virtual environments (created locally)
- `.ipynb_checkpoints/` - Jupyter checkpoints
- `__pycache__/` - Python cache
- `.vscode/`, `.idea/` - IDE settings

---

## Git Status Summary

### Files Being Tracked

When you clone this repository, the following are already committed:
- ✅ All `ltr/` library files
- ✅ All `notebooks/opensearch/` content
- ✅ Core configuration files
- ✅ Requirements and Dockerfiles
- ✅ Documentation

### Files to Create Locally

When you clone and set up, you'll create:
- 🔨 Virtual environment: `ltr3/`
- 📥 Installed packages (from requirements.txt)
- 📂 Data files (downloaded by notebooks)
- 🛠️ Temporary files (Jupyter checkpoints, cache, etc.)

These are all automatically ignored by `.gitignore`.

---

## Key Changes Made

### 1. Updated `.gitignore`

**Changes**:
- ❌ **Removed ignores**: `.ipynb` files are now tracked
- ✅ **Added to ignore**: `.claw/`, `.sandbox-home/`, `.sandbox-tmp/`
- ✅ **Scoped ignores**: `notebooks/` ignored except `notebooks/opensearch/`
- ✅ **Allowed data**: Specific data files in `notebooks/opensearch/tmdb/data/`

### 2. Created `SETUP_GUIDE.md`

**Includes**:
- Step-by-step setup instructions
- Python environment creation
- Dependency installation
- Running Docker containers
- Notebook descriptions
- Troubleshooting guide
- Reset procedures

---

## Workflow for Users

When someone clones this repository:

```bash
# 1. Clone
git clone <url>
cd hello-ltr

# 2. Setup environment
python3 -m venv ltr3
source ltr3/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start OpenSearch
cd notebooks/opensearch
docker compose up

# 5. Open Jupyter and run notebooks
# http://localhost:8888
```

All notebooks and code are ready to run!

---

## Dependencies

### Required Packages (in requirements.txt)

**Data & ML**:
- pandas==2.0.3
- numpy==1.23.5
- scikit-learn==1.3.0
- xgboost==1.7.6

**Search Clients**:
- opensearch-py==2.2.0
- elasticsearch==7.16.2

**Visualization**:
- plotly==5.5.0
- plotnine==0.12.2
- matplotlib==3.7.2
- graphviz==0.19.1

**Jupyter & Notebooks**:
- jupyter
- ipython
- ipykernel
- notebook

**Utilities**:
- requests==2.27.1
- pandas==2.0.3
- joblib==1.1.1
- fuzzywuzzy==0.18.0
- retrying==1.3.3
- tqdm==4.62.3

All automatically installed via `pip install -r requirements.txt`

---

## Important Notes

### Notebook Dependencies

Both primary notebooks (`ltr-tmdb.ipynb` and `ML_Models_Training_UPDATED.ipynb`) use:

**ltr library modules**:
```python
from ltr.client import OpenSearchClient, ElasticClient
from ltr.index import rebuild
from ltr.helpers.movies import indexable_movies
from ltr.judgments import judgments_open, judgments_from_file
from ltr.log import FeatureLogger
from ltr.ranklib import trainModel, save_model
from ltr import download
```

**External packages**:
```python
import pandas, numpy, sklearn, xgboost, requests
import plotly, matplotlib, plotnine
```

All dependencies are in `requirements.txt` - no need to manually install individual packages.

---

## File Structure After Setup

```
hello-ltr/
├── ltr/                          # ✅ Tracked - Core library
│   ├── client/                   # OpenSearch, Elasticsearch clients
│   ├── helpers/                  # Helper utilities
│   ├── clickmodels/              # Click models
│   └── ... (other modules)
├── notebooks/opensearch/         # ✅ Tracked - Main content
│   ├── docker-compose.yml        # ✅ Docker config
│   ├── tmdb/
│   │   ├── ltr-tmdb.ipynb       # ✅ Main tutorial
│   │   ├── ML_Models_Training_UPDATED.ipynb  # ✅ Training
│   │   ├── ltr.py               # ✅ Helpers
│   │   ├── data/                # ✅ Tracked data
│   │   └── ... (other notebooks)
│   └── osc-blog/                # ✅ Blog examples
├── ltr3/                         # 🔨 Created locally (ignored)
├── requirements.txt              # ✅ Tracked
├── docker-compose.yml            # ✅ Tracked
├── Dockerfile                    # ✅ Tracked
├── SETUP_GUIDE.md               # ✅ Tracked
└── .gitignore                    # ✅ Tracked
```

---

## Testing the Configuration

To verify all tracked files:

```bash
cd /home/madhav/Projects/hello-ltr

# Check what's tracked
git ls-files | grep opensearch | head -10

# Verify notebooks are not ignored
git check-ignore notebooks/opensearch/tmdb/ltr-tmdb.ipynb || echo "✓ Not ignored"

# Check ignore status
git check-ignore .claw/ && echo "✓ .claw/ is ignored" || echo "Not ignored"
```

---

## Additional Commands

### Clone and Setup New Repo

```bash
git clone <repository-url>
cd hello-ltr
python3 -m venv ltr3
source ltr3/bin/activate
pip install -r requirements.txt
cd notebooks/opensearch
docker compose up
```

### Update After Git Pull

```bash
git pull
source ltr3/bin/activate
pip install -r requirements.txt  # In case of new dependencies
```

### Reset Everything

```bash
# Stop Docker
cd notebooks/opensearch
docker compose down -v

# Remove virtual environment
rm -rf ltr3/

# Reinstall
python3 -m venv ltr3
source ltr3/bin/activate
pip install -r requirements.txt
docker compose up
```
