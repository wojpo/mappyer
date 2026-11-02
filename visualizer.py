from pyvis.network import Network


def visualize(modules_to_files, edges):
    net = Network(
        height="100vh",
        width="100%",
        directed=True,
        bgcolor="#18181B",
        font_color="#FAFAFA",
        neighborhood_highlight=True,
        cdn_resources="in_line",
    )

    net.barnes_hut(
        gravity=-8000,
        central_gravity=0.25,
        spring_length=180,
        spring_strength=0.02,
        damping=0.2,
        overlap=0.5
    )

    nodes = set(modules_to_files)

    for node in nodes:
        net.add_node(
            node,
            label=node,
            title=str(modules_to_files[node]),
            color={
            "background": "#27272A",
            "border": "#52525B",
            "highlight": {
                "background": "#F59E0B",
                "border": "#FBBF24"
                }
            },
            font={"color": "#FAFAFA"})

    for source, target in edges:
        net.add_edge(
            source,
            target,
            color="#71717A",
            width=1.5
        )

    with open("mappyer.html", "w", encoding="utf-8") as file:
        file.write(net.generate_html())