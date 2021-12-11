from basesolver import BaseSolver

digits = {
    0 : {
        "segments": "abcefg"
    },
    1 : {
        "segments": "cf"
    },
    2 : {
        "segments": "acdeg"
    },
    3 : {
        "segments": "acdfg"
    },
    4 : {
        "segments": "bcdf"
    },
    5 : {
        "segments": "abdfg"
    },
    6 : {
        "segments": "abdefg"
    },
    7 : {
        "segments": "acf"
    },
    8 : {
        "segments": "abcdefg"
    },
    9 : {
        "segments": "abcdfg"
    }
}

positions = {
    'tt': None,
    'tl': None,
    'tr': None,
    'm': None,
    'bl': None,
    'br': None,
    'bb': None,
}

def deduction(input_values):
    # get 5 (2, 3, 5) and 6 (0, 6, 9) segment input values
    five_segment_input_values = []
    six_segment_input_values = []
    for input_value in input_values:
        if len(input_value) == 5:
            five_segment_input_values.append(input_value)
        if len(input_value) == 6:
            six_segment_input_values.append(input_value)

    # segments of unique segment count digits
    unique_segment_count_digits = [1, 4, 7, 8]
    for input_value in input_values:
        for unique_segment_count_digit in unique_segment_count_digits:
            digit_segment_count = len(digits[unique_segment_count_digit]["segments"])
            if digit_segment_count == len(input_value):
                digits[unique_segment_count_digit]['bad_segments'] = input_value

    # use 1 and 7 to figure out what is at positon tt
    positions['tt'] = list(set(digits[7]['bad_segments']).difference(set(digits[1]['bad_segments'])))[0]

    # use 1, 0, 6, 9 to figure out what is 6 - you know bad_segments of 1, 0 and 9 both contain those segments, odd one out is 6
    for six_segment_input_value in six_segment_input_values:
        if set(digits[1]['bad_segments']).intersection(six_segment_input_value) != set(digits[1]['bad_segments']):
            digits[6]['bad_segments'] = six_segment_input_value

    # use 1, 2, 3, 5 to figure out what is 3 - you know bad_segments of 1, only 3 contains both of those segments
    for five_segment_input_value in five_segment_input_values:
        if set(digits[1]['bad_segments']).intersection(five_segment_input_value) == set(digits[1]['bad_segments']):
            digits[3]['bad_segments'] = five_segment_input_value
    
    # figure out what is 9, only 6 segment which has same segments as 4
    for six_segment_input_value in six_segment_input_values:
        if set(digits[4]['bad_segments']).intersection(six_segment_input_value) == set(digits[4]['bad_segments']):
            digits[9]['bad_segments'] = six_segment_input_value
    
    # figure out 0 since it is the only 6 segment left
    for six_segment_input_value in six_segment_input_values:
        if six_segment_input_value not in [digits[6]['bad_segments'], digits[9]['bad_segments']]:
            digits[0]['bad_segments'] = six_segment_input_value
    
    # use 0 and 8 to figure out what is at position m
    positions['m'] = list(set(digits[8]['bad_segments']).difference(set(digits[0]['bad_segments'])))[0]

    # use 1, 4 and what is at position m to figure out what is at position tl
    positions['tl'] = list(set(digits[4]['bad_segments']).difference(set(digits[1]['bad_segments'])))
    positions['tl'].remove(positions['m'])
    positions['tl'] = positions['tl'][0]

    # use what is at tl to figure out which of the two remaining segments is 5 and which is 2
    two_and_five_segments = five_segment_input_values.copy()
    two_and_five_segments.remove(digits[3]['bad_segments'])
    for segment in two_and_five_segments:
        if positions['tl'] in segment:
            digits[5]['bad_segments'] = segment
        else:
            digits[2]['bad_segments'] = segment

    result = {}
    for digit in digits.keys():
        result[digits[digit]['bad_segments']] = digit
    
    return result


def find_digit(result, value):
    for segments, digit in result.items():
        if sorted(segments) == sorted(value):
            return str(digit)


class Y2021D08Solver(BaseSolver):
    def solve_part_a(self):
        inputs = []
        outputs = []
        for line in self.lines:
            inputs.append(line.split(' | ')[0].split())
            outputs.append(line.split(' | ')[1].split())
        
        unique_segment_count_digits = [1, 4, 7, 8]

        unique_segment_count_digits_count = 0
        for output_values in outputs:
            for output_value in output_values:
                for unique_segment_count_digit in unique_segment_count_digits:
                    digit_segment_count = len(digits[unique_segment_count_digit]["segments"])
                    if digit_segment_count == len(output_value):
                        unique_segment_count_digits_count += 1
        
        return unique_segment_count_digits_count
    

    def solve_part_b(self):
        sum = 0
        for line in self.lines:
            input_values = line.split(' | ')[0].split()
            output_values = line.split(' | ')[1].split()
            result = deduction(input_values)
            output_digits = ''
            for output_value in output_values:
                output_digits += find_digit(result, output_value)
            sum += int(output_digits)
        
        return sum

