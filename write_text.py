import argparse
import os


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--text", default="hello world")

    args = parser.parse_args()

    print(f"{args.text}")

    # print the current working directory
    print(os.getcwd())

    # print the contents of the directory
    print(os.listdir())

    # print the contents of the directory /results
    print(os.listdir("/results"))

    # print the contents of the directory /results/frej
    print(os.listdir("/results/frej"))

    with open("/results/frej/hello.txt", "w") as f:
        f.write(args.text)


if __name__ == "__main__":
    main()
