from __future__ import annotations

from itertools import chain
from numbers import Number
from typing import Generic, TypeVar, Iterable, Type, Any, Tuple, Dict, Optional, Mapping, Union

from dyndis import Self
import numpy as np

from snake_eyes.support_space import DiscreteFiniteSupportSpace, JoinedSupportSpace

try:
    from scipy import stats
except ImportError:
    stats = None

from snake_eyes.bufferer import Bufferer, ChoiceBufferer
from snake_eyes.distribution import Distribution, add, mul, div, ConstDistribution, ReciprocalDistribution, \
    SumDistribution, ProductDistribution, _maybe_parenthesise
from snake_eyes.util import prod, common_type

T = TypeVar('T')


class BufferedDistribution(Generic[T], Distribution[T]):
    """
    A generic distribution that takes a bufferer and adapts it into a distribution
    """

    def __init__(self, bufferer: Bufferer):
        self.bufferer = bufferer

    def get(self) -> T:
        return next(self.bufferer)

    def reciprocal(self):
        return ReciprocalBufferedDistribution(self)

    @add.implementor()
    def add(self, other: Self):
        return SumBufferedDistribution((self, other))

    @add.implementor()
    def add(self, other: Number):
        return SumConstBufferedDistribution(self, other)

    @add.implementor()
    def add(self, other: ConstDistribution):
        return self + other.value

    @mul.implementor()
    def mul(self, other: Self):
        return ProductBufferedDistribution((self, other))

    @mul.implementor()
    def mul(self, other: Number):
        return ProductConstBufferedDistribution(self, other)

    @mul.implementor()
    def mul(self, other: ConstDistribution):
        return self * other.value

    def get_n(self, n):
        return self.bufferer.get_n(n)


class ReciprocalBufferedDistribution(Generic[T], BufferedDistribution[T], ReciprocalDistribution):
    def __init__(self, inner: BufferedDistribution[T]):
        BufferedDistribution.__init__(self, inner.bufferer.reciprocal())
        ReciprocalDistribution.__init__(self, inner)


class SumBufferedDistribution(Generic[T], BufferedDistribution[T], SumDistribution):
    def __init__(self, parts: Iterable[BufferedDistribution[T]]):
        SumDistribution.__init__(self, parts)
        BufferedDistribution.__init__(self, sum(p.bufferer for p in self.parts))

    @add.implementor(symmetric=True)
    def add(self, other: BufferedDistribution):
        p = self.parts + (other,)
        return type(self)(p)


class SumConstBufferedDistribution(Generic[T], BufferedDistribution[T]):
    """
    A distribution that is the sum of a buffered distribution and a constant value
    """

    def __init__(self, inner: BufferedDistribution[T], const: T):
        self.inner = inner
        self.const = const
        super().__init__(inner.bufferer + const)

    def mean(self):
        m = self.inner.mean()
        if m is None:
            return None
        return m + self.const

    def variance(self):
        return self.inner.variance()

    def cumulative_density(self, k):
        return self.inner.cumulative_density(k - self.const)

    def probability(self, k):
        return self.inner.probability(k - self.const)

    def support_space(self):
        iss = self.inner.support_space()
        return iss and (iss + self.const)

    @add.implementor(symmetric=True)
    def add(self, other: BufferedDistribution):
        return (self.inner + other) + self.const

    @add.implementor(symmetric=True)
    def add(self, other: Any):
        if isinstance(other, Distribution):
            return NotImplemented
        return self.inner + (self.const + other)

    @add.implementor()
    def add(self, other):
        return (self.inner + other.inner) + (self.const + other.const)

    @add.implementor(symmetric=True)
    def add(self, other: SumBufferedDistribution):
        return (other + self.inner) + self.const

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        return self.inner * other + self.const * other

    @div.implementor()
    def truediv(self, other: Any):
        return self.inner / other + self.const / other

    def __eq__(self, other):
        return type(self) is type(other) and (self.inner, self.const) == (other.inner, other.const)

    def __str__(self):
        return f'{_maybe_parenthesise(self.inner)} + {self.const}'


class ProductBufferedDistribution(Generic[T], BufferedDistribution[T], ProductDistribution):
    def __init__(self, parts: Iterable[BufferedDistribution[T]]):
        ProductDistribution.__init__(self, parts)
        BufferedDistribution.__init__(self, prod(p.bufferer for p in self.parts))

    @mul.implementor(symmetric=True)
    def mul(self, other: BufferedDistribution):
        p = self.parts + (other,)
        return type(self)(p)


class ProductConstBufferedDistribution(Generic[T], BufferedDistribution[T]):
    """
    A distribution that is the product of a buffered distribution and a constant value
    """

    def __init__(self, inner: BufferedDistribution[T], const: T):
        self.inner = inner
        self.const = const
        super().__init__(inner.bufferer * const)

    def mean(self):
        m = self.inner.mean()
        if m is None:
            return None
        return m * self.const

    def variance(self):
        m = self.inner.variance()
        if m is None:
            return None
        return m * self.const ** 2

    def support_space(self):
        iss = self.inner.support_space()
        return iss and (iss * self.const)

    def cumulative_density(self, k):
        return self.inner.cumulative_density(k / self.const)

    def probability(self, k):
        return self.inner.probability(k / self.const)

    @mul.implementor(symmetric=True)
    def mul(self, other: BufferedDistribution):
        return (self.inner * other) * self.const

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        if isinstance(other, Distribution):
            return NotImplemented
        return self.inner * (self.const * other)

    @mul.implementor()
    def mul(self, other):
        return (self.inner * other.inner) * (self.const * other.const)

    @mul.implementor(symmetric=True)
    def mul(self, other: ProductBufferedDistribution):
        return (other * self.inner) * self.const

    def __eq__(self, other):
        return type(self) is type(other) and (self.inner, self.const) == (other.inner, other.const)

    def __str__(self):
        return f'{_maybe_parenthesise(self.inner)} * {self.const}'


class BuffererMakerDistribution(Generic[T], BufferedDistribution[T]):
    """
    A specialized bufferer distribution that makes use of already created and cached bufferers using the
     bufferer's make method.
    """

    def __init__(self, bufferer_cls: Type[Bufferer], args, kwargs=None):
        super().__init__(bufferer_cls.make(args, kwargs))
        self.args: Tuple[Tuple, Optional[Dict[str, Any]]] = (args, kwargs)

    def __repr__(self):
        args_str = self.args_str()
        args = ()
        kwargs = None
        if isinstance(args_str, Mapping):
            kwargs = args_str
        elif len(args_str) != 2 or not isinstance(args_str[1], Mapping) or not isinstance(args_str[0], Iterable):
            args = args_str
        else:
            args, kwargs = args_str

        args_str = (repr(a) for a in args)
        if kwargs:
            args_str = chain(args_str, (f'{k}={v!r}' for (k, v) in kwargs.items()))
        return type(self).__name__ + "(" + ", ".join(args_str) + ")"

    def args_str(self) -> Union[Tuple[Iterable, Optional[Mapping[str, Any]]], Iterable, Mapping[str, Any]]:
        return self.args

    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args


class ChoiceDistribution(BuffererMakerDistribution):
    """
    A discrete distribution that chooses from a numpy array as np.random.choice
    """

    def __init__(self, choices, p=None):
        choices = tuple(choices)
        if p is not None:
            p = tuple(p)
        super().__init__(ChoiceBufferer, (choices,), {'p': p})
        self.choices = choices
        self.p = p

    def mean(self):
        if self.p is not None:
            return sum(
                i * p for (i, p) in zip(self.choices, self.p)
            )
        return sum(
            i for i in self.choices
        ) / len(self.choices)

    def variance(self):
        if self.p is not None:
            return sum(
                i * p for (i, p) in zip(self.choices, self.p)
            ) - self.mean()
        return sum(
            i for i in self.choices
        ) / len(self.choices) - self.mean()

    def support_space(self):
        return DiscreteFiniteSupportSpace(self.choices)

    def cumulative_density(self, k):
        if self.p is not None:
            return np.sum(self.p[self.choices <= k])
        return np.sum(self.choices <= k) / len(self.choices)

    def probability(self, k):
        if self.p is not None:
            return np.sum(self.p[self.choices == k])
        return np.sum(self.choices == k) / len(self.choices)

    @add.implementor(symmetric=True)
    def add(self, other: Number):
        choices = [c + other for c in self.choices]
        return type(self)(choices, p=self.p)

    @mul.implementor(symmetric=True)
    def mul(self, other: Number):
        choices = [c * other for c in self.choices]
        return type(self)(choices, p=self.p)

    def reciprocal(self):
        choices = [1 / c for c in self.choices]
        return type(self)(choices, p=self.p)

    def truncate(self, min=None, max=None):
        if self.p is not None:
            choices = []
            probs = []
            prob_sum = 0
            for c, p in zip(self.choices, self.p):
                if (min is None or min <= c) and (max is None or max >= c):
                    choices.append(c)
                    probs.append(p)
                    prob_sum += p
            if not prob_sum:
                raise ValueError("can't truncate all options")
            probs = [p / prob_sum for p in probs]
            return type(self)(choices, p=probs)
        else:
            choices = []
            for c in self.choices:
                if (min is None or min <= c) and (max is None or max >= c):
                    choices.append(c)
            if not choices:
                raise ValueError("can't truncate all options")
            return type(self)(choices)


class SplitDistribution(Generic[T], Distribution[T]):
    """
    A distribution that has a chance to delegate other distributions
    """

    def __init__(self, options: Iterable[Distribution[T]], probabilites: Iterable[float]):
        self.options: Tuple[Distribution[T]] = tuple(options)
        self.probabilities = tuple(probabilites)
        self.index_distribution = ChoiceDistribution(range(len(self.options)), p=self.probabilities)

    @classmethod
    def create(cls, options: Iterable[Tuple[Any, Union[type(...), float]]], normalize=False):
        partial_total = 0
        dists = []
        probs = []
        for (d, p) in options:
            dists.append(cls.coerce(d))
            if p is ...:
                if normalize:
                    raise ValueError('cannot use normalize and ... together')
                p = 1-partial_total
            if p == 0:
                continue
            if p < 0:
                raise ValueError(f'option {d} had negative probability')
            probs.append(p)
            partial_total += p
            if not normalize and partial_total > 1:
                raise ValueError('total probabilities exceed 1')
        if normalize:
            probs = (p/partial_total for p in probs)
        return cls(dists, probs)

    def get(self):
        return self.options[self.index_distribution.get()].get()

    def get_n(self, n):
        indices = np.asanyarray(self.index_distribution.get_n(n))
        individuals = [
            np.asanyarray(option.get_n(np.sum(indices == i)))
            for (i, option) in enumerate(self.options)
        ]
        dtype = common_type(*individuals)
        ret = np.empty(shape=n, dtype=dtype)
        for i in range(len(individuals)):
            ret[indices == i] = individuals[i]
        return ret

    def mean(self):
        ret = 0
        for o, p in zip(self.options, self.probabilities):
            m = o.mean()
            if m is None:
                return None
            ret += (m * p)
        return ret

    def variance(self):
        mean = self.mean()
        if mean is None:
            return None
        ret = mean ** 2
        for p, sub_dist in zip(self.probabilities, self.options):
            subdist_mean = sub_dist.mean()
            if subdist_mean is None:
                return None
            subdist_var = sub_dist.variance()
            if subdist_var is None:
                return None
            subdist_mean_sq = subdist_var + subdist_mean ** 2
            ret += p * (subdist_mean_sq - 2 * mean * subdist_mean)

        return ret

    def support_class(self):
        ss = tuple(p.support_space() for p in self.options)
        if None in ss:
            return None
        return JoinedSupportSpace.join(ss)

    def cumulative_density(self, k):
        ret = 0
        for (o, p) in zip(self.options, self.probabilities):
            m = o.cumulative_density(k)
            if m is None:
                return None
            ret += p * m
        return ret

    def probability(self, k):
        ret = 0
        for (o, p) in zip(self.options, self.probabilities):
            m = o.probability(k)
            if m is None:
                return None
            ret += p * m
        return ret

    def __neg__(self):
        return type(self)(
            (-s for s in self.options),
            self.probabilities
        )

    def reciprocal(self):
        return type(self)(
            (s.reciprocal() for s in self.options),
            self.probabilities
        )

    @add.implementor(symmetric=True)
    def add(self, other: Any):
        return type(self)(
            (s + other for s in self.options),
            self.probabilities
        )

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        return type(self)(
            (s * other for s in self.options),
            self.probabilities
        )

    def truncate(self, min=None, max=None):
        return type(self)(
            (s.truncate(min, max) for s in self.options),
            self.probabilities
        )

    def __str__(self):
        return type(self).__name__ + '(' \
               + ", ".join(f"{p:.1%}: {_maybe_parenthesise(c)}" for (c, p) in zip(self.options, self.probabilities)) \
               + ')'

    def __eq__(self, other):
        return type(self) is type(other) \
               and set(zip(self.options, self.probabilities)) == set(zip(other.options, other.probabilites))
