# Mappyer

Mappyer is a Python CLI tool that generates interactive dependency graphs for Python projects. 

Mappyer was built using Python's built-in Abstract Syntax Tree (AST) module to analyze import statements without executing the source code. It recursively scans Python files, resolves local module dependencies, and uses PyVis to generate an interactive HTML graph. Each node represents a module, while directed edges show import relationships.

The generated graph supports zooming, dragging, module highlighting, and file path tooltips. Everything runs locally, and the resulting HTML file can be opened directly in a browser.

## Features

- Recursive Python file scanning
- Absolute and relative import resolution
- Support for `src/` layouts
- Interactive dependency graphs
- Standalone HTML export

## Installation

Requires Python 3.10+.

```bash
pip install git+https://github.com/wojpo/mappyer.git@v0.1.0
```

## Usage

Analyze the current directory:

```bash
mappyer .
```

Analyze another project with a custom output path:

```bash
mappyer ./my-project -o dependencies.html
```

Open the generated HTML file in your browser to explore the dependencies.

## Development

```bash
git clone https://github.com/wojpo/mappyer.git
cd mappyer
pip install -e .
pip install pytest
python -m pytest
```

## Tech Stack

Python · AST · PyVis · pytest