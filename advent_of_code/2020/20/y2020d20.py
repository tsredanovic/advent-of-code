import math

from advent_of_code.basesolver import BaseSolver


class Tile:
    BORDER_TOP = "border_top"
    BORDER_BOTTOM = "border_bottom"
    BORDER_LEFT = "border_left"
    BORDER_RIGHT = "border_right"

    CORNER_CONN_COUNT = 2
    SIDE_CONN_COUNT = 3
    MID_CONN_COUNT = 4

    TAG_CORNER = "tag_corner"
    TAG_SIDE = "tag_side"
    TAG_MID = "tag_mid"

    def __init__(self, id, rows) -> None:
        self.id = id
        self.rows = rows
        self.tag = None
        self.connects_to = []

    def __str__(self) -> str:
        return "Tile {}".format(self.id)

    def __repr__(self) -> str:
        return str(self)

    def draw(self) -> None:
        row_strs = []
        for row in self.rows:
            row_strs.append("".join(row))
        print("\n".join(row_strs))

    def border(self, direction):
        border = []
        if direction == Tile.BORDER_TOP:
            for i in range(len(self.rows[0])):
                border.append(self.rows[0][i])
        elif direction == Tile.BORDER_BOTTOM:
            for i in range(len(self.rows[-1])):
                border.append(self.rows[-1][i])
        elif direction == Tile.BORDER_LEFT:
            for i in range(len(self.rows)):
                border.append(self.rows[i][0])
        elif direction == Tile.BORDER_RIGHT:
            for i in range(len(self.rows)):
                border.append(self.rows[i][-1])
        return border

    def borders(self):
        border_directions = [
            Tile.BORDER_TOP,
            Tile.BORDER_BOTTOM,
            Tile.BORDER_LEFT,
            Tile.BORDER_RIGHT,
        ]
        borders = {}
        for direction in border_directions:
            borders[direction] = self.border(direction)
        return borders


class Connection:
    def __init__(
        self, tile1_id, tile2_id, tile1_border, tile2_border, inverted
    ) -> None:
        self.tile1_id = tile1_id
        self.tile2_id = tile2_id
        self.tile1_border = tile1_border
        self.tile2_border = tile2_border
        self.inverted = inverted

    def __str__(self) -> str:
        return "Conn {}<->{} ({}<->{}) - {}".format(
            self.tile1_id,
            self.tile2_id,
            self.tile1_border,
            self.tile2_border,
            "inverted" if self.inverted else "not inverted",
        )

    def __repr__(self) -> str:
        return str(self)


class TileImage:
    def __init__(self, tile_count) -> None:
        self.wh = int(math.sqrt(tile_count))
        self.tiles = [[None for _ in range(self.wh)] for _ in range(self.wh)]

    def draw_tile_ids(self):
        tile_ids = []
        for tile_row in self.tiles:
            tile_ids_row = []
            for tile in tile_row:
                if tile:
                    tile_ids_row.append(tile.id)
                else:
                    tile_ids_row.append(None)
            tile_ids.append(tile_ids_row)
        for tile_ids_row in tile_ids:
            print(tile_ids_row)

    def draw_ids(self):
        self.draw_tile_ids()

    def draw_tiles(self, spaces=False):
        out_str = ""

        tile_wh = len(self.tiles[0][0].rows[0])
        img_wh = tile_wh * self.wh
        for i in range(0, img_wh):
            i_tile = int(math.floor(i / tile_wh))
            i_tile_pos = i % tile_wh
            if i_tile_pos == 0 and i != 0 and spaces:
                out_str += " " * img_wh + "\n"
            for j in range(0, img_wh):
                j_tile = int(math.floor(j / tile_wh))
                j_tile_pos = j % tile_wh
                if j_tile_pos == 0 and j != 0 and spaces:
                    out_str += " "

                char = self.tiles[i_tile][j_tile].rows[i_tile_pos][j_tile_pos]
                out_str += char
            out_str += "\n"

        print(out_str)


def create_tiles(lines):
    tiles = []
    current_tile = None
    for line in lines:
        if line.startswith("Tile"):
            current_id = int(line.split(" ")[1].rstrip(":"))
            current_tile = Tile(current_id, [])
        elif not line:
            tiles.append(current_tile)
        else:
            current_tile.rows.append(list(line))
    tiles.append(current_tile)
    return tiles


def find_connections(tiles):
    conn_touples = []

    for tile1 in tiles:
        for tile2 in tiles:

            if tile1.id == tile2.id:
                continue

            for tile1_border_direction, tile1_border in tile1.borders().items():
                for tile2_border_direction, tile2_border in tile2.borders().items():
                    if tile1.id < tile2.id:
                        real_tile1 = tile1
                        real_tile2 = tile2
                        real_tile1_border = tile1_border
                        real_tile2_border = tile2_border
                    else:
                        real_tile1 = tile2
                        real_tile2 = tile1
                        real_tile1_border = tile2_border
                        real_tile2_border = tile1_border

                    conn_touple = None
                    if real_tile1_border == real_tile2_border:
                        conn_touple = (
                            real_tile1.id,
                            real_tile2.id,
                            real_tile1_border,
                            real_tile2_border,
                            False,
                        )
                    elif tile1_border[::-1] == tile2_border:
                        conn_touple = (
                            real_tile1.id,
                            real_tile2.id,
                            real_tile1_border,
                            real_tile2_border,
                            True,
                        )

                    if not conn_touple or conn_touple in conn_touples:
                        continue

                    conn_touples.append(conn_touple)

    connections = []
    for conn_touple in conn_touples:
        connections.append(
            Connection(
                conn_touple[0],
                conn_touple[1],
                conn_touple[2],
                conn_touple[3],
                conn_touple[4],
            )
        )

    return connections


class Y2020D20Solver(BaseSolver):
    def solve_part_a(self):
        tiles = create_tiles(self.lines)

        connections = find_connections(tiles)

        conn_counts = {}
        for connection in connections:
            if connection.tile1_id not in conn_counts.keys():
                conn_counts[connection.tile1_id] = 0
            if connection.tile2_id not in conn_counts.keys():
                conn_counts[connection.tile2_id] = 0
            conn_counts[connection.tile1_id] += 1
            conn_counts[connection.tile2_id] += 1

        result = 1
        for tile_id, conn_count in conn_counts.items():
            if conn_count == Tile.CORNER_CONN_COUNT:
                result *= tile_id

        return result

    def solve_part_b(self):
        tiles = create_tiles(self.lines)

        tiles_dict = {}
        for tile in tiles:
            tiles_dict[tile.id] = tile

        connections = find_connections(tiles)
        for connection in connections:
            tiles_dict[connection.tile1_id].connects_to.append(
                tiles_dict[connection.tile2_id]
            )
            tiles_dict[connection.tile2_id].connects_to.append(
                tiles_dict[connection.tile1_id]
            )

        conn_counts = {}
        for connection in connections:
            if connection.tile1_id not in conn_counts.keys():
                conn_counts[connection.tile1_id] = 0
            if connection.tile2_id not in conn_counts.keys():
                conn_counts[connection.tile2_id] = 0
            conn_counts[connection.tile1_id] += 1
            conn_counts[connection.tile2_id] += 1

        for tile_id, tile_conn_count in conn_counts.items():
            if tile_conn_count == Tile.CORNER_CONN_COUNT:
                tiles_dict[tile_id].tag = Tile.TAG_CORNER
            elif tile_conn_count == Tile.SIDE_CONN_COUNT:
                tiles_dict[tile_id].tag = Tile.TAG_SIDE
            elif tile_conn_count == Tile.MID_CONN_COUNT:
                tiles_dict[tile_id].tag = Tile.TAG_MID
            else:
                print("NOT GOOD 1")
                import pdb

                pdb.set_trace()

        corners = [tile for tile in tiles_dict.values() if tile.tag == Tile.TAG_CORNER]
        sides = [tile for tile in tiles_dict.values() if tile.tag == Tile.TAG_SIDE]
        mid_tiles = [tile for tile in tiles_dict.values() if tile.tag == Tile.TAG_MID]

        img = TileImage(len(tiles))

        # Fill first corner
        first_corner = corners.pop()
        img.tiles[0][0] = first_corner

        # Fill top side
        used_up_ids = [first_corner.id]
        for i in range(1, img.wh):
            if i == 1:
                first_connection = first_corner.connects_to[0]
                used_up_ids.append(first_connection.id)
                img.tiles[0][1] = first_connection
            else:
                left_tile = img.tiles[0][i - 1]
                connects_to_not_mid = [
                    tile for tile in left_tile.connects_to if tile.tag != Tile.TAG_MID
                ]
                connects_to_not_mid_not_used_up = [
                    tile for tile in connects_to_not_mid if tile.id not in used_up_ids
                ]
                if len(connects_to_not_mid_not_used_up) != 1:
                    print("NOT GOOD 2")
                    import pdb

                    pdb.set_trace()
                img.tiles[0][i] = connects_to_not_mid_not_used_up[0]
                used_up_ids.append(connects_to_not_mid_not_used_up[0].id)

                if i == img.wh - 1:
                    corners.remove(connects_to_not_mid_not_used_up[0])

        # Fill left side
        used_up_ids.append(first_corner.id)
        for i in range(1, img.wh):
            if i == 1:
                first_connection = first_corner.connects_to[1]
                used_up_ids.append(first_connection.id)
                img.tiles[1][0] = first_connection
            else:
                left_tile = img.tiles[i - 1][0]
                connects_to_not_mid = [
                    tile for tile in left_tile.connects_to if tile.tag != Tile.TAG_MID
                ]
                connects_to_not_mid_not_used_up = [
                    tile for tile in connects_to_not_mid if tile.id not in used_up_ids
                ]
                if len(connects_to_not_mid_not_used_up) != 1:
                    print("NOT GOOD 2")
                    import pdb

                    pdb.set_trace()
                img.tiles[i][0] = connects_to_not_mid_not_used_up[0]
                used_up_ids.append(connects_to_not_mid_not_used_up[0].id)

                if i == img.wh - 1:
                    corners.remove(connects_to_not_mid_not_used_up[0])

        # Fill last corner
        if len(corners) != 1:
            print("NOT GOOD 3")
            import pdb

            pdb.set_trace()
        img.tiles[img.wh - 1][img.wh - 1] = corners[0]

        # Fill right side
        used_up_ids.append(img.tiles[0][img.wh - 1].id)
        for i in range(1, img.wh - 1):
            left_tile = img.tiles[i - 1][img.wh - 1]
            connects_to_not_mid = [
                tile for tile in left_tile.connects_to if tile.tag != Tile.TAG_MID
            ]
            connects_to_not_mid_not_used_up = [
                tile for tile in connects_to_not_mid if tile.id not in used_up_ids
            ]
            if len(connects_to_not_mid_not_used_up) != 1:
                print("NOT GOOD 2")
                import pdb

                pdb.set_trace()
            img.tiles[i][img.wh - 1] = connects_to_not_mid_not_used_up[0]
            used_up_ids.append(connects_to_not_mid_not_used_up[0].id)

            if i == img.wh - 1:
                corners.remove(connects_to_not_mid_not_used_up[0])

        # Fill bottom side
        used_up_ids.append(img.tiles[img.wh - 1][0].id)
        for i in range(1, img.wh - 1):
            left_tile = img.tiles[img.wh - 1][i - 1]
            connects_to_not_mid = [
                tile for tile in left_tile.connects_to if tile.tag != Tile.TAG_MID
            ]
            connects_to_not_mid_not_used_up = [
                tile for tile in connects_to_not_mid if tile.id not in used_up_ids
            ]
            if len(connects_to_not_mid_not_used_up) != 1:
                print("NOT GOOD 2")
                import pdb

                pdb.set_trace()
            img.tiles[img.wh - 1][i] = connects_to_not_mid_not_used_up[0]
            used_up_ids.append(connects_to_not_mid_not_used_up[0].id)

            if i == img.wh - 1:
                corners.remove(connects_to_not_mid_not_used_up[0])

        # Fill middle
        for i in range(1, img.wh - 1):
            for j in range(1, img.wh - 1):
                neighbour_tiles = [
                    img.tiles[i - 1][j],
                    img.tiles[i + 1][j],
                    img.tiles[i][j - 1],
                    img.tiles[i][j + 1],
                ]
                neighbour_tiles = [tile for tile in neighbour_tiles if tile]
                neighbour_connects_to_tiles = [
                    set(tile.connects_to) for tile in neighbour_tiles
                ]
                same_neighbours = list(set.intersection(*neighbour_connects_to_tiles))
                same_neighbours_no_used_up = [
                    tile for tile in same_neighbours if tile.id not in used_up_ids
                ]
                if len(same_neighbours_no_used_up) != 1:
                    print("NOT GOOD 3")
                    import pdb

                    pdb.set_trace()
                img.tiles[i][j] = same_neighbours_no_used_up[0]
                used_up_ids.append(same_neighbours_no_used_up[0].id)

        img.draw_tiles()
        import pdb

        pdb.set_trace()
