# PRD: Siri Redirect — Voice-Triggered AI Voice Mode Launchers (iPhone)

## Goal

Ship a tiny side project that lets anyone with an iPhone trigger the native voice-conversation mode of major AI apps with a single Siri phrase. The deliverable is a small set of one-tap-install iOS Shortcuts.

## Scope (v1)

Two trigger phrases, both prefixed with "Hey Siri":

| Trigger phrase | Result |
|---|---|
| "Hey Siri, ChatGPT voice" | ChatGPT app opens directly into its voice-conversation mode |
| "Hey Siri, Gemini live" | Gemini app opens directly into Gemini Live |

Deliverable artifacts:
- Two iCloud Shortcut share links (one per app)
- A README with screenshots and copy-pasteable install steps
- Optional: a single-page site, a RoutineHub submission

**Claude is intentionally not in v1.** See "Findings: Claude voice-mode limitation" below for the documented reasons.

## Why this scope is fully shareable

iOS Shortcuts created in the Shortcuts app can be exported as iCloud links (`icloud.com/shortcuts/...`). Tapping such a link on iPhone imports the shortcut directly into the user's library. Once imported, "Hey Siri, [shortcut name]" runs it — no Settings dive, no accessibility configuration, no per-device training, no manual phrase recording.

This is the only iOS distribution path that is genuinely one-tap for end users. Voice Control commands and Vocal Shortcut trigger phrases live in `Settings → Accessibility` and have no export format, so anything that depends on them cannot be shared as an artifact.

## Implementation plan

### Step 1 — Build `ChatGPT voice` shortcut
In the Shortcuts app on iPhone:
- New Shortcut → Add Action → search "ChatGPT" → select **Start voice conversation with ChatGPT**
- Name it `ChatGPT voice`
- Verify with "Hey Siri, ChatGPT voice" — should land directly in voice mode

### Step 2 — Build `Gemini live` shortcut
- New Shortcut → Add Action → search "Gemini" → select **Talk Live with Gemini**
- Name it `Gemini live`
- Verify with "Hey Siri, Gemini live" — should land directly in Gemini Live

### Step 3 — Naming guardrails
- Avoid generic "open" verbs (e.g. `Open ChatGPT`); Siri may route those to its built-in app launcher rather than the shortcut.
- Avoid bare app names (`ChatGPT`); on iOS with Apple Intelligence enabled, Siri may route bare "ChatGPT" to the Apple-Intelligence ChatGPT extension.
- The multi-word distinctive names `ChatGPT voice` and `Gemini live` are deliberate.

### Step 4 — Generate iCloud share links
- In the Shortcuts app, long-press each shortcut → **Share** → **Copy iCloud Link**.
- iCloud sharing must be enabled (`Settings → Shortcuts → Allow Sharing`); document this in the README.

### Step 5 — Publish
- Create a public GitHub repo (`siri-redirect` or similar) with:
  - `README.md` with the two iCloud links, install instructions, screenshots, and the Claude limitation note.
  - Optional `screenshots/` directory.
- Optionally cross-post to RoutineHub for community discovery.
- Optionally add a one-page GitHub Pages site for non-technical users.

## Findings: Claude voice-mode limitation

This section documents why Claude is deferred from v1, with first-hand sources, so the decision is auditable and re-examinable when Anthropic ships changes.

### Finding 1 — Claude iOS exposes only two App Intents, neither of which is voice
Anthropic's official help article enumerating the iOS integration surface lists exactly:
- "Ask Claude" — text-only query intent
- "Analyze Photo with Claude" — image-analysis control

There is no voice-mode App Intent.

> Source: *Using Claude App Intents, Shortcuts, and Widgets on iOS* — Claude Help Center
> https://support.claude.com/en/articles/10263469-using-claude-app-intents-shortcuts-and-widgets-on-ios

### Finding 2 — Voice mode is explicitly documented as not compatible with iOS app integrations
The Claude voice mode help article states the only activation method is a manual UI tap:

> "Tap the voice mode icon (sound wave symbol next to the microphone icon) in the text input field."

And Anthropic explicitly notes the limitation:

> "Most functionality with iOS apps is not compatible with the voice mode beta feature at this time."

> Sources:
> *Using voice mode* — https://support.claude.com/en/articles/11101966-using-voice-mode
> *Using voice mode on Claude Mobile Apps* — https://support.claude.com/en/articles/11101966-using-voice-mode-on-claude-mobile-apps

### Finding 3 — No iOS URL scheme is documented
The `claude://` URL scheme is documented for Claude Desktop only (macOS / Windows), with paths `claude://claude.ai/new`, `claude://code/new`, `claude://cowork/new` — none of which are voice mode entry points, and none of which are documented as registered on iOS.

> Source: *Open Claude Desktop with a link* — Claude Help Center
> https://support.claude.com/en/articles/14729294-open-claude-desktop-with-a-link

No reverse-engineered iOS URL scheme for the Claude app appears in any community source surveyed.

### Finding 4 — Anthropic has signaled iOS Shortcut expansion is not on the near-term roadmap
A community feature request (`anthropics/claude-code` issue #28420) asking for iOS Siri Shortcuts / App Intents was **closed as "not planned"** and labeled `stale`. The issue concerns Claude Code (not the consumer Claude app), but it is the clearest public signal of Anthropic's current posture toward iOS Shortcut surface expansion.

> Source: https://github.com/anthropics/claude-code/issues/28420

Anthropic's published 2026 voice roadmap focuses on offline voice packs, custom voice cloning, and language expansion. iOS Shortcut / App Intent integration for voice mode is not mentioned.

### Finding 5 — The latest Claude iOS release does not change this
The most recent App Store release (v1.260416.0) lists only "Squashed some bugs and improved the overall experience" in its changelog. No new intents, URL schemes, or voice-launch features have shipped.

> Source: *Claude by Anthropic* — App Store
> https://apps.apple.com/us/app/claude-by-anthropic/id6473753684

### Conclusion
There is no current iOS Shortcuts-, intent-, or URL-based path to launch Claude voice mode. The only known full-automation workaround relies on iOS Voice Control with a recorded UI-tap gesture, which is non-shareable and therefore incompatible with this project's "one-tap install" goal. Claude is deferred until at least one of the unblockers below ships.

## Triggers to reopen Claude scope

Re-evaluate Claude inclusion when any of the following ship:
1. Claude iOS app exposes a "Start voice conversation with Claude" App Intent (parallel to ChatGPT and Gemini's intents). This collapses Claude into the same one-line shortcut as the other two.
2. Claude iOS registers a URL scheme path that lands in voice mode (e.g., `claude://voice` or a universal link such as `claude.ai/voice` that bounces into the native app).
3. iOS 19 ships system-level third-party voice-assistant slots — would also obsolete the need for this project entirely.

Monitoring cadence: a quarterly re-check of the App Store changelog and the Claude Help Center pages cited above is sufficient.

## Risks

| Risk | Mitigation |
|---|---|
| OpenAI removes or renames `Start voice conversation with ChatGPT` | Project is small; rebuild the shortcut and rotate the iCloud link, note the change in README. |
| Google removes or renames `Talk Live with Gemini` | Same. |
| Siri misroutes the trigger phrase to a built-in handler | Default names are distinctive (`ChatGPT voice`, `Gemini live`); document a fallback rename in the README troubleshooting section. |
| iCloud Shortcut sharing setting must be enabled by the receiver | Call out in the README install steps. |
| iOS 19 obsoletes the project | Acceptable. Ship now; archive gracefully when system-level third-party assistants land. |

## Out of scope (deliberately)

- Claude (per "Findings" above; revisit per the listed unblockers).
- Custom non-"Hey Siri" trigger phrases (would require Vocal Shortcuts, which can't be exported).
- Voice Control / Accessibility-based workarounds (can't be packaged for sharing).
- A companion native iOS app (out of proportion for the problem; would need App Store review and ongoing maintenance for limited additional value).
- Paid distribution, marketing, or infrastructure beyond a free static repo / page.

## Distribution plan

- **Primary:** Public GitHub repo with README, two iCloud links, screenshots, troubleshooting section.
- **Optional, additive:** RoutineHub submission, GitHub Pages landing page, Show HN / r/shortcuts post.
- **Not pursued:** App Store, paid hosting, custom domain (unless the project gains traction post-launch).
