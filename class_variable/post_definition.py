class Class1:
    @staticmethod
    def add_one(n: int) -> int:
        return n + 1


Class1.one_list = [Class1.add_one(n) for n in range(1)]

if __name__ == "__main__":
    from pprint import pprint

    print(f"dir(Class1):")
    pprint(dir(Class1), compact=True, indent=4)
    print(f"Class1.one_list: {Class1.one_list}")
