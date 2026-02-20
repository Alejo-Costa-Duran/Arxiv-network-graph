import requests
import networkx as nx
from pyvis.network import Network
import os

def fetch_arxiv_data_via_openalex(topic, limit=100):
    url = f"https://api.openalex.org/works?search={topic}&per_page={limit}&filter=has_fulltext:true"
    print(f"📡 Searching OpenAlex for '{topic}'...", flush=True)
    try:
        response = requests.get(url, timeout=10)
        results = response.json().get('results', [])
        return results
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        return []

def build_mega_graph(data, include_authors=True):
    G = nx.DiGraph()
    # 1. Add Paper Nodes
    for work in data:
        p_id = work.get('id')
        if p_id:
            G.add_node(p_id, 
                       title=f"PAPER: {work.get('display_name')}", 
                       label=" ", # Clean look: no text on node
                       citations=work.get('cited_by_count', 0),
                       type='paper')

    # 2. Add Edges (Citations and optionally Authors)
    for work in data:
        p_id = work.get('id')
        if not p_id: continue
        
        for cited_id in work.get('referenced_works', []):
            if cited_id in G:
                G.add_edge(p_id, cited_id, relation='cites')

        if include_authors:
            for authorship in work.get('authorships', []):
                author = authorship.get('author', {})
                a_id = author.get('id')
                if a_id:
                    if a_id not in G:
                        G.add_node(a_id, 
                                   title=f"AUTHOR: {author.get('display_name')}", 
                                   label=" ", 
                                   type='author',
                                   color='#888888',
                                   shape='square',
                                   size=5)
                    G.add_edge(a_id, p_id, relation='authored')
    return G

def apply_visuals_and_save(G, output_file="research_graph.html"):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    
    # Calculate paper citation scaling
    paper_cites = [d.get('citations', 0) for n, d in G.nodes(data=True) if d.get('type') == 'paper']
    max_cites = max(paper_cites) if paper_cites else 1

    for n, data in G.nodes(data=True):
        node_props = data.copy()
        if data.get('type') == 'paper':
            cites = data.get('citations', 0)
            # Heatmap color
            if cites > (max_cites * 0.6): node_props['color'] = '#FFD700'
            elif cites > (max_cites * 0.2): node_props['color'] = '#FF8C00'
            else: node_props['color'] = '#4682B4'
            node_props['size'] = 10 + (cites / max_cites * 40)
        
        net.add_node(n, **node_props)

    for s, t in G.edges():
        net.add_edge(s, t, color='#555555')

    net.toggle_physics(True)
    path = os.path.join("/app/output", output_file)
    net.save_graph(path)
    print(f"✅ Graph saved to {path}")

if __name__ == "__main__":
    TOPIC = "Ising Model"
    LIMIT = 200 
    
    results = fetch_arxiv_data_via_openalex(TOPIC, limit=LIMIT)
    if results:
        # Toggle include_authors=True/False here to switch modes
        graph = build_mega_graph(results, include_authors=False)
        apply_visuals_and_save(graph)