from typing import Dict

def remove_boundaries(input : str, delim : str)->str:
    """Returns a new string with the given boundaries removed"""
    output = ""
    for char in input:
        if char != delim:
            output += char
    return output

def predict_word_boundaries(input : str, sub_boundary: str, boundary_to_insert: str, transitional_probabilities : Dict[str, float]):
    """Given the transitional probabilities of syllables and the input string, predicts word boundaries"""
    curr_probability = 0
    last_probability = 0
    output_string = ""
    curr_syl : str = ""
    last_syl : str = ""
    for char in input:
        # If we've reached a boundary, update our counts
        if char == sub_boundary:
            if last_syl and curr_syl:
                lookup = last_syl + " " + curr_syl
                new_probability = transitional_probabilities[lookup]
                if (curr_probability < last_probability) and (curr_probability < new_probability):
                    output_string += boundary_to_insert
                last_probability = curr_probability
                curr_probability = new_probability

            # update the current and last syllables
            if last_syl:
                output_string += last_syl+sub_boundary
            last_syl = curr_syl
            curr_syl = ""
        # Otherwise, append to the current syllable
        else:
            curr_syl += char
    if last_syl:
        output_string += last_syl + sub_boundary + boundary_to_insert
    return output_string



def get_transitional_probabilities(input: str, sub_boundary: str)->Dict[str, float]:
    """Gets the transitional probabilities from the input and returns a dictionary of syllables
    separated by spaces, mapped to the transitional probabilities of the two syllables"""
    total_frequency : Dict[str, int] = {}
    transitional_frequency : Dict[str, int] = {}
    curr_syl: str = ""
    last_syl: str = ""
    for char in input:
        # If we've reached a boundary, update our counts
        if char == sub_boundary:
            # update the total counts
            if curr_syl not in total_frequency:
                total_frequency[curr_syl] = 0
            total_frequency[curr_syl] += 1
            # only update the transitional frequency if we're not at a boundary
            if curr_syl and last_syl:
                transitional : str = last_syl+" "+curr_syl
                if transitional not in transitional_frequency:
                    transitional_frequency[transitional] = 0
                transitional_frequency[transitional] += 1
            # update the current and last syllables
            last_syl = curr_syl
            curr_syl = ""
        # If there's an utterance boundary, don't count transitional probabilities across it
        elif char == "U":
            curr_syl = ""
            last_syl = ""
        # Otherwise, append to the current syllable
        else:
            curr_syl += char
    # now that we have the transitional frequency and total frequency, we calculate TP(A->B) = P(AB)/P(A)
    transitional_probabilities : Dict[str, float] = {}
    for transition in transitional_frequency:
        # get the transitional frequency of B following A
        p_AB = transitional_frequency[transition]
        # get the total frequency of A and set the transitional probability accordingly
        p_A = total_frequency[transition.split()[0]]
        transitional_probabilities[transition] = p_AB/p_A
    return transitional_probabilities


dev_input = "bPih1PgPSWdPrPah1PmPSWbPih1PgPSWdPrPah1PmPSWU"
dev_no_word_boundaries = remove_boundaries(dev_input, "W")

transitional_probabilities = get_transitional_probabilities(dev_no_word_boundaries, "S")
print(transitional_probabilities)
utterances = [utterance for utterance in dev_no_word_boundaries.split("U") if len(utterance) > 0]
actual = [utterance for utterance in dev_input.split("U") if len(utterance) > 0]
print(utterances)
for utterance in utterances:
    print(predict_word_boundaries(utterance, "S", "W", transitional_probabilities))
for utterance in actual:
    print(utterance)





# input : str = ""
# for line in open("mother.speech.txt"):
#     input += line.strip()
#
# print(input[1:20])
# print(remove_boundaries(input, 'W')[1:20])
