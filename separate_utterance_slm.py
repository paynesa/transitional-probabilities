"""Runs a modified version of the learner specified in
https://www.ling.upenn.edu/~ycharles/papers/quick.pdf that predicts
separately on each utterance"""

from typing import Dict, List
from run_slm import remove_boundaries
import argparse


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
    output = syllables[0] + sub_boundary
    for i in range(0, len(tps)):
        if (i == 0 or tps[i - 1] > tps[i]) and (
            i == len(tps) - 1 or tps[i] < tps[i + 1]
        ):
            output += boundary_to_insert
        output += syllables[i + 1] + sub_boundary
    output += boundary_to_insert
    return output


def get_transitional_probabilities(input: str, sub_boundary: str) -> Dict[str, float]:
    """Gets the transitional probabilities from the input and returns a dictionary of syllables
    separated by spaces, mapped to the transitional probabilities of the two syllables"""
    total_frequency: Dict[str, int] = {}
    transitional_frequency: Dict[str, int] = {}
    # iterate through each utterance separately to get the overall frequency and transitional frequencies
    for utterance in [utt for utt in input.split("U") if utt]:
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


def main(path: str, boundary: str, keep_accents: bool):
    """Executes the statistical learning with transitional probabilities and generation,
    handling each utterance entirely separately"""
    print(f"Running the modified SLM model in {path}...")
    sub_boundary = "S" if boundary == "W" else "P"
    # get the input, both with and without word boundaries
    input: str = ""
    for line in open(path):
        input += line.strip()
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

    # get the correct utterances and the utterances to generate from
    correct_utterances = [utt for utt in input.split("U") if utt]
    utterances_no_boundaries = [
        utt for utt in input_without_word_boundaries.split("U") if utt
    ]
    i: int = 0
    total_correct = 0
    total_generated = 0
    total_right = 0
    print(f"Generating on {len(correct_utterances)} predictions...")
    # iterate through the utterances and generate for each using the transitional probabilities
    while i < len(correct_utterances):
        hypothesized: str = predict_word_boundaries(
            utterances_no_boundaries[i],
            sub_boundary,
            boundary,
            transitional_probabilities,
        )
        # get the correct and hypothesized words and tally up the precision and recall
        correct_words = [word for word in correct_utterances[i].split(boundary) if word]
        hypothesized_words = [word for word in hypothesized.split(boundary) if word]
        num_correct = len(
            [word for word in correct_words if word in hypothesized_words]
        )
        total_correct += len(correct_words)
        total_generated += len(hypothesized_words)
        total_right += num_correct
        i += 1
    precision: float = total_right / total_generated
    recall: float = total_right / total_correct
    print("===============================================================")
    print(f"Precision: {precision * 100 : .3f}%")
    print(f"Recall: {recall * 100: .3f}%")
    print(f"F-score: {(2*precision*recall)/(precision+recall)*100: .3f}%")


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
