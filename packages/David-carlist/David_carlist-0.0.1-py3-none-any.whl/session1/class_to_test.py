from session1.functions import is_perfect_square


class ClassToTest:

    @staticmethod
    def call_perfect_square(num: int):
        return is_perfect_square(num)


print(f'Hey: {ClassToTest.call_perfect_square(4)}')

