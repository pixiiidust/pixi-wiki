---
title: Verb-First Product Positioning
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [concept, product-management, strategy, customer-discovery]
sources: [discord-thread]
confidence: high
status: active
---

# Verb-first product positioning

## Definition

Verb-first product positioning describes a product by the concrete job it performs before naming its category.

The rule: describe products with verbs before nouns. Say what the product does to a specific input, for whom, with what outcome, and what pain it removes.

## Why it matters

Noun-first descriptions make users decode an abstract category.

> "We're building a cloud platform for AI."

That sentence names a market category, but it does not show the product doing useful work.

Verb-first descriptions make the work visible.

> "We containerize your code and run it on GPUs in the cloud so you don't have to manage the infra yourself."

That sentence names the input, action, environment, and removed pain.

## Canonical formula

Use this shape:

> We [verb] your [specific input] so you can [desired outcome] without [specific pain].

Shorter version:

> We [verb] [object] so [user] can [result].

## Required pieces

A good product sentence should answer:

1. What does the product touch?
   - code, emails, invoices, calls, PDFs, appointments, leads, reports
2. What does it do to that input?
   - summarize, route, generate, detect, schedule, reconcile, convert, monitor, clean, file, approve
3. What changes for the user?
   - save time, avoid mistakes, get paid faster, respond faster, ship faster, stay compliant
4. What pain disappears?
   - manual work, infra, chasing people, copy-paste, missed follow-ups, spreadsheet hell

## Rewrite trigger

If the first sentence names what the product is before saying what it does, rewrite it.

Bad pattern:

> We're building a [noun/category] for [market].

Examples:

- "An AI platform for small businesses."
- "A productivity tool for founders."
- "A cloud infrastructure layer for developers."
- "A workflow automation system for agencies."

Better pattern:

> We [do concrete action] to/with your [specific input] so you can [outcome] without [pain].

Examples:

- "We turn your customer emails into draft replies so you can answer faster without hiring support staff."
- "We watch your invoices and flag late payments so you can chase cash without living in spreadsheets."
- "We containerize your code and run it on cloud GPUs so you don't have to manage infra."
- "We turn messy meeting notes into follow-up tasks so your team doesn't lose decisions."

## Pass/fail test

If someone can respond with "What does that mean?", the description failed.

If they respond with "Oh, I need that", it worked.

## Relationship to Jamie's product work

This concept supports Jamie's AI product strategy: buyers want outcomes, not tools. It pairs with [[ai-native-problem-framing-framework]] by forcing the product idea to name the real workflow, input, action, and payoff.

It also fits the [[matt-pocock-sdlc-rhythm]] because positioning should be tested early during grilling and prototype work, before the team commits to a vague category or broad build.

## Hermes infrastructure

This concept is supported by a reusable Hermes skill and routing rule:

- **Skill:** `~/.hermes/skills/product-management/verb-first/SKILL.md` — loaded when Jamie is working on product descriptions or positioning. Covers the verb-first formula, rewrite trigger, pass/fail test, and rewrite examples.
- **Local knowledge concept:** `~/.hermes/knowledge/concepts/verb-first-product-positioning.md` — Hermes-level mirror of this vault page so agents serving product work have the durable concept in their knowledge layer without needing vault access.
- **USER.md routing rule:** When the user asks for product description or positioning work, the `verb-first` skill is loaded and `.hermes/knowledge/concepts/verb-first-product-positioning.md` is sourced as the canonical reference.

This layered architecture — vault (durable human truth) → Hermes knowledge (agent-accessible concept) → skill (executable procedure) → USER.md (routing rule) — follows the [[profile-memory-boundaries]] model.

## Operational notes

- **Quill dispatch default:** When Jamie says "update these milestones into Obsidian," Pixoid routes the scribe task to Quill (this agent) by default to save main-chat tokens. This is now an established operating preference.

## Related pages

- [[find-the-lock-problem-first]]
- [[ai-native-problem-framing-framework]]
- [[matt-pocock-sdlc-rhythm]]
- [[profile-memory-boundaries]]
