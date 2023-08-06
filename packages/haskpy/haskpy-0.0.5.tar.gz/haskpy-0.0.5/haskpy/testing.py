import hypothesis.strategies as st
import attr

from haskpy.utils import singleton



def sample_list(**kwargs):
    t = sample_any_type(**kwargs)
    return t.map(st.lists)


def types():
    from haskpy import types
    from haskpy.types import hypothesis
    return (
        types.Maybe,
        types.List,
        types.Identity,
        types.And,
        types.Or,
        types.Sum,
        types.String,
        hypothesis.HypothesisList,
        hypothesis.HypothesisInteger,
    )


@singleton
class sample_type_of():


    def __init__(self):
        self.__depth = 0
        return


    def __call__(self, f):

        def try_sample(cls):
            try:
                return f(cls)
            except AttributeError:
                return None

        if self.__depth > 3:
            return st.nothing()

        self.__depth += 1
        try:
            t = st.one_of(*filter(None, map(try_sample, types())))
        finally:
            self.__depth -= 1

        return t


def sample_type():
    return sample_type_of(lambda cls: cls.sample_type())


def sample_hashable_type():
    return sample_type_of(lambda cls: cls.sample_hashable_type())


def sample_monoid_type():
    return sample_type_of(lambda cls: cls.sample_monoid_type())


def sample_commutative_type():
    return sample_type_of(lambda cls: cls.sample_commutative_type())


@st.composite
def sample_function(draw, b):
    return memoize(lambda _: draw(b))


def sample_class(typeclass):
    return st.sampled_from(
        tuple(filter(lambda cls: issubclass(cls, typeclass), types()))
    )


@attr.s(frozen=True)
class memoize():


    __f = attr.ib()
    __memory = attr.ib(factory=list, init=False)


    def __call__(self, x):
        for (key, value) in self.__memory:
            if key == x:
                return value
        y = self.__f(x)
        self.__memory.append((x, y))
        return y
