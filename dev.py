from typing import Dict, List


def remove_boundaries(input: str, delim: str) -> str:
    """Returns a new string with the given boundaries removed"""
    output = ""
    for char in input:
        if char != delim:
            output += char
    return output


def predict_word_boundaries(
    input: str,
    sub_boundary: str,
    boundary_to_insert: str,
    transitional_probabilities: Dict[str, float],
):
    """Given the transitional probabilities of syllables and the input string, predicts word boundaries"""
    curr_probability = 0
    last_probability = 0
    output_string = ""
    curr_syl: str = ""
    last_syl: str = ""
    for char in input:
        # If we've reached a boundary, update our counts
        if char == sub_boundary:
            if last_syl and curr_syl:
                lookup = last_syl + " " + curr_syl
                new_probability = transitional_probabilities[lookup]
                if (curr_probability < last_probability) and (
                    curr_probability < new_probability
                ):
                    output_string += boundary_to_insert
                last_probability = curr_probability
                curr_probability = new_probability

            # update the current and last syllables
            if last_syl:
                output_string += last_syl + sub_boundary
            last_syl = curr_syl
            curr_syl = ""
        # Otherwise, append to the current syllable
        else:
            curr_syl += char
    if last_syl:
        output_string += last_syl + sub_boundary + boundary_to_insert
    return output_string


def get_transitional_probabilities(input: str, sub_boundary: str) -> Dict[str, float]:
    """Gets the transitional probabilities from the input and returns a dictionary of syllables
    separated by spaces, mapped to the transitional probabilities of the two syllables"""
    total_frequency: Dict[str, int] = {}
    transitional_frequency: Dict[str, int] = {}
    # iterate through each utterance separately
    utterances: List[str] = [utt for utt in input.split("U") if len(utt) > 0]
    for utterance in utterances:
        curr_syl = ""
        last_syl = ""
        for char in utterance:
            if char == sub_boundary:
                # update the total counts
                if curr_syl not in total_frequency:
                    total_frequency[curr_syl] = 0
                total_frequency[curr_syl] += 1
                # only update the transitional frequency if we're not at a boundary
                if curr_syl and last_syl:
                    transitional: str = last_syl + " " + curr_syl
                    if transitional not in transitional_frequency:
                        transitional_frequency[transitional] = 0
                    transitional_frequency[transitional] += 1
                last_syl = curr_syl
                curr_syl = ""
            else:
                curr_syl += char
    transitional_probabilities: Dict[str, float] = {}
    for transition in transitional_frequency:
        # get the transitional frequency of B following A
        p_AB = transitional_frequency[transition]
        # get the total frequency of A and set the transitional probability accordingly
        p_A = total_frequency[transition.split()[0]]
        transitional_probabilities[transition] = p_AB / p_A
    return transitional_probabilities


def main():
    input: str = ""
    for line in open("mother.speech.txt"):
        input += line.strip()
    input_without_word_boundaries = remove_boundaries(input, "W")
    transitional_probabilities = get_transitional_probabilities(
        input_without_word_boundaries, "S"
    )
    # print(transitional_probabilities)
    correct_utterances = [
        utterance for utterance in input.split("U") if len(utterance) > 0
    ]
    utterances_no_boundares = [
        utterance
        for utterance in input_without_word_boundaries.split("U")
        if len(utterance) > 0
    ]
    i: int = 0
    total = 0
    recall = 0
    precision = 0
    while i < len(correct_utterances):
        correct = correct_utterances[i]
        hypothesized = predict_word_boundaries(
            utterances_no_boundares[i], "S", "W", transitional_probabilities
        )
        correct_words = [word for word in correct.split("W") if len(word) > 0]
        hypothesized_words = [word for word in hypothesized.split("W") if len(word) > 0]
        num_correct = len([word for word in hypothesized_words if word in correct])
        # print(num_correct/len(correct_words), num_correct/len(hypothesized_words))
        recall += num_correct / len(correct_words)
        precision += num_correct / len(hypothesized_words)
        total += 1
        i += 1
    print(recall / total)
    print(precision / total)


if __name__ == "__main__":
    main()
