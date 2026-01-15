#!/usr/bin/env node
const https = require("https");
const { URL } = require("url");

const baseUrl = process.env.N8N_BASE_URL;
const apiKey = process.env.N8N_API_KEY;
if (!baseUrl || !apiKey) {
  console.error("Set N8N_BASE_URL and N8N_API_KEY in your shell before running this helper.");
  process.exit(1);
}

const [tool, workflowId, payloadJson] = process.argv.slice(2);

const call = (method, path, body) => {
  const url = new URL(path, baseUrl);
  const options = {
    method,
    headers: {
      "X-N8N-API-KEY": apiKey,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  };
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve({ status: res.statusCode, body: data }));
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
};

(async () => {
  try {
    let response;
    switch (tool) {
      case "list_workflows":
        response = await call("GET", "/api/v1/workflows");
        break;
      case "get_workflow":
        response = await call("GET", `/api/v1/workflows/${workflowId}`);
        break;
      case "create_workflow":
        response = await call("POST", "/api/v1/workflows", JSON.parse(payloadJson));
        break;
      case "update_workflow":
        response = await call("PUT", `/api/v1/workflows/${workflowId}`, JSON.parse(payloadJson));
        break;
      case "delete_workflow":
        response = await call("DELETE", `/api/v1/workflows/${workflowId}`);
        break;
      default:
        throw new Error("Unknown tool. Try list_workflows, get_workflow, create_workflow, update_workflow, or delete_workflow.");
    }
    console.log(response.body);
  } catch (error) {
    console.error("Helper error:", error.message);
    process.exit(1);
  }
})();
