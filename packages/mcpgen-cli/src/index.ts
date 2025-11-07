#!/usr/bin/env node
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

yargs(hideBin(process.argv))
  .command(
    'parse',
    'Parse an API specification file.',
    (yargs) => {
      return yargs.option('in', {
        describe: 'Path to the input specification file.',
        type: 'string',
        demandOption: true,
      });
    },
    (argv) => {
      console.log(`Placeholder: Parsing spec file at: ${argv.in}`);
    }
  )
  .demandCommand(1, 'You need at least one command before moving on')
  .help().argv;
