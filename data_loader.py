import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly


class DataLoader:
    def __init__(self, search_agent=None):
        print("DataLoader Init")
        self.search_agent = search_agent

    def fetch_arxiv_papers(self, query):
        """
            Fetches top 5 research papers from ArXiv based on the user query.
            If <5 papers are found, expands the search using related topics.
            
            Returns:
                list: A list of dictionaries containing paper details (title, summary, link).
        """
        
        def search_arxiv(query):
            """Helper function to query ArXiv API."""
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
            except Exception:
                return []

            try:
                root = ET.fromstring(response.text)
            except ET.ParseError:
                return []

            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            def get_text(el, local_tag):
                node = el.find(f'atom:{local_tag}', ns)
                return node.text.strip() if node is not None and node.text else ""

            papers = []
            for entry in root.findall('atom:entry', ns):
                title = get_text(entry, 'title')
                summary = get_text(entry, 'summary')
                link = get_text(entry, 'id')
                papers.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })

            return papers

        papers = search_arxiv(query)

        if len(papers) < 5 and getattr(self, 'search_agent', None):  # If fewer than 5 papers, expand search
            try:
                related_topics_response = self.search_agent.generate_reply(
                    messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
                )
                related_text = related_topics_response.get("content", "") if isinstance(related_topics_response, dict) else str(related_topics_response)
                related_topics = [t.strip() for t in related_text.split("\n") if t.strip()]
            except Exception:
                related_topics = []

            for topic in related_topics:
                if topic and len(papers) < 5:
                    new_papers = search_arxiv(topic)
                    for p in new_papers:
                        if len(papers) >= 5:
                            break
                        if p not in papers:
                            papers.append(p)

        return papers

    def fetch_google_scholar_papers(self, query):
        """
            Fetches top 5 research papers from Google Scholar.
            Returns:
                list: A list of dictionaries containing paper details (title, summary, link)
        """
        papers = []
        try:
            search_results = scholarly.search_pubs(query)
            for i, paper in enumerate(search_results):
                if i >= 5:
                    break
                bib = paper.get("bib", {}) if isinstance(paper, dict) else {}
                title = bib.get("title", "No title") if isinstance(bib, dict) else "No title"
                summary = bib.get("abstract", "No summary available") if isinstance(bib, dict) else "No summary available"
                link = paper.get("pub_url", "No link available") if isinstance(paper, dict) else "No link available"
                papers.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })
        except Exception:
            pass

        return papers