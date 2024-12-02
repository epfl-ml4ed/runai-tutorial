import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--text", default="hello world")
    parser.add_argument("--output", default="hello.txt")

    args = parser.parse_args()

    print(f"{args.text}")

    with open(args.output, "w") as f:
        f.write(args.text)


if __name__ == "__main__":
    main()
