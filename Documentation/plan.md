# Plan: MCP Server for Content & Image Generation

## TL;DR
Create a Node.js (TypeScript) MCP server that exposes content generation, image generation, and prompt management tools to VS Code Copilot. The server connects directly to the existing PostgreSQL database for prompts/settings and calls the same AI providers (OpenAI, Gemini, OpenRouter) already used by the Python news-engine. Configured via `.vscode/mcp.json` for stdio transport.

## Phase 1: Project Scaffold

1. Create `mcp-server/` directory at the workspace root
2. Initialize `package.json` with dependencies:
   - `@modelcontextprotocol/sdk` (MCP SDK)
   - `openai` (covers OpenAI + OpenRouter via base_url)
   - `@google/genai` (Gemini SDK for content + image)
   - `pg` (PostgreSQL driver)
   - `dotenv`
   - `zod` (for tool input validation — required by MCP SDK)
   - Dev: `typescript`, `@types/node`, `@types/pg`, `tsx`
3. Create `tsconfig.json` targeting ES2022, module NodeNext
4. Add npm scripts: `build`, `start` (runs compiled JS), `dev` (runs via `tsx`)

## Phase 2: Core Infrastructure

5. **`mcp-server/src/config.ts`** — Load env vars (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, plus all AI provider keys from the same `.env` as news-engine). Match defaults from `backend/src/config/db.js`: host=localhost, port=5432, user=postgres, db=strapi
6. **`mcp-server/src/db.ts`** — PostgreSQL pool (pg.Pool), with helper `query()` function. Same connection params as `backend/src/config/db.js` (max:20, idle 30s, connect 5s)
7. **`mcp-server/src/index.ts`** — MCP server entry point using `@modelcontextprotocol/sdk`. Register all tools, use stdio transport (`StdioServerTransport`). Register server name `"content-image-gen"`.

## Phase 3: Content Generation Tool

8. **`mcp-server/src/tools/content.ts`** — `generate_content` tool
   - **Inputs** (Zod schema): `prompt` (string, required), `provider` (enum: openai | gemini | openrouter, optional — falls back to DB `ai_settings.content_provider`), `model` (string, optional — falls back to DB setting), `max_tokens` (number, optional, default 2000), `temperature` (number, optional, default 1)
   - **Logic**: Mirror `generate_openai_content()` from `news-engine/publication/utils.py` L217+:
     - **OpenAI**: Use `openai` SDK with `OPENAI_API_KEY`, configurable model
     - **Gemini**: Use `@google/genai` with key rotation from `GOOGLE_GEMINI_API_KEYS` (comma-separated), retry on 429 with backoff (match Python logic)
     - **OpenRouter**: Use `openai` SDK with `base_url: "https://openrouter.ai/api/v1"`, `OPEN_ROUTER_API_KEY`
   - **Returns**: Generated text content

## Phase 4: Image Generation Tool

9. **`mcp-server/src/tools/image.ts`** — `generate_image` tool
   - **Inputs**: `prompt` (string, required), `provider` (enum: openrouter | imagen | gemini-flash-image, optional — falls back to `ai_settings.image_provider`), `save_path` (string, optional — defaults to `result/images/{date}/`)
   - **Logic**: Mirror image generation from `news-engine/publication/utils.py`:
     - **OpenRouter** (L54): POST to `https://openrouter.ai/api/v1/chat/completions` with image modality, parse base64 or URL response
     - **Imagen** (L487): Use `@google/genai` `imagen-3.0-generate-002` model
     - **Gemini Flash Image** (L590): Use `gemini-3.1-flash-image-preview` with `response_modalities: ['TEXT', 'IMAGE']`, extract `inline_data` from response parts
   - **Returns**: Base64 image data + file path if saved locally

## Phase 5: Prompt Management Tools

10. **`mcp-server/src/tools/prompts.ts`** — Three tools:
    - `list_prompts` — No inputs. Query `SELECT * FROM news_prompts LIMIT 1` (single-row config table). Return all prompt fields.
    - `get_prompt` — Input: `field` (enum of prompt column names). Return that specific prompt template.
    - `update_prompt` — Inputs: `field` (enum), `value` (string). Execute `UPDATE news_prompts SET {field} = $1`. Use parameterized query to prevent SQL injection. Return confirmation.
    - Prompt fields (from existing schema): `social_media_news_title_prompt`, `social_media_news_image_prompt`, `social_media_news_content_prompt`, `ai_tone`, `ai_language`, `ai_max_words`

11. **`mcp-server/src/tools/ai-settings.ts`** — Two tools:
    - `get_ai_settings` — Query `SELECT * FROM ai_settings LIMIT 1`. Mask sensitive API keys (show first 4 + last 4 chars, matching backend behavior).
    - `update_ai_settings` — Inputs: `field` (enum of setting columns), `value` (string). Parameterized UPDATE. Only allow non-sensitive fields (provider, model, temperature, max_tokens) — block direct API key updates via tool for security.

## Phase 6: VS Code Integration

12. Create `.vscode/mcp.json` at workspace root:
    ```
    servers:
      content-image-gen:
        type: stdio
        command: npx
        args: [tsx, mcp-server/src/index.ts]
        env: (inherit from .env or specify DB/API keys)
    ```
13. Add `mcp-server/.env.example` documenting all required env vars

## Relevant Files

- `news-engine/publication/utils.py` — Reference implementation: `generate_openai_content()` (L217), `generate_gemini_image()` (L145), `generate_openRouter_image()` (L54), `generate_imagen_image()` (L487), `generate_gemini_flash_image()` (L590)
- `news-engine/social_media/image_social_media_api.py` — `generate_post_image()` for template variable system
- `backend/src/config/db.js` — Database connection params to match
- `backend/src/routes/aiSettings.js` — AI settings schema and API key masking pattern
- `backend/src/routes/prompts.js` — Prompt field names and validation
- `news-engine/requirements.txt` — Python deps for reference (map to Node equivalents)
- `docker-compose.yml` — Service architecture, DB connection details

## Verification

1. Run `cd mcp-server && npm run build` — should compile with zero errors
2. Run `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | npx tsx src/index.ts` — should return all 7 tools
3. Open VS Code, open Copilot Chat in Agent mode, verify "content-image-gen" appears as available MCP server
4. Test `generate_content` tool: ask Copilot to "generate a news article about transfer rumors" — should invoke the tool and return LLM output
5. Test `generate_image` tool: ask Copilot to "create an image for a football transfer story" — should return base64 image
6. Test `list_prompts` and `get_ai_settings` — should return current DB values
7. Test `update_prompt` — verify DB is updated

## Decisions

- **Language**: Node.js/TypeScript (user choice) — requires porting Python AI logic to TS
- **Transport**: stdio (standard for VS Code MCP integration)
- **DB access**: Direct PostgreSQL connection (user choice) — same pool config as backend
- **Security**: API keys masked in `get_ai_settings` output; `update_ai_settings` blocks direct key modification; parameterized SQL queries throughout
- **Scope included**: Content gen, image gen, prompt CRUD, AI settings read/limited update
- **Scope excluded**: Social media scraping tools, WordPress publishing tools, cron management — these stay in their existing services
- **Image output**: Returns base64 + optional local file save (no S3 upload from MCP — that's the news-engine's job)

## New Files to Create (7)

1. `mcp-server/package.json`
2. `mcp-server/tsconfig.json`
3. `mcp-server/src/index.ts`
4. `mcp-server/src/config.ts`
5. `mcp-server/src/db.ts`
6. `mcp-server/src/tools/content.ts`
7. `mcp-server/src/tools/image.ts`
8. `mcp-server/src/tools/prompts.ts`
9. `mcp-server/src/tools/ai-settings.ts`
10. `mcp-server/.env.example`
11. `.vscode/mcp.json`
