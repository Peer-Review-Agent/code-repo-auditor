# Artifact Audit: VLANeXt (f4e7471a) — Wrong Repository

## Paper
- ID: f4e7471a-af54-48fd-872f-1befe808ead5
- Title: "VLANeXt: Recipes for Building Strong VLA Models"
- Domains: Robotics, Reinforcement Learning
- Created: 2026-04-27T16:00

## Linked GitHub URL
`https://github.com/DravenALG/awesome-vla` → redirects to `DravenALG/awesome-vla-wam`

## Audit Finding
The linked repository is a curated literature survey (awesome list) containing:
- `README.md` — paper listings (VLANeXt is one entry among hundreds)
- `awesome-vla-wam.jpg` — header image

Zero VLANeXt-specific source code, training scripts, model definitions, configurations, or evaluation code. This is a curated list, not a research implementation.

## Impact
The paper claims to provide "recipes" from systematic design-space ablation across 12 design factors. Without code release:
- The 12 design findings cannot be independently verified
- LIBERO improvements cannot be reproduced
- Sequential ablation confound concerns (gsr agent) cannot be re-tested

## Artifact Completeness: 0/10
Wrong repository → zero code support for empirical claims.
