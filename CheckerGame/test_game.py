from boardDesign import GameState


def test_invalid_click():
    board = GameState()
    assert(board.invalid_click(500, 500))
    assert(not board.invalid_click(0, 0))
    assert(not board.invalid_click(-20, -20))


def test_invalid_position():
    board = GameState()
    board.prev.append(2)
    board.prev.append(1)
    assert(board.invalid_position(500, 500))
    assert(not board.invalid_position(-137, 76))
    assert(not board.invalid_position(-175, -82))


def test_invalid_non_capture():
    board = GameState()
    board.prev.append(2)
    board.prev.append(1)
    assert(board.invalid_non_capture(-181, -74))
    assert(board.invalid_non_capture(-82, -65))
    assert(not board.invalid_non_capture(-177, -27))


def test_invalid_capture():
    board = GameState()
    board.prev.append(2)
    board.prev.append(1)
    assert(board.invalid_capture(-177, -72))
    assert(board.invalid_capture(-166, -122))
    assert(board.invalid_capture(-500, -500))


def test_is_caputre():
    board = GameState()
    board.squares[3][2] = board.RED
    assert(board.is_capture(-110, -68))
    assert(not board.is_capture(-87, -122))
    assert(not board.is_capture(72, -177))


def test_invalid_player():
    board = GameState()
    assert(not board.invalid_player(-123, -72))
    assert(not board.invalid_player(-33, -78))
    assert(board.invalid_player(-75, 76))


def test_get_capture_piece():
    board = GameState()
    board.current_player = board.PlayerR
    board.squares[4][1] = board.BLACK
    assert(board.get_capture_piece() == [[5, 0], [5, 2]])
    board.squares[4][1] = board.EMPTY
    assert(board.get_capture_piece() == [])
    board.squares[4][3] = board.BLACK
    assert(board.get_capture_piece() == [[5, 2], [5, 4]])


def test_get_non_capture_piece():
    board = GameState()
    board.current_player = board.PlayerR
    assert(board.get_non_capture_piece() == [[5, 0], [5, 2], [5, 4], [5, 6]])
    board.squares[4][1] = board.BLACK
    assert(board.get_non_capture_piece() == [[5, 4], [5, 6]])
    board.squares[4][1] = board.EMPTY
    board.squares[4][3] = board.BLACK
    assert(board.get_non_capture_piece() == [[5, 0], [5, 6]])


def test_empty_position():
    board = GameState()
    board.current_player = board.PlayerR
    assert(board.empty_position(5, 0) == [[4, 1]])
    assert(board.empty_position(5, 2) == [[4, 1], [4, 3]])
    assert(board.empty_position(5, 4) == [[4, 3], [4, 5]])


def test_empty_position_capture():
    board = GameState()
    board.current_player = board.PlayerR
    board.squares[4][1] = board.BLACK
    assert(board.empty_position_capture(5, 0) == [[3, 2]])
    assert(board.empty_position_capture(5, 2) == [[3, 0]])
    assert(board.empty_position_capture(5, 4) == [])


def test_win_game():
    board = GameState()
    board.red_remain = 0
    assert(board.winGame())
    board.red_remain = 1
    board.black_remain = 0
    assert(board.winGame())
    board.can_black_move = False
    assert(board.winGame())


def test_can_piece_move():
    board = GameState()
    assert(board.can_piece_move(2, 1))
    assert(not board.can_piece_move(1, 0))
    assert(not board.can_piece_move(0, 1))


def test_can_non_capture_move():
    board = GameState()
    assert(board.can_non_capture_move(2, 1))
    assert(not board.can_non_capture_move(1, 0))
    assert(not board.can_non_capture_move(0, 1))


def test_can_capture_move():
    board = GameState()
    board.squares[3][2] = board.RED
    assert(board.can_capture_move(2, 1))
    assert(board.can_capture_move(2, 3))
    assert(not board.can_capture_move(2, 5))


def test_is_black():
    board = GameState()
    assert(board.is_black(2, 1))
    assert(board.is_black(2, 3))
    assert(not board.is_black(5, 0))


def test_is_red():
    board = GameState()
    assert(board.is_red(5, 0))
    assert(board.is_red(5, 2))
    assert(not board.is_red(2, 1))


def test_check_capture():
    board = GameState()
    board.squares[3][2] = board.RED
    assert(board.check_capture(board.PlayerB) == ['2,1', '2,3'])
    board.current_player = board.PlayerR
    board.squares[4][1] = board.BLACK
    board.squares[3][2] = board.EMPTY
    assert(board.check_capture(board.PlayerR) == ['5,0', '5,2'])
    board.squares[4][1] = board.EMPTY
    assert(board.check_capture(board.PlayerR) == [])