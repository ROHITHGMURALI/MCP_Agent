from typing import Dict, List, Any
from .ir import Type, TypeRef, Constraints, Operation, Inputs, Outputs, Body, Response, SecurityScheme
import hashlib
import json

def stable_id(data: Any) -> str:
    """Creates a stable SHA256 hash from a JSON-serializable dictionary."""
    # Exclude 'description' and other non-structural fields for stability
    structural_data = data.copy()
    if 'description' in structural_data:
        del structural_data['description']

    encoded = json.dumps(structural_data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

def get_schemas(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Gets the schema definitions from either OpenAPI 2.x or 3.x."""
    if "components" in spec and "schemas" in spec["components"]:
        return spec["components"]["schemas"]
    elif "definitions" in spec:
        return spec["definitions"]
    return {}

def resolve_ref(ref: str) -> str:
    """Resolves a local JSON schema reference."""
    if ref.startswith("#/definitions/"):
        return ref[len("#/definitions/"):]
    if ref.startswith("#/components/schemas/"):
        return ref[len("#/components/schemas/"):]
    raise ValueError(f"Unsupported reference format: {ref}")

def transform_schemas(spec: Dict[str, Any]) -> List[Type]:
    """Transforms OpenAPI schemas into a list of IR Type objects."""
    types = []
    schemas = get_schemas(spec)

    for name, schema in schemas.items():
        kind = schema.get("type", "object")
        type_id = stable_id(schema)

        properties = {}
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                if "$ref" in prop_schema:
                    ref_name = resolve_ref(prop_schema["$ref"])
                    # Find the referenced schema to generate its stable ID
                    ref_schema = schemas.get(ref_name, {})
                    properties[prop_name] = TypeRef(typeId=stable_id(ref_schema))
                else:
                    inline_type_id = stable_id(prop_schema)
                    properties[prop_name] = TypeRef(typeId=inline_type_id)

        items = None
        if kind == "array" and "items" in schema:
            if "$ref" in schema["items"]:
                ref_name = resolve_ref(schema["items"]["$ref"])
                ref_schema = schemas.get(ref_name, {})
                items = TypeRef(typeId=stable_id(ref_schema))

        constraints = Constraints(
            minLength=schema.get("minLength"),
            maxLength=schema.get("maxLength"),
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
            pattern=schema.get("pattern"),
        )

        ir_type = Type(
            id=type_id,
            name=name,
            kind=kind,
            description=schema.get("description"),
            properties=properties,
            required=schema.get("required", []),
            items=items,
            enum=schema.get("enum", []),
            allOf=[TypeRef(typeId=stable_id(schemas.get(resolve_ref(s["$ref"]), {}))) for s in schema.get("allOf", [])],
            oneOf=[TypeRef(typeId=stable_id(schemas.get(resolve_ref(s["$ref"]), {}))) for s in schema.get("oneOf", [])],
            constraints=constraints,
        )
        types.append(ir_type)

    return types

def transform_paths(spec: Dict[str, Any]) -> List[Operation]:
    """Transforms OpenAPI paths into a list of IR Operation objects."""
    operations = []
    paths = spec.get("paths", {})
    schemas = get_schemas(spec)

    for path, path_item in paths.items():
        for method, op_spec in path_item.items():
            if method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]:
                continue

            operation_id = op_spec.get("operationId")
            if not operation_id:
                continue

            # --- Inputs ---
            inputs = Inputs()
            for param in op_spec.get("parameters", []):
                param_schema = param.get("schema", {})
                if "$ref" in param_schema:
                    ref_name = resolve_ref(param_schema["$ref"])
                    ref_schema = schemas.get(ref_name, {})
                    type_ref = TypeRef(typeId=stable_id(ref_schema))
                else:
                    type_ref = TypeRef(typeId=stable_id(param))

                if param["in"] == "path":
                    inputs.pathParams[param["name"]] = type_ref
                elif param["in"] == "query":
                    inputs.queryParams[param["name"]] = type_ref
                elif param["in"] == "header":
                    inputs.headers[param["name"]] = type_ref
                elif param["in"] == "body":
                    inputs.body = Body(contentTypes=["application/json"], schema_ref=type_ref)

            # --- Outputs ---
            outputs = Outputs()
            for status_code, resp_spec in op_spec.get("responses", {}).items():
                if status_code.startswith('2'):
                    schema_ref = resp_spec.get("schema", {}).get("$ref")
                    if schema_ref:
                        ref_name = resolve_ref(schema_ref)
                        ref_schema = schemas.get(ref_name, {})
                        outputs.success.append(Response(
                            status=int(status_code),
                            contentTypes=list(resp_spec.get("content", {}).keys()),
                            schema_ref=TypeRef(typeId=stable_id(ref_schema))
                        ))

            ir_op = Operation(
                id=stable_id(op_spec),
                name=operation_id,
                transport="http",
                method=method.upper(),
                pathTemplate=path,
                summary=op_spec.get("summary"),
                description=op_spec.get("description"),
                tags=op_spec.get("tags", []),
                inputs=inputs,
                outputs=outputs,
            )
            operations.append(ir_op)

    return operations

def get_security_schemes(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Gets the security scheme definitions from either OpenAPI 2.x or 3.x."""
    if "components" in spec and "securitySchemes" in spec["components"]:
        return spec["components"]["securitySchemes"]
    elif "securityDefinitions" in spec:
        return spec["securityDefinitions"]
    return {}

def transform_security_schemes(spec: Dict[str, Any]) -> List[SecurityScheme]:
    """Transforms OpenAPI security schemes into a list of IR SecurityScheme objects."""
    schemes = []
    security_schemes = get_security_schemes(spec)

    for name, scheme_spec in security_schemes.items():
        scheme = SecurityScheme(
            id=stable_id(scheme_spec),
            name=name,
            type=scheme_spec.get("type"),
            in_val=scheme_spec.get("in"),
            scheme=scheme_spec.get("scheme"),
        )
        schemes.append(scheme)

    return schemes
