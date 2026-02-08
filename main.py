from kipy import KiCad
from kipy.board_types import BoardItem, BoardRectangle, Zone
from kipy.geometry import Box2, PolygonWithHoles, PolyLine, PolyLineNode, Vector2
from kipy.proto.board import BoardGraphicShape, BoardLayer
from kipy.util.units import from_mm

SWITCH_DIM = 19.05
SWITCH_OFFSET = SWITCH_DIM / 2
DIODE_OFFSET_X = 8.5
DIODE_OFFSET_Y = 5
OFFSET = 50
PADDING = 10
MIN_X = OFFSET - SWITCH_OFFSET - PADDING
MIN_Y = OFFSET - SWITCH_DIM - PADDING
MAX_X = 0
MAX_Y = 0

key_diode_pairs = {}

keymap = {
    0: (0, 1),
    1: (1, 1),
    2: (2, 1),
    3: (3, 1),
    4: (4, 1),
    5: (5, 1),
    6: (6, 1),
    7: (7, 1),
    8: (8, 1),
    9: (9, 1),
    10: (10, 1),
    11: (11, 1),
    12: (12, 1),
    13: (13, 1),
    14: (14, 1),
    15: (15, 1),
    16: (0, 2),
    17: (1, 2),
    18: (2, 2),
    19: (3, 2),
    20: (4, 2),
    21: (5, 2),
    22: (6, 2),
    23: (7, 2),
    24: (8, 2),
    25: (9, 2),
    26: (10, 2),
    27: (11, 2),
    28: (12, 2),
    29: (13, 2),
    30: (14, 2),
    31: (0, 3),
    32: (1, 3),
    33: (2, 3),
    34: (3, 3),
    35: (4, 3),
    36: (5, 3),
    37: (6, 3),
    38: (7, 3),
    39: (8, 3),
    40: (9, 3),
    41: (10, 3),
    42: (11, 3),
    43: (12, 3),
    44: (13, 3),
    45: (14, 3),
    46: (0, 4),
    47: (1, 4),
    48: (2, 4),
    49: (3, 4),
    50: (4, 4),
    51: (5, 4),
    52: (6, 4),
    53: (7, 4),
    54: (8, 4),
    55: (9, 4),
    56: (10, 4),
    57: (11, 4),
    58: (12, 4),
    59: (13, 4),
    60: (0, 5),
    61: (1, 5),
    62: (2, 5),
    63: (3, 5),
    64: (4, 5),
    65: (5, 5),
    66: (6, 5),
    67: (7, 5),
    68: (8, 5),
    69: (9, 5),
    70: (10, 5),
    71: (11, 5),
    72: (12, 5),
    73: (13, 5),
    74: (0, 6),
    75: (1, 6),
    76: (2, 6),
    77: (3, 6),
    78: (4, 6),
    79: (5, 6),
    80: (6, 6),
    81: (7, 6),
    82: (8, 6),
    83: (9, 6),
}
_keymap = {
    "1": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
    "2": (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30),
    "3": (31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45),
    "4": (46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59),
    "5": (60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73),
    "6": (74, 75, 76, 77, 78, 79, 80, 81, 82, 83),
}

board = KiCad().get_board()
footprints = board.get_footprints()
for footprint in footprints:
    if "MX-Hotswap" in footprint.definition.id.name:
        print(f"Hotswap footprint found: {footprint.definition.id.name}")
        switch_index = int(footprint.reference_field.text.value.replace("K", ""))
        for _footprint in footprints:
            if (
                "Diode" in _footprint.definition.id.library
                and int(_footprint.reference_field.text.value.replace("D", ""))
                == switch_index
            ):
                print(f"Found corresponding diode: {_footprint.definition.id.name}")
                print(f"{footprint.reference_field.text.value}")
                print(f"{_footprint.reference_field.text.value}")
                key_diode_pairs[switch_index] = (footprint, _footprint)
            continue
    continue

for key, value in _keymap.items():
    offset = OFFSET
    print(f"row: {key}")
    x = 0
    y = 0
    for _value in value:
        coord = keymap[_value]
        switch_size = (
            key_diode_pairs[_value][0]
            .definition.id.name.replace("MX-Hotswap-", "")
            .replace("U", "")
        )
        print(f"switch_size: {switch_size}")
        x = (
            coord[0] + round(((float(switch_size) * SWITCH_DIM) - SWITCH_DIM) / 2, 4)
        ) + offset
        y = round((coord[1] * SWITCH_DIM) + SWITCH_OFFSET, 4)
        offset = round(offset + (float(switch_size) * SWITCH_DIM), 4) - 1
        print(f"x: {x} y: {y}")
        key_diode_pairs[_value][0].position = Vector2.from_xy_mm(x, y)

        x_d = (key_diode_pairs[_value][0].position.x / 1000000) + DIODE_OFFSET_X
        y_d = (key_diode_pairs[_value][0].position.y / 1000000) + DIODE_OFFSET_Y
        key_diode_pairs[_value][1].position = Vector2.from_xy_mm(x_d, y_d)
    MAX_X = x
    MAX_Y = y
    print(f"max x: {MAX_X}, max y: {MAX_Y}")

_min = key_diode_pairs[min(keymap)][0].position.from_xy(
    key_diode_pairs[min(keymap)][0].position.x,
    key_diode_pairs[min(keymap)][0].position.y,
)
_max = key_diode_pairs[min(keymap)][0].position.from_xy(
    key_diode_pairs[max(keymap)][0].position.x,
    key_diode_pairs[max(keymap)][0].position.y,
)
MIN_X = _min.x
MIN_Y = _min.y
MAX_X = _max.x
MAX_Y = _max.y

print("drawing board outline")
print(f"MIN X: {MIN_X / 1000000} mm, MIN Y: {MIN_Y / 1000000} mm")
print(f"MAX X: {MAX_X / 1000000} mm, MAX Y: {MAX_Y / 1000000} mm")
outline = PolyLine()
outline.append(PolyLineNode.from_xy(from_mm(MIN_X), from_mm(MIN_Y)))
outline.append(PolyLineNode.from_xy(from_mm(MAX_X), from_mm(MIN_Y)))
outline.append(PolyLineNode.from_xy(from_mm(MAX_X), from_mm(MAX_Y)))
outline.append(PolyLineNode.from_xy(from_mm(MIN_X), from_mm(MAX_Y)))

polygon = PolygonWithHoles()
polygon.outline = outline
fillZone = Zone()
fillZone.layers = [BoardLayer.BL_F_Cu, BoardLayer.BL_B_Cu]
fillZone.outline = polygon

board_outline = Zone()
board_outline.type = ZoneType.OUTLINE
board_outline.filled = true
board_outline.layers = [BoardLayer.BL_Edge_Cuts]
board_outline.outline = polygon

board.create_items(board_outline)
board.update_items(board_outline)
board.create_items(fillZone)
board.update_items(footprints)
board.refill_zones(block=False)
board.save()
# print(key_diode_pairs[1][1].position.x)
# print(key_diode_pairs[1][1].reference_field.text.value)
