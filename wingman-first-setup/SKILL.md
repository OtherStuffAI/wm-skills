---
name: wingman-first-setup
description: "Guide a user through a first Wingman Be Free setup: Docker or native Bun Autopilot, Tower workspace, sovereign bot, and Flight Deck connection over HTTPS, local HTTP, or FIPS."
---

# Wingman first setup (pilot v0.3)

Help the user reach a verified loop: their bot runs in their Autopilot, belongs to their Tower workspace, appears in Flight Deck, and answers a test message. This is an interactive setup guide, not an unattended provisioner. Inspect the current release and its documentation before commands; setup contracts can change. Never claim a step succeeded from a command exit code alone.

## Interview and setup manifest

Interview the user in short turns. Inspect the host and existing agent tools first. Ask one decision or two related decisions at a time, explain the consequence, and use an answer already given rather than repeating the question. Do not present an eight-item questionnaire or ask the user to compose a semicolon-separated setup string.

Maintain `.wingman-first-setup.json` in the chosen setup working directory using [the manifest contract](references/setup-manifest.md). Store only choices, public IDs/URLs, observed step states, blockers, and next action; set mode `0600`. Never put signing keys, tokens, passwords, or recovery material in it. Resume from observed state, including existing workspace, bot, and connection records; do not create duplicates after a restart.

Ask in this order unless context has already answered a question:

1. **Tower:** Offer the **Other Stuff Hosted Tower** at `https://tower-stable-api.b.otherstuff.ai/` as the default, or a new self-hosted Tower. Tell the user the hosted offer described for this pilot includes 1 GB per month free, then storage is paid per GB per month; verify the current rate and billing terms before a paid commitment. For self-hosted Tower, establish host, admin authority, and current deployment instructions. Ask whether to use an existing workspace or create one, and its name.
2. **Human identity:** Ask for the user's public `npub`. If they do not have one, offer to install/build Wingman App and generate an identity in its own onboarding vault. Check current Wingman App release/build instructions and platform support before promising an install. Explain that Wingman App's device npub and human account npub are different; use the human npub as Tower owner. Never ask them to send an `nsec`.
3. **Agent runtime:** Ask whether agent tools are already installed on the target computer and whether the user wants to use those installations or keep agents isolated. If using existing tools, prefer native Bun when available. If isolated, select Docker. Inspect actual installed harnesses before asking which one should run the first bot; do not assume the setup-skill installer installed the harness binaries.
4. **Connection:** Ask for target host/OS if it is not the current machine, then choose local HTTP, public HTTPS, FIPS only, or HTTPS plus FIPS. Ask for the bot name. Explain any transport limitation before proceeding.

When the choices and authority are complete, show a short human-readable summary, run `node <skill-directory>/scripts/check-manifest.mjs .wingman-first-setup.json --ready`, then apply its values through the current supported Autopilot, Tower, Wingman App, and transport setup commands below. The manifest is the input to the staged setup; this pilot does not have a single unattended provisioner. Keep the JSON and step evidence current after each operation. An optional form can later produce the same manifest without changing the execution flow.

Public HTTP and FIPS HTTP are distinct. Local HTTP belongs on loopback or an explicitly trusted private test network. Internet access uses HTTPS. A FIPS URL has the form http://<node-npub>.fips:<port>/ and needs a working peer; it is not a public HTTP deployment.

## 1. Preflight authority and source

- Confirm the user controls the target host and is authorized to create the Tower workspace. Identify the exact Tower service and owner. Do not assume Tower admin authority exists.
- Use the user's chosen checkout or current official Autopilot release. Read its README.md, docs/setup.md and relevant FIPS docs, plus repository agent instructions. Do not run a remote installation script unseen.
- Check disk, runtime, Docker Compose v2 or Bun, persistent storage, and the chosen harness's login requirements. Choose a durable process manager for native Bun and record backup/restart ownership.
- Keep owner, Tower service, workspace service, Autopilot installation, FIPS node, and bot npubs distinct. Never ask for an nsec, provider token, or capability in chat or Tower connection metadata. Bot private identity stays in Autopilot's vault; sessions use brokered capabilities.
- The npm installer installs this skill into Codex, Claude Code, Goose, and OpenCode skill directories by default. Verify the chosen agent CLI is actually present and authenticated; install or authenticate it only through its current supported flow.

## 2. Install or inspect Autopilot

- Docker: follow current docs/setup.md. Current source offers bun run docker:provision with --admin-npub, --instance-name, --env, --host-port, --base-url, and --workspace-host-path. Review the generated env without printing secrets. Use docker compose --env-file .env.<name> up -d --build, then require compose ps, bun run docker:check inside the container, health, and recent logs. Docker FIPS is in the main compose file; the old FIPS overlay is compatibility only.
- Native Bun: follow current README and .env.example; install locked dependencies, configure persistent data, owner admin npub, bind/base URL and process manager, then use the documented bun start entry point. A development shell is not the durable server. Verify process, health, logs, and restart policy. Do not copy another machine's .env or keys.
- Existing instance: inspect configuration and health first. Preserve profiles, data, and signing identities. Do not recreate, rotate, or restart merely to make steps uniform.

## 3. Configure transport

- HTTPS: configure TLS reverse proxy and real public origin. Test advertised Autopilot URL, login, health, WebSocket, and SSE through that origin.
- FIPS: follow current OS-specific FIPS installation and ingress docs. Require a ready daemon, a listening descriptor from GET /api/system/fips or bun clis/status.ts fips, the exact mesh URL, paired client node, and actual client request. Local listening does not prove remote access. Never substitute HTTPS while labelling it FIPS. FIPS-only setups must retain workable management access without assuming a public URL.
- Local HTTP: bind to loopback or the explicitly trusted test network. Record that outside clients cannot use it until a transport is added.
- If the product rejects the selected combination, capture the exact validation error and stop that branch. Do not invent an endpoint or bypass identity checks.

## 4. Create or select the Tower workspace

For the selected Tower, list the owner's existing workspaces first and reuse the intended one. Current Tower has an admin-only POST /api/v4/admin/flightdeck-pg/workspaces bootstrap route with workspace_name and creator_npub; it creates the PG workspace and defaults. Use an authorized Tower admin signing path for that exact request or the supported Flight Deck flow. A normal bot or new owner's npub is not automatically a Tower admin. Never seek a human secret as a workaround. If the hosted service lacks a user-authorized workspace creation path, stop at that exact blocker rather than presenting the admin endpoint as a user operation.

Read back the workspace descriptor and membership. Confirm owner npub, creator membership, app namespace, defaults, and that the user can open it in Flight Deck. If no authorized creation path exists, report this blocker precisely.

## 5. Create the bot and connect it

In Autopilot Settings, create a sovereign local agent profile for the selected harness and working directory. Current Settings generates a non-exportable bot identity. Record its public npub and agent ID. Configure harness login in the persistent server/container home without copying credentials into the setup record.

Configure Autopilot's Tower connection for the exact workspace, owner, service, and chosen transport; test before subscribing the bot. Use maintained UI/CLI/API and exact NIP-98 targets with broker authority. Grant only required workspace permissions. A 403 calls for checking target, delegation and route, not extracting a signing key.

Use Autopilot's signed short-lived Connect Package and Flight Deck's Add agent/Autopilot connection flow where available. Verify package, installation identity, and discovered bot before saving. Do not store credentials in Tower metadata. Read back the connection and workspace-agent records and check the expected workspace and bot npub.

Check the live Flight Deck connection form or API contract before creating the connection. The pilot build observed a required `fips_endpoint` even with `https_endpoint`; if that remains true and the user chose HTTPS-only or local HTTP-only, do not fabricate an endpoint. Mark connection blocked by the exact validation result; workspace and bot can still be verified separately.

## 6. Acceptance and handoff

From Flight Deck, open the workspace, see the installed bot, send one tagged test message, and observe the reply in the same thread. For FIPS, test through a paired mesh client; for HTTPS, use the public origin. Check Autopilot logs for the corresponding session and confirm retry created no duplicate records.

Finish with a compact report: hosting mode; transport and tested endpoint; workspace name/ID; bot name/npub; connection/subscription state; health and round-trip evidence; blocked step with exact error; next safe action. Never call the setup ready until the round trip works.
