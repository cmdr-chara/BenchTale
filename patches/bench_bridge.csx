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

// apply pending command
if (file_exists(""bench_cmd.json""))
{
    var cf = file_text_open_read(""bench_cmd.json"");
    var cjson = """";
    while (!file_text_eof(cf)) { cjson += file_text_read_string(cf); file_text_readln(cf); }
    file_text_close(cf);
    var cmd = json_decode(cjson);
    if (ds_exists(cmd, ds_type_map))
    {
        var seq = cmd[? ""seq""];
        if (seq > global.bench_seq)
        {
            global.bench_seq = seq;
            var keys = cmd[? ""keys""];
            var knames = ds_list_create();
            // order must match env/undertale_bench/keys.py
            ds_list_add(knames, ""left"", ""right"", ""up"", ""down"", ""z"", ""x"", ""c"", ""enter"", ""shift"", ""ctrl"");
            var vks = ds_list_create();
            ds_list_add(vks, vk_left, vk_right, vk_up, vk_down, ord(""Z""), ord(""X""), ord(""C""), vk_enter, vk_shift, vk_control);
            var i;
            for (i = 0; i < ds_list_size(knames); i++)
            {
                var want = 0;
                var kname = knames[| i];
                if (ds_map_exists(keys, kname)) want = keys[? kname];
                var vk = vks[| i];
                var have = keyboard_check(vk);
                if (want && !have) keyboard_key_press(vk);
                if (!want && have) keyboard_key_release(vk);
            }
            ds_list_destroy(knames);
            ds_list_destroy(vks);
            var af = file_text_open_write(""bench_ack.txt"");
            file_text_write_string(af, string(seq) + "" "" + string(global.bench_frame));
            file_text_close(af);
        }
        ds_map_destroy(cmd);
    }
}

// export state
var m = ds_map_create();
m[? ""frame""] = global.bench_frame;
m[? ""room""] = room;
m[? ""room_name""] = room_get_name(room);
var mc = asset_get_index(""obj_mainchara"");
if (mc != -1 && instance_exists(mc)) { m[? ""px""] = mc.x; m[? ""py""] = mc.y; }
if (variable_global_exists(""hp"")) m[? ""hp""] = global.hp;
if (variable_global_exists(""maxhp"")) m[? ""maxhp""] = global.maxhp;
if (variable_global_exists(""lv"")) m[? ""lv""] = global.lv;
if (variable_global_exists(""exp"")) m[? ""exp""] = global.exp;
if (variable_global_exists(""gold"")) m[? ""gold""] = global.gold;
if (variable_global_exists(""plot"")) m[? ""plot""] = global.plot;
if (variable_global_exists(""battlegroup"")) m[? ""battlegroup""] = global.battlegroup;
if (variable_global_exists(""mercymod"")) m[? ""mercymod""] = global.mercymod;
if (variable_global_exists(""myfight"")) m[? ""myfight""] = global.myfight;
if (variable_global_exists(""battlephase"")) m[? ""battlephase""] = global.battlephase;
if (variable_global_exists(""at"")) m[? ""at""] = global.at;
if (variable_global_exists(""df"")) m[? ""df""] = global.df;
if (variable_global_exists(""kills"")) m[? ""kills""] = global.kills;
if (variable_global_exists(""msg""))
{
    var msg = """";
    var mi;
    var msglen = 0;
    msglen = array_length_1d(global.msg);
    if (msglen > 20) msglen = 20;
    for (mi = 0; mi < msglen; mi++) { if (is_string(global.msg[mi])) msg += global.msg[mi] + "" ""; }
    m[? ""msg""] = msg;
}
if (variable_global_exists(""flag""))
{
    var fl = ds_list_create();
    var fi;
    var nflags = array_length_1d(global.flag);
    if (nflags > 512) nflags = 512;
    for (fi = 0; fi < nflags; fi++) ds_list_add(fl, global.flag[fi]);
    ds_map_add_list(m, ""flags"", fl);
}
var bc = asset_get_index(""obj_battlecontroller"");
var wr = asset_get_index(""obj_writer"");
m[? ""in_battle""] = (bc != -1 && instance_exists(bc));
m[? ""dialogue""] = (wr != -1 && instance_exists(wr));
var sf = file_text_open_write(""bench_state.json"");
file_text_write_string(sf, json_encode(m));
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
