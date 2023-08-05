from collections import OrderedDict


TOP_BUTTONS = OrderedDict([
    (104, 'UP'),
    (105, 'DOWN'),
    (106, 'LEFT'),
    (107, 'RIGHT'),
    (108, 'SESSION'),
    (109, 'USER1'),
    (110, 'USER2'),
    (111, 'MIXER'),
])
RIGHT_BUTTONS = OrderedDict([
    (89, 'VOLUME'),
    (79, 'PAN'),
    (69, 'SENDA'),
    (59, 'SENDB'),
    (49, 'STOP'),
    (39, 'MUTE'),
    (29, 'SOLO'),
    (19, 'RECORDARM'),
])
GRID_BUTTONS = OrderedDict([
    (81, (0, 0)),
    (82, (1, 0)),
    (83, (2, 0)),
    (84, (3, 0)),
    (85, (4, 0)),
    (86, (5, 0)),
    (87, (6, 0)),
    (88, (7, 0)),

    (71, (0, 1)),
    (72, (1, 1)),
    (73, (2, 1)),
    (74, (3, 1)),
    (75, (4, 1)),
    (76, (5, 1)),
    (77, (6, 1)),
    (78, (7, 1)),

    (61, (0, 2)),
    (62, (1, 2)),
    (63, (2, 2)),
    (64, (3, 2)),
    (65, (4, 2)),
    (66, (5, 2)),
    (67, (6, 2)),
    (68, (7, 2)),

    (51, (0, 3)),
    (52, (1, 3)),
    (53, (2, 3)),
    (54, (3, 3)),
    (55, (4, 3)),
    (56, (5, 3)),
    (57, (6, 3)),
    (58, (7, 3)),

    (41, (0, 4)),
    (42, (1, 4)),
    (43, (2, 4)),
    (44, (3, 4)),
    (45, (4, 4)),
    (46, (5, 4)),
    (47, (6, 4)),
    (48, (7, 4)),

    (31, (0, 5)),
    (32, (1, 5)),
    (33, (2, 5)),
    (34, (3, 5)),
    (35, (4, 5)),
    (36, (5, 5)),
    (37, (6, 5)),
    (38, (7, 5)),

    (21, (0, 6)),
    (22, (1, 6)),
    (23, (2, 6)),
    (24, (3, 6)),
    (25, (4, 6)),
    (26, (5, 6)),
    (27, (6, 6)),
    (28, (7, 6)),

    (11, (0, 7)),
    (12, (1, 7)),
    (13, (2, 7)),
    (14, (3, 7)),
    (15, (4, 7)),
    (16, (5, 7)),
    (17, (6, 7)),
    (18, (7, 7)),
])
TOP_BUTTONS_INV = OrderedDict(zip(TOP_BUTTONS.values(), TOP_BUTTONS.keys()))
RIGHT_BUTTONS_INV = OrderedDict(zip(RIGHT_BUTTONS.values(), RIGHT_BUTTONS.keys()))
GRID_BUTTONS_INV = OrderedDict(zip(GRID_BUTTONS.values(), GRID_BUTTONS.keys()))


def coord_to_note(x, y):
    # return int((((7 - y) * 10) + x) + 11)
    return GRID_BUTTONS_INV[(x, y)]


def note_to_coord(note):
    # x = int((note - 11) % 10)
    # y = int(7 - ((note - 11) / 10))
    # return x, y
    return GRID_BUTTONS[note]


def get_button(message):
    if message.type == 'control_change':
        return 'TOP', TOP_BUTTONS.get(message.control), message.value > 0
    elif message.type in ('note_on', 'note_off'):
        button = RIGHT_BUTTONS.get(message.note)
        if button:
            return 'RIGHT', button, message.velocity > 0

        return 'GRID', note_to_coord(message.note), message.velocity > 0

    return None, None, None


class ButtonGroup(list):
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        super(ButtonGroup, self).__init__()
        if x1 in ('TOP', 'RIGHT'):
            fromlist = globals()[x1 + '_BUTTONS'].values()
            if y1 is None:
                self += [(x1, v) for v in fromlist]
            else:
                try:
                    y1 = int(y1)
                    self.append((x1, fromlist[y1]))
                except (ValueError, TypeError):
                    self.append((x1, y1))

        else:
            if x1 is None: x1 = 0
            if y1 is None: y1 = 0
            if x2 is None: x2 = 7
            if y2 is None: y2 = 7
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    self.append(('GRID', (x, y)))
