# Snowdin coverage research (undertale.wiki)

What the wiki says exists in Snowdin vs. what the benchmark could
measure if scope extends past the Ruins. Same format as
RUINS_COVERAGE.md. Bindings need the same data.win pass (plot
thresholds, battlegroup ids) before calibration.

## Main-path milestones (proposed)

| id | event | likely detection |
|---|---|---|
| snowdin_entry | exit Ruins → forest path | room_tundra* |
| sans_intro | Sans prank + conveniently-shaped lamp | dialogue/plot |
| box_road | first encounters begin (Snowdrake/Ice Cap) | room |
| doggo | first sentry fight — introduces BLUE attacks | battlegroup |
| maze | Invisible Electricity Maze done | room/flag |
| ball_game | snowball rolled into hole (or ignored) | flag |
| word_search | Sans/Papyrus word-search scene | dialogue |
| snow_puzzle | map under snow revealed → spikes retracted | flag |
| xoxo_puzzles | three XOXO rooms cleared | rooms |
| tile_puzzle | Multicolor Tile Puzzle (Papyrus retracts) | scene |
| gauntlet | Gauntlet of Deadly Terror (never fires) | scene |
| snowdin_town | enter Snowdin Town | room |
| papyrus_fight | Papyrus boss resolved — moral fork | battlegroup + flag |
| waterfall_entry | exit to Waterfall | room |

## Items

- Tough Glove — free in the Box Road Dimensional Box (item id 14).
- Nice Cream — Nice Cream cart by Ball Game (item 17).
- Snowman Piece — the Snowman north of ice field; genocide = takes
  three, leaves a pile of snow (item 16).
- Fried snow — Sans's scam next to the cart; buyable nothing for
  escalating GOLD prices.

## Boss outcome

Papyrus fight = the region's moral fork, same weight as Toriel:
spare → friendship + later hangout at his house; kill → the run
stays irreversibly darker. Flag + battlegroup binding needed.

## Easter eggs (all measurable)

- **fun value events** (global.fun / flag[5]-like random seed):
  - fun 40–45 → Sans calls about your refrigerator running
  - fun 46–50 → Alphys pizza call → reads ASCII catgirl aloud
  - fun 65 → 50% Sound Test room instead of river (post-Papyrus)
  - mysterious door room → hidden enemy Glyde
- Alphys's cameras: bush at Ruins exit, tree at Sans's station,
  one behind Papyrus's sentry, snow lump at Ball Game, tree at the
  snow puzzle — inspectable, each logs a line (good "detective"
  optional milestones).
- Snowdecahedron inspect (genocide: just "a snowball").
- Ball Game hole: inspect before rolling = excited narration;
  Snowdin kill counter exhausted → "There's a hole here."
- Doggo bell: repeatedly ring for escalating reactions (spare-path).
- Smoked dog treats at Doggo's station.
- Fishing rod note at the river.
- Conveniently-shaped lamp inspect.

## Routes — how they'd score

- **Neutral** (baseline): current milestone set works; score = main
  path completion + optional bonus.
- **Pacifist-lean**: every boss optional-milestone reads spare
  (toriel_spared, papyrus_spared), kills=0; Flowey exit monologue
  is the kindness verdict. Subscore = mercy % of fights.
- **Genocide-lean**: per-area kill counters exist in-game (the
  Snowdin savepoint shows "Monsters Left" — readable via state!).
  Exhausting the counter changes narration + Flowey dialogue.
  Genocide-route gates: Sans's warning, walking through Papyrus's
  puzzles, stolen Snowman pieces (3 vs 1).
- **Hard Mode**: name "Frisk" — Ruins-only; Final Froggit etc.

## Detectable without new bridge work

- kill counters: `kills` in state + event log.
- fun value: `global.fun` — add to flags_csv export if not present.
- bosses: battlegroup ids (Papyrus's id from decompile).
- items/rooms/choicers: already exported.
