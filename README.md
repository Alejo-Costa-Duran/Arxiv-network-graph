## ARXiv Citation & Co-authorship Graph

This is a pthon based tool to visualize the connections in research papers on arXiv. This tool fetches data from OpenAlex (indexing arXiv) to build a directed graph showing authors and papers connections. 

# Features
- Bipartite mapping: Distinguishes between Author nodes and Paper Nodes
- Citation tracking: Automatically maps references between papers in the dataset
- Dockerized: Containerized using docker
- Customizable: You can change the topic and number of papers to analyze.

# Quick start
1. Install dependencies
```pip install requests networkx matplotlib arxiv scipy pyvis```
2. Configure `arxiv-network-graph.py` and edit the constants, i.e.
```
TOPIC="Statistical Mechanics"
LIMIT_PAPERS=50
```
3. Run
```python arxiv-network-graph.py```

# Running with Docker
1. Build the image
``` docker build -t arxiv-graph . ```

2. Run and save output
```docker run -v "$(pwd):/app/output" arxiv-graph```

# Understanding the Graph
- Orange nodes Authors
- Blue Nodes research papers
- Edges: `Author -> paper`indicates authorship. `paper -> paper` who cited whom

# Note on Data Sources
This project uses the OpenAlex API. While it pulls arXiv papers, it uses OpenAlex's processed metadata because standard arXiv metadata does not natively include citation links in a machine-readable format.