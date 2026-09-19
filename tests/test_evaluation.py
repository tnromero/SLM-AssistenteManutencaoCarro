import csv

from slm_assistentemanutencaocarro.controller.ruled_based_classifier import (
    RuleBasedIntentClassifier,
)


def test_rule_based_accuracy():
    classifier = RuleBasedIntentClassifier()

    total = 0
    correct = 0

    with open("data/intents.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            result = classifier.classify(row["description"])

            total += 1

            if result.intent.value == row["expected_intent"]:
                correct += 1

    accuracy = correct / total

    assert accuracy >= 0.70