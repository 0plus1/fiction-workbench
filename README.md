# Fiction Workbench

LLM agent skills for long-form fiction writing.

This repo is intentionally small. It ships one skill, [`/fiction-workbench`](.claude/skills/fiction-workbench/SKILL.md), designed to work with a simple fiction-project layout built around a `bible/` directory and a `manuscript/chapters/` directory.

## Why This Exists

AI-assisted fiction writing usually breaks down after a few chapters:

- voice drifts
- characters flatten or contradict themselves
- continuity gets sloppy
- revisions lose the original intent

This repo gives Agents a tighter workflow for long-form fiction. It does not replace authorship. It gives the model a disciplined way to read your canon, operate on a chapter, and stay inside the story you are already building.

## What’s Included

```text
claude-fiction-skills/
├── README.md
├── LICENSE
└── .claude/
    └── skills/
        └── fiction-workbench/
            └── SKILL.md
```

## Install

We recommend using [skills](https://skills.sh)
`npx skills add https://github.com/0plus1/fiction-workbench --skill fiction-workbench`

## Usage

Invoke the skill manually:

```text
/fiction-workbench write manuscript/chapters/chapter-1.md
/fiction-workbench edit manuscript/chapters/chapter-1.md
/fiction-workbench critique manuscript/chapters/chapter-1.md
/fiction-workbench seal manuscript/chapters/chapter-1.md
```

### Modes

- `write`: draft, expand, or rewrite a chapter while preserving canon and voice
- `edit`: improve prose at the line level without changing story intent
- `critique`: give literary feedback without rewriting
- `seal`: produce a concise chapter summary, continuity notes, motifs, and open threads

## Expected Project Shape

The skill is opinionated about project structure. It works best when your fiction project looks like this:

```text
your-novel/
├── bible/
│   ├── characters/
│   │   ├── marco.md
│   │   └── malia.md
│   ├── locations/
│   │   ├── apartment.md
│   │   └── coast-road.md
│   ├── themes/
│   │   ├── exile.md
│   │   └── desire.md
│   ├── emotional-arc.md
│   ├── style-guide.md
│   └── narrative-spine.md
└── manuscript/
    └── chapters/
        ├── chapter-1.md
        ├── chapter-2.md
        └── chapter-x.md
```

The skill assumes this structure by default. It reads the target chapter, then consults the relevant files under `bible/` before drafting, editing, critiquing, or sealing.

We recommend using [murmur](https://github.com/0plus1/murmur) as the editor for your novel.

## How It Behaves

`/fiction-workbench` is deliberately manual. It uses `disable-model-invocation: true`.

The skill tells agents to:

- read the target chapter first
- inspect the `bible/` files and folders
- preserve established voice, chronology, and character integrity
- avoid inventing lore or symbolic systems that are not supported by the text
- keep the human in charge of taste, structure, and final judgment

For `write` and `edit`, the skill is intended to revise the target chapter. For `critique` and `seal`, it should return notes unless you explicitly ask Claude to write those notes into project files.

## Philosophy

This repo is not an autopilot novel generator.

The author still owns:

- theme
- structure
- taste
- final language

Agents' role here is narrower:

- reduce drift
- keep continuity in view
- help with disciplined iteration

That is the point of the repo.

## Customising

If your project uses different folder names, edit [`SKILL.md`](skills/fiction-workbench/SKILL.md) directly. Keep the skill procedural. Put story-specific canon in your own project, not inside the public skill repo.

