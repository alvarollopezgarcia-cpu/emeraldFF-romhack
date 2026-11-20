# Pokémon Emerald ROM hack (Spanish)

&nbsp;[Leer en español](README.es.md)

A difficulty-focused hack of Pokémon Emerald, in Spanish, built from source on top of [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion) (the community decompilation of the game, extended with modern mechanics). It's a work in progress, distributed as a patch.

<!-- Screenshots: add 2-4 images to docs/ and list them here, e.g. ![Gym battle](docs/gym.png) -->

## Features

- **Harder, planned fights.** Reworked trainers and gym battles, with the full teams documented so you can prepare (see Documentation).
- **Hard level cap, free leveling.** Pokémon can't level past the current cap, and Rare Candies are sold in Poké Marts, so you spend your time on team building instead of grinding.
- **PokéNav tools.** The PokéNav gains a menu: MAPA (region map), LUZ (lights up caves, no Flash needed), CURAR (one full party heal, recharged at any Pokémon Center), NIVEL (spends Rare Candies to bring the party up to the cap, stopping for new moves and evolutions) and TELÉFONO.
- **An extra fight after the Champion.** A two-trainer double battle in the Champion's room.
- **Modern mechanics** from pokeemerald-expansion: newer moves, abilities and Pokémon, the physical/special split, and updated battle rules.
- **Spanish.** Dialogue is being translated to Spain Spanish area by area; menu and battle UI terms stay in English for now.
- Nuzlocke-friendly: Set battle style by default, and nothing in the design relies on healing items in battle.

## Documentation

PDF guides with the changes to Pokémon stats, wild encounters, and every important trainer's team:

> 📁 **[Documentation on Google Drive](https://drive.google.com/drive/folders/12XBxm5k3Po57j-Xq7z6-83392AX4XSWC)** (Spanish, view only)

## How to play

You need your own clean copy of **Pokémon Emerald (USA, Europe)**. Its SHA-1 must be `f3ae088181bf583e55daf962a92bb46f4f1d07b7`.

1. Download the `.bps` patch from [Releases](../../releases).
2. Open [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) in your browser (or use Floating IPS on Windows).
3. Select your Emerald ROM and the patch, then **Apply patch**. The patch checks the ROM: it refuses a wrong or modified one.
4. Play the result in a GBA emulator such as [mGBA](https://mgba.io).

This repository contains no ROM. Pokémon is © Nintendo / Game Freak / Creatures; this is a non-commercial fan project.

## Under the hood

The game is written in C and built with `arm-none-eabi-gcc`. Alongside the hack I built a developer tool that tracks how the player fights and describes their style with an LLM, writing it back into the game: [llm-fight-tracker](https://github.com/alvarollopezgarcia-cpu/llm-fight-tracker). It's switched off in the builds released here.

`tools/make_bps_patch.py` is the script that makes each release's patch. It writes BPS directly and refuses to save a patch that doesn't rebuild the hack byte for byte.

## Credits

- [pret](https://github.com/pret/pokeemerald), for the Pokémon Emerald decompilation.
- [Rom Hacking Hideout](https://github.com/rh-hideout/pokeemerald-expansion) and every contributor to pokeemerald-expansion.
- [Porymap](https://github.com/huderlem/porymap), for map editing.
