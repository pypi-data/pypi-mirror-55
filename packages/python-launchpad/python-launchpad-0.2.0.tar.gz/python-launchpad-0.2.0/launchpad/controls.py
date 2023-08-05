import itertools
from collections import OrderedDict

from .buttons import ButtonGroup
from .colors import Color, Colors


class Control(object):
    def __init__(self, callback=None, buttons=None):
        self.callback = callback or (lambda *a, **ka: None)
        self.buttons = buttons or []

    def dispatch(self, lp, type_, button, value):
        for check_type, check_button in self.buttons:
            if type_ == check_type and button == check_button:
                self._dispatch(lp, type_, button, value)
                return True
        return False

    def render(self, lp):
        pass

    def _dispatch(self, lp, type_, button, value):
        raise NotImplementedError()

    def set_color(self, lp, type_, button, color):
        if type_ == 'GRID':
            lp.set_color(button[0], button[1], color)
        else:
            lp.set_color(type_, button, color)

    def set_all_color(self, lp, color):
        for type_, button in self.buttons:
            self.set_color(lp, type_, button, color)


class Momentary(Control):
    def __init__(self, on_color=None, off_color=None, *args, **kwargs):
        super(Momentary, self).__init__(*args, **kwargs)
        self.on_color = on_color or Color(Colors.GREEN)
        self.off_color = off_color or Color(Colors.OFF)

    def _get_color(self, mode, type_, button):
        c = getattr(self, mode + '_color')
        if isinstance(c, list):
            return c[self.buttons.index((type_, button))]
        return c

    def render(self, lp):
        for type_, button in self.buttons:
            self.set_color(lp, type_, button, self._get_color('off', type_, button))

    def _dispatch(self, lp, type_, button, value):
        if value:
            self.set_color(lp, type_, button, self._get_color('on', type_, button))
        else:
            self.set_color(lp, type_, button, self._get_color('off', type_, button))
        self.callback(lp, type_, button, value)


class Toggle(Control):
    def __init__(self, states=None, colors=None, group=False, *args, **kwargs):
        super(Toggle, self).__init__(*args, **kwargs)
        self.states = states or 2
        self.colors = colors or [Color(Colors.OFF), Color(Colors.GREEN)]
        self.group = group

        if len(self.colors) != self.states:
            raise ValueError("Number of colors ({}) must match number of states({})".format(len(self.colors), self.states))

        self.button_states = {}

    def render(self, lp):
        for type_, button in self.buttons:
            state = self.button_states.get((hash(lp), type_, button), 0)
            self.set_color(lp, type_, button, self.colors[state])

    def _dispatch(self, lp, type_, button, value):
        if value:
            if self.group:
                for g_type_, g_button in self.buttons:
                    if g_type != type_ and g_button != button:
                        self.button_states[(hash(lp), g_type_, g_button)] = 0
            state = self.button_states.get((hash(lp), type_, button), 0)
            state += 1
            if state + 1 > self.states:
                state = 0
            self.set_color(lp, type_, button, self.colors[state])
            self.button_states[(hash(lp), type_, button)] = state
            self.callback(lp, type_, button, state)


class Slider(Control):
    O_HZ = 1
    O_VT = 2

    CM_GROUP = 1
    CM_ALL = 2

    def __init__(self, position, orientation=None, on_colors=None, off_color=None, color_mode=None, *args, **kwargs):
        self.position = position
        self.orientation = orientation or self.O_VT
        self.on_colors = on_colors or Color(Colors.YELLOW)
        self.off_color = off_color or Color(Colors.OFF)
        self.color_mode = color_mode or self.CM_ALL

        if isinstance(self.on_colors, Color):
            self.on_colors = OrderedDict([(i, self.on_colors) for i in range(8)])
        elif isinstance(self.on_colors, list):
            self.on_colors = OrderedDict([(i, self.on_colors[int(i / len(self.on_colors))]) for i in range(8)])
        else:
            self.on_colors = OrderedDict(self.on_colors.items())

        if self.orientation == self.O_HZ:
            buttons = ButtonGroup(0, self.position, 7, self.position)
        elif self.orientation == self.O_VT:
            buttons = ButtonGroup(self.position, 0, self.position, 7)

        self.values = {}

        super(Slider, self).__init__(buttons=buttons, *args, **kwargs)

    def render(self, lp):
        value = self.values.setdefault(hash(lp), 0)
        if self.orientation == self.O_HZ:
            on = 0, value + 1
            off = value + 1, 8
        else:
            on = 7 - value, 8
            off = 0, 7 - value

        for i in range(*on):
            if self.color_mode == self.CM_ALL:
                color_i = 7 - ((7 - value) if self.orientation == self.O_VT else value)
            elif self.color_mode == self.CM_GROUP:
                if self.orientation == self.O_VT:
                    color_i = 7 - i
                else:
                    color_i = i
            self.set_color(lp, self.buttons[i][0], self.buttons[i][1], self.on_colors[color_i])
        for i in range(*off):
            self.set_color(lp, self.buttons[i][0], self.buttons[i][1], self.off_color)

    def _dispatch(self, lp, type_, button, value):
        if value:
            if self.orientation == self.O_HZ:
                lp_value = button[0]
            else:
                lp_value = 7 - button[1]

            self.values[hash(lp)] = lp_value

            self.render(lp)
            self.callback(lp, type_, button, lp_value)


# class MultiSlider(Control):
#     M_CONTINUOUS = 1
#     M_LINKED = 2
#     M_SUM = 3

#     def __init__(self, position, orientation=None, on_colors=None, off_color=None, color_mode=None, width=None, mode=None, *args, **kwargs):
#         self.position = position
#         self.orientation = orientation or Slider.O_VT
#         self.on_colors = on_colors or Color(Colors.YELLOW)
#         self.off_color = off_color or Color(Colors.OFF)
#         self.color_mode = color_mode or Slider.CM_ALL
#         self.width = width or 2
#         self.mode = mode or self.M_CONTINUOUS

#         color_range = ((8 * self.width) - 1) if self.mode == self.M_CONTINUOUS else 8
#         if isinstance(self.on_colors, Color):
#             self.on_colors = OrderedDict([(i, self.on_colors) for i in range(color_range)])
#         elif isinstance(self.on_colors, list):
#             print(len(self.on_colors), color_range, list(range(color_range)))
#             print([int(i/((color_range - 1) / len(self.on_colors))) for i in range(color_range)])
#             self.on_colors = OrderedDict([(i, self.on_colors[int(i / (color_range / len(self.on_colors)))]) for i in range(color_range)])
#         else:
#             self.on_colors = OrderedDict(self.on_colors.items())

#         if self.orientation == Slider.O_HZ:
#             buttons = [ButtonGroup(0, i, 7, i) for i in range(self.position, self.position + self.width)]
#         elif self.orientation == Slider.O_VT:
#             buttons = [ButtonGroup(i, 0, i, 7) for i in range(self.position, self.position + self.width)]

#         super(MultiSlider, self).__init__(buttons=itertools.chain(*buttons), *args,**kwargs)

#         self.sliders = [
#             Slider(
#                 position=i,
#                 orientation=self.orientation,
#                 on_colors=self.on_colors.values()[i:i + 8] if self.mode == self.M_CONTINUOUS else self.on_colors,
#                 off_color=self.off_color,
#                 color_mode=self.color_mode,
#                 callback=self._handle_press
#             )
#             for i in range(self.position, self.position + self.width)
#         ]
#         self.values = {}

#     def render(self, lp):
#         for s in self.sliders:
#             s.render(lp)

#     def _dispatch(self, lp, type_, button, value):
#         import pudb;pudb.set_trace()
#         if value:
#             dispatched_to = None
#             for s in self.sliders:
#                 if s.dispatch(lp, type_, button, value):
#                     dispatched_to = s

#             if self.mode == self.M_SUM:
#                 self.values[hash(lp)] = sum([s.values.get(hash(lp), 0) for s in self.sliders])
#             elif self.mode == self.M_LINKED:
#                 if dispatched_to:
#                     self.values[hash(lp)] = dispatched_to.values.get(hash(lp), 0)
#                     for s in self.sliders:
#                         s.value[hash(lp)] = self.values.get(hash(lp), 0)
#             elif self.mode == self.M_CONTINUOUS:
#                 if dispatched_to:
#                     self.values[hash(lp)] = ((dispatched_to.position - self.position) * 8) + dispatched_to.value

#             for s in self.sliders:
#                 s.render(lp)
#             self.callback(lp, type_, button, self.values.get(hash(lp), 0))

#     def _handle_press(self, lp, type_, button, value):
#         return
#         # self._dispatch(lp, type_, button, value)
