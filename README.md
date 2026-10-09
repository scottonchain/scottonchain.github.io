# Microcredit delivery site

This repository serves the project's published app and audio at
[scottonchain.github.io](https://scottonchain.github.io). It contains generated
releases; maintain the code in the upstream repositories listed in `sources.json`.

| Served path | Maintained source |
| --- | --- |
| `/pool/` | [microcredit-contract/packages/nextjs](https://github.com/scottonchain/microcredit-contract/tree/main/packages/nextjs) |
| `/listen/` | [microcredit-vision/audio](https://github.com/scottonchain/microcredit-vision/tree/main/audio) and its audio build tools |
| `/.well-known/agent-card.json` | [microcredit-agent-testbed/agent-card.json](https://github.com/scottonchain/microcredit-agent-testbed/blob/main/agent-card.json) |

Run `python tools/check.py --testbed ../microcredit-agent-testbed` for read-only
release checks. The testbed's `coordination/check_workspace.py` checks all five
repo identities, app deployment addresses and card mirrors together.

Build from reviewed upstream source, then copy only the intended release directory.
Do not hand-edit compiled JavaScript, generated HTML, podcast feeds or copied cards.
Keep the upstream source revision with each release and inspect the full delivery
diff. A maintenance check does not publish or lift an existing publication hold.

The pool uses Base Sepolia test tokens only. The agent inbox stores messages for
review; its card does not promise autonomous execution.
