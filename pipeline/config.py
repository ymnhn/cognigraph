# ==========================================
# COGNIGRAPH: PIPELINE CONFIGURATION
# ==========================================

# 1. AI Model Settings
# We use this specific model because it is fast enough to run on GitHub Actions
MODEL_NAME = 'all-MiniLM-L6-v2'

# 2. The Semantic "North Star"
# The script will score every paper against this exact description.
TARGET_CONCEPT = """
Research focusing on computational cognitive science, neural manifolds, 
active inference, and the intersection of artificial intelligence with 
human cognitive architectures.
"""

# 3. Algorithm Strictness
# 0.0 (Accept Everything) to 1.0 (Exact Match Only)
SIMILARITY_THRESHOLD = 0.60

# 4. File Management
# AstroPaper expects blog posts (our research papers) to be here
OUTPUT_DIR = "src/data/blog"

# 5. Search API Parameters
# We will use arXiv's open API for this example
MAX_RESULTS = 20
SEARCH_QUERY = 'all:"cognitive science" OR all:"computational modeling"'