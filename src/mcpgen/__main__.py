import argparse
import sys
import json
from mcpgen.parser import parse_spec

def main():
    parser = argparse.ArgumentParser(description="MCP Tool Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Parse Command ---
    parse_parser = subparsers.add_parser("parse", help="Parse an API specification file.")
    parse_parser.add_argument("--in", dest="in_file", required=True, help="Path to the input specification file.")
    parse_parser.add_argument("--out", dest="out_file", help="Path to the output IR file. If not provided, prints to stdout.")

    # --- Gen Command ---
    gen_parser = subparsers.add_parser("gen", help="Generate a FastAPI project from an IR file.")
    gen_parser.add_argument("--in", dest="in_file", required=True, help="Path to the input IR JSON file.")
    gen_parser.add_argument("--out", dest="out_dir", required=True, help="Path to the output directory for the generated project.")

    args = parser.parse_args()

    if args.command == "parse":
        try:
            ir = parse_spec(args.in_file)
            output = json.dumps(ir, indent=2)
            if args.out_file:
                with open(args.out_file, "w") as f:
                    f.write(output)
                print(f"Successfully wrote IR to {args.out_file}")
            else:
                print(output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "gen":
        from mcpgen.generator import generate_fastapi_project
        try:
            generate_fastapi_project(args.in_file, args.out_dir)
            print("Successfully generated FastAPI project.")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
