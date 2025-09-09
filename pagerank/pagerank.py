import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    distribution = {}

    links = corpus[page]
    num_links = len(links)

    if num_links ==0:
        links = list(corpus.keys())
        num_links = len(links)

    for p in corpus:
        prob = (1-damping_factor)/num_pages

        if p in links:
            prob += damping_factor * (1/num_links)
        distribution[p] = prob
    
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import random

    visits = {page:0 for page in corpus}

    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        visits[current_page] +=1

        probs = transition_model(corpus, current_page, damping_factor)

        current_page = random.choices(
            population = list(probs.keys()),
            weights=list(probs.values()),
            k =1
        )[0]

        total = sum(visits.values())
    return {page:count/total for page, count in visits.items()}



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)

    pagerank = {page: 1/N for page in corpus}

    while True:
        new_pagerank = {}
        max_change = 0

        for page in corpus:
            new_pr = (1 - damping_factor) / N
            for linking_page, links in corpus.items():
                if not links:
                    links = list(corpus.keys())
                if page in links:
                    new_pr += damping_factor * (pagerank[linking_page]/len(links))
            new_pagerank[page] = new_pr

            max_change = max(max_change, abs(new_pr-pagerank[page]))
        
        pagerank = new_pagerank

        if max_change < 0.001:
            break
    
    total = sum(pagerank.values())
    return {page:rank/total for page, rank in pagerank.items()}

if __name__ == "__main__":
    main()
