# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
from math import inf,sqrt,atan
from pprint import pformat

def center_of_screen(screen):
    x,y=screen.x,screen.y
    w,h=screen.width,screen.height
    return x+w/2,y+h/2

def center_of_window(w):
    x,y=w['x'],w['y']
    w,h=w['width'],w['height']
    return x+w/2,y+h/2

def direction_to_screen_id(qtile,direction):
    screens = qtile.screens.copy()
    positions = []
    for i in range(len(screens)):
        screen=screens[i]
        positions.append(center_of_screen(screen))
        if screen.index == qtile.current_screen.index:
            current_screen = screen
            current_screen_list_index = i
    lowest_distance = inf
    lowest_distance_index = None
    own_pos=positions[current_screen_list_index]
    for i in range(len(positions)):
        p=positions[i]
        if direction in ('right','down'):
            if p[0] > own_pos[0] and point_is_in_direction_from_point(own_pos,direction,p):
                d = distance_of_points(own_pos,p)
                if d < lowest_distance:
                    lowest_distance=d
                    lowest_distance_index = i
            else:
                p = None
        elif direction in ('left','up'):
            if p[0] < own_pos[0] and point_is_in_direction_from_point(own_pos,direction,p):
                d = distance_of_points(own_pos,p)
                if d < lowest_distance:
                    lowest_distance=d
                    lowest_distance_index = i
            else:
                p = None
    if not lowest_distance_index is None:
        return screens[lowest_distance_index].index

def val_in_interval(v,interval):
    return interval[0] < v < interval[1]

def pos_in_2D_interval(pos,interval):
    return val_in_interval(pos[0],interval[0]) and val_in_interval(pos[1],interval[1])

def direction_to_win_id_on_current_screen(qtile,direction):
    windows = qtile.cmd_windows()
    positions = []
    for i in range(len(windows)):
        window=windows[i]
        positions.append(center_of_window(window))
        try:
            if window["id"] == qtile.current_window.info()['id']:
                current_window = window
                current_window_list_index = i
        except AttributeError:
            return None
    lowest_distance = inf
    lowest_distance_index = None
    own_pos=positions[current_window_list_index]
    interval_x = qtile.current_screen.x,qtile.current_screen.x+qtile.current_screen.width
    interval_y = qtile.current_screen.y,qtile.current_screen.y+qtile.current_screen.height
    for i in range(len(positions)):
        p=positions[i]
        if pos_in_2D_interval(p,(interval_x,interval_y)):
            if direction in ('right','down'):
                if p[0] > own_pos[0] and point_is_in_direction_from_point(own_pos,direction,p):
                    d = distance_of_points(own_pos,p)
                    if d < lowest_distance:
                        lowest_distance=d
                        lowest_distance_index = i
                else:
                    p = None
            elif direction in ('left','up'):
                if p[0] < own_pos[0] and point_is_in_direction_from_point(own_pos,direction,p):
                    d = distance_of_points(own_pos,p)
                    if d < lowest_distance:
                        lowest_distance=d
                        lowest_distance_index = i
                else:
                    p = None
        else:
            p = None
    if not lowest_distance_index is None:
        return windows[lowest_distance_index]['id']

def point_is_in_direction_from_point(p0,direction,p1):
    p = (p1[0]-p0[0], p1[1]-p0[1])
    if direction in ('left', 'right'):
        return (p[1]/p[0])**2 <= 1
    elif direction in ('up', 'down'):
        return (p[1]/p[0])**2 >= 1

def distance_of_points(p0,p1):
    p = (p1[0]-p0[0], p1[1]-p0[1])
    return sqrt(p[0]**2+p[1]**2)

def move_win(qtile,direction):
    sid = direction_to_screen_id(qtile,direction)
    if not sid is None:
        group = qtile.screens[sid].group.name
        qtile.current_window.togroup(group)
    elif qtile.current_layout.name == "verticaltile":
        if direction == "up":
            qtile.current_layout.cmd_shuffle_up()
        elif direction == "down":
            qtile.current_layout.cmd_shuffle_down()
   # else:
   #     logger.log(99,"no screen in this direction")

def go(qtile,direction):
    if qtile.current_layout.name == "treetab":
        if direction == "up":
            qtile.current_layout.cmd_up()
        elif direction == "down":
            qtile.current_layout.cmd_down()
        else:
            go_screen(qtile,direction)
    elif qtile.current_layout.name == "verticaltile":
        # somehow the wid thing below does not work
        # TODO: fix the wid thing to work and remove this elif section
        if direction == "up":
            qtile.current_layout.cmd_up()
        elif direction == "down":
            qtile.current_layout.cmd_down()
        else:
            go_screen(qtile,direction)
    else:
        logger.log(99,"else")
        wid = direction_to_win_id_on_current_screen(qtile,direction)
        if not wid is None:
            if direction == "right":
                qtile.current_layout.cmd_right()
            elif direction == "left":
                qtile.current_layout.cmd_left()
            elif direction == "up":
                qtile.current_layout.cmd_up()
            elif direction == "down":
                qtile.current_layout.cmd_down()
        else:
            go_screen(qtile,direction)

def go_screen(qtile,direction):
    sid = direction_to_screen_id(qtile,direction)
    if not sid is None:
        group = qtile.screens[sid].group.name
        #msg=pformat([qtile,dir(qtile),type(qtile),qtile.warp_to_screen.__doc__])
        #logger.log(99,msg)
        qtile.cmd_to_screen(sid)
    else:
        logger.log(99,"no screen in this direction")


CA  = ["mod1", "control"]
CAS = CA + ["shift"]
terminal = guess_terminal()

keys = [
    # Switch between windows
    Key(CA, "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    Key(CA , "s", lazy.function(go,"left")),
    Key(CA , "f", lazy.function(go,"right")),
    Key(CA , "d", lazy.function(go,"down")),
    Key(CA , "e", lazy.function(go,"up")),

    Key(CA, "j", lazy.function(move_win,"left")),
    Key(CA, "l", lazy.function(move_win,"right")),
    Key(CA, "k", lazy.function(move_win,"down")),
    Key(CA, "i", lazy.function(move_win,"up")),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(CAS, "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key(CA, "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key(CA, "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key(CA, "q", lazy.window.kill(), desc="Kill focused window"),
    Key(CA, "w", lazy.window.toggle_floating()),

    Key(CAS, "r", lazy.restart(), desc="Restart Qtile"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key(CA, i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key(CAS , i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key(mod + [ "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    #layout.MonadWide(),
    layout.RatioTile(),
    # layout.Tile(),
    layout.TreeTab(),
    layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

fake_screens = [
    Screen(
        x=0,
        y=156,
        width=1366,
        height=768,
    #    bottom=bar.Bar(
    #        [
    #            widget.CurrentLayout(),
    #            widget.GroupBox(),
    #            widget.Prompt(),
    #            widget.WindowName(),
    #            widget.Chord(
    #                chords_colors={
    #                    'launch': ("#ff0000", "#ffffff"),
    #                },
    #                name_transform=lambda name: name.upper(),
    #            ),
    #            widget.TextBox("my config", name="default"),
    #            widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
    #            widget.Systray(),
    #            widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
    #            widget.QuickExit(),
    #        ],
    #        24,
    #    ),
    ),
    Screen(
        x=1366,
        y=0,
        width=960,
        height=1080,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(CA, "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag(CA, "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click(CA, "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
