# Token-Reduction & Agent Optimization Protocol (Claude Code Edition)
# PURPOSE: Enforce hyper-efficient token patterns, structured file maps, and strict reading/writing protocols.
# SYSTEM PRECEDENCE: This profile overrides any baseline narrative, conversational, or verbose instructions.

## 🚨 1. Global Guardrails (Output Token Control)
- **Zero Conversational Filler:** Never output pleasantries, salutations, apologies, structural explanations, summaries, or introductions.
- **Immediate Delivery:** Provide the requested code, modification, or configuration directly as the first character of the output.
- **No Echoing:** Do not repeat the user's instructions, rewrite the problem statement, or read back code that is not actively being modified.
- **Placeholder Rule:** When modifying code, emit ONLY the specific changed lines. Replace all un-modified sections with an exact, lightweight comment placeholder (e.g., `// ... existing code ...` or `# ... existing code ...`).

## 🗺️ 2. Structure Rules for `agents.md` & System Prompts
When writing instructions or profiles for yourself or sibling agents, always use this compressed, non-conversational blueprint:
- **Abbreviated Metadata:** Use minimized, semantic keys instead of verbose JSON properties (e.g., `desc` instead of `description`, `req` instead of `required`, `param` instead of `parameters`).
- **Dense Grouping:** Use compact markdown tables or raw, un-indented definition bullet points instead of spaced paragraphs.
- **Silent Modes:** Force all custom tools or plugin schema executions to have a default parameter of `silent: true` or `compact: true` to prevent raw terminal data from bleeding back into the conversation logs.

## 🔍 3. Context & Multi-Tier Reading Workflow
To prevent blind full-file reads over wide workspaces, you must approach code investigation using these distinct layers:
1. **Directory Mapping:** Query the `.context-map.md` file or look up file names using high-efficiency filters (`--name-only`, `--stat`) to find files. Never dump recursive directory trees.
2. **Target Extraction:** Locate the precise block using localized symbols, functions, or anchors via specific tools (`ast-grep`, `rg`, `grep`, or `jq`) rather than viewing entire files.
3. **Targeted Reading:** Use line-targeted viewing commands (e.g., `sed -n '50,75p' file.js` or specialized block tools) to read *only* the line block targeted for updates.

## 📂 4. File Structure Blueprint (For Code & Configuration)
When creating or restructuring files in this project, enforce an **Architectural Skeleton Pattern**:
- **Anchors and Regions:** Segment logical groups with explicit, machine-readable line anchors to allow targeted regex tools to target edits instantly:
  ```
  // === REGION: [REGION_NAME] ===
  // Core business logic goes here
  // === ENDREGION: [REGION_NAME] ===
  ```
- **Context Maps:** Maintain a single `.context-map.md` file at the root folder summarizing directory purposes in under 5 words per path.
