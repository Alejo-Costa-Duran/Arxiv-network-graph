import requests
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import os
def visualize_interactive_graph(G, output_file="research_graph.html"):
    print("Creating interactive graph...", flush=True)
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    
    
    for n, data in G.nodes(data=True):
        label = data.get('label', str(n))
        color = data.get('color', '#808080') 
        
        
        net.add_node(n, label=label[:30], title=label, color=color)

    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, title=data.get('relation', ''))

    net.force_atlas_2based()
    
    path = os.path.join("/app/output", output_file)
    net.save_graph(path)
    print(f"✅ Interactive graph saved to {path}")


def fetch_arxiv_data_via_openalex(topic, limit=50):
    url = f"https://api.openalex.org/works?search={topic}&per_page={limit}&filter=has_fulltext:true"
    
    print(f"📡 Searching OpenAlex for '{topic}'...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        arxiv_papers = []
        for work in results:
            locations = str(work.get('locations', [])).lower()
            if 'arxiv' in locations:
                arxiv_papers.append(work)
        
        if not arxiv_papers:
            print("⚠️ No strict arXiv matches found, returning general results for this topic.",flush=True)
            return results
            
        print(f"✅ Found {len(arxiv_papers)} papers.", flush=True)
        return arxiv_papers
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        return []

def build_mega_graph(data):
    G = nx.DiGraph() 

    for work in data:
        paper_id = work.get('id')
        paper_title = work.get('display_name')
        
        if not paper_id:
            continue
            
        G.add_node(paper_id, label=paper_title, type='paper', color='skyblue')

        for authorship in work.get('authorships', []):
            author = authorship.get('author', {})
            author_id = author.get('id')
            author_name = author.get('display_name') or "Unknown Author"
            
            if author_id:
                G.add_node(author_id, label=author_name, type='author', color='orange')
                G.add_edge(author_id, paper_id, relation='authored')

        for cited_paper_id in work.get('referenced_works', []):
            if cited_paper_id:
                G.add_edge(paper_id, cited_paper_id, relation='cites')

    return G

if __name__ == "__main__":
    TOPIC = "Black Holes"
    LIMIT_PAPERS = 30

    results = fetch_arxiv_data_via_openalex(TOPIC, limit=LIMIT_PAPERS)
    print(f"Found {len(results)} papers", flush=True)
    if results:
        graph = build_mega_graph(results)
        visualize_interactive_graph(graph)
        
        print(f"\nGraph Stats:", flush=True)
        print(f"Total Entities (Authors + Papers): {graph.number_of_nodes()}", flush=True)
        print(f"Total Connections (Authorship + Citations): {graph.number_of_edges()}", flush=True)