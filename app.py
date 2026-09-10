"""
Application Streamlit : Implémentation et visualisation de PageRank
sur un réseau social simulé, à l'aide de la bibliothèque NetworkX.

Lancement :
    streamlit run app.py
"""

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuration de la page
# ---------------------------------------------------------------------------
st.set_page_config(page_title="PageRank sur un réseau social", layout="wide")
st.title("🔗 Implémentation de PageRank sur un réseau social")
st.markdown(
    "Cette application calcule et visualise le score **PageRank** des "
    "membres d'un réseau social, à l'aide de la bibliothèque **NetworkX** "
    "(`nx.pagerank`)."
)

# ---------------------------------------------------------------------------
# 1. Construction du graphe : chaque noeud représente une personne nommée
# ---------------------------------------------------------------------------
# On utilise un graphe orienté : une arête A -> B signifie
# "A suit / recommande / interagit avec B" (comme un abonnement Twitter/X).
G = nx.DiGraph()

noms_utilisateurs = [
    "Alicia", "Bob", "Chloé", "David", "Emma",
    "Farid", "Grace", "Hugo", "Inès", "Julien",
]
G.add_nodes_from(noms_utilisateurs)

# Relations (arêtes) représentant les interactions du réseau social
relations = [
    ("Alicia", "Bob"), ("Alicia", "Chloé"), ("Bob", "Chloé"),
    ("Chloé", "David"), ("David", "Emma"), ("Emma", "Alicia"),
    ("Farid", "Alicia"), ("Farid", "Bob"), ("Grace", "Farid"),
    ("Hugo", "Grace"), ("Inès", "Hugo"), ("Julien", "Inès"),
    ("Julien", "Alicia"), ("Emma", "Julien"), ("David", "Grace"),
    ("Bob", "Hugo"), ("Chloé", "Inès"),
]
G.add_edges_from(relations)

# ---------------------------------------------------------------------------
# 2. Paramètres interactifs (barre latérale)
# ---------------------------------------------------------------------------
st.sidebar.header("Paramètres de l'algorithme")
alpha = st.sidebar.slider(
    "Facteur d'amortissement (damping factor)", 0.50, 0.99, 0.85, 0.01
)
nb_iterations = st.sidebar.slider("Nombre maximal d'itérations", 10, 200, 100, 10)

# ---------------------------------------------------------------------------
# 3. Calcul du PageRank avec la bibliothèque NetworkX
# ---------------------------------------------------------------------------
scores_pagerank = nx.pagerank(G, alpha=alpha, max_iter=nb_iterations)
scores_tries = sorted(scores_pagerank.items(), key=lambda item: item[1], reverse=True)

# ---------------------------------------------------------------------------
# 4. Affichage des résultats
# ---------------------------------------------------------------------------
col_graphe, col_scores = st.columns([2, 1])

with col_scores:
    st.subheader("Classement de PageRank")
    for rang, (nom, score) in enumerate(scores_tries, start=1):
        st.write(f"**{rang}. {nom}** — {score:.4f}")

    st.subheader("Diagramme des scores")
    st.bar_chart({nom: score for nom, score in scores_tries})

with col_graphe:
    st.subheader("Visualisation du réseau")

    fig, ax = plt.subplots(figsize=(8, 7))
    disposition = nx.spring_layout(G, seed=42)

    # La taille de chaque noeud est proportionnelle à son score PageRank
    tailles_noeuds = [scores_pagerank[noeud] * 25000 for noeud in G.nodes()]

    nx.draw_networkx_nodes(
        G, disposition, node_size=tailles_noeuds,
        node_color="#4C9BE8", edgecolors="black", ax=ax,
    )
    nx.draw_networkx_edges(
        G, disposition, arrowstyle="-|>", arrowsize=15,
        edge_color="gray", connectionstyle="arc3,rad=0.05", ax=ax,
    )
    nx.draw_networkx_labels(G, disposition, font_size=10, font_weight="bold", ax=ax)

    ax.set_title("Réseau social — taille des noeuds proportionnelle au PageRank")
    ax.axis("off")
    st.pyplot(fig)

st.markdown("---")
st.caption(
    "Graphe généré avec NetworkX · Visualisation Matplotlib · "
    "Application hébergée avec Streamlit"
    "Team Overflow" 
)
