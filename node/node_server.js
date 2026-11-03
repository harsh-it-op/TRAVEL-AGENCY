#!/usr/bin/env node
/**
 * TOURLY – Standalone Node.js Lightweight Server Demonstration (node/node_server.js)
 * Syllabus Requirement:
 * - Create a lightweight standalone HTTP server using built-in Node.js `http` and `url` modules
 * - Avoid external frameworks like Express.js
 * - Handle basic GET requests and return JSON responses
 * - Provide a `/status` server health endpoint and `/api/advisories` travel feed
 *
 * Usage:
 *     node node/node_server.js
 *     Default Port: 4000 (configurable via PORT environment variable)
 */

const http = require("http");
const url = require("url");
const os = require("os");

const PORT = parseInt(process.env.PORT || "4000", 10);
const HOST = process.env.HOST || "127.0.0.1";

const TRAVEL_ADVISORIES = [
    {
        destination: "Manali",
        weather: "8°C Clear Alpine Skies",
        highway_status: "Atal Tunnel & Solang Highway Open",
        recommended_season: "Nov - Jun"
    },
    {
        destination: "Goa",
        weather: "29°C Sunny Coastal Breeze",
        highway_status: "All Coastal Ferry & Water Sports Active",
        recommended_season: "Oct - Apr"
    },
    {
        destination: "Kashmir",
        weather: "6°C Crisp Autumn/Winter Air",
        highway_status: "Srinagar-Gulmarg Gondola Phase 1 & 2 Operational",
        recommended_season: "Year-Round"
    },
    {
        destination: "Dubai",
        weather: "27°C Pleasant Desert Evening",
        highway_status: "International Flights & Desert Camps Operating Normally",
        recommended_season: "Oct - Apr"
    }
];

function createTourlyNodeServer() {
    return http.createServer((req, res) => {
        const parsedUrl = url.parse(req.url, true);
        const pathname = parsedUrl.pathname;

        // Standard CORS and JSON headers
        res.setHeader("Access-Control-Allow-Origin", "*");
        res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
        res.setHeader("Content-Type", "application/json; charset=utf-8");

        if (req.method === "OPTIONS") {
            res.writeHead(204);
            res.end();
            return;
        }

        if (req.method !== "GET") {
            res.writeHead(405);
            res.end(JSON.stringify({
                status: "error",
                message: "Method Not Allowed. This lightweight Node.js service handles GET requests."
            }));
            return;
        }

        // Route 1: Server Status Endpoint (/ or /status)
        if (pathname === "/" || pathname === "/status") {
            res.writeHead(200);
            res.end(JSON.stringify({
                service: "Tourly Lightweight Node.js Micro-Service",
                status: "online",
                primary_backend: "Django MVT + MySQL",
                node_version: process.version,
                uptime_seconds: Math.round(process.uptime()),
                hostname: os.hostname(),
                timestamp: new Date().toISOString(),
                endpoints: ["/status", "/api/advisories", "/api/currency"]
            }, null, 2));
            return;
        }

        // Route 2: Live Travel Advisories & Weather JSON Endpoint (/api/advisories)
        if (pathname === "/api/advisories") {
            const filterDest = (parsedUrl.query.destination || "").toLowerCase();
            const filtered = filterDest
                ? TRAVEL_ADVISORIES.filter(item => item.destination.toLowerCase().includes(filterDest))
                : TRAVEL_ADVISORIES;

            res.writeHead(200);
            res.end(JSON.stringify({
                status: "ok",
                count: filtered.length,
                advisories: filtered
            }, null, 2));
            return;
        }

        // Route 3: Currency Reference Endpoint (/api/currency)
        if (pathname === "/api/currency") {
            const inrAmount = parseFloat(parsedUrl.query.inr || "18500");
            res.writeHead(200);
            res.end(JSON.stringify({
                status: "ok",
                base_currency: "INR",
                amount_inr: inrAmount,
                converted: {
                    USD: Number((inrAmount / 84.0).toFixed(2)),
                    AED: Number((inrAmount / 22.85).toFixed(2)),
                    EUR: Number((inrAmount / 90.5).toFixed(2))
                }
            }, null, 2));
            return;
        }

        // 404 Fallback
        res.writeHead(404);
        res.end(JSON.stringify({
            status: "error",
            message: `Endpoint '${pathname}' not found on Tourly Node.js server.`
        }));
    });
}

if (require.main === module) {
    const server = createTourlyNodeServer();
    server.listen(PORT, HOST, () => {
        console.log(`[Tourly Node.js Server] Listening at http://${HOST}:${PORT}/status`);
    });
}

module.exports = { createTourlyNodeServer };
