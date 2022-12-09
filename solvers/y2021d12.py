from collections import Counter

from advent_of_code.basesolver import BaseSolver

class Node:
    def __init__(self, id) -> None:
        self.id = id
        self.conn_node_ids = []
    
    def add_conn_node_id(self, conn_node_id):
        if conn_node_id not in self.conn_node_ids:
            self.conn_node_ids.append(conn_node_id)
    
    def __str__(self) -> str:
        return '{} -> {}'.format(self.id, self.conn_node_ids)
    
    def __repr__(self) -> str:
        return str(self)
    
    @property
    def is_small(self):
        return self.id.islower()
    
    @property
    def is_end(self):
        return self.id == 'end'
    
    @property
    def is_start(self):
        return self.id == 'start'

def generate_nodes_dict(lines):
    nodes_dict = {}
    for line in lines:
        id1, id2 = line.split('-')
        if id1 not in nodes_dict.keys():
            nodes_dict[id1] = Node(id1)
        if id2 not in nodes_dict.keys():
            nodes_dict[id2] = Node(id2)
        nodes_dict[id1].add_conn_node_id(id2)
        nodes_dict[id2].add_conn_node_id(id1)
    
    return nodes_dict


def path_has_two_small_caves_once_or_less(nodes_dict, path):
    node_counter = Counter(path)
    small_caves_above_1_count = 0
    for node_id, count in node_counter.items():
        if nodes_dict[node_id].is_small and count > 2:
            return False
        if nodes_dict[node_id].is_small and count >= 2:
            small_caves_above_1_count += 1

    if small_caves_above_1_count <= 1:
        return True
    return False


class Y2021D12Solver(BaseSolver):
    def solve_part_a(self):
        nodes_dict = generate_nodes_dict(self.lines)

        current_paths = [['start']]
        finished_paths = []
        while current_paths:
            current_path = current_paths.pop()
            current_path_last_node = current_path[-1]
            current_path_next_nodes = nodes_dict[current_path_last_node].conn_node_ids

            possible_next_paths = []
            for current_path_next_node in current_path_next_nodes:
                possible_next_path = current_path.copy()
                possible_next_path.append(current_path_next_node)
                possible_next_paths.append(possible_next_path)
            
            next_paths = []
            for possible_next_path in possible_next_paths:
                last_node_id = possible_next_path[-1]
                last_node = nodes_dict[last_node_id]
                previous_node_ids = possible_next_path[:-1]

                if last_node.is_end:
                    finished_paths.append(possible_next_path)
                elif last_node.is_small and last_node_id in previous_node_ids:
                    continue
                else:
                    next_paths.append(possible_next_path)

            for next_path in next_paths:
                current_paths.append(next_path)
        
        return len(finished_paths)
    

    def solve_part_b(self):
        nodes_dict = generate_nodes_dict(self.lines)

        current_paths = [['start']]
        finished_paths = []
        while current_paths:
            current_path = current_paths.pop()
            current_path_last_node = current_path[-1]
            current_path_next_nodes = nodes_dict[current_path_last_node].conn_node_ids

            possible_next_paths = []
            for current_path_next_node in current_path_next_nodes:
                possible_next_path = current_path.copy()
                possible_next_path.append(current_path_next_node)
                possible_next_paths.append(possible_next_path)
            
            next_paths = []
            for possible_next_path in possible_next_paths:
                last_node_id = possible_next_path[-1]
                last_node = nodes_dict[last_node_id]
                previous_node_ids = possible_next_path[:-1]

                if last_node.is_end:
                    finished_paths.append(possible_next_path)
                elif last_node.is_start and last_node_id in previous_node_ids:
                    continue
                elif last_node.is_small and last_node_id in previous_node_ids and not path_has_two_small_caves_once_or_less(nodes_dict, possible_next_path):
                    continue
                else:
                    next_paths.append(possible_next_path)

            for next_path in next_paths:
                current_paths.append(next_path)
            
            #print('Current paths: {}'.format(current_paths))
            #print('Finished paths: {}'.format(finished_paths))
        
        return len(finished_paths)

