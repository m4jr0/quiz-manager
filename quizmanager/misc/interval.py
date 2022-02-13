class Interval:
    __min = 0
    __max = 0

    def __repr__(self):
        return "Interval[__min: {min}, __max: {max}]".format(
            min=self.__min,
            max=self.__max,
        )

    def __str__(self):
        return "[{min}, {max}]".format(
            min=self.__min,
            max=self.__max,
        )

    def __init__(
        self,
        x=0,
        y=0,
    ):
        self.set(x, y)

    def set(
        self,
        x,
        y,
    ):
        if not isinstance(x, int):
            raise ValueError(
                "Variable should be a number: {variable}.".format(
                    variable=x,
                )
            )
        elif not isinstance(y, int):
            raise ValueError(
                "Variable should be a number: {variable}.".format(
                    variable=y,
                )
            )

        self.__min = min(x, y)
        self.__max = max(x, y)

    def contains(
        self,
        x,
    ):
        return self.__min <= x and x <= self.__max
