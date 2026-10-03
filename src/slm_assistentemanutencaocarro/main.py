from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_assistant,
)
from slm_assistentemanutencaocarro.presentation.cli import run


def main():
    assistant = build_assistant(
        json_file_vehicle="data/vehicle.json",
    )

    run(assistant)


if __name__ == "__main__":
    main()