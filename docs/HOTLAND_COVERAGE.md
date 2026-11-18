# Hotland / CORE / Castle census (goto + scan, live-verified at plot 122)

All rooms below load and spawn objects correctly via `goto` (bridge alive in each).

## Lab block
- **room_fire_lab1**: ~1100px dark hallway; Alphys/Mettaton intro trigger ~x663 -> bg48 quiz
- **room_fire_lab2**: Alphys lab interior (anime posters, lollipop counter); intro
  conveyor (obj_sideconveyorl) + scene lock until quiz done; west conveyor pushes left
- **Mettaton quiz (bg48)**: obj_answernodule grid; stalls at hp=1 in our hands — the
  wrong-answer zap floors at 1 but the writer chain never advances. Not plot-gating.

## Main path east
- **fire3**: lab north exit; Alphys status-notification scene at x~180; climb shaft -> fire5
- **fire5**: tall conveyor/bluejet gauntlet (encount_fire1 armed, bg51 3-mob groups)
- **fire6**: bounce tiles + savepoint + encount_fire1
- **fire6A**: conveyors + npc
- **lasers1**: orange/blue laser puzzle (obj_orangelaser_o/bluelaser_o + laserswitch1)
- **fire7**: chipdoor_l/r (gate), bouncers, npc_marker
- **fire8**: lighttower, bluelaser, phonecall trigger
- **shootguy_1..4, preshootguy4**: Mettaton shooting minigames (obj_shootguy/targetguy)
- **fire9, fire_turn**: corridor rooms (door_u branches)
- **fire10**: kitchenforcefield + triswitch (triple-switch puzzle) + phonecall
- **cookingshow**: obj_mettcounter — Mettaton's cooking show stage
- **hotdog**: Sans hotdog stand (obj_sans_room, sentrystation, hotdoggen)
- **walkandbranch / walkandbranch2**: branch corridors; wb2 has chipdoor trigger +
  door_ruins13 (secret back-door obj seen in several rooms)
- **sorry**: art club sign (obj_artclass_sign — So Sorry room, real-time gated)
- **apron**: Stained Apron room
- **rpuzzle**: r-block/conveyor puzzle (obj_rblock, rtile)
- **mewmew2**: mousehole + savepoint (Mew Mew room)
- **boysnightout**: steam room (obj_boysnightout)
- **newsreport**: obj_mettnewsevent — MTT news report stage (lasers + bouncers)
- **coreview2**: backgrounder_core vista + phonecall
- **elevator_l2/l3**: more hub spokes (doors to hotel side)
- **spidershop**: Muffet's bake sale (obj_spidergirl_shop, webs, spiderstrand)
- **conveyorlaser**: conveyor + blue laser + echoflower
- **savepoint2**: savepoint + door_ruins13 + spiderstrand
- **spider**: MUFFET corridor — spidertalkevent + slowdownwalk zones (walk slowed)
- **pacing**: corridor w/ readable
- **operatest**: obj_playmovement — opera/movement-test room
- **multitile**: colored tile gauntlet (tilepink/red/green/orange/blue/purple/yellow,
  tileblueactsyellow, insidiousconveyor, mettaton_flightdress) + multitileevent

## MTT Resort block
- **hotelfront_1**: nicecreamguy + royal_rabbitbounce NPCs + door_ruins13
- **hotelfront_2**: sans_prefinaldate (Sans date room) + doorX
- **hotellobby**: receptionist, ficus, shamblingmass, saddragon, businessmanticore,
  mttfountain, savepoint, coresign
- **restaurant**: MTT restaurant (snowdrakedad + readables)
- **hoteldoors**: room doors + slimejanitor + obj_knock_room (room-service knock)
- **hotelbed**: bedlump room
- **elevator_r3**: Heats Flamesman again + door_ruins13
- **precore**: darkman_actor + precore_event (CORE approach scene)

## CORE
- **core1/2**: entry corridors (core_lightstrip, elevatordoor, hearthflame)
- **core_center**: hub w/ encount_core1 + door_ruins13 + readable
- **core_branch**: savepoint + doors + door_ruins13
- **core_laserfun**: powerlaser_event (orange/blue lasers)
- **core_freebattle**: darkman_actor + core_enemyevent2 -> scripted bg60 battle
  (armed live: battlegroup 60 fired on entry, intr=3)

## Mechanics verified live
- Elevator: face-up + z on panel -> "Click" -> "Please select a location." ->
  floor grid (Cancel default). Ride = select floor, walk SOUTH out the door.
- Savepoints: need z press while overlapping; save wrote file9 @ savepoint1.
- door_ruins13 objects appear in savepoint2, walkandbranch2, hotelfront_1,
  elevator_r3, core_center, core_branch — a back-route network worth mapping later.
