from slm_assistentemanutencaocarro.application.exception import VectorIndexError
from slm_assistentemanutencaocarro.infrastructure.composition import (
    build_application,
)
from slm_assistentemanutencaocarro.presentation.cli import run


def main():
    try:
        application = build_application(
            json_file_vehicle="data/vehicle.json",
        )
    except VectorIndexError as exc:
        print(f"Não foi possível iniciar a aplicação: {exc}")
        return
    
    run(application)


if __name__ == "__main__":
    main()