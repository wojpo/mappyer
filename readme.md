# Mappyer

Python cli tool that generates graphs for projects local dependencies analysis

Mappyer uses python AST to analyze imports, resolve local module dependencies, and visualize them using PyVis

## Features

- Recursive Python file scanning
- Absolute and relative import resolution
- Interactive, directed dependency graphs
- Module highlighting and file path tooltips
- Standalone HTML export

## Usage

Analyze the current directory:

`mappyer .`

Analyze another project and specify the output:

`mappyer ./my-project -o dependencies.html`

Open the generated HTML file in your browser to explore the graph.

## Development

```git clone https://github.com/wojpo/mappyer.git
cd mappyer
pip install -e .
pip install pytest
python -m pytest
```

Tech Stack

- Python
- PyVis
- pytest