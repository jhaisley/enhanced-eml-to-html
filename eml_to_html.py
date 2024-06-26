from email import message_from_file
from email.message import Message
from pathlib import Path
import sys
import argparse
from typing import Any, List, Union


def message_to_str(message: Message) -> str:
    payload: Any = message.get_payload()

    if isinstance(payload, str):
        payload_decoded: bytes = message.get_payload(decode=True)
        payload_decoded_str: str = payload_decoded.decode("utf-8")
        return payload_decoded_str
    elif isinstance(payload, List):
        return "\n".join(
            [
                message_to_str(message)
                for message in payload
                if message.get_content_type() == "text/html"
            ]
        )
    else:
        raise ValueError(f"`payload` type is {type(payload)}")


def eml_to_html(eml_path_str: Union[str, Path]) -> Path:
    eml_path: Path = Path(eml_path_str)
    if not eml_path.is_file():
        print(f"🟡 Skipping `{eml_path}`; is not a file")

    if eml_path.suffix != ".eml":
        print(f"🟡 Skipping `{eml_path}`; not an .eml file")

    html_path: Path = eml_path.with_suffix(".html")
    with eml_path.open(mode="r") as eml_file, html_path.open(
        mode="w", encoding="utf-8"
    ) as html_file:
        message: Message = message_from_file(eml_file)
        payload: str = message_to_str(message)
        html_file.write(payload)

    print(f"🟢 Written `{html_path.name}`")

    return html_path



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively process directories')
    parser.add_argument('paths', nargs='*', help='Paths to process')
    args = parser.parse_args()

    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            eml_to_html(path)
        elif path.is_dir() and args.recursive:
            for eml_path in path.rglob('*.eml'):
                eml_to_html(eml_path)



if __name__ == "__main__":
    main()
