# MCP Tool Generator (Python)

This project is a Python implementation of the MCP Tool Generator, a system for generating development tools from API specifications.

## Overview

The system ingests heterogeneous API specifications (OpenAPI/GraphQL/gRPC/Postman/AsyncAPI), normalizes them into a rigorous Intermediate Representation (IR), and generates production-ready MCP tool bundles, runtimes, tests, docs, mocks, and governance.

This Python implementation is a fresh start, focusing on a clean and robust architecture. The core transformation logic is now in place, allowing for the conversion of OpenAPI v2 and v3 specifications into the defined IR format.

## Installation

To install the project and its dependencies, it is recommended to use a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the project in editable mode
pip install -e .
```

## Usage

The primary entry point for the tool is the `mcpgen` command-line interface.

### Parse an API Specification

The `parse` command reads an API specification file, transforms it into the Intermediate Representation (IR), and outputs the result.

```bash
mcpgen parse --in <path-to-spec> --out <path-to-output-ir.json>
```

**Arguments:**

*   `--in`: Path to the input specification file (e.g., `examples/openapi-petstore/spec.yaml`).
*   `--out`: (Optional) Path to the output IR file. If not provided, the IR will be printed to standard output.

**Example:**

```bash
mcpgen parse --in examples/openapi-petstore/spec.yaml
```
