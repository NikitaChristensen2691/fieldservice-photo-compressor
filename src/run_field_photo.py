import base64
import json
import sys

from field_image_service import InfraiImageClient, WorkOrderPhoto, prepare_photo


def main() -> None:
    image_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGNoWDABAANUAbFfHesEAAAAAElFTkSuQmCC"
    )
    photo = WorkOrderPhoto("WO-1042", "tech-17", image_bytes, "arrival.png", "on_site")
    result = prepare_photo(photo, InfraiImageClient())
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
