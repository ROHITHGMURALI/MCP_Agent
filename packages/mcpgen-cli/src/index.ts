#!/usr/bin/env node
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { parseOpenApiSpec, transformOpenApiToIr } from 'mcpgen-core';
import path from 'path';

yargs(hideBin(process.argv))
  .command(
    'parse',
    'Parse an API specification file and transform it into the MCP Intermediate Representation.',
    (yargs) => {
      return yargs.option('in', {
        describe: 'Path to the input specification file.',
        type: 'string',
        demandOption: true,
      });
    },
    async (argv) => {
      try {
        // Resolve the file path relative to the current working directory
        const absolutePath = path.resolve(process.cwd(), argv.in);
        console.error(`Parsing spec file at: ${absolutePath}`);

        const spec = await parseOpenApiSpec(absolutePath);
        const ir = transformOpenApiToIr(spec);

        console.log(JSON.stringify(ir, null, 2));
      } catch (error) {
        console.error("Failed to parse and transform the specification:", error);
        process.exit(1);
      }
    }
  )
  .demandCommand(1, 'You need at least one command before moving on')
  .help().argv;
