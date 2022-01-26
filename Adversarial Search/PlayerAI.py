# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 07:37:11 2021

@author: mjvat
"""

import time
from math import inf
from BaseAI import BaseAI

class PlayerAI(BaseAI):
    
    def __init__(self):
        
        self.current_depth = 0
        self.max_search_depth = 0
    
    def getMove(self, grid):
    
        self.start_time = time.time()
        self.alpha = -inf
        self.beta = inf
        self.current_depth = 0
        self.max_search_depth = self.depthLimitedSearch(grid)

        move, _ = self.maximize(grid, -inf, inf)
        return move
    
    def maximize(self, grid, alpha, beta):
       
        self.current_depth += 1
        if self.current_depth >= self.max_search_depth:
            return None, self.heuristic(grid)        
        elif not grid.canMove():
            return None, self.heuristic(grid)        
        elif time.time() - self.start_time > 0.2:
            return None, self.heuristic(grid)        
            
        (maxMove, maxUtility) = (None, -inf)

        getMoves = grid.getAvailableMoves()
        getMoves = sorted(map(int, getMoves), key=lambda num: num%2)

        for move in getMoves:            
            gridCopy = grid.clone()
            gridCopy.move(move)
            grid.move(move)
            (_, utility) = self.minimize(grid, alpha, beta)
            self.current_depth -=1
            
            if utility > maxUtility:
                (maxMove, maxUtility) = (move, utility)
                
            if maxUtility >= beta:
                break
            
            if maxUtility > alpha:
                alpha = maxUtility
            
            if time.time() - self.start_time > 0.2:
                break 
            
        return (maxMove, maxUtility)

    def minimize(self, grid, alpha, beta):
        
        self.current_depth += 1       
        if self.current_depth >= self.max_search_depth:
            return None, self.heuristic(grid)
        elif not grid.canMove():
            return None, self.heuristic(grid)        
        elif time.clock() - self.start_time >= 0.1:
            return None, self.heuristic(grid)        
        
        (minCell, minUtility) = (None, inf)
        getCells = grid.getAvailableCells()
        for cell in getCells:
            gridCopy = grid.clone()
            gridCopy.setCellValue(cell, 2)
            grid.setCellValue(cell, 2)                                       
            (_, utility) = self.maximize(grid, alpha, beta)
            self.current_depth -=1
            
            if utility < minUtility:
                (minCell, minUtility) = (cell, utility)
            
            if minUtility <= alpha:
                break
            
            if minUtility < beta:
                beta = minUtility
        
            if time.time() - self.start_time > 0.2:
                break
            
        return (minCell, minUtility)
    
    def depthLimitedSearch(self, grid):
        
        empty_cells = len(grid.getAvailableCells())
        if empty_cells >= 16: 
            return 2
        elif empty_cells >= 8:
            return 4
        elif empty_cells >= 4:
            return 6
        else:
            return 8

    def heuristic(self, grid):
        return 3
