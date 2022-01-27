class PostdefinedVariable:
    @staticmethod
    def add_one(n: int) -> int:
        return n + 1


PostdefinedVariable.one_list = [PostdefinedVariable.add_one(n) for n in range(1)]


def main() -> None:  # pragma: no cover
    from pprint import pprint

    print(f"dir(Class1):")
    pprint(dir(PostdefinedVariable), compact=True, indent=4)
    print(f"Class1.one_list: {PostdefinedVariable.one_list}")


if __name__ == "__main__":  # pragma: no cover
    main()
