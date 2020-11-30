from typing import Dict

def remove_boundaries(input : str, delim : str)->str:
    """Returns a new string with the given boundaries removed"""
    output = ""
    for char in input:
        if char != delim:
            output += char
    return output

def get_transitional_probabilities(input: str, sub_boundary: str):
    total_frequency : Dict[str, int] = {}
    transitional_frequency : Dict[str, int] = {}
    curr_syl: str = ""
    last_syl: str = ""
    for char in input:
        # this means we have reached a boundary
        if char == sub_boundary:
            # update the total counts
            if curr_syl not in total_frequency:
                total_frequency[curr_syl] = 0
            # only update the transitional frequency if we're not at a boundary
            if curr_syl and last_syl:
                transitional : str = last_syl+curr_syl
                if transitional not in transitional_frequency:
                    transitional_frequency[transitional] = 0
                transitional_frequency[transitional] += 1
            total_frequency[curr_syl] += 1
            last_syl = curr_syl
            curr_syl = ""
        # TODO: want to kind of reset here
        elif char == "U":
            curr_syl = ""
            last_syl = ""
        else:
            curr_syl += char
    print(total_frequency)
    print(transitional_frequency)


dev_input = "bPih1PgPSWdPrPah1PmPSWbPih1PgPSWdPrPah1PmPSWU"
dev_no_word_boundaries = remove_boundaries(dev_input, "W")
print(dev_input)
print(dev_no_word_boundaries)
get_transitional_probabilities(dev_no_word_boundaries, "S")





# input : str = ""
# for line in open("mother.speech.txt"):
#     input += line.strip()
#
# print(input[1:20])
# print(remove_boundaries(input, 'W')[1:20])
