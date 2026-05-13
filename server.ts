import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";

async function startServer() {
  const app = express();
  const PORT = 3000;

  // Middleware for JSON
  app.use(express.json());

  // API routes
  app.get("/api/health", (req, res) => {
    res.json({ 
      status: "online", 
      type: "Minecraft Infrastructure",
      region: "europe-west2",
      nodes: 42,
      latency: "8ms",
      uptime: process.uptime()
    });
  });

  // Simulation endpoint for Minecraft Terminal
  app.post("/api/terminal/exec", (req, res) => {
    const { command, instanceId } = req.body;
    let output = "";
    const cmd = command.toLowerCase().trim();
    
    if (cmd === "list") {
      output = "There are 0 of a max 20 players online.";
    } else if (cmd === "tps") {
      output = "TPS from last 1m, 5m, 15m: 20.0, 20.0, 19.98";
    } else if (cmd === "version") {
      output = "This server is running Paper version git-Paper-448 (MC: 1.20.4) (Implementing API version 1.20.4-R0.1-SNAPSHOT)";
    } else if (cmd === "whoami") {
      output = "mc_server_admin";
    } else if (cmd === "df -h") {
      output = "Filesystem      Size  Used Avail Use% Mounted on\n/dev/nvme0n1p1   120G   8G   112G   7% /home/minecraft";
    } else if (cmd === "plugins") {
      output = `Plugins (3): EssentialsX*, LuckPerms*, Vault*`;
    } else if (cmd.startsWith("op ")) {
      output = `Made ${command.split(' ')[1]} a server operator`;
    } else if (cmd === "help") {
      output = "MC Commands: list, tps, version, plugins, op [player], whitelist [add|remove], kick [player], stop, restart";
    } else {
      output = `Unknown command. Type "help" for help.`;
    }

    res.json({ output });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`CloudEngine Backend running on http://localhost:${PORT}`);
  });
}

startServer();
