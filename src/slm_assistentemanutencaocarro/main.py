from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_application,
)
from slm_assistentemanutencaocarro.presentation.cli import run


def main():
    application = build_application(
        json_file_vehicle="data/vehicle.json",
    )

    run(application)


if __name__ == "__main__":
    main()