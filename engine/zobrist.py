import chess.polyglot as cpoly
import numpy as np
import chess
from abc import ABC, abstractmethod

class ZobristHasherBase(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def compute_zobrist_hash(self, board):
        pass

class ZobristHasherPoly(ZobristHasherBase):
    
    def __init__(self) -> None:
        super().__init__()
        self.hasher = self.initialize()
    
    def initialize(self):
        return cpoly.ZobristHasher(cpoly.POLYGLOT_RANDOM_ARRAY)

    def compute_zobrist_hash(self, board):
        return self.hasher(board)


class ZobristHasher(ZobristHasherBase):
    def __init__(self) -> None:
        super().__init__()
        self.tables = self.initialize()
        self.table_square = self.tables[0]
        self.table_castling = self.tables[1]
        self.table_ep = self.tables[2]
        
    def initialize(self):
        # piece_type, color, squares, castling_rights, en_passant
        table_squares = np.empty((6, 2, 64), dtype=np.uint64)
        table_castling = np.empty((16), dtype=np.uint64)
        table_ep = np.empty((9), dtype=np.uint64)
        
        for index in np.ndindex(table_squares.shape):
            table_squares[index] = np.random.randint(0, 2**63 - 1)
            
        for index in np.ndindex(table_castling.shape):
            table_castling[index] = np.random.randint(0, 2**63 - 1)
            
        for index in np.ndindex(table_ep.shape):
            table_ep[index] = np.random.randint(0, 2**63 - 1)

        return table_squares, table_castling, table_ep

    def compute_zobrist_hash(self, board):
        
        hash_value = 0
        
        castling_index = self.castling_rights_index(board)
        hash_value = np.bitwise_xor(hash_value, self.table_castling[castling_index])
        
        ep_index = 0
        if board.ep_square:
            ep_index = chess.square_file(board.ep_square) + 1
        hash_value = np.bitwise_xor(hash_value, self.table_ep[ep_index])
        
        for square, piece in board.piece_map().items():
            if piece:
                index = piece.piece_type - 1
                color = int(piece.color)
                
                table = self.table_square[(index, color, square)]
                
                hash_value = np.bitwise_xor(hash_value, table)
                
        return hash_value
    
    def castling_rights_index(self, board):
        index = 0
        if board.has_kingside_castling_rights(chess.WHITE):
            index |= 1
        if board.has_queenside_castling_rights(chess.WHITE):
            index |= 2
        if board.has_kingside_castling_rights(chess.BLACK):
            index |= 4
        if board.has_queenside_castling_rights(chess.BLACK):
            index |= 8
        return index
