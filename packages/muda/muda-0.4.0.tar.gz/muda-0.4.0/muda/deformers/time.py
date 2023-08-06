#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# CREATED:2015-02-02 10:09:43 by Brian McFee <brian.mcfee@nyu.edu>
"""Time stretching deformations"""

import pyrubberband as pyrb
import numpy as np

from ..base import BaseTransformer, _get_rng

__all__ = ["TimeStretch", "RandomTimeStretch", "LogspaceTimeStretch"]


class AbstractTimeStretch(BaseTransformer):
    """Abstract base class for time stretching

    This contains the deformation functions and
    annotation query mapping, but does not manage
    state or parameters.
    """

    def __init__(self):
        BaseTransformer.__init__(self)

        # Build the annotation mappers
        self._register(".*", self.deform_times)
        self._register("tempo", self.deform_tempo)

    @staticmethod
    def audio(mudabox, state):
        # Deform the audio and metadata
        mudabox._audio["y"] = pyrb.time_stretch(
            mudabox._audio["y"], mudabox._audio["sr"], state["rate"]
        )

    @staticmethod
    def metadata(metadata, state):
        # Deform the metadata
        metadata.duration /= state["rate"]

    @staticmethod
    def deform_tempo(annotation, state):
        # Deform a tempo annotation

        for obs in annotation.pop_data():
            annotation.append(
                time=obs.time,
                duration=obs.duration,
                confidence=obs.confidence,
                value=state["rate"] * obs.value,
            )

    @staticmethod
    def deform_times(ann, state):
        # Deform time values for all annotations.

        ann.time /= state["rate"]

        if ann.duration is not None:
            ann.duration /= state["rate"]

        for obs in ann.pop_data():
            ann.append(
                time=obs.time / state["rate"],
                duration=obs.duration / state["rate"],
                value=obs.value,
                confidence=obs.confidence,
            )


class TimeStretch(AbstractTimeStretch):
    """Static time stretching by a fixed rate

    This transformation affects the following attributes:

    - Annotations
        - all: time, duration
        - tempo: values
    - metadata
        - duration
    - Audio


    Attributes
    ----------
    rate : float or list of floats, strictly positive
        The rate at which to speedup the audio.
        - rate > 1 speeds up,
        - rate < 1 slows down.

    Examples
    --------
    >>> D = muda.deformers.TimeStretch(rate=2.0)
    >>> out_jams = list(D.transform(jam_in))

    See Also
    --------
    LogspaceTimeStretch
    RandomTimeStretch
    """

    def __init__(self, rate=1.2):
        """Time stretching"""
        AbstractTimeStretch.__init__(self)

        self.rate = np.atleast_1d(rate).flatten()
        if np.any(self.rate <= 0):
            raise ValueError("rate parameter must be strictly positive.")
        self.rate = self.rate.tolist()

    def states(self, jam):
        for rate in self.rate:
            yield dict(rate=rate)


class LogspaceTimeStretch(AbstractTimeStretch):
    """Logarithmically spaced time stretching.

    `n_samples` are generated with stretching spaced logarithmically
    between `2.0**lower` and 2`.0**upper`.

    This transformation affects the following attributes:

    - Annotations
        - all: time, duration
        - tempo: values
    - metadata
        - duration
    - Audio

    Attributes
    ----------
    n_samples : int > 0
        Number of deformations to generate

    lower : float
    upper : float > lower
        Minimum and maximum bounds on the stretch parameters

    See Also
    --------
    TimeStretch
    RandomTimeStretch
    """

    def __init__(self, n_samples=3, lower=-0.3, upper=0.3):
        AbstractTimeStretch.__init__(self)

        if upper <= lower:
            raise ValueError("upper must be strictly larger than lower")

        if n_samples <= 0:
            raise ValueError("n_samples must be strictly positive")

        self.n_samples = n_samples
        self.lower = float(lower)
        self.upper = float(upper)

    def states(self, jam):
        rates = 2.0 ** np.linspace(
            self.lower, self.upper, num=self.n_samples, endpoint=True
        )

        for rate in rates:
            yield dict(rate=rate)


class RandomTimeStretch(AbstractTimeStretch):
    """Random time stretching

    For each deformation, the rate parameter is drawn from a
    log-normal distribution with parameters `(location, scale)`

    - Annotations
        - all: time, duration
        - tempo: values
    - metadata
        - duration
    - Audio

    Attributes
    ----------
    n_samples : int > 0
        The number of samples to generate

    location : float
    scale : float > 0
        Parameters of a log-normal distribution from which
        rate parameters are sampled.

    rng : None, int, or np.random.RandomState
        The random number generator state.

        If `None`, then `np.random` is used.

        If `int`, then `rng` becomes the seed for the random state.

    See Also
    --------
    TimeStretch
    LogspaceTimeStretch
    numpy.random.lognormal
    """

    def __init__(self, n_samples=3, location=0.0, scale=1.0e-1, rng=None):

        AbstractTimeStretch.__init__(self)

        if scale <= 0:
            raise ValueError("scale parameter must be strictly positive.")

        if n_samples <= 0:
            raise ValueError("n_samples must be strictly positive")

        self.n_samples = n_samples
        self.location = location
        self.scale = scale
        self.rng = rng
        self._rng = _get_rng(rng)

    def states(self, jam):
        rates = self._rng.lognormal(
            mean=self.location, sigma=self.scale, size=self.n_samples
        )

        for rate in rates:
            yield dict(rate=rate)
