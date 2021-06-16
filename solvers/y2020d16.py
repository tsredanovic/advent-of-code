from itertools import groupby

from basesolver import BaseSolver

class Rule:
    def __init__(self, index, line):
        self.index = index
        self.name = line.split(': ')[0]
        self.ranges = []
        for single_rule_line in line.split(': ')[1].split(' or '):
            num1 = int(single_rule_line.split('-')[0])
            num2 = int(single_rule_line.split('-')[1])
            self.ranges.append([num1, num2])
    
    def check(self, value):
        for rng in self.ranges:
            if rng[0] <= value <= rng[1]:
                return True
        return False
    
    def __str__(self):
        return '{}: {}'.format(self.name, self.ranges)
    
    def __repr__(self):
        return self.__str__()
    

class TicketTrans:
    def __init__(self, input_lines):
        groups = [list(group) for k, group in groupby(input_lines, lambda x: x == '') if not k]

        self.my_ticket = [int(value) for value in groups[1][1].split(',')]

        self.nearby_tickets = []
        for nearby_ticket_line in groups[2][1:]:
            self.nearby_tickets.append([int(value) for value in nearby_ticket_line.split(',')])

        self.rules = {}
        for i, rule_line in enumerate(groups[0]):
            self.rules[i] = Rule(i, rule_line)
    
    @property
    def rules_list(self):
        return [rule for rule in self.rules.values()]
    
    def all_values_in_any_rule(values, rules):
        for value in values:
            value_in_any_rule = False
            for rule in rules:
                is_value_in_rule = rule.check(value)
                if is_value_in_rule:
                    value_in_any_rule = True
                    break
            if not value_in_any_rule:
                return False, value
        return True, None

    def nearby_tickets_validity(self):
        valid_tickets = []
        invalid_tickets = []
        for nearby_ticket in self.nearby_tickets:
            are_all_values_in_any_rule, invalid_value = TicketTrans.all_values_in_any_rule(nearby_ticket, self.rules_list)
            if are_all_values_in_any_rule:
                valid_tickets.append(nearby_ticket)
            else:
                invalid_tickets.append({'ticket': nearby_ticket, 'invalid_value': invalid_value})
        return valid_tickets, invalid_tickets
    
    def valid_rule_names_for_value(self, value):
        valid_rule_names = []
        for rule in self.rules_list:
            if rule.check(value):
                valid_rule_names.append(rule.name)
        return valid_rule_names


class Y2020D16Solver(BaseSolver):
    def solve_part_a(self):
        tt = TicketTrans(self.lines)
        valid_tickets, invalid_tickets = tt.nearby_tickets_validity()
        result = sum(inv_tck['invalid_value'] for inv_tck in invalid_tickets)
        return str(result)
    

    def solve_part_b(self):
        tt = TicketTrans(self.lines)
        valid_tickets, invalid_tickets = tt.nearby_tickets_validity()

        #for rule in tt.rules_list:
        #    print(rule)

        columns_valid_names = {}
        for i in range(len(tt.my_ticket)):
            columns_valid_names[i] = []

        for valid_ticket in valid_tickets:
            for col_i, value in enumerate(valid_ticket):
                valid_rule_names = tt.valid_rule_names_for_value(value)
                #print('{}: {}'.format(value, valid_rule_names))
                columns_valid_names[col_i].append(valid_rule_names)
        
        all_rules_names = [rule.name for rule in tt.rules_list]

        columns_min_names = {}
        for i in range(len(tt.my_ticket)):
            columns_min_names[i] = []

        for col_i, valid_names in columns_valid_names.items():
            columns_min_names[col_i] = list(set.intersection(*map(set, valid_names)))

        solution = {}
        for i in range(len(tt.my_ticket)):
            solution[i] = None
        
        while True:
            # Break if solution is complete
            if None not in solution.values():
                break
            
            # Find lonely name
            for col_i, names in columns_min_names.items():
                if len(names) == 1:
                    lonely_name = names[0]
                    break
            
            # Set part of solution
            solution[col_i] = lonely_name

            # Remove lonely name everywhere
            keys_to_delete = []
            for col_i, names in columns_min_names.items():
                if lonely_name in names:
                    names = [name for name in names if name != lonely_name]
                    if not names:
                        keys_to_delete.append(col_i)
                    else:
                        columns_min_names[col_i] = names
            for key_to_delete in keys_to_delete:
                del columns_min_names[key_to_delete]

        solution_indexes = {y:x for x,y in solution.items()}
        solution_values = {}
        for key, index in solution_indexes.items():
            value = tt.my_ticket[index]
            solution_values[key] = value
        
        result = 1
        for name, value in solution_values.items():
            if name.startswith('departure'):
                result *= value
        return str(result)
