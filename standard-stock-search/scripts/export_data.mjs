import fs from 'node:fs/promises';
import {buildSheets} from './report_data.mjs';
const [mode,input]=process.argv.slice(2);
try{console.log(JSON.stringify(buildSheets(mode,JSON.parse(await fs.readFile(input,'utf8')))));}
catch(e){console.error(e.message);process.exitCode=1;}
