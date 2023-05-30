from Celula import Celula
from collections import deque

class PriorityQueue:
    def __init__(self, start: tuple[Celula, int]) -> None:
        self.queue: deque[tuple[Celula, int]] = deque()
        self.queue.append(start)


    def get_key(self, pos: int):
        return list(self.queue[pos].keys())[0]
    
    def ordered_insert(self, insert_elem: tuple[Celula, int]):
        is_equals = False
        index = 0
        for i in range(len(self.queue)):
            cell, prior = self.queue[i]
            insert_cell, insert_prior = insert_elem

            if insert_prior < prior:
                index = i
                break

            if insert_prior == prior:
                index = i
                is_equals = True
                break

        if is_equals == True:
            self.queue.insert((index + 1), insert_elem)
        else:
            self.queue.insert(index, insert_elem)


    # A lista ordenada é basicamente a resposta
    def return_ordered_list_cell(self):
        ordered_list_cell = []
        for item in self.queue:
            ordered_list_cell.append(item[0])
        return ordered_list_cell
    
    def get_priority_list(self):
        lst_prior = []
        for item in self.queue:
            lst_prior.append(item[1])
        return lst_prior

    
    def get_lowest_prior(self):
        return self.queue.popleft()
    
    def get_highest_prior(self):
        return self.queue.pop()
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def exists_in_queue(self, v: Celula):
        for i in range(len(self.queue)):
            cell, prior = self.queue[i]
            if v.x == cell.x and v.y == cell.y:
                return True
        return False