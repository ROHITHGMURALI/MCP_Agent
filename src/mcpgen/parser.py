import yaml
import json
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def parse_spec(spec_path: str) -> dict:
    """
    Parses and validates an OpenAPI specification, then transforms it into the IR format.
    """
    spec_dict, _ = read_from_filename(spec_path)
    validate(spec_dict)

    ir = {}

    # --- Transform Info/Service ---
    info = spec_dict.get("info", {})
    ir["service"] = {
        "id": to_camel_case(info.get("title", "")),
        "title": info.get("title", ""),
        "version": info.get("version", ""),
        "description": info.get("description", ""),
    }

    # --- Transform Servers ---
    servers = []
    if "servers" in spec_dict: # OpenAPI 3.x
        for server in spec_dict["servers"]:
            servers.append({
                "url": server["url"],
                "variables": server.get("variables", {}),
            })
    elif "host" in spec_dict: # OpenAPI 2.x
        host = spec_dict["host"]
        base_path = spec_dict.get("basePath", "")
        schemes = spec_dict.get("schemes", ["http"])
        for scheme in schemes:
            servers.append({
                "url": f"{scheme}://{host}{base_path}"
            })
    ir["servers"] = servers

    return ir
