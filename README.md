# MCP Tool Generator (Python)

This project is a Python implementation of the **MCP Tool Generator**, a system for generating development tools from API specifications. It serves as the reference implementation for the architecture and technical plan provided.

## Overview

The core purpose of this tool is to automate the creation of a robust, production-ready toolchain from a formal API specification. The workflow is as follows:

1.  **Parse**: An API specification (currently OpenAPI v2/v3) is parsed, validated, and transformed into a standardized **Intermediate Representation (IR)**. This IR is a clean, language-agnostic model of the API's capabilities.
2.  **Generate**: The IR is used as a blueprint to generate source code for a specific target. The currently supported target is a **FastAPI + FastMCP** project, which creates a runnable server with a set of MCP Tools corresponding to the API operations.

## Project Structure

The project is a Python monorepo with the following structure:

```
├── .gitignore
├── LICENSE
├── README.md
├── examples/
│   └── openapi-petstore/
│       └── spec.yaml
├── pyproject.toml
├── schemas/
│   ├── ir.schema.json
│   └── tool-manifest.schema.json
└── src/
    └── mcpgen/
        ├── __init__.py
        ├── __main__.py     # CLI entry point
        ├── generator.py    # Code generation logic
        ├── ir.py           # IR data model (dataclasses)
        ├── parser.py       # Spec parsing and transformation
        ├── transformer.py  # OpenAPI -> IR transformation logic
        └── validator.py    # IR validation (placeholder)
```

## Installation

To get started, it is recommended to use a virtual environment.

1.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install the project in editable mode:**

    This will install the `mcpgen` package and all its dependencies.

    ```bash
    pip install -e .
    ```

## Usage

The primary entry point is the `mcpgen` command-line interface.

### `parse` Command

The `parse` command reads an API specification file, transforms it into the Intermediate Representation (IR), and outputs the result as a JSON file.

**Usage:**

```bash
mcpgen parse --in <path-to-spec> --out <path-to-output-ir.json>
```

**Arguments:**

*   `--in`: Path to the input specification file (e.g., `examples/openapi-petstore/spec.yaml`).
*   `--out`: (Optional) Path to the output IR file. If not provided, the IR will be printed to standard output.

**Example:**

```bash
mcpgen parse --in examples/openapi-petstore/spec.yaml --out petstore_ir.json
```

### `gen` Command

The `gen` command takes an IR JSON file and generates a complete, runnable FastAPI + FastMCP project.

**Usage:**

```bash
mcpgen gen --in <path-to-ir.json> --out <output-directory>
```

**Arguments:**

*   `--in`: Path to the input IR JSON file.
*   `--out`: The directory where the generated project will be saved.

**Example:**

```bash
mcpgen gen --in petstore_ir.json --out ./generated_project
```

This will create a `generated_project` directory with a runnable FastAPI application.

## Development

To set up the project for development, follow the installation instructions above. The project uses standard Python tooling.

*   **Dependencies:** Project dependencies are managed in `pyproject.toml`.
*   **Running the CLI locally:** You can run the CLI directly as a module:

    ```bash
    python -m src.mcpgen <command> [options]
    ```
