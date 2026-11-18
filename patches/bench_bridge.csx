// undertale-bench bridge injector.
// Creates a persistent obj_bench_bridge object and places an instance in the
// first room. Its Step event polls bench_cmd.json and writes bench_state.json
// inside the GameMaker sandbox (%LOCALAPPDATA%\UNDERTALE\).
//
// Usage:  UndertaleModCli.exe load data.win -s bench_bridge.csx -o data_bench.win
using System.Text;
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using UndertaleModLib.Models;
using UndertaleModLib.Util;
using UndertaleModLib.Compiler;

EnsureDataLoaded();

const string ObjName = "obj_bench_bridge";

if (Data.GameObjects.ByName(ObjName) != null)
{
    ScriptMessage("obj_bench_bridge already present — data.win already patched?");
    return;
}

// ---------------------------------------------------------------- object ---
var obj = new UndertaleGameObject();
obj.Name = Data.Strings.MakeString(ObjName);
obj.Persistent = true;
obj.Sprite = null;
Data.GameObjects.Add(obj);

// -------------------------------------------------------------- step GML ---
const string stepGml = @"
// ---- undertale-bench bridge (injected) ----
if (!variable_global_exists(""bench_seq"")) { global.bench_seq = -1; global.bench_frame = 0; }
global.bench_frame += 1;

// one-time init of watched values for the event stream
if (!variable_global_exists(""bench_ev_init""))
{
    global.bench_ev_init = 1;
    global.bench_eseq = 0;
    global.bench_pv_room = -999;
    global.bench_pv_hp = -999;
    global.bench_pv_plot = -9999;
    global.bench_pv_battle = -1;
    global.bench_pv_bg = -999;
    global.bench_pv_dlg = -1;
    global.bench_pv_choice = -999;
    global.bench_pv_choicer = -1;
    var _i; for (_i = 0; _i < 8; _i++) global.bench_pv_item[_i] = -999;
    global.bench_pv_exp = -999;
    global.bench_pv_lv = -999;
    global.bench_pv_gold = -999;
    global.bench_pv_kills = -999;
    var _h; for (_h = 0; _h < 16; _h++) { global.bench_hvk[_h] = -1; global.bench_hon[_h] = 0; }
}

// held keys: keyboard_key_press only simulates one frame in GMS1.4,
// so re-press every frame while a key is held down
var _hi;
for (_hi = 0; _hi < 16; _hi++)
{
    if (global.bench_hon[_hi] == 1 && global.bench_hvk[_hi] != -1)
    {
        if (!keyboard_check(global.bench_hvk[_hi])) keyboard_key_press(global.bench_hvk[_hi]);
    }
}

// apply pending command (flat text: first line seq N, then key 0|1)
if (file_exists(""bench_cmd.txt""))
{
    var cf = file_text_open_read(""bench_cmd.txt"");
    if (cf != -1)
    {
    var hdr = file_text_read_string(cf); file_text_readln(cf);
    var seq = -1;
    if (is_string(hdr) && string_length(hdr) >= 5)
        seq = real(string_copy(hdr, 5, 12));
    if (seq > global.bench_seq)
    {
        global.bench_seq = seq;
        while (!file_text_eof(cf))
        {
            var line = file_text_read_string(cf); file_text_readln(cf);
            var sp = string_pos("" "", line);
            var k = line;
            if (sp > 0) k = string_copy(line, 1, sp - 1);
            if (true)
            {
                var v = (string_copy(line, sp + 1, 4) == ""1"");
                if (k == ""goto"")
                {
                    var rn = string_copy(line, sp + 1, 64);
                    var ridx = asset_get_index(rn);
                    if (ridx != -1) room_goto(ridx);
                }
                // calibration-only admin commands; every use is logged as an
                // admin event so a scored run that used them is flagged.
                var admin = """";
                if (k == ""heal"") { global.hp = global.maxhp; admin = k; }
                if (k == ""item"")
                {
                    var iid = real(string_copy(line, sp + 1, 8));
                    scr_itemget(iid); admin = k + "" "" + string(iid);
                }
                if (k == ""gold"")
                {
                    var gv = real(string_copy(line, sp + 1, 8));
                    global.gold += gv; admin = k + "" "" + string(gv);
                }
                if (k == ""flag"")
                {
                    var rest = string_copy(line, sp + 1, 40);
                    var sp2 = string_pos("" "", rest);
                    var fid = real(string_copy(rest, 1, sp2 - 1));
                    var fval = real(string_copy(rest, sp2 + 1, 20));
                    global.flag[fid] = fval; admin = k + "" "" + string(fid) + ""="" + string(fval);
                }
                if (k == ""plot"")
                {
                    var pv = real(string_copy(line, sp + 1, 8));
                    global.plot = pv; admin = k + "" "" + string(pv);
                }
                if (k == ""speed"")
                {
                    var sv = real(string_copy(line, sp + 1, 8));
                    room_speed = sv; admin = k + "" "" + string(sv);
                }
                if (k == ""freeme"")
                {
                    global.interact = 0;
                    var wn = ""|obj_writer|obj_dialoguer|obj_choicer|obj_unfader|obj_fader|obj_gameoverfake|obj_persistentfader|obj_introimage|"";
                    with (all)
                    {
                        var oname = ""|"" + object_get_name(object_index) + ""|"";
                        if (string_pos(oname, wn) > 0) instance_destroy();
                    }
                    var mci = asset_get_index(""obj_mainchara"");
                    var had = (mci != -1 && instance_exists(mci));
                    if (!had && mci != -1) { instance_create(320, 240, mci); }
                    // do NOT clear obj_mainchara.cutscene: cutscene controllers
                    // rely on it to drive scripted view_yview animations; clearing
                    // it makes mainchara reset the view every frame and stalls
                    // e.g. obj_undyneencounter1 at cn==1.2 forever.
                    admin = k + "" had="" + string(had);
                }
                if (k == ""scan"")
                {
                    var seen = ""|"";
                    var n = 0;
                    var sf3 = file_text_open_append(""bench_events.txt"");
                    with (all)
                    {
                        var on2 = object_get_name(object_index);
                        var key = ""|"" + on2 + ""|"";
                        if (string_pos(key, seen) == 0 && n < 80)
                        {
                            seen += on2 + ""|"";
                            file_text_write_string(sf3, string(global.bench_frame) + "" obj "" + on2 + "" "" + string(x) + "" "" + string(y) + chr(10));
                            n += 1;
                        }
                    }
                    file_text_close(sf3);
                    admin = k + "" n="" + string(n);
                }
                if (admin != """")
                {
                    global.bench_eseq += 1;
                    var af2 = file_text_open_append(""bench_events.txt"");
                    file_text_write_string(af2, string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" admin "" + admin + chr(10));
                    file_text_close(af2);
                }
                var vk = -1;
                // names must match env/undertale_bench/keys.py
                if (k == ""left"") vk = vk_left;
                if (k == ""right"") vk = vk_right;
                if (k == ""up"") vk = vk_up;
                if (k == ""down"") vk = vk_down;
                if (k == ""z"") vk = ord(""Z"");
                if (k == ""x"") vk = ord(""X"");
                if (k == ""c"") vk = ord(""C"");
                if (k == ""enter"") vk = vk_enter;
                if (k == ""f4"") vk = vk_f4;
                if (k == ""shift"") vk = vk_shift;
                if (k == ""ctrl"") vk = vk_control;
                if (vk != -1)
                {
                    var hs = -1;
                    var hj;
                    for (hj = 0; hj < 16; hj++)
                    {
                        if (global.bench_hvk[hj] == vk) hs = hj;
                        if (hs == -1 && global.bench_hvk[hj] == -1) hs = hj;
                    }
                    if (v)
                    {
                        if (hs != -1) { global.bench_hvk[hs] = vk; global.bench_hon[hs] = 1; }
                        if (!keyboard_check(vk)) keyboard_key_press(vk);
                    }
                    else
                    {
                        if (hs != -1 && global.bench_hvk[hs] == vk) global.bench_hon[hs] = 0;
                        if (keyboard_check(vk)) keyboard_key_release(vk);
                    }
                }
            }
        }
        var af = file_text_open_write(""bench_ack.txt"");
        file_text_write_string(af, string(seq) + "" "" + string(global.bench_frame));
        file_text_close(af);
    }
    file_text_close(cf);
    }
}

// export state - JSON built by hand (no ds_map/json_encode: not portable)
var q = chr(34);
var bs = chr(92);
var s = ""{"";
s += q + ""frame"" + q + "":"" + string(global.bench_frame);
s += "","" + q + ""room"" + q + "":"" + string(room);
s += "","" + q + ""room_name"" + q + "":"" + q + room_get_name(room) + q;
var mc = asset_get_index(""obj_mainchara"");
if (mc != -1 && instance_exists(mc)) { s += "","" + q + ""px"" + q + "":"" + string(mc.x) + "","" + q + ""py"" + q + "":"" + string(mc.y); }
if (mc != -1 && instance_exists(mc)) { with (mc) { global.bench_mv = movement; global.bench_cs = cutscene; } s += "","" + q + ""mv"" + q + "":"" + string(global.bench_mv) + "","" + q + ""cs"" + q + "":"" + string(global.bench_cs); }
s += "","" + q + ""intr"" + q + "":"" + string(global.interact);
if (variable_global_exists(""hp"")) s += "","" + q + ""hp"" + q + "":"" + string(global.hp);
if (variable_global_exists(""maxhp"")) s += "","" + q + ""maxhp"" + q + "":"" + string(global.maxhp);
if (variable_global_exists(""lv"")) s += "","" + q + ""lv"" + q + "":"" + string(global.lv);
if (variable_global_exists(""exp"")) s += "","" + q + ""exp"" + q + "":"" + string(global.exp);
if (variable_global_exists(""gold"")) s += "","" + q + ""gold"" + q + "":"" + string(global.gold);
if (variable_global_exists(""plot"")) s += "","" + q + ""plot"" + q + "":"" + string(global.plot);
if (variable_global_exists(""battlegroup"")) s += "","" + q + ""battlegroup"" + q + "":"" + string(global.battlegroup);
if (variable_global_exists(""mercymod"")) s += "","" + q + ""mercymod"" + q + "":"" + string(global.mercymod);
if (variable_global_exists(""myfight"")) s += "","" + q + ""myfight"" + q + "":"" + string(global.myfight);
if (variable_global_exists(""battlephase"")) s += "","" + q + ""battlephase"" + q + "":"" + string(global.battlephase);
if (variable_global_exists(""interact"")) s += "","" + q + ""interact"" + q + "":"" + string(global.interact);
if (variable_global_exists(""at"")) s += "","" + q + ""at"" + q + "":"" + string(global.at);
if (variable_global_exists(""df"")) s += "","" + q + ""df"" + q + "":"" + string(global.df);
if (variable_global_exists(""kills"")) s += "","" + q + ""kills"" + q + "":"" + string(global.kills);
if (variable_global_exists(""msg""))
{
    var msg = """";
    var mi;
    var msglen = array_length_1d(global.msg);
    if (msglen > 20) msglen = 20;
    for (mi = 0; mi < msglen; mi++) { if (is_string(global.msg[mi])) msg += global.msg[mi] + "" ""; }
    msg = string_replace_all(msg, bs, bs + bs);
    msg = string_replace_all(msg, q, bs + q);
    msg = string_replace_all(msg, ""#"", "" "");
    s += "","" + q + ""msg"" + q + "":"" + q + msg + q;
}
if (variable_global_exists(""flag""))
{
    var fs = """";
    var fi;
    var nflags = array_length_1d(global.flag);
    if (nflags > 512) nflags = 512;
    for (fi = 0; fi < nflags; fi++)
    {
        var fv = global.flag[fi];
        if (is_real(fv) || is_string(fv)) fs += string(fv);
        fs += "","";
    }
    s += "","" + q + ""flags_csv"" + q + "":"" + q + fs + q;
}
var bc = asset_get_index(""obj_battlecontroller"");
var wr = asset_get_index(""obj_writer"");
var di = asset_get_index(""obj_dialoguer"");
var ch = asset_get_index(""obj_choicer"");
var inbt = (bc != -1 && instance_exists(bc));
var haswr = (wr != -1 && instance_exists(wr));
var hasdi = (di != -1 && instance_exists(di));
var hasch = (ch != -1 && instance_exists(ch));
s += "","" + q + ""in_battle"" + q + "":"" + string(inbt);
s += "","" + q + ""dialogue"" + q + "":"" + string(haswr || hasdi || hasch);
s += "","" + q + ""choicer"" + q + "":"" + string(hasch);
if (variable_global_exists(""choice"")) s += "","" + q + ""choice"" + q + "":"" + string(global.choice);
if (variable_global_exists(""item""))
{
    var its = """";
    var ii;
    var nitems = 8;
    for (ii = 0; ii < nitems; ii++) { its += string(global.item[ii]); its += "",""; }
    s += "","" + q + ""items_csv"" + q + "":"" + q + its + q;
}
// soul + bullet + monster positions for dodge-aware agents
var ho = asset_get_index(""obj_heart"");
if (ho != -1 && instance_exists(ho)) { s += "","" + q + ""soul_x"" + q + "":"" + string(ho.x) + "","" + q + ""soul_y"" + q + "":"" + string(ho.y); }
var bcv = """";
var bpa; bpa[0] = asset_get_index(""blt_parent""); bpa[1] = asset_get_index(""blt_parent_noborder"");
var bpp;
for (bpp = 0; bpp < 2; bpp++)
{
    var bp = bpa[bpp];
    if (bp == -1) continue;
    var bn = instance_number(bp);
    var bi;
    for (bi = 0; bi < bn; bi++)
    {
        var bo = instance_find(bp, bi);
        bcv += string(bo.x) + ""|"" + string(bo.y) + ""|"";
    }
}
if (bcv != """") s += "","" + q + ""bullets"" + q + "":"" + q + bcv + q;
var mp = asset_get_index(""obj_monsterparent"");
if (mp != -1)
{
    var mn = instance_number(mp);
    if (mn > 0)
    {
        var mcv = """";
        var ki;
        for (ki = 0; ki < mn; ki++)
        {
            var mo = instance_find(mp, ki);
            var spx = 0;
            if (variable_instance_exists(mo, ""spareable"") && mo.spareable) spx = 1;
            mcv += object_get_name(mo.object_index) + ""|"" + string(mo.x) + ""|"" + string(mo.y) + ""|"" + string(spx) + "";"";
        }
        s += "","" + q + ""monsters"" + q + "":"" + q + mcv + q;
    }
}
if (variable_global_exists(""monsterhp""))
{
    var mh = """";
    var mi2;
    for (mi2 = 0; mi2 < 3; mi2++) { mh += string(global.monsterhp[mi2]); mh += "",""; }
    s += "","" + q + ""monsterhp"" + q + "":"" + q + mh + q;
}
s += "","" + q + ""dbg_zcheck"" + q + "":"" + string(keyboard_check(ord(""Z"")));
s += "","" + q + ""dbg_zdirect"" + q + "":"" + string(keyboard_check_direct(ord(""Z"")));
s += "","" + q + ""dbg_rcheck"" + q + "":"" + string(keyboard_check(vk_right));
s += "","" + q + ""dbg_rdirect"" + q + "":"" + string(keyboard_check_direct(vk_right));
var tm = asset_get_index(""obj_time"");
if (tm != -1 && instance_exists(tm)) { with (tm) { global.bench_tr = right; global.bench_tryr = try_right; } s += "","" + q + ""tr"" + q + "":"" + string(global.bench_tr) + "","" + q + ""tryr"" + q + "":"" + string(global.bench_tryr); }
var ue = asset_get_index(""obj_undyneencounter1"");
if (ue != -1 && instance_exists(ue)) { with (ue) { global.bench_cn = cn; } s += "","" + q + ""cn"" + q + "":"" + string(global.bench_cn); }
s += ""}"";
var sf = file_text_open_write(""bench_state.json"");
file_text_write_string(sf, s);
file_text_close(sf);

// ---------------------------------------------------- event stream ----
// every observable change becomes one line in bench_events.txt:
// <eseq> <frame> <type> <detail>
var ev = """";
var nl = chr(10);

if (room != global.bench_pv_room)
{
    global.bench_eseq += 1;
    ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" room "" + room_get_name(room) + nl;
    global.bench_pv_room = room;
}

if (variable_global_exists(""hp""))
{
    var dh = global.hp - global.bench_pv_hp;
    if (global.bench_pv_hp != -999 && dh != 0)
    {
        global.bench_eseq += 1;
        ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" hp "" + string(dh) + nl;
    }
    global.bench_pv_hp = global.hp;
}

if (inbt != global.bench_pv_battle)
{
    global.bench_eseq += 1;
    ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" battle "" + string(inbt) + nl;
    global.bench_pv_battle = inbt;
}

if (variable_global_exists(""battlegroup""))
{
    if (global.battlegroup != global.bench_pv_bg)
    {
        global.bench_eseq += 1;
        ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" battlegroup "" + string(global.battlegroup) + nl;
        global.bench_pv_bg = global.battlegroup;
    }
}

var dlg = (haswr || hasdi || hasch);
if (dlg != global.bench_pv_dlg)
{
    global.bench_eseq += 1;
    ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" dialogue "" + string(dlg) + nl;
    global.bench_pv_dlg = dlg;
}

if (hasch != global.bench_pv_choicer)
{
    global.bench_eseq += 1;
    ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" choicer "" + string(hasch) + nl;
    global.bench_pv_choicer = hasch;
}

if (variable_global_exists(""choice""))
{
    if (global.choice != global.bench_pv_choice)
    {
        global.bench_eseq += 1;
        ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" choice "" + string(global.choice) + nl;
        global.bench_pv_choice = global.choice;
    }
}

if (variable_global_exists(""item""))
{
    var islot;
    for (islot = 0; islot < 8; islot++)
    {
        if (global.item[islot] != global.bench_pv_item[islot])
        {
            if (global.bench_pv_item[islot] != -999)
            {
                global.bench_eseq += 1;
                ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" item "" + string(islot) + "" "" + string(global.item[islot]) + nl;
            }
            global.bench_pv_item[islot] = global.item[islot];
        }
    }
}

if (variable_global_exists(""plot""))
{
    if (global.plot != global.bench_pv_plot)
    {
        global.bench_eseq += 1;
        ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" plot "" + string(global.plot) + nl;
        global.bench_pv_plot = global.plot;
    }
}

if (variable_global_exists(""exp"")) { if (global.exp != global.bench_pv_exp) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" exp "" + string(global.exp) + nl; global.bench_pv_exp = global.exp; } }
if (variable_global_exists(""lv"")) { if (global.lv != global.bench_pv_lv) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" lv "" + string(global.lv) + nl; global.bench_pv_lv = global.lv; } }
if (variable_global_exists(""gold"")) { if (global.gold != global.bench_pv_gold) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" gold "" + string(global.gold) + nl; global.bench_pv_gold = global.gold; } }
if (variable_global_exists(""kills"")) { if (global.kills != global.bench_pv_kills) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" kills "" + string(global.kills) + nl; global.bench_pv_kills = global.kills; } }

// death = shattered-heart object or gameover screen
var hd = asset_get_index(""obj_heartdefeated"");
var go = asset_get_index(""obj_gameover"");
var dead = ((hd != -1 && instance_exists(hd)) || (go != -1 && instance_exists(go)));
if (dead && !variable_global_exists(""bench_dead"")) global.bench_dead = 0;
if (dead && global.bench_dead == 0) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" death -"" + nl; global.bench_dead = 1; }
if (!dead) global.bench_dead = 0;

// savepoint interaction
var sp1 = asset_get_index(""obj_savepoint"");
var sp2 = asset_get_index(""obj_savepoint_fake"");
var spinter = ((sp1 != -1 && instance_exists(sp1) && (sp1).myinteract > 0) || (sp2 != -1 && instance_exists(sp2) && (sp2).myinteract > 0));
if (spinter && !variable_global_exists(""bench_sp"")) global.bench_sp = 0;
if (spinter && global.bench_sp == 0) { global.bench_eseq += 1; ev += string(global.bench_eseq) + "" "" + string(global.bench_frame) + "" save -"" + nl; global.bench_sp = 1; }
if (!spinter) global.bench_sp = 0;

if (ev != """")
{
    var lf = file_text_open_append(""bench_events.txt"");
    file_text_write_string(lf, ev);
    file_text_close(lf);
}
";

var stepCode = obj.EventHandlerFor(EventType.Step, EventSubtypeStep.Step, Data);

var importGroup = new CodeImportGroup(Data) { MainThreadAction = MainThreadAction };
importGroup.QueueAppend(stepCode, stepGml);
importGroup.Import();

// NOTE: do NOT patch obj_time keyboard_check_direct reads. On this runtime
// keyboard_check_direct observes keyboard_key_press simulation while
// keyboard_check does not -- the earlier suspicion was inverted; leave stock.


// ------------------------------------------------- place in the first room ---
UndertaleRoom room = Data.Rooms.ByName("room_introstory")
    ?? (Data.Rooms.Count > 0 ? Data.Rooms[0] : null);
if (room != null)
{
    var inst = new UndertaleRoom.GameObject();
    inst.InstanceID = Data.GeneralInfo.LastObj++;
    inst.ObjectDefinition = obj;
    inst.X = 0; inst.Y = 0;
    inst.CreationCode = null;
    room.GameObjects.Add(inst);
    ScriptMessage($"bench_bridge injected; instance {inst.InstanceID} placed in {room.Name.Content}.");
}
else
{
    ScriptMessage("bench_bridge injected as object only — no rooms in data file");
}

ChangeSelection(obj);
