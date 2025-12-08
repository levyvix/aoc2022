import datetime
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]
    day_number = 0
    if len(args) == 0 or args[0] == "":
        day_number = datetime.date.today().strftime("%d").removeprefix("0")
    else:
        day_number = args[0]

    file_content = """from icecream import ic
    from pathlib import Path

    file_name = "t.in"
    """

    folder_path = Path(__file__).parent.parent / f"d{day_number}"
    if folder_path.exists():
        print("Folder already exists. Doing Nothing...")
        return
    folder_path.mkdir(parents=True, exist_ok=True)

    # create p1
    p1 = folder_path / "p1.py"
    p1.touch()
    p1.write_text(file_content)

    # create p2
    p2 = folder_path / "p2.py"
    p2.touch()
    p2.write_text(file_content)


if __name__ == "__main__":
    main()
