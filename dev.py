from typing import Dict, List


def remove_boundaries(input: str, delim: str) -> str:
    """Returns a new string with the given boundary removed"""
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
    """Given the transitional probabilities of syllables and the input string, predicts word boundaries
    for an utterance and returns a new string containing these boundaries"""
    syllables: List[str] = [s for s in input.split(sub_boundary) if s]
    tps: List[float] = [
        transitional_probabilities[syllables[i] + "_" + syllables[i + 1]]
        for i in range(0, len(syllables) - 1)
    ]
    output = syllables[0] + "S"
    for i in range(0, len(tps)):
        if (i == 0 or tps[i - 1] > tps[i]) and (
            i == len(tps) - 1 or tps[i] < tps[i + 1]
        ):
            output += "W"
        output += syllables[i + 1] + "S"
    output += "W"
    print(syllables)
    print(tps)
    print(output)
    return output


def get_transitional_probabilities(input: str, sub_boundary: str) -> Dict[str, float]:
    """Gets the transitional probabilities from the input and returns a dictionary of syllables
    separated by spaces, mapped to the transitional probabilities of the two syllables"""
    total_frequency: Dict[str, int] = {}
    transitional_frequency: Dict[str, int] = {}
    # iterate through each utterance separately to get the overall frequency and transitional frequencies
    for utterance in [input]:  # [utt for utt in input.split("U") if utt]:
        # iterate through each syllable in the utterance
        syllables: List[str] = [syll for syll in utterance.split(sub_boundary) if syll]
        i: int = 0
        while i < len(syllables):
            curr_syl = syllables[i]
            # update the frequency of the given syllable
            if curr_syl not in total_frequency:
                total_frequency[curr_syl] = 0
            total_frequency[curr_syl] += 1
            # if not word initial, update the transitional probabilities
            if i > 0:
                transitional: str = syllables[i - 1] + "_" + curr_syl
                if transitional not in transitional_frequency:
                    transitional_frequency[transitional] = 0
                transitional_frequency[transitional] += 1
            i += 1
    # now, calculate the transitional probabilities based off of the frequencies
    return {
        transition: (
            transitional_frequency[transition]
            / total_frequency[transition.split("_")[0]]
        )
        for transition in transitional_frequency
    }


def main():
    """Executes the statistical learning with transitional probabilities and generation"""
    # get the input, both with and without word boundaries
    input: str = ""  # "bPih1PgPSWdPrPah1PmPSWbPih1PgPSWdPrPah1PmPSWUbPih1PgPSWdPrPah1PmPSWU"
    for line in open("mother.speech.txt"):
        input += line.strip()
    input2 = ""
    for char in input:
        if char != "0" and char != "1" and char != "2":
            input2 += char
    input = input2
    input_without_word_boundaries = remove_boundaries(input, "W")
    # calculate the transitional probabilites of words from the transitions between syllables
    transitional_probabilities = get_transitional_probabilities(
        input_without_word_boundaries, "S"
    )
    generated = predict_word_boundaries(
        input_without_word_boundaries, "S", "W", transitional_probabilities
    )
    test_correct = [utt for utt in input.split("U") if utt]
    test_generated = [utt for utt in generated.split("U") if utt]
    total_correct = 0
    total_generated = 0
    total_right = 0

    for i in range(0, len(test_correct)):
        correct = [w for w in test_correct[i].split("W") if w]
        generated = [w for w in test_generated[i].split("W") if w]
        total_right += len([w for w in generated if w in correct])
        total_correct += len(correct)
        total_generated += len(generated)
    print(total_right / total_generated)
    print(total_right / total_correct)
    return

    # get the correct utterances and the utterances to generate from
    correct_utterances = [utt for utt in input.split("U") if utt]
    utterances_no_boundaries = [
        utt for utt in input_without_word_boundaries.split("U") if utt
    ]
    i: int = 0
    recall = 0
    precision = 0
    total_precision_numerator = 0
    total_precision_denominator = 0
    total_recall_denominator = 0
    # iterate through the utterances and generate for each using the transitional probabilities
    while i < len(correct_utterances):
        hypothesized: str = predict_word_boundaries(
            utterances_no_boundaries[i], "S", "W", transitional_probabilities
        )
        # get the correct and hypothesized words and tally up the precision and recall
        correct_words = [word for word in correct_utterances[i].split("W") if word]
        hypothesized_words = [word for word in hypothesized.split("W") if word]
        num_correct = len(
            [word for word in correct_words if word in hypothesized_words]
        )
        print(len(correct_words), num_correct, len(hypothesized_words))
        recall += num_correct / len(correct_words)
        # TODO: what's going on here?
        precision += num_correct / len(hypothesized_words)
        total_precision_denominator += len(hypothesized_words)
        total_precision_numerator += num_correct
        total_recall_denominator += len(correct_words)
        i += 1
    print(recall / i)
    print(precision / i)
    print(total_precision_numerator / total_precision_denominator)
    print(total_precision_numerator / total_recall_denominator)


if __name__ == "__main__":
    main()
