// Quick script to extract node code from workflow JSON
const fs = require('fs');

const data = fs.readFileSync('/Users/computer/.claude/projects/-Users-computer-coding-stuff/100ebb4f-8855-49dc-9eaf-868434857f31/tool-results/mcp-n8n-mcp-n8n_get_workflow-1769040288133.txt', 'utf8');
const json = JSON.parse(data);
const workflow = JSON.parse(json[0].text);

const node = workflow.data.nodes.find(n => n.id === 'code-convert-pdf');

if (node && node.parameters && node.parameters.jsCode) {
  console.log(node.parameters.jsCode);
} else {
  console.log('Node or code not found');
}
