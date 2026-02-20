import requests
import networkx as nx
import matplotlib.pyplot as plt

def fetch_arxiv_data_via_openalex(topic, limit=50):
    """
    Queries OpenAlex for arXiv papers. 
    OpenAlex is 'pre-indexed' arXiv data that includes citation links.
    """
    url = f"https://api.openalex.org/works?filter=primary_location.source.id:S4306400127,title.search:{topic}&per_page={limit}"
    
    print(f"Fetching {limit} papers about '{topic}'...")
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching data.")
        return []
    
    return response.json().get('results', [])

def build_mega_graph(data):
    G = nx.DiGraph()

    for work in data:
        paper_id = work.get('id')
        paper_title = work.get('display_name')
        
        G.add_node(paper_id, label=paper_title, type='paper', color='skyblue')

        for authorship in work.get('authorships', []):
            author = authorship.get('author', {})
            author_id = author.get('id')
            author_name = author.get('display_name')
            
            G.add_node(author_id, label=author_name, type='author', color='orange')
            G.add_edge(author_id, paper_id, relation='authored')
        for cited_paper_id in work.get('referenced_works', []):
            G.add_edge(paper_id, cited_paper_id, relation='cites')

    return G

def visualize_graph(G, output_file="research_graph.png"):
    plt.figure(figsize=(12, 12))
    
    node_colors = [data['color'] for n, data in G.nodes(data=True)]
    labels = {n: data['label'][:20] + "..." if len(data['label']) > 20 else data['label'] 
              for n, data in G.nodes(data=True)}

    pos = nx.spring_layout(G, k=0.3)
    nx.draw(G, pos, labels=labels, with_labels=True, 
            node_color=node_colors, node_size=1000, 
            font_size=7, edge_color='gray', alpha=0.6)

    plt.title("arXiv Author-Citation Network")
    plt.savefig(output_file)
    print(f"Graph successfully saved to {output_file}")

if __name__ == "__main__":
    TOPIC = "Black Holes"
    LIMIT_PAPERS = 30

    results = fetch_arxiv_data_via_openalex(TOPIC, limit=LIMIT_PAPERS)
    if results:
        graph = build_mega_graph(results)
        visualize_graph(graph)
        
        print(f"\nGraph Stats:")
        print(f"Total Entities (Authors + Papers): {graph.number_of_nodes()}")
        print(f"Total Connections (Authorship + Citations): {graph.number_of_edges()}")