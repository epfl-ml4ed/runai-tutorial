import argparse


def main():
    parser = argparse.ArgumentParser(description="Write text to a file.")

    # Add a named argument '--text'.
    parser.add_argument(
        "--text", default="hello world", help="Text to write to the file."
    )

    args = parser.parse_args()

    print(f"{args.text}")

    with open("/results/hello.txt", "w") as f:
        f.write(args.text)


if __name__ == "__main__":
    main()
