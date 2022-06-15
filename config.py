# -*- coding: utf-8 -*-
import os
import re
import socket
import asyncio
import dbus
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
alt = "mod1"
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "control"], "l",
             lazy.spawn("betterlockscreen -l"),
             desc='Lock Screen'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='firefox'
             ),
         Key([mod], "d",
             lazy.spawn("thunar"),
             desc='thunar'
             ),
         Key([mod, "control"], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod, "shift"], "p",
             lazy.spawn("flameshot gui"),
             desc='flameshot screenshot'
             ),
         Key([mod, "control"], "h",
             lazy.spawn("dunstctl history-pop"),
             desc='show dunst history'
             ),
         ### rofi
         Key([mod, "control"], "Return",
             lazy.spawn("rofi -show run"),
             desc='Run Launcher'
             ),
         Key([mod], "space",
             lazy.spawn("rofi -show drun"),
             desc='Run Launcher with .desktop apps'
             ),
         Key([mod], "Tab",
             lazy.spawn("rofi -show window"),
             desc='Window-Control All'
             ),
         Key([mod, "control"], "w",
             lazy.spawn("rofi -show windowcd"),
             desc='Window Control current'
             ),
         Key([mod, "control"], "t",
             lazy.spawn("rofi -show calc"),
             desc='Calculator'
             ),
         Key([mod, "control"], "f",
             lazy.spawn("rofi -show filebrowser"),
             desc='filebrowser'
             ),
         Key([mod, "control"], "e",
             lazy.spawn("rofi -show emoji"),
             desc='emoji'
             ),
         Key([mod, "control"], "r",
             lazy.spawn("rofi -show"),
             desc='rofi base'
             ),
         Key([mod, "control"], "c",
             lazy.spawn("clipmenu"),
             desc='Clipboard Menu'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "e",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "w",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ## Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod], "h",
             lazy.layout.left(),
             desc='Move focus left in current stack pane'
             ),
         Key([mod], "l",
             lazy.layout.right(),
             desc='Move focus right in current stack pane'
             ),

         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod, "shift"],  "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod, "control"], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### Media Controls
         Key([], "XF86AudioLowerVolume", 
                 lazy.spawn("amixer sset Master 5%-"), 
                 desc="Lower Volume by 5%"),
         Key([], "XF86AudioRaiseVolume", 
                 lazy.spawn("amixer sset Master 5%+"), 
                 desc="Raise Volume by 5%"),
         Key([], "XF86AudioMute", 
                 lazy.spawn("amixer sset Master 1+ toggle"), 
                 desc="Mute/Unmute Volume"),
         Key([mod], "p", 
                 lazy.spawn("playerctl play-pause"), 
                 desc="Play/Pause player")
]

groups = [Group("", layout='monadtall', matches=[Match(wm_class=["firefox"])]),
          Group("", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("", layout='monadtall', matches=[Match(wm_class=["Thunderbird"])]),
          Group("", layout='monadtall'),
          Group("", layout='floating'),
          Group("", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("", layout='monadtall')]


@hook.subscribe.client_new
async def move_spotify(client):
        await asyncio.sleep(0.01)
        if client.name == 'Spotify': client.togroup('')
        elif client.name == 'Discord': client.togroup('')
        elif client.name == 'Joplin': client.togroup('')
        elif client.name == 'Kalender': client.togroup('')
        elif client.name == 'Signal': client.togroup('')

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 13,
                "border_focus": "#8ec07c",
                "border_normal": "#282828"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "ShareTechMono",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "c678dd",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
    layout.Floating(**layout_theme)
]

colors = [["#282828", "#282828"], #0 Gruv bg
          ["#458588", "#458588"], #1 Gruv Blue
          ["#ebdbb2", "#ebdbb2"], #2 Gruv fg
          ["#fabd2f", "#fabd2f"], #3 Gruv yellow
          ["#fb4934", "#fb4934"], #4 Gruv red
          ["#b8bb26", "#b8bb26"], #5 Gruv green
          ["#fe8019", "#fe8019"], #6 Gruv Orange
          ["#928374", "#928374"], #7 Gruv gray
          ["#8ec07c", "#8ec07c"], #8 Gruv aqua
          ["#b16286", "#b16286"]] #9 Gruv Purple

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="ShureTechMono Nerd Font Bold",
    fontsize = 15,
    padding = 4,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "ShureTechMono Nerd Font Bold" ,
                       fontsize = 27,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = True,
                       highlight_color = colors[1],
                       highlight_method = "block",
                       this_current_screen_border = colors[8],
                       this_screen_border = colors [6],
                       other_current_screen_border = colors[8],
                       other_screen_border = colors[6],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "ShureTechMono Nerd Font Bold",
                       background = colors[0],
                       foreground = 'd79921',
                       padding = 2,
                       fontsize = 16
                       ),
             widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
             widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[0],
                       foreground = colors[6],
                       padding = 0,
                       fontsize = 42
                       ),
             widget.Mpris2(
                       background = colors[6],
                       foreground = colors[0],
                       name='spotify',
                       fmt = " {}",
                       objname="org.mpris.MediaPlayer2.spotify",
                       display_metadata=['xesam:title', 'xesam:artist'],
                       scroll_chars=None
                       ),
             widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[6],
                       foreground = colors[1],
                       padding = 0,
                       fontsize = 42
                       ),
             widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[1],
                       padding = 0,
                       scale = 0.7
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[1],
                       background = colors[1]
                       ),
            widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[1],
                       foreground = colors[9],
                       padding = 0,
                       fontsize = 42
                       ),
              widget.Volume(
                       foreground = colors[0],
                       background = colors[9],
                       fmt = '墳 {}',
                       padding = 6,
                       mouse_callbacks = {"Button3": lazy.spawn("pavucontrol")}
                       ),
              widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[9],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 42
                       ),
              widget.KeyboardLayout(
                       foreground = colors[0],
                       background = colors[8],
                       fmt = '  {}',
                       configured_keyboards=['de','us'],
                       padding = 5
                       ),
              widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[8],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 42
                       ),
              widget.Clock(
                       foreground = colors[0],
                       background = colors[5],
                       format = "  %A, %d. %B - %H:%M Uhr"
                       ),
               widget.TextBox(
                      text = '',
                       font = "Ubuntu Bold",
                       background = colors[5],
                       foreground = colors[0],
                       padding = 0,
                       fontsize = 42
                       ),
             widget.Systray(
                       background = colors[0],
                       padding = 5 
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
             widget.TextBox(
                      text = '⏻',
                       font = "Ubuntu Bold",
                       background = colors[6],
                       foreground = colors[0],
                       padding = 5,
                       mouse_callbacks = {"Button1": lazy.spawn("powermenu.sh")},
                       fontsize = 42
                       )
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                 # Alle Widgets auf Monitor 1, DP1, BenQ

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[16:19]              # Sys-Tray wird von Monitor 2, DP3, Acer entfernt 
    return widgets_screen2                 

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=34), wallpaper="/home/manuel/Bilder/wallpapers/wrc7zf2wlpr61.jpg", wallpaper_mode="fill"),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=34), wallpaper="/home/manuel/Bilder/wallpapers/wrc7zf2wlpr61.jpg", wallpaper_mode="fill")]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
