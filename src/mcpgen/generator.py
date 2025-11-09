from pathlib import Path
import json
from .ir import IR

def load_ir(ir_path: str) -> IR:
    """Loads an Intermediate Representation (IR) file."""
    with open(ir_path, "r") as f:
        ir_dict = json.load(f)
    return IR.from_dict(ir_dict)

def generate_fastapi_project(ir_path: str, out_dir: str):
    """
    Generates a FastAPI project from an Intermediate Representation (IR) file.
    """
    ir = load_ir(ir_path)

    print(f"Generating FastAPI project for service: {ir.service.title}")

    # Create the output directory structure
    app_dir = Path(out_dir) / "app"
    app_dir.mkdir(parents=True, exist_ok=True)

    # --- Generate models.py ---
    models_content = generate_models(ir)
    (app_dir / "models.py").write_text(models_content)

    # --- Generate tools.py ---
    tools_content = generate_tools(ir)
    (app_dir / "tools.py").write_text(tools_content)

    # --- Generate main.py ---
    main_content = generate_main()
    (app_dir / "main.py").write_text(main_content)

    # --- Generate requirements.txt ---
    req_content = generate_requirements()
    (Path(out_dir) / "requirements.txt").write_text(req_content)

    # --- Generate __init__.py ---
    (app_dir / "__init__.py").touch()

def generate_models(ir: IR) -> str:
    """Generates the content for the models.py file."""
    content = "from pydantic import BaseModel\nfrom typing import List, Optional, Any\n\n"

    type_map = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
    }

    type_id_to_name = {t.id: t.name for t in ir.types}

    for ir_type in ir.types:
        if ir_type.kind == "object":
            content += f"class {ir_type.name}(BaseModel):\n"
            if not ir_type.properties:
                content += "    pass\n\n"
            for prop_name, prop_ref in ir_type.properties.items():
                py_type = type_id_to_name.get(prop_ref.typeId, "Any")

                is_required = prop_name in ir_type.required
                if not is_required:
                    py_type = f"Optional[{py_type}] = None"

                content += f"    {prop_name}: {py_type}\n"
            content += "\n"

    for op in ir.operations:
        model_name = f"{op.name.capitalize()}Input"
        content += f"class {model_name}(BaseModel):\n"
        if not op.inputs.queryParams and not op.inputs.body:
             content += "    pass\n\n"
        for param_name, param_ref in op.inputs.queryParams.items():
            py_type = type_map.get(param_ref.typeId, "str") # Simplified
            content += f"    {param_name}: Optional[{py_type}] = None\n"

        if op.inputs.body:
            ref_type = type_id_to_name.get(op.inputs.body.schema_ref.typeId)
            if ref_type:
                content += f"    body: {ref_type}\n"
        content += "\n"

    return content

def generate_main() -> str:
    """Generates the content for the main.py file."""
    return '''
from fastapi import FastAPI
from fastmcp.router import MCPRouter
from . import tools

app = FastAPI()
mcp_router = MCPRouter(tools_module=tools)
app.include_router(mcp_router)
'''

def generate_requirements() -> str:
    """Generates the content for the requirements.txt file."""
    return '''
fastapi
uvicorn
fastmcp
dataclasses-json
'''

def generate_tools(ir: IR) -> str:
    """Generates the content for the tools.py file."""
    content = "from fastmcp.tool import mcp_tool\nfrom .models import *\nfrom typing import Any\n\n"
    type_id_to_name = {t.id: t.name for t in ir.types}

    for op in ir.operations:
        input_model_name = f"{op.name.capitalize()}Input"

        output_type = "Any"
        if op.outputs.success:
            ref_type_id = op.outputs.success[0].schema_ref.typeId
            ref_type = type_id_to_name.get(ref_type_id)
            if ref_type:
                output_type = ref_type

        content += f"@mcp_tool(name='{op.name}', description='{op.summary or ''}')\n"
        content += f"def {op.name}(input: {input_model_name}) -> {output_type}:\n"
        content += f'    """{op.description or ""}"""\n'
        content += f"    # TODO: Implement the tool logic here\n"
        content += f"    print(f'Running tool {op.name} with input: {{input}}')\n"
        content += f"    return {{}}\n\n"

    return content
