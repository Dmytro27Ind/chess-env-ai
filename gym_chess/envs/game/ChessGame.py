import copy

# reprezentácia šachových figúrok
W_PAWN = W = 1
W_BISHOP = WB = 4
W_KNIGHT = WN = 2
W_ROOK = WR = 3
W_QUEEN = WQ = 5
W_KING = WK = 6
B_PAWN = B = 7
B_BISHOP = BB = 10
B_KNIGHT = BN = 8
B_ROOK = BR = 9
B_QUEEN = BQ = 11
B_KING = BK = 12
EMPTY = 0

WHITE = 'white'
BLACK = 'black'

 # herný stav
DRAW = 'draw'
WHITE_WIN = 'white_win'
BLACK_WIN = 'black_win'
PLAYING = 'playing'

# počiatočný rad pešiakov
START_W_PAWN_POS = 6
START_B_PAWN_POS = 1

BLACK_RANGE = range(B_PAWN, B_KING + 1)
WHITE_RANGE = range(W_PAWN, W_KING + 1)

# ceny šachových figúrok
PAWN_COST = 1
BISHOP_COST = 3
KNIGHT_COST = 3
ROOK_COST = 5
QUEEN_COST = 9


class ChessGame:
    """
    Toto je trieda, ktorá predstavuje šachovú hru.

    Hlavné metódy, ktoré musia používatelia tejto triedy poznať, sú:

        get_available_moves
        make_move
        check_move
        check_in_board

    Rovnako ako nasledujúce atribúty, ktoré musíme poznať:

        board: šachovnica, ktorá predstavuje ako list 8x8
        current_color: aktuálna farba (WHITE alebo BLACK)
        history: história šachových ťahov v hre
        status: DRAW, WHITE_WIN, BLACK_WIN or PLAYING
        check: True alebo False
        white_takes: šachové figúrky prevzaté bielym
        black_takes: šachové figúrky prevzaté čiernym

    """
    def __init__(self):
        self.board = [
            [9, 8, 10, 11, 12, 10, 8, 9],
            [7, 7, 7, 7, 7, 7, 7, 7],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [3, 2, 4, 5, 6, 4, 2, 3],
        ]
        self.current_color = WHITE
        self.history = []
        self.status = PLAYING
        self.black_takes = []
        self.white_takes = []
        self.delta_score_white = 0
        self.delta_score_black = 0
        self.check = False
        self.in_check = False

    def get_available_moves(self):
        """
        Táto metóda vráti list možných pohybov.
        :return: list možných pohybov
        """
        available_moves = []
        for i in range(8):
            for j in range(8):
                if self.current_color == WHITE:
                    if self.board[i][j] == EMPTY or self.board[i][j] in BLACK_RANGE:
                        continue
                    elif self.board[i][j] == W_PAWN:
                        available_moves += self.get_pawn_moves(i, j)
                    elif self.board[i][j] == W_ROOK:
                        available_moves += self.get_rook_moves(i, j)
                    elif self.board[i][j] == W_BISHOP:
                        available_moves += self.get_bishop_moves(i, j)
                    elif self.board[i][j] == W_QUEEN:
                        available_moves += self.get_queen_moves(i, j)
                    elif self.board[i][j] == W_KNIGHT:
                        available_moves += self.get_knight_moves(i, j)
                    elif self.board[i][j] == W_KING:
                        available_moves += self.get_king_moves(i, j)

                elif self.current_color == BLACK:
                    if self.board[i][j] == EMPTY or self.board[i][j] in WHITE_RANGE:
                        continue
                    elif self.board[i][j] == B_PAWN:
                        available_moves += self.get_pawn_moves(i, j)
                    elif self.board[i][j] == B_ROOK:
                        available_moves += self.get_rook_moves(i, j)
                    elif self.board[i][j] == B_BISHOP:
                        available_moves += self.get_bishop_moves(i, j)
                    elif self.board[i][j] == B_QUEEN:
                        available_moves += self.get_queen_moves(i, j)
                    elif self.board[i][j] == B_KNIGHT:
                        available_moves += self.get_knight_moves(i, j)
                    elif self.board[i][j] == B_KING:
                        available_moves += self.get_king_moves(i, j)

        return available_moves

    def __king_not_move(self) -> bool:
        if self.current_color == WHITE and self.board[7][4] != W_KING:
            return False
        elif self.current_color == BLACK and self.board[0][4] != B_KING:
            return False

        for move in self.history:
            if len(move) > 1:
                if self.current_color == WHITE and move[0] == 7 and move[1] == 4:
                    return False
                elif self.current_color == BLACK and move[0] == 0 and move[1] == 4:
                    return False
        return True

    def __rook_not_move(self, row, column) -> bool:
        if self.board[row][column] != W_ROOK and self.board[row][column] != B_ROOK:
            return False

        for move in self.history:
            if len(move) > 1:
                if move[0] == row and move[1] == column:
                    return False
        return True

    def __pieces_castling(self, short) -> bool:
        """
        :param short: ak True, skontrolujte medzi kráľom a vežou na krátkej strane, ak nie na dlhej strane.
        :return: vráti hodnotu true, ak sú medzi kráľom a vežou figúrky.
        """
        if short and self.current_color == WHITE:
            if self.board[7][5] != EMPTY or self.board[7][6] != EMPTY:
                return True
        elif short and self.current_color == BLACK:
            if self.board[0][5] != EMPTY or self.board[0][6] != EMPTY:
                return True
        elif not short and self.current_color == WHITE:
            if self.board[7][1] != EMPTY or self.board[7][2] != EMPTY or self.board[7][3] != EMPTY:
                return True
        elif not short and self.current_color == BLACK:
            if self.board[0][1] != EMPTY or self.board[0][2] != EMPTY or self.board[0][3] != EMPTY:
                return True
        return False

    def castling_check(self, short) -> bool:
        """
        :param short: short: ak True, skontrolujte medzi kráľom a vežou na krátkej strane, ak nie na dlhej strane.
        :return: vráti hodnotu True, ak kráľ alebo polia, ktorými prejde, do rošády je v šachu.
        """
        if short and self.current_color == WHITE:
            if self.check_in_board(self.board, WHITE) or self.check_move([7, 4, 7, 5]) or self.check_move([7, 4, 7, 6]):
                return True
        elif short and self.current_color == BLACK:
            if self.check_in_board(self.board, BLACK) or self.check_move([0, 4, 0, 5]) or self.check_move([0, 4, 0, 6]):
                return True
        elif not short and self.current_color == WHITE:
            if self.check_in_board(self.board, WHITE) or self.check_move([7, 4, 7, 3]) or self.check_move([7, 4, 7, 2])\
                    or self.check_move([7, 4, 7, 1]):
                return True
        elif not short and self.current_color == BLACK:
            if self.check_in_board(self.board, BLACK) or self.check_move([0, 4, 0, 3]) or self.check_move([0, 4, 0, 2])\
                    or self.check_move([0, 4, 0, 1]):
                return True
        return False

    def __append_castling(self, available_moves):
        """
        Pridáva rošádu k možným šachovým ťahom (available_moves).
        [0] - krátka rošáda, [1] - dlhá rošáda.
        :param available_moves: pole s možnými šachovými ťahmi pre aktuálny stav šachovnice
        """
        if not self.__king_not_move():
            return
        if self.current_color == WHITE:
            if self.__rook_not_move(7, 7) and not self.__pieces_castling(short=True) \
                    and not self.castling_check(short=True):
                available_moves.append([0])
            if self.__rook_not_move(7, 0) and not self.__pieces_castling(short=False) \
                    and not self.castling_check(short=False):
                available_moves.append([1])
        elif self.current_color == BLACK:
            if self.__rook_not_move(0, 7) and not self.__pieces_castling(short=True) \
                    and not self.castling_check(short=True):
                available_moves.append([0])
            if self.__rook_not_move(0, 0) and not self.__pieces_castling(short=False) \
                    and not self.castling_check(short=False):
                available_moves.append([1])

    def get_king_moves(self, row: int, column: int):
        """
        :param row: pozícia kráľa na šachovnici
        :param column: pozícia kráľa na šachovnici
        :return: vráti všetky možné ťahy kráľa
        """
        if self.board[row][column] != W_KING and self.board[row][column] != B_KING:
            raise ValueError

        available_moves = []
        enemy_range = BLACK_RANGE if self.current_color == WHITE else WHITE_RANGE

        for deltaRow, deltaColumn in [[-1, -1], [-1, 1], [1, 1], [1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]]:
            r, c = row, column
            r += deltaRow
            c += deltaColumn
            if r < 0 or r > 7 or c < 0 or c > 7:
                continue
            elif self.board[r][c] == EMPTY or self.board[r][c] in enemy_range:
                move = [row, column, r, c]
                self.__append_move(available_moves, move)

        # rošáda v oboch smeroch
        if not self.in_check:
            self.__append_castling(available_moves)

        return available_moves

    def get_knight_moves(self, row: int, column: int):
        """
        :param row: pozícia jazdca na šachovnici
        :param column: pozícia jazdca na šachovnici
        :return: vráti všetky možné ťahy jazdca
        """
        if self.board[row][column] != W_KNIGHT and self.board[row][column] != B_KNIGHT:
            raise ValueError

        available_moves = []
        enemy_range = BLACK_RANGE if self.current_color == WHITE else WHITE_RANGE

        for deltaRow, deltaColumn in [[-1, -2], [-2, -1], [-1, 2], [-2, 1], [1, 2], [2, 1], [1, -2], [2, -1]]:
            r, c = row, column
            r += deltaRow
            c += deltaColumn
            if r < 0 or r > 7 or c < 0 or c > 7:
                continue
            elif self.board[r][c] == EMPTY or self.board[r][c] in enemy_range:
                move = [row, column, r, c]
                self.__append_move(available_moves, move)

        return available_moves

    def get_queen_moves(self, row: int, column: int):
        """
        :param row: pozícia dámy na šachovnici
        :param column: pozícia dámy na šachovnici
        :return: vráti všetky možné ťahy dámy
        """
        if self.board[row][column] != W_QUEEN and self.board[row][column] != B_QUEEN:
            raise ValueError

        available_moves = []
        moves = self.__vert_hor_diagonal(row, column,
                                         [[-1, -1], [-1, 1], [1, 1], [1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]])
        for move in moves:
            self.__append_move(available_moves, move)
        return available_moves

    def get_bishop_moves(self, row: int, column: int):
        """
        :param row: pozícia strelca na šachovnici
        :param column: pozícia strelca na šachovnici
        :return: vráti všetky možné ťahy strelca
        """
        if self.board[row][column] != W_BISHOP and self.board[row][column] != B_BISHOP:
            raise ValueError

        available_moves = []
        moves = self.__vert_hor_diagonal(row, column, [[-1, -1], [-1, 1], [1, 1], [1, -1]])
        for move in moves:
            self.__append_move(available_moves, move)
        return available_moves

    def get_rook_moves(self, row: int, column: int):
        """
        :param row: pozícia veže na šachovnici
        :param column: pozícia veže na šachovnici
        :return: vráti všetky možné ťahy vežou
        """
        if self.board[row][column] != W_ROOK and self.board[row][column] != B_ROOK:
            raise ValueError

        available_moves = []
        moves = self.__vert_hor_diagonal(row, column, [[0, -1], [0, 1], [-1, 0], [1, 0]])
        for move in moves:
            self.__append_move(available_moves, move)
        return available_moves

    def __vert_hor_diagonal(self, row, column, delta_range):
        available_moves = []
        for deltaRow, deltaColumn in delta_range:
            r, c = row, column
            while True:
                r += deltaRow
                c += deltaColumn
                if r < 0 or r > 7 or c < 0 or c > 7:
                    break

                enemy_range = BLACK_RANGE if self.current_color == WHITE else WHITE_RANGE
                current_range = WHITE_RANGE if self.current_color == WHITE else BLACK_RANGE

                if self.board[r][c] == EMPTY:
                    available_moves.append([row, column, r, c])
                elif self.board[r][c] in enemy_range:
                    available_moves.append([row, column, r, c])
                    break
                elif self.board[r][c] in current_range:
                    break

        return available_moves

    def __is_pawn_promotion(self, move) -> bool:
        """
        Vrati True ak tento ťah pešiaka a pešiak dosiahol koniec šachovnice a chce sa zmeniť
        na dámu, vežu, jazdca alebo strelca.
        :param move: ťah pešiaka
        :return: True alebo False
        """
        if self.board[move[0]][move[1]] != W_PAWN and self.board[move[0]][move[1]] != B_PAWN:
            raise ValueError

        if self.current_color == 'white' and move[0] == 1 and move[2] == 0:
            return True
        elif self.current_color == 'black' and move[0] == 6 and move[2] == 7:
            return True
        else:
            return False

    def __append_prom_move(self, available_moves, move):
        """
        ťah [r1, c1, r2, c2] --> [r1, c1, r2, c2, x]. Piaty parameter môže byť v rozsahu od 2 do 5.
        x=2 - Jazdec
        x=3 - Strelec
        x=4 - veža
        x=5 - kráľovná
        """
        if not self.__is_pawn_promotion(move):
            raise ValueError
        for i in range(2, 6):
            temp_move = move + [i]
            self.__append_move(available_moves, temp_move)

    def get_pawn_moves(self, row: int, column: int):
        """
        :param row: pozícia pešiaka na šachovnici
        :param column: pozícia pešiaka na šachovnici
        :return: vráti všetky možné ťahy pešiakom
        """
        if self.board[row][column] != W_PAWN and self.board[row][column] != B_PAWN:
            raise ValueError

        available_moves = []
        if self.current_color == WHITE:
            if row == START_W_PAWN_POS and self.board[row - 1][column] == EMPTY and self.board[row - 2][
                column] == EMPTY:
                move = [row, column, row - 2, column]
                self.__append_move(available_moves, move)

            if row > 0 and self.board[row - 1][column] == EMPTY:
                move = [row, column, row - 1, column]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            if row > 0 and 0 < column and self.board[row - 1][column - 1] in BLACK_RANGE:
                move = [row, column, row - 1, column - 1]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            if row > 0 and column < 7 and self.board[row - 1][column + 1] in BLACK_RANGE:
                move = [row, column, row - 1, column + 1]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            # en passant
            if self.history != [] and row == START_B_PAWN_POS + 2:
                if column > 0 and self.history[-1] == [START_B_PAWN_POS, column - 1, START_B_PAWN_POS + 2, column - 1]:
                    # piaty parameter na odstránenie zajatého pešiaka
                    move = [row, column, row - 1, column - 1, 1]
                    self.__append_move(available_moves, move)
                if column < 7 and self.history[-1] == [START_B_PAWN_POS, column + 1, START_B_PAWN_POS + 2, column + 1]:
                    # piaty parameter na odstránenie zajatého pešiaka
                    move = [row, column, row - 1, column + 1, 1]
                    self.__append_move(available_moves, move)

        elif self.current_color == BLACK:
            if row == START_B_PAWN_POS and self.board[row + 1][column] == EMPTY and self.board[row + 2][
                column] == EMPTY:
                move = [row, column, row + 2, column]
                self.__append_move(available_moves, move)

            if row < 7 and self.board[row + 1][column] == EMPTY:
                move = [row, column, row + 1, column]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            if row < 7 and column > 0 and self.board[row + 1][column - 1] in WHITE_RANGE:
                move = [row, column, row + 1, column - 1]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            if row < 7 and column < 7 and self.board[row + 1][column + 1] in WHITE_RANGE:
                move = [row, column, row + 1, column + 1]
                # Ak je pešiak kráľ
                if self.__is_pawn_promotion(move):
                    self.__append_prom_move(available_moves, move)
                else:
                    self.__append_move(available_moves, move)

            #  en passant
            if self.history != [] and row == START_W_PAWN_POS - 2:
                if column > 0 and self.history[-1] == [START_W_PAWN_POS, column - 1, START_W_PAWN_POS - 2, column - 1]:
                    # piaty parameter na odstránenie zajatého pešiaka
                    move = [row, column, row + 1, column - 1, -1]
                    self.__append_move(available_moves, move)
                if column < 7 and self.history[-1] == [START_W_PAWN_POS, column + 1, START_W_PAWN_POS - 2, column + 1]:
                    # piaty parameter na odstránenie zajatého pešiaka
                    move = [row, column, row + 1, column + 1, -1]
                    self.__append_move(available_moves, move)

        return available_moves

    def __append_move(self, available_moves, move):
        if not self.in_check:
            if not self.check_move(move):
                available_moves.append(move)
        else:
            available_moves.append(move)

    def check_move(self, move) -> bool:
        """
        Kontroluje akýkoľvek ťah (aj nesprávny), ak po ňom bude šach na nášho kráľa.
        To znamená, že podľa pravidiel šachu sa takýto ťah nemôže uskutočniť.
        :param move: akýkoľvek ťah
        :return: True alebo False
        """
        temp_board = copy.deepcopy(self.board)
        if len(move) > 1:
            temp_board[move[2]][move[3]] = temp_board[move[0]][move[1]]
            temp_board[move[0]][move[1]] = EMPTY

        # Odstráni pešiaka po zajatí en passant
        if len(move) == 5 and (move[4] == 1 or move[4] == -1):
            temp_board[move[2] + move[4]][move[3]] = EMPTY

        # Ak je pešiak kráľ
        if len(move) == 5 and (move[4] in range(2, 6)):
            if move[4] == 2:
                temp_board[move[2]][move[3]] = WN if self.current_color == WHITE else BN
            elif move[4] == 3:
                temp_board[move[2]][move[3]] = WB if self.current_color == WHITE else BB
            elif move[4] == 4:
                temp_board[move[2]][move[3]] = WR if self.current_color == WHITE else BR
            elif move[4] == 5:
                temp_board[move[2]][move[3]] = WQ if self.current_color == WHITE else BQ

        # castling
        elif len(move) == 1:
            if self.current_color == WHITE:
                if move == [0]:
                    temp_board[7][4] = EMPTY
                    temp_board[7][7] = EMPTY
                    temp_board[7][6] = W_KING
                    temp_board[7][5] = W_ROOK
                elif move == [1]:
                    temp_board[7][4] = EMPTY
                    temp_board[7][0] = EMPTY
                    temp_board[7][2] = W_KING
                    temp_board[7][3] = W_ROOK
            elif self.current_color == BLACK:
                if move == [0]:
                    temp_board[0][4] = EMPTY
                    temp_board[0][7] = EMPTY
                    temp_board[0][6] = B_KING
                    temp_board[0][5] = B_ROOK
                elif move == [1]:
                    temp_board[0][4] = EMPTY
                    temp_board[0][0] = EMPTY
                    temp_board[0][2] = B_KING
                    temp_board[0][3] = B_ROOK

        if self.check_in_board(temp_board, self.current_color):
            return True
        return False

    def check_in_board(self, board, color) -> bool:
        """
        :param board: šachovnica
        :param color: aktuálna farba
        :return: Vráti True, ak je šach pre kráľa aktuálnej farby
        """
        openent_range = BLACK_RANGE if color == WHITE else WHITE_RANGE
        king = None
        for i in range(8):
            for j in range(8):
                if board[i][j] == (W_KING if color == WHITE else B_KING):
                    king = [i, j]

        temp_game = ChessGame()
        temp_game.board = board
        temp_game.current_color = BLACK if color == WHITE else WHITE
        temp_game.in_check = True
        available_moves = temp_game.get_available_moves()
        temp_game.in_check = False
        for move in available_moves:
            if len(move) > 1 and move[2] == king[0] and move[3] == king[1]:
                return True
        return False

    def impossible_mate(self) -> bool:
        """
        Vráti True v situáciách, keď nie je možné dať kráľovi mat. Tu sú situácie:
            - kráľ proti kráľovi
            - kráľ proti kráľovi a strelca
            - kráľ proti kráľovi a jazdca
            - kráľ a strelec proti kráľovi a strelca, pričom obaja strelca sú na poliach rovnakej farby
        :return: True alebo False
        """
        white_p = []
        black_p = []
        p = [EMPTY, W_KING, B_KING, W_BISHOP, B_BISHOP, W_KNIGHT, B_KNIGHT]

        for i in range(8):
            for j in range(8):
                if self.board[i][j] not in p:
                    return False
                elif self.board[i][j] in WHITE_RANGE:
                    if self.board[i][j] == W_BISHOP:
                        if (i+j) % 2 == 0:
                            white_p.append(self.board[i][j])
                        else:
                            white_p.append(-self.board[i][j])
                    else:
                        white_p.append(self.board[i][j])

                elif self.board[i][j] in BLACK_RANGE:
                    if self.board[i][j] == B_BISHOP:
                        if (i + j) % 2 == 0:
                            black_p.append(self.board[i][j])
                        else:
                            black_p.append(-self.board[i][j])
                    else:
                        black_p.append(self.board[i][j])

        if len(white_p) > 2 or len(black_p) > 2:
            return False
        if (white_p == [W_KING] and black_p == [B_KING])\
                or (white_p == [W_KING] and black_p == [B_KING, B_KNIGHT])\
                or (white_p == [W_KING, W_KNIGHT] and black_p == [B_KING])\
                or (white_p == [W_KING] and black_p == [B_KING, B_BISHOP])\
                or (white_p == [W_KING, W_BISHOP] and black_p == [B_KING]) \
                or (white_p == [W_KING] and black_p == [B_KING, -B_BISHOP]) \
                or (white_p == [W_KING, -W_BISHOP] and black_p == [B_KING]) \
                or (white_p == [W_KING, -W_BISHOP] and black_p == [B_KING, -B_BISHOP])\
                or (white_p == [W_KING, W_BISHOP] and black_p == [B_KING, B_BISHOP]):
            return True
        return False

    def rule_three_times(self) -> bool:
        """
        :return: vráti True pri troch opakovaniach ťahov
        """
        if len(self.history) < 8:
            return False
        a = self.history[-4:]
        b = self.history[-8:-4]
        if a == b:
            return True
        return False

    def __set_delta_score(self):
        white_score = 0
        black_score = 0

        for i in range(len(self.white_takes)):
            if self.white_takes[i] == B_PAWN:
                white_score += PAWN_COST
            elif self.white_takes[i] == B_ROOK:
                white_score += ROOK_COST
            elif self.white_takes[i] == B_BISHOP:
                white_score += BISHOP_COST
            elif self.white_takes[i] == B_QUEEN:
                white_score += QUEEN_COST
            elif self.white_takes[i] == B_KNIGHT:
                white_score += KNIGHT_COST

        for i in range(len(self.black_takes)):
            if self.black_takes[i] == W_PAWN:
                black_score += PAWN_COST
            elif self.black_takes[i] == W_ROOK:
                black_score += ROOK_COST
            elif self.black_takes[i] == W_BISHOP:
                black_score += BISHOP_COST
            elif self.black_takes[i] == W_QUEEN:
                black_score += QUEEN_COST
            elif self.black_takes[i] == W_KNIGHT:
                black_score += KNIGHT_COST

        self.delta_score_white = white_score - black_score
        self.delta_score_black = black_score - white_score

    def make_move(self, move: list) -> bool:
        """
        Táto metóda urobí šachový ťah.
        :param move: šachový ťah
        :return: vráti True, ak urobí pohyb, a False, ak to nevyjde
        """
        if self.status != PLAYING:
            return False

        available_moves = self.get_available_moves()
        if move in available_moves:

            if len(move) > 1:
                if self.current_color == WHITE and self.board[move[2]][move[3]] in BLACK_RANGE:
                    self.white_takes.append(self.board[move[2]][move[3]])
                elif self.current_color == BLACK and self.board[move[2]][move[3]] in WHITE_RANGE:
                    self.black_takes.append(self.board[move[2]][move[3]])

                # Pridajme zachytenú šachovú figúrku pri en passant k zvyšku zachytených figúrok
                if len(move) == 5 and (move[4] == 1 or move[4] == -1):
                    if self.current_color == WHITE:
                        self.white_takes.append(self.board[move[2] + move[4]][move[3]])
                    elif self.current_color == BLACK:
                        self.black_takes.append(self.board[move[2] + move[4]][move[3]])

                # Odstráni pešiaka po zajatí en passant
                if len(move) == 5 and (move[4] == 1 or move[4] == -1):
                    self.board[move[2] + move[4]][move[3]] = EMPTY

                self.board[move[2]][move[3]] = self.board[move[0]][move[1]]
                self.board[move[0]][move[1]] = EMPTY

                # Ak je pešiak kráľ
                if len(move) == 5 and (move[4] in range(2, 6)):
                    if move[4] == 2:
                        self.board[move[2]][move[3]] = WN if self.current_color == WHITE else BN
                    elif move[4] == 3:
                        self.board[move[2]][move[3]] = WB if self.current_color == WHITE else BB
                    elif move[4] == 4:
                        self.board[move[2]][move[3]] = WR if self.current_color == WHITE else BR
                    elif move[4] == 5:
                        self.board[move[2]][move[3]] = WQ if self.current_color == WHITE else BQ
            # castling
            elif len(move) == 1:
                if self.current_color == WHITE:
                    if move == [0]:
                        self.board[7][4] = EMPTY
                        self.board[7][7] = EMPTY
                        self.board[7][6] = W_KING
                        self.board[7][5] = W_ROOK
                    elif move == [1]:
                        self.board[7][4] = EMPTY
                        self.board[7][0] = EMPTY
                        self.board[7][2] = W_KING
                        self.board[7][3] = W_ROOK
                elif self.current_color == BLACK:
                    if move == [0]:
                        self.board[0][4] = EMPTY
                        self.board[0][7] = EMPTY
                        self.board[0][6] = B_KING
                        self.board[0][5] = B_ROOK
                    elif move == [1]:
                        self.board[0][4] = EMPTY
                        self.board[0][0] = EMPTY
                        self.board[0][2] = B_KING
                        self.board[0][3] = B_ROOK

            if self.current_color == WHITE:
                self.current_color = BLACK
            elif self.current_color == BLACK:
                self.current_color = WHITE

            # Pridajme pohyb v histórii hry
            self.history.append(move)

            # Nastaveme delta skóre
            self.__set_delta_score()

            # Skontrolovať patovú situáciu (pat)
            if self.status == PLAYING and not self.check_in_board(self.board, self.current_color) \
                    and not self.get_available_moves():
                self.status = DRAW
            # Skontrolujte situácie, v ktorých nie je dostatok figúrok na mat
            elif self.impossible_mate():
                self.status = DRAW
            # trojité opakovanie pohybov
            elif self.rule_three_times():
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ")
                self.status = DRAW
            # Mat (checkmate)
            elif self.status == PLAYING and self.check_in_board(self.board,
                                                                self.current_color) and not self.get_available_moves():
                self.status = (BLACK_WIN if self.current_color == WHITE else WHITE_WIN)
            # Skontrolujem aktuálnu farbu
            if self.check_in_board(self.board, self.current_color):
                self.check = True
            else:
                self.check = False
            return True
        return False
