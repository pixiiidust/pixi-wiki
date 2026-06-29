# PRD — Discord Council Mode Hardening

## Problem Statement

Jamie wants the Pixi crew to feel multiplayer-capable without turning Discord into an uncontrolled agent dogpile.

The current implementation has moved in the right direction: `@Crew` and `crew:` are intended to stay Pixoid-led, Pixoid can open or reuse a bounded huddle in `#agent-workbench`, and Boba, Quill, and Tinker are invited with one-round stop rules. Worker profiles are configured to require mentions in threads and accept bot messages only when directly mentioned.

The remaining problem is operational reliability. The council path needs to be durable, testable, and easy to reason about before it becomes the default collaboration surface. Otherwise a future gateway restart, Discord event duplicate, broad worker channel reach, or local Hermes update could regress the behavior back into duplicate replies, lost huddle state, or unclear accountability.

## Solution

Harden council mode as a governed Discord route:

```text
@Crew / crew:
→ Pixoid coordinator route
→ bounded huddle in #agent-workbench
→ invited specialists reply once in assigned lanes
→ Pixoid closes the huddle
→ Pixoid returns one synthesized final answer to the origin thread
```

The product goal is not “all bots talk all the time.” The product goal is controlled multiplayer: one visible owner for the user-facing thread, explicit specialist participation in a workbench huddle, and traceable final synthesis.

Directly mentioning a specialist should still work when Jamie intentionally summons them. The default restriction should prevent ambient worker chatter and broad crew dogpiles, not remove Jamie’s ability to call `@Boba`, `@Quill`, or `@Tinker` on purpose.

## User Stories

1. As Jamie, I want `@Crew` to wake Pixoid as coordinator, so that crew requests produce one organized response instead of several independent bot replies.
2. As Jamie, I want `crew:` to behave like a Pixoid-led council request, so that text-based crew calls are as safe as role mentions.
3. As Jamie, I want Pixoid to open or reuse a huddle in `#agent-workbench`, so that specialist discussion does not bury the user-facing thread.
4. As Jamie, I want Boba, Quill, and Tinker invited explicitly, so that I know which specialists were asked to contribute.
5. As Jamie, I want each specialist to stay in their assigned lane, so that council feedback is complementary instead of repetitive.
6. As Jamie, I want specialists to reply once by default, so that council mode has a natural stopping point.
7. As Jamie, I want Pixoid to close the huddle clearly, so that workers do not keep responding after enough input has been gathered.
8. As Jamie, I want Pixoid to synthesize one final answer in the origin thread, so that I get a clean recommendation instead of a transcript dump.
9. As Jamie, I want to directly summon `@Boba`, `@Quill`, or `@Tinker` when needed, so that specialist profiles remain available on purpose.
10. As Jamie, I want worker profiles restricted from ambient participation, so that they do not respond just because a thread is active.
11. As Jamie, I want direct specialist summons to be explicit mentions by allowed users in approved contexts, so that “restricted by default” does not mean “unreachable.”
12. As Pixoid, I want route records for huddles, so that I can recover or explain council state after restarts and failures.
13. As Pixoid, I want each huddle tied to one origin request, so that unrelated council runs do not collide in reused threads.
14. As Pixoid, I want to close when all invited workers reply once or timeout hits, so that council mode is responsive without waiting unnecessarily.
15. As Pixoid, I want missing worker replies recorded, so that final answers do not pretend every specialist contributed.
16. As Boba, I want a clear research/reality-check lane, so that I challenge assumptions without rewriting the whole answer.
17. As Quill, I want a source-of-truth/docs lane, so that durable knowledge and wording implications are covered.
18. As Tinker, I want an implementation/verification lane, so that feasibility and breakage risks are surfaced.
19. As a maintainer, I want tests for role mentions, crew aliases, huddle closure, bot-message filtering, and duplicate events, so that Discord orchestration does not regress silently.
20. As a maintainer, I want a controlled live smoke test, so that success means the real Discord gateway behavior works, not just unit tests.
21. As a maintainer, I want gateway restart behavior verified, so that code/config changes actually affect running profiles.
22. As a maintainer, I want the local Hermes patch made durable, so that council mode is not lost during updates or upstream pulls.
23. As a maintainer, I want worker blast radius minimized, so that worker bots cannot be accidentally woken across every visible channel.
24. As a maintainer, I want public documentation and issue tracking in `pixi-wiki`, so that the coordination design and implementation slices are durable and reviewable.
25. As a future agent, I want issue slices with acceptance criteria, so that council hardening can be implemented methodically without rediscovering the whole context.

## Implementation Decisions

- Treat this as a Pixi crew / Hermes gateway hardening effort tracked from `pixiiidust/pixi-wiki` because this repo is Jamie’s public docs and planning surface for agent workflow work.
- Store the PRD in `pixi-wiki/docs/PRD-council-mode-hardening.md`.
- Use `pixiiidust/pixi-wiki` issues as the planning and coordination tracker for this effort.
- The implementation target is the Hermes Discord gateway council-mode behavior, not the Pixi Wiki static site itself.
- Default route: `@Crew` and `crew:` wake Pixoid only.
- Workbench route: Pixoid opens or reuses a bounded huddle in `#agent-workbench`.
- Worker route: Boba, Quill, and Tinker are explicitly mentioned/invited by Pixoid inside the huddle.
- Worker behavior: reply once, stay in assigned lane, do not run tools unless explicitly asked, ignore acknowledgements, stop after the close marker.
- Final answer behavior: Pixoid reads huddle transcript, closes the huddle, and returns one synthesized answer to the origin thread.
- Direct specialist summons remain allowed: Jamie or another allowed user can intentionally mention `@Boba`, `@Quill`, or `@Tinker` to get that specialist, but workers should not wake from ambient thread chatter or broad crew aliases.
- Defer a `CrewLive` / direct live multiplayer mode. It can be added later as an explicit test-only escape hatch, but it is not part of this v1 hardening pass.
- Prefer an all-replied-or-timeout close policy: close when each invited worker has replied once, with timeout as fallback.
- Persist or reconstruct route state so each huddle has a traceable route record: origin, huddle, invited workers, actual responders, status, opened time, closed time, and final delivery target.
- Add route or event identifiers to huddle briefs/closures so huddle reuse cannot mix unrelated requests.
- Restrict worker profile blast radius while preserving direct summons. Workers should be quiet by default and available by explicit mention in approved contexts.
- Gateway restarts remain approval-gated/manual unless Jamie explicitly authorizes restart for a given implementation pass.
- Do not broaden worker tool permissions as part of council mode. Workers may recommend side effects; Pixoid owns approval, execution, and verification boundaries.
- Make the local Hermes council-mode patch durable before relying on it: commit/branch/PR/snapshot it so updates cannot silently erase it.

## Testing Decisions

Tests should cover externally visible routing behavior and failure modes, not private implementation details.

Good test seams:

- Discord adapter route classification for role mentions and crew aliases.
- Bot-message filtering with `allow_bots: mentions`.
- Thread mention behavior with `thread_require_mention: true`.
- Huddle creation/reuse behavior for workbench threads.
- Worker invitation and huddle brief formatting.
- Huddle close marker behavior.
- All-replied-or-timeout close policy.
- Duplicate Discord event idempotency.
- Gateway restart/state recovery behavior where feasible.

Required verification:

- Unit/focused gateway tests pass.
- Replay tests cover the real observed failure cases: existing thread membership trap, role mention behavior, worker close marker, `ok/lol/thanks` silence, duplicate event suppression, and worker bot messages that mention other agents.
- One controlled live smoke test in Discord verifies the full path:

```text
@Crew discuss tiny test request
→ Pixoid opens/reuses huddle
→ workers reply once
→ Pixoid posts Huddle closed
→ Pixoid returns one final answer to origin
→ workers remain quiet after close
```

- Gateway restart is verified after code/config changes before declaring the feature live.
- If public docs or issue references change, `pixi-wiki` repository checks and GitHub Pages deployment checks run as appropriate.

## Out of Scope

- No broad rewrite of Hermes gateway architecture.
- No new Discord server/channel taxonomy unless a later issue approves it.
- No `CrewLive` / all-bots direct multiplayer mode in v1.
- No autonomous worker tool use in council huddles.
- No unrestricted worker participation across all visible Discord channels.
- No merging/deploying/restarting gateways without the appropriate approval gate.
- No moving this PRD to `docs/PRD.md`; existing docs PRDs remain separate.
- No changes to secrets, token handling, or credential storage.
- No public exposure of private huddle transcript content beyond necessary issue summaries and sanitized verification proof.
- No assumption that unit tests alone prove live Discord behavior.

## Further Notes

Current agreed defaults from the grill session:

```text
1. Harden the current Hermes Discord council-mode patch.
2. Track planning/issues in pixi-wiki for now.
3. Default UX is Pixoid-led council mode.
4. Defer CrewLive / direct multiplayer escape hatch.
5. Restrict workers by default, but preserve direct @ summons when Jamie intentionally calls them.
6. Use persistent or reconstructable route records.
7. Close when all workers reply once, with timeout fallback.
8. Acceptance bar: unit tests + replay tests + live Discord smoke + gateway restart verification.
9. Ask before gateway restart.
```

Important invariant:

```text
restricted by default ≠ unreachable
```

Boba, Quill, and Tinker should not ambiently join every conversation, but Jamie should be able to summon a specialist with an explicit mention when she wants that profile’s voice.

Recommended next `/to-issues` shape:

1. Make the local council-mode patch durable.
2. Lock the direct-summon vs ambient-worker route contract.
3. Add replay tests for observed Discord failure modes.
4. Add durable/reconstructable huddle route records.
5. Implement all-replied-or-timeout close behavior.
6. Restrict worker blast radius while preserving direct summons.
7. Run controlled live Discord smoke and restart verification.
