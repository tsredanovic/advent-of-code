
from advent_of_code.basesolver import BaseSolver


ALL_BAGS = []

class BagFactory:
    def extract_objects(all_lines):
        objects = []
        for line in all_lines:
            obj = BagFactory.object_from_line(line)
            objects.append(obj)
        return objects

    def object_from_line(line):
        bag_id = line.split(' bags')[0]
        contain_part = line.split(' contain ')[1].rstrip('.')
        children = {}
        for contain_bag_part in contain_part.split(', '):
            if contain_bag_part == 'no other bags':
                children = {}
                continue
            count = int(contain_bag_part.split(' ')[0])
            child_bag_id = ' '.join(contain_bag_part.split(' ')[1:-1])

            children[child_bag_id] = count
        return Bag(bag_id, children)


class Bag:
    def __init__(self, id, children):
        self.id = id
        self.children = children
    
    def can_contain_count(self, bag_id):
        return self.children.get(bag_id, 0)
    
    def can_contain(self, bag_id):
        if self.children.get(bag_id, 0):
            return True
        else:
            return False

    def get_bag(bag_id):
        for bag in ALL_BAGS:
            if bag.id == bag_id:
                return bag
        return None
    
    def get_children(self):
        children = []

        children_ids = list(self.children.keys())
        for child_id in children_ids:
            child = Bag.get_bag(child_id)
            children.append(child)
        return children
    
    def is_descendant(self, descendant_bag_id):
        bags_to_check = [self]
        while bags_to_check:
            #print('Bags to check: {}'.format(bags_to_check))
            bag_to_check = bags_to_check.pop(0)
            #print('Checking: {}'.format(bag_to_check))
            children = bag_to_check.get_children()
            #print('Children: {}'.format(children))
            for child in children:
                if child.id == descendant_bag_id:
                    return True
                bags_to_check.append(child)
        return False
    
    def fits_bags(self):
        fits_bags = 0
        current_bags = [self]
        while current_bags:
            #print('Current bags: {}'.format([cb.id for cb in current_bags]))
            current_bag = current_bags.pop(0)
            #print('Checking `{}`: {}'.format(current_bag.id, current_bag.children))
            fits_bags += 1

            for child_id, count in current_bag.children.items():
                global_child = Bag.get_bag(child_id)
                for _ in range(count):
                    current_bags.append(Bag(global_child.id, global_child.children))
        return fits_bags - 1


class Y2020D07Solver(BaseSolver):
    def solve_part_a(self):
        global ALL_BAGS
        ALL_BAGS = BagFactory.extract_objects(self.lines)

        input_bag_id = 'shiny gold'

        bags_to_check = [bag for bag in ALL_BAGS if bag.id != input_bag_id]

        valid_bags_count = 0
        for bag in bags_to_check:
            if bag.is_descendant(input_bag_id):
                valid_bags_count += 1

        return str(valid_bags_count)
    

    def solve_part_b(self):
        global ALL_BAGS
        ALL_BAGS = BagFactory.extract_objects(self.lines)

        input_bag_id = 'shiny gold'
        input_bag = Bag.get_bag(input_bag_id)
        fits_bags = input_bag.fits_bags()
        
        return str(fits_bags)

