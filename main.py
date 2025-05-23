import chess
import random

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pawn_table = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]
knight_table = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]
bishop_table = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]
rook_table = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]
queen_table = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]
king_table_middle = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

def reverse_table(table):
    return [row.copy() for row in reversed(table)]

pawn_table_black = reverse_table(pawn_table)
knight_table_black = reverse_table(knight_table)
bishop_table_black = reverse_table(bishop_table)
rook_table_black = reverse_table(rook_table)
queen_table_black = reverse_table(queen_table)
king_table_middle_black = reverse_table(king_table_middle)

def get_positional_value(piece, square):
    color = piece.color
    piece_type = piece.piece_type
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    row = 7 - rank
    
    if color == chess.WHITE:
        if piece_type == chess.PAWN:
            table = pawn_table
        elif piece_type == chess.KNIGHT:
            table = knight_table
        elif piece_type == chess.BISHOP:
            table = bishop_table
        elif piece_type == chess.ROOK:
            table = rook_table
        elif piece_type == chess.QUEEN:
            table = queen_table
        elif piece_type == chess.KING:
            table = king_table_middle
    else:
        if piece_type == chess.PAWN:
            table = pawn_table_black
        elif piece_type == chess.KNIGHT:
            table = knight_table_black
        elif piece_type == chess.BISHOP:
            table = bishop_table_black
        elif piece_type == chess.ROOK:
            table = rook_table_black
        elif piece_type == chess.QUEEN:
            table = queen_table_black
        elif piece_type == chess.KING:
            table = king_table_middle_black
    
    return table[row][file]

opening_book = {}

def load_opening_book(filename):
    book = {}
    current_fen = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('pos'):
                parts = line.split()
                fen_str = ' '.join(parts[1:])  # 提取FEN部分
                # 标准化FEN（只保留前四个部分）
                fen_parts = fen_str.split(' ')[:4]
                current_fen = ' '.join(fen_parts)
                book[current_fen] = []
            else:
                if current_fen is None:
                    continue  # 忽略格式错误的行
                move_str, weight = line.split()
                book[current_fen].append((move_str, int(weight)))
    return book

opening_book = load_opening_book('Book.txt')

def evaluate(board):
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
        return 0

    white_score = 0
    black_score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        # 基础价值
        base_value = piece_values[piece.piece_type]
        # 位置价值
        positional_value = get_positional_value(piece, square)

        if piece.color == chess.WHITE:
            white_score += base_value + positional_value
        else:
            black_score += base_value + positional_value

    return white_score - black_score

def order_moves(board, moves):
    scored_moves = []
    for move in moves:
        score = 0
        if board.is_capture(move):
            if board.is_en_passant(move):
                score += piece_values[chess.PAWN]
            else:
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += piece_values[captured_piece.piece_type]
        if move.promotion is not None:
            score += piece_values[move.promotion]
        scored_moves.append((score, move))
    scored_moves.sort(key=lambda x: (-x[0], str(x[1])))
    return [move for (_, move) in scored_moves]

def quiescence(board, alpha, beta):
    stand_pat = -evaluate(board)
    if board.turn == chess.BLACK:
        stand_pat = -stand_pat

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    captures = [move for move in board.legal_moves if board.is_capture(move)]
    ordered_captures = order_moves(board, captures)

    for move in ordered_captures:
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def minimax(board, depth, alpha, beta):
    if board.is_checkmate():
        return -9999 - depth if board.turn == chess.WHITE else 9999 + depth
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
        return 0

    if depth == 0:
        return quiescence(board, alpha, beta)

    legal_moves = list(board.legal_moves)
    ordered_moves = order_moves(board, legal_moves)

    if board.turn == chess.WHITE:
        max_eval = -float('inf')
        for move in ordered_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in ordered_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board, depth):
    # 先检查开局库
    current_fen = board.fen()
    fen_parts = current_fen.split(' ')[:4]
    trimmed_fen = ' '.join(fen_parts)
    
    if trimmed_fen in opening_book:
        # 获取所有合法走法的UCI字符串
        legal_moves = {move.uci(): move for move in board.legal_moves}
        # 过滤合法走法并计算总权重
        valid_moves = []
        total_weight = 0
        for move_str, weight in opening_book[trimmed_fen]:
            if move_str in legal_moves:
                valid_moves.append((move_str, weight))
                total_weight += weight
        
        if valid_moves:
            # 按权重随机选择
            move_str = random.choices(
                [move[0] for move in valid_moves],
                weights=[move[1] for move in valid_moves],
                k=1
            )[0]
            return legal_moves[move_str]
    
    best_move = None
    best_value = -float('inf') if board.turn == chess.WHITE else float('inf')

    legal_moves = list(board.legal_moves)
    ordered_moves = order_moves(board, legal_moves)

    for move in ordered_moves:
        board.push(move)
        current_value = minimax(board, depth-1, -float('inf'), float('inf'))
        board.pop()

        if board.turn == chess.WHITE:
            if current_value > best_value:
                best_value = current_value
                best_move = move
        else:
            if current_value < best_value:
                best_value = current_value
                best_move = move

    return best_move

def main():
    board = chess.Board()
    
    while not board.is_game_over():
        print("\nCurrent Board:")
        print(board)
        
        if board.turn == chess.WHITE:
            print("White to move")
            while True:
                move_uci = input("Input your move:").strip()
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("Invalid move!")
                except ValueError:
                    print("Invalid format!")
        else:
            print("AI is thinking...")
            ai_move = get_best_move(board, 4)
            board.push(ai_move)
            print(f"AI played: {ai_move.uci()}")
    
    print("\nGame Over")
    print("Final result:", board.result())
    print("Endgame board:")
    print(board)

if __name__ == "__main__":
    main()