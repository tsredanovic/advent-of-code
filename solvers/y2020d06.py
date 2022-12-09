
from advent_of_code.basesolver import BaseSolver


class GroupFactory:
    def extract_groups(all_lines):
        grouped_lines = GroupFactory.separate_lines(all_lines)
        objects = []
        for lines in grouped_lines:
            obj = GroupFactory.object_from_lines(lines)
            objects.append(obj)
        return objects

    def separate_lines(all_lines):
        object_lines = []
        single_object_lines = []
        for line in all_lines:
            if line:
                single_object_lines.append(line)
            else:
                object_lines.append(single_object_lines)
                single_object_lines = []
        object_lines.append(single_object_lines)
        return object_lines
    
    def object_from_lines(lines):
        return Group(lines)


class Group:
    def __init__(self, group_answers):
        self.group_answers = group_answers
    
    def __str__(self):
        return str(self.group_answers)
    
    def __repr__(self):
        return self.__str__()
    
    def any_yes_answers(self):
        yes_answers = []
        for person_answers in self.group_answers:
            for answer in person_answers:
                if answer not in yes_answers:
                    yes_answers.append(answer)
        return yes_answers
    
    def any_yes_aneswers_count(self):
        return len(self.any_yes_answers())
    
    def all_yes_answers(self):
        distinct_answers = self.any_yes_answers()
        #print('Group answers: {}'.format(self.group_answers))
        #print('Distinct answers: {}'.format(distinct_answers))

        all_yes_answers = []
        for distinct_answer in distinct_answers:
            everyone_answered_yes = True
            #print('Checking: {}'.format(distinct_answer))
            for person_i, person_answers in enumerate(self.group_answers):
                #print('Checking person {}: {}'.format(person_i, person_answers))
                person_answered_yes = False
                for answer in person_answers:
                    #print('Is {}=={}? {}'.format(answer, distinct_answer, answer == distinct_answer))
                    if answer == distinct_answer:
                        person_answered_yes = True
                        break
                #print('Person {} answer to {}: {}'.format(person_i, distinct_answer, person_answered_yes))
                if not person_answered_yes:
                    everyone_answered_yes = False
                    break
            if everyone_answered_yes:
                all_yes_answers.append(distinct_answer)
        
        return all_yes_answers
    
    def all_yes_aneswers_count(self):
        return len(self.all_yes_answers())


class Y2020D06Solver(BaseSolver):
    def solve_part_a(self):
        groups = GroupFactory.extract_groups(self.lines)
        
        result = 0
        for group in groups:
            result += group.any_yes_aneswers_count()
        
        return str(result)
    

    def solve_part_b(self):
        groups = GroupFactory.extract_groups(self.lines)
        
        result = 0
        for group in groups:
            result += group.all_yes_aneswers_count()
        
        return str(result)
