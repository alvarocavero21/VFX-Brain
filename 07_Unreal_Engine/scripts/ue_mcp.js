// Cliente MCP minimo para el servidor de Unreal 5.8 (http://localhost:8000/mcp).
// Uso:
//   node ue_mcp.js tools                         -> lista meta-tools
//   node ue_mcp.js call <tool> '<json args>'     -> llama a una tool
// Guarda la sesion en ue_mcp_session.txt para reutilizarla entre llamadas.
const fs = require("fs");
const path = require("path");
const URL = process.env.UE_MCP_URL || "http://127.0.0.1:8000/mcp";
const SESSION_FILE = path.join(__dirname, "ue_mcp_session.txt");
let id = 1;

async function rpc(method, params, session) {
  const headers = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };
  if (session) headers["Mcp-Session-Id"] = session;
  const body = { jsonrpc: "2.0", method, params };
  if (!method.startsWith("notifications/")) body.id = id++;
  const res = await fetch(URL, { method: "POST", headers, body: JSON.stringify(body) });
  const sid = res.headers.get("mcp-session-id");
  const text = await res.text();
  let json = null;
  if (text) {
    // respuesta JSON directa o SSE (lineas "data: {...}")
    const dataLines = text.split("\n").filter((l) => l.startsWith("data:"));
    const raw = dataLines.length ? dataLines[dataLines.length - 1].slice(5) : text;
    try { json = JSON.parse(raw); } catch { json = { raw: text }; }
  }
  return { status: res.status, sid, json };
}

async function session() {
  if (fs.existsSync(SESSION_FILE)) {
    const s = fs.readFileSync(SESSION_FILE, "utf8").trim();
    const probe = await rpc("tools/list", {}, s);
    if (probe.status === 200 && !probe.json?.error) return s;
  }
  const init = await rpc("initialize", {
    protocolVersion: "2025-06-18",
    capabilities: {},
    clientInfo: { name: "vfxbrain-cli", version: "1" },
  });
  if (!init.sid) throw new Error("Sin Mcp-Session-Id: " + JSON.stringify(init));
  await rpc("notifications/initialized", {}, init.sid);
  fs.writeFileSync(SESSION_FILE, init.sid);
  return init.sid;
}

(async () => {
  const [cmd, tool, args] = process.argv.slice(2);
  const s = await session();
  let r;
  if (cmd === "tools") r = await rpc("tools/list", {}, s);
  else if (cmd === "call") r = await rpc("tools/call", { name: tool, arguments: args ? JSON.parse(args) : {} }, s);
  else throw new Error("comando desconocido");
  const out = r.json?.result?.content?.map((c) => c.text ?? JSON.stringify(c)).join("\n") ?? JSON.stringify(r.json, null, 1);
  console.log(out);
})().catch((e) => { console.error("ERROR", e.message); process.exit(1); });
