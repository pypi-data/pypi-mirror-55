import fnmatch
import uuid
import threading

import mido

from .buttons import (
    TOP_BUTTONS,
    RIGHT_BUTTONS,
    TOP_BUTTONS_INV,
    RIGHT_BUTTONS_INV,
    get_button,
    coord_to_note,
)
from .colors import Color, Colors
from .controls import Momentary, Toggle


class Page(object):
    def __init__(self, include_top=True, include_right=True, controls=None):
        self.include_top = include_top
        self.include_right = include_right
        if isinstance(controls, dict):
            self.controls = controls
        else:
            for c in controls or []:
                self.add_control(c)

        self.control_lock = threading.Lock()
        self.control_queue = {}

    def add_control(self, lp, control, name=None):
        self.control_queue[name or str(uuid.uuid4())] = control
        if self._apply_control_queue():
            self.render(lp)

    def remove_control(self, lp, control_or_name):
        if control_or_name in self.controls:
            self.control_queue[control_or_name] = False
        else:
            for k, v in self.controls.items():
                if v is control_or_name:
                    self.control_queue[k] = False
                    break
        if self._apply_control_queue():
            lp.render()

    def _apply_control_queue(self):
        changed = False
        if self.control_lock.acquire(False):
            try:
                for k, v in self.control_queue.items():
                    changed = True
                    if v is False:
                        del self.controls[k]
                    else:
                        self.controls[k] = v
                self.control_queue = {}
            finally:
                self.control_lock.release()
        return changed

    def render(self, lp):
        lp.reset(reset_top=self.include_top, reset_right=self.include_right)
        for control in self.controls.values():
            control.render(lp)

    def dispatch(self, lp, type_, button, value):
        with self.control_lock:
            for control in self.controls.values():
                control.dispatch(lp, type_, button, value)
        if self._apply_control_queue():
            lp.render()


# class PageManager(object):
#     def __init__(self, grid_pages=None, user_pages=None, mixer_pages=None):
#         self.grid_pages = grid_pages or {}
#         self.user_pages = user_pages or {}
#         self.mixer_pages = mixer_pages or {}
#         self.session_page = Page(include_top=False, include_right=False)
#         self.default_page = Page(controls=[
#             # def __init__(self, on_color=None, off_color=None, *args, **kwargs):
#             Momentary(callback=self.shift_grid(0, -1), buttons=[('TOP', 'UP')]),
#             Momentary(callback=self.shift_grid(0, 1), buttons=[('TOP', 'DOWN')]),
#             Momentary(callback=self.shift_grid(-1, 0), buttons=[('TOP', 'LEFT')]),
#             Momentary(callback=self.shift_grid(1, 0), buttons=[('TOP', 'RIGHT')]),
#             Toggle(callback=self.show_page, buttons=[
#                 ('TOP', 'SESSION'),
#                 ('TOP', 'USER1'),
#                 ('TOP', 'USER2'),
#                 ('TOP', 'MIXER'),
#             ]),
#         ])


class Launchpad(object):
    @classmethod
    def list_devices(self):
        inputs = set(mido.get_input_names())
        outputs = inputs & set(mido.get_output_names())
        return [d for d in outputs if fnmatch.fnmatch(d, '*Launchpad*')]

    def __init__(self, device=None):
        self.device = device or self.list_devices()[0]
        self.inp = mido.open_input(self.device)
        self.outp = mido.open_output(self.device)
        self.pages = []
        self.reset()

    def __hash__(self):
        return hash(str(self.device))

    def reset(self, reset_top=True, reset_right=True):
        if reset_top:
            for y in TOP_BUTTONS.values():
                self.set_color('TOP', y, Color(Colors.OFF))
        if reset_right:
            for y in RIGHT_BUTTONS.values():
                self.set_color('RIGHT', y, Color(Colors.OFF))
        for x in range(8):
            for y in range(8):
                self.set_color(x, y, Color(Colors.OFF))

    def _set_color_basic(self, x, y, color, channel=None):
        if color.intensity == None:
            color = color.color.on
        else:
            color = color.color.intensity(color.intensity)

        if x == 'TOP':
            button = TOP_BUTTONS_INV[y]
            self.outp.send(mido.Message('control_change', channel=channel or 0, control=button, value=color))
        elif x == 'RIGHT':
            button = RIGHT_BUTTONS_INV[y]
            self.outp.send(mido.Message('note_on', channel=channel or 0, note=button, velocity=color))
        else:
            self.outp.send(mido.Message('note_on', channel=channel or 0, note=coord_to_note(x, y), velocity=color))

    def _set_color_rgb(self, x, y, color, channel=None):
        r = int(color.r * 63)
        g = int(color.g * 63)
        b = int(color.b * 63)
        if x == 'TOP':
            button = TOP_BUTTONS_INV[y]
            self.outp.send(mido.Message('sysex', data=[0, 32, 41,  2, 24, 11, button, r, g, b]))
        elif x == 'RIGHT':
            button = RIGHT_BUTTONS_INV[y]
            self.outp.send(mido.Message('sysex', data=[0, 32, 41,  2, 24, 11, button, r, g, b]))
        else:
            button = int(11 + (((7 - y) * 10) + x))
            self.outp.send(mido.Message('sysex', data=[0, 32, 41,  2, 24, 11, button, r, g, b]))

    def set_color(self, x, y, color):
        if hasattr(color, 'color'):
            self._set_color_basic(x, y, color)
        else:
            self._set_color_rgb(x, y, color)

    def poll(self):
        for message in self.inp.iter_pending():
            type_, button, value = get_button(message)
            for page in reversed(self.pages):
                if type_ == 'TOP':
                    if page.include_top:
                        page.dispatch(self, type_, button, value)
                        break
                    else:
                        continue
                elif type_ == 'RIGHT':
                    if page.include_right:
                        page.dispatch(self, type_, button, value)
                        break
                    else:
                        continue
                else:
                    page.dispatch(self, type_, button, value)
                    break

    def poll_callback(self, callback):
        for message in self.inp.iter_pending():
            callback(*get_button(message))

    def render(self):
        self.pages[-1].render(self)

    def push_page(self, page):
        self.pages.append(page)
        self.render()

    def pop_page(self, if_not_pages=None):
        if self.pages:
            if if_not_pages:
                if self.pages[-1] in if_not_pages:
                    return

            self.pages.pop()
            if self.pages:
                self.pages[-1].render(self)
            else:
                self.reset()
