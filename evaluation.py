import csv

from slm_assistentemanutencaocarro.controller.ruled_based_classifier import (
    RuleBasedIntentClassifier,
)


def main():
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
            else:
                print(
                    f"ERRO: {row['description']}"
                    f" | esperado={row['expected_intent']}"
                    f" | obtido={result.intent.value}"
                )

    accuracy = correct / total * 100

    print()
    print(f"Acurácia: {accuracy:.2f}%")
    print(f"Acertos: {correct}/{total}")


if __name__ == "__main__":
    main()