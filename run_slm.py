from typing import Dict, List
import argparse


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
    # extract the syllables from the utterance to generate from and extract the corresponding transitional probabilities
    syllables: List[str] = [s for s in input.split(sub_boundary) if s]
    tps: List[float] = [
        transitional_probabilities[syllables[i] + "_" + syllables[i + 1]]
        for i in range(0, len(syllables) - 1)
    ]
    # initialize the output and iterate through the tps to check for local minima
    output = syllables[0] + sub_boundary
    for i in range(0, len(tps)):
        # add word boundary at local minimum, provided you're not at either end of the word
        if i > 0 and i < len(tps) - 1 and tps[i - 1] > tps[i] and tps[i] < tps[i + 1]:
            output += boundary_to_insert
        output += syllables[i + 1] + sub_boundary
    output += boundary_to_insert
    return output


def get_transitional_probabilities(input: str, sub_boundary: str) -> Dict[str, float]:
    """Gets the transitional probabilities from the input and returns a dictionary of syllables
    separated by underscores, mapped to the transitional probabilities of the two syllables"""
    total_frequency: Dict[str, int] = {}
    transitional_frequency: Dict[str, int] = {}
    # iterate through each syllable separately to get the overall frequency and transitional frequencies
    syllables: List[str] = [syll for syll in input.split(sub_boundary) if syll]
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
    # now, calculate and return the transitional probabilities based off of the frequencies
    return {
        transition: (
            transitional_frequency[transition]
            / total_frequency[transition.split("_")[0]]
        )
        for transition in transitional_frequency
    }


def main(path: str, boundary: str, keep_accents: bool):
    """Executes the statistical learning with transitional probabilities and generation"""
    print(f"Calculating transitional probabilities over {path}...")
    sub_boundary: str = "S" if boundary == "W" else "P"
    # get the input, both with and without word boundaries
    input: str = ""
    for line in open(path):
        input += line.strip()
    # remove accents from the input
    if not keep_accents:
        input2 = ""
        for char in input:
            if char != "0" and char != "1" and char != "2":
                input2 += char
        input = input2
    input_without_word_boundaries = remove_boundaries(input, boundary)
    # calculate the transitional probabilites of words from the transitions between syllables
    transitional_probabilities = get_transitional_probabilities(
        input_without_word_boundaries, sub_boundary
    )
    # generate over the entire input using these transitional probabilities
    generated = predict_word_boundaries(
        input_without_word_boundaries,
        sub_boundary,
        boundary,
        transitional_probabilities,
    )
    # evaluate utterance by utterance and average the precision and recall
    test_correct = [utt for utt in input.split("U") if utt]
    test_generated = [utt for utt in generated.split("U") if utt]
    print(f"Evaluating {len(test_correct)} predictions ...")
    total_correct = 0
    total_generated = 0
    total_right = 0
    for i in range(0, len(test_correct)):
        correct = [w for w in test_correct[i].split(boundary) if w]
        generated = [w for w in test_generated[i].split(boundary) if w]
        total_right += len([w for w in correct if w in generated])
        total_correct += len(correct)
        total_generated += len(generated)
    print("=================================================================")
    print(f"Precision: {total_right / total_generated*100 : .3f}%")
    print(f"Recall: {total_right / total_correct*100: .3f}%")


if __name__ == "__main__":
    # Parse the user input and call main with the parameters to execute the program
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "path", type=str, help="path of the file to perform SLM learning on"
    )
    argument_parser.add_argument(
        "-boundary",
        type=str,
        choices=["W", "S"],
        default="W",
        help="boundary of interest (default=W)",
    )
    argument_parser.add_argument(
        "-keep_accents",
        type=bool,
        default=False,
        choices=[True, False],
        help="keep accents when calculating TPs (default=F)",
    )
    args = argument_parser.parse_args()
    main(args.path, args.boundary, args.keep_accents)
