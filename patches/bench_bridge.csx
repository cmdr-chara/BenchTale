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

// apply pending command (flat text: first line seq N, then key 0|1)
if (file_exists(""bench_cmd.txt""))
{
    var cf = file_text_open_read(""bench_cmd.txt"");
    var hdr = file_text_read_string(cf); file_text_readln(cf);
    var seq = real(string_copy(hdr, 5, 12));
    if (seq > global.bench_seq)
    {
        global.bench_seq = seq;
        while (!file_text_eof(cf))
        {
            var line = file_text_read_string(cf); file_text_readln(cf);
            var sp = string_pos("" "", line);
            if (sp > 0)
            {
                var k = string_copy(line, 1, sp - 1);
                var v = (string_copy(line, sp + 1, 4) == ""1"");
                if (k == ""goto"")
                {
                    var rn = string_copy(line, sp + 1, 64);
                    var ridx = asset_get_index(rn);
                    if (ridx != -1) room_goto(ridx);
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
                if (k == ""shift"") vk = vk_shift;
                if (k == ""ctrl"") vk = vk_control;
                if (vk != -1)
                {
                    if (v && !keyboard_check(vk)) keyboard_key_press(vk);
                    if (!v && keyboard_check(vk)) keyboard_key_release(vk);
                }
            }
        }
        var af = file_text_open_write(""bench_ack.txt"");
        file_text_write_string(af, string(seq) + "" "" + string(global.bench_frame));
        file_text_close(af);
    }
    file_text_close(cf);
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
s += "","" + q + ""in_battle"" + q + "":"" + string(bc != -1 && instance_exists(bc));
s += "","" + q + ""dialogue"" + q + "":"" + string(wr != -1 && instance_exists(wr));
s += "","" + q + ""dbg_zcheck"" + q + "":"" + string(keyboard_check(ord(""Z"")));
s += "","" + q + ""dbg_zdirect"" + q + "":"" + string(keyboard_check_direct(ord(""Z"")));
s += ""}"";
var sf = file_text_open_write(""bench_state.json"");
file_text_write_string(sf, s);
file_text_close(sf);
";

var stepCode = obj.EventHandlerFor(EventType.Step, EventSubtypeStep.Step, Data);

var importGroup = new CodeImportGroup(Data) { MainThreadAction = MainThreadAction };
importGroup.QueueAppend(stepCode, stepGml);
importGroup.Import();

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
