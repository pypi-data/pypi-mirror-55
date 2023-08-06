"""
Pareto conjugate prior distribution model.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2019

import numpy as np

from scipy import integrate
from scipy import optimize
from scipy import stats

from .base import BayesABTest
from .base import BayesModel
from .base import BayesMVTest
from .ci import ci_interval
from .utils import check_ab_method
from .utils import check_mv_method


def probability_to_beat(a0, b0, a1, b1):
    """Closed-form probability a Pareto is greater than another."""
    r = a0 / (a0 + a1)

    if b1 > b0:
        return (b0 / b1) ** a0 * (r - 1) + 1
    else:
        return (b1 / b0) ** a1 * r


def expected_loss(a0, b0, a1, b1):
    """Closed-form expectation max(difference Pareto, 0)."""
    if b1 > b0:
        r = (b0 / b1) ** a0
        t = a1 * b1 / (a1 - 1) * (1 - r)
        q = a0 / (a0 - 1) * (b0 - b1 * r)
        s = a0 * b1 / (a0 + a1 - 1) * r / (a1 - 1)
        return t - q + s
    else:
        return a0 * b0 / (a0 + a1 - 1) * (b1 / b0) ** a1 / (a1 - 1)


def func_mv_ppf(x, variant_params, p):
    """Function CDF of max of pareto random variables for root-finding."""
    cdf = 1.0
    for (a, b) in variant_params:
        cdf *= 1 - (b / x) ** a
    return cdf - p


def func_mv_prob(x, a, b, variant_params):
    """Integrand probability integral."""
    pdf = np.exp(np.log(a) + a * np.log(b) - (a + 1) * np.log(x))
    g = np.prod([1 - (b / x) ** a for a, b in variant_params], axis=0)
    return pdf * g


def func_mv_el(x, a, b, variant_params):
    """Integrand expected loss integral."""
    n = len(variant_params)

    aa, bb = map(np.array, zip(*variant_params))

    pdf = np.exp(np.log(aa) + aa * np.log(bb) - (aa + 1) * np.log(x))

    s = np.dot(pdf, [np.prod([1 - (bb[j] / x) ** aa[j]
               for j in range(n) if j != i], axis=0) for i in range(n)])

    p = x * (1 - (b / x) ** a)
    q = a * b / (a - 1) * (1 - (b / x) ** (a - 1))
    return s * (p - q)


def func_mv_elr(x, variant_params):
    """Integrand expected loss relative integral."""
    n = len(variant_params)

    aa, bb = map(np.array, zip(*variant_params))

    pdf = np.exp(np.log(aa) + aa * np.log(bb) - (aa + 1) * np.log(x))

    s = np.dot(pdf, [np.prod([1 - (bb[j] / x) ** aa[j]
               for j in range(n) if j != i], axis=0) for i in range(n)])
    return x * s


class ParetoModel(BayesModel):
    """
    Pareto conjugate prior distribution model.

    Parameters
    ----------
    scale : float (default=0.005)
        Prior parameter scale.

    shape : float (default=0.005)
        Prior parameter shape.
    """
    def __init__(self, name="", scale=0.005, shape=0.005):
        super().__init__(name)

        self.scale = scale
        self.shape = shape

        self._scale_posterior = scale
        self._shape_posterior = shape

        if self.scale <= 0:
            raise ValueError("scale must be > 0; got {}.".format(self.scale))

        if self.shape <= 0:
            raise ValueError("shape must be > 0; got {}.".format(self.shape))

    @property
    def scale_posterior(self):
        """
        Posterior parameter scale.

        Returns
        -------
        scale : float
        """
        return self._scale_posterior

    @property
    def shape_posterior(self):
        """
        Posterior parameter shape.

        Returns
        -------
        shape : float
        """
        return self._shape_posterior

    def mean(self):
        """
        Mean of the posterior distribution.

        Returns
        -------
        mean : float
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).mean()

    def var(self):
        """
        Variance of the posterior distribution.

        Returns
        -------
        var : float
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).var()

    def std(self):
        """
        Standard deviation of the posterior distribution.

        Returns
        -------
        std : float
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).std()

    def pdf(self, x):
        """
        Probability density function of the posterior distribution.

        Parameters
        ----------
        x : array-like
            Quantiles.

        Returns
        -------
        pdf : numpy.ndarray
           Probability density function evaluated at x.
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).pdf(x)

    def cdf(self, x):
        """
        Cumulative distribution function of the posterior distribution.

        Parameters
        ----------
        x : array-like
            Quantiles.

        Returns
        -------
        cdf : numpy.ndarray
            Cumulative distribution function evaluated at x.
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).cdf(x)

    def ppf(self, q):
        """
        Percent point function (quantile) of the posterior distribution.

        Parameters
        ----------
        x : array-like
            Lower tail probability.

        Returns
        -------
        ppf : numpy.ndarray
            Quantile corresponding to the lower tail probability q.
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).ppf(q)

    def rvs(self, size=1, random_state=None):
        """
        Random variates of the posterior distribution.

        Parameters
        ----------
        size : int (default=1)
            Number of random variates.

        random_state : int or None (default=None)
            The seed used by the random number generator.

        Returns
        -------
        rvs : numpy.ndarray or scalar
            Random variates of given size.
        """
        return stats.pareto(b=self._shape_posterior,
                            scale=self._scale_posterior).rvs(
                            size=size, random_state=random_state)


class ParetoABTest(BayesABTest):
    """
    Bayesian A/B testing with prior pareto distribution.

    Parameters
    ----------
    modelA : object
        The pareto model for variant A.

    modelB : object
        The pareto model for variant B.

    simulations : int or None (default=1000000)
        Number of Monte Carlo simulations.

    random_state : int or None (default=None)
        The seed used by the random number generator.
    """
    def __init__(self, modelA, modelB, simulations=None, random_state=None):
        super().__init__(modelA, modelB, simulations, random_state)

    def probability(self, method="exact", variant="A", lift=0):
        """
        Compute the error probability or *chance to beat control*.

        * If ``variant == "A"``, :math:`P[A > B + lift]`
        * If ``variant == "B"``, :math:`P[B > A + lift]`
        * If ``variant == "all"``, both.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        variant : str (default="A")
            The chosen variant. Options are "A", "B", "all".

        lift : float (default=0.0)
           The amount of uplift.

        Returns
        -------
        probability : float or tuple of floats
        """
        check_ab_method(method=method, method_options=("exact", "MC"),
                        variant=variant, lift=lift)

        if method == "exact":
            bA = self.modelA.scale_posterior
            aA = self.modelA.shape_posterior

            bB = self.modelB.scale_posterior
            aB = self.modelB.shape_posterior

            if variant == "A":
                return probability_to_beat(aB, bB, aA, bA)
            elif variant == "B":
                return probability_to_beat(aA, bA, aB, bB)
            else:
                return (probability_to_beat(aB, bB, aA, bA),
                        probability_to_beat(aA, bA, aB, bB))
        else:
            xA = self.modelA.rvs(self.simulations, self.random_state)
            xB = self.modelB.rvs(self.simulations, self.random_state)

            if variant == "A":
                return (xA > xB + lift).mean()
            elif variant == "B":
                return (xB > xA + lift).mean()
            else:
                return (xA > xB + lift).mean(), (xB > xA + lift).mean()

    def expected_loss(self, method="exact", variant="A", lift=0):
        r"""
        Compute the expected loss. This is the expected uplift lost by choosing
        a given variant.

        * If ``variant == "A"``, :math:`\mathrm{E}[\max(B - A - lift, 0)]`
        * If ``variant == "B"``, :math:`\mathrm{E}[\max(A - B - lift, 0)]`
        * If ``variant == "all"``, both.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        variant : str (default="A")
            The chosen variant. Options are "A", "B", "all".

        lift : float (default=0.0)
            The amount of uplift.

        Returns
        -------
        expected_loss : float or tuple of floats
        """
        if method == "exact":
            bA = self.modelA.scale_posterior
            aA = self.modelA.shape_posterior

            bB = self.modelB.scale_posterior
            aB = self.modelB.shape_posterior

            if variant == "A":
                return expected_loss(aA, bA, aB, bB)
            elif variant == "B":
                return expected_loss(aB, bB, aA, bA)
            else:
                return (expected_loss(aA, bA, aB, bB),
                        expected_loss(aB, bB, aA, bA))
        else:
            xA = self.modelA.rvs(self.simulations, self.random_state)
            xB = self.modelB.rvs(self.simulations, self.random_state)

            if variant == "A":
                return np.maximum(xB - xA - lift, 0).mean()
            elif variant == "B":
                return np.maximum(xA - xB - lift, 0).mean()
            else:
                return (np.maximum(xB - xA - lift, 0).mean(),
                        np.maximum(xA - xB - lift, 0).mean())

    def expected_loss_relative(self, method="exact", variant="A"):
        r"""
        Compute expected relative loss for choosing a variant. This can be seen
        as the negative expected relative improvement or uplift.

        * If ``variant == "A"``, :math:`\mathrm{E}[(B - A) / A]`
        * If ``variant == "B"``, :math:`\mathrm{E}[(A - B) / B]`
        * If ``variant == "all"``, both.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        variant : str (default="A")
            The chosen variant. Options are "A", "B", "all".

        Returns
        -------
        expected_loss_relative : float or tuple of floats
        """
        check_ab_method(method=method, method_options=("exact", "MC"),
                        variant=variant)

        if method == "exact":
            bA = self.modelA.scale_posterior
            aA = self.modelA.shape_posterior

            bB = self.modelB.scale_posterior
            aB = self.modelB.shape_posterior

            if variant == "A":
                return aB * bB / (aB - 1) * aA / (bA * (aA + 1)) - 1
            elif variant == "B":
                return aA * bA / (aA - 1) * aB / (bB * (aB + 1)) - 1
            else:
                return (aB * bB / (aB - 1) * aA / (bA * (aA + 1)) - 1,
                        aA * bA / (aA - 1) * aB / (bB * (aB + 1)) - 1)
        else:
            xA = self.modelA.rvs(self.simulations, self.random_state)
            xB = self.modelB.rvs(self.simulations, self.random_state)

            if variant == "A":
                return ((xB - xA) / xA).mean()
            elif variant == "B":
                return ((xA - xB) / xB).mean()
            else:
                return (((xB - xA) / xA).mean(), ((xA - xB) / xB).mean())

    def expected_loss_ci(self, method="MC", variant="A", interval_length=0.9,
                         ci_method="ETI"):
        r"""
        Compute credible intervals on the difference distribution of
        :math:`Z = B-A` and/or :math:`Z = A-B`.

        * If ``variant == "A"``, :math:`Z = B - A`
        * If ``variant == "B"``, :math:`Z = A - B`
        * If ``variant == "all"``, both.

        Parameters
        ----------
        method : str (default="MC")
            The method of computation.

        variant : str (default="A")
            The chosen variant. Options are "A", "B", "all".

        interval_length : float (default=0.9)
            Compute ``interval_length``\% credible interval. This is a value in
            [0, 1].

        ci_method : str (default="ETI")
            Method to compute credible intervals. Supported methods are Highest
            Density interval (``method="HDI``) and Equal-tailed interval
            (``method="ETI"``). Currently, ``method="HDI`` is only available
            for ``method="MC"``.

        Returns
        -------
        expected_loss_ci : np.ndarray or tuple of np.ndarray
        """
        check_ab_method(method=method, method_options=("MC"),
                        variant=variant, interval_length=interval_length)

        xA = self.modelA.rvs(self.simulations, self.random_state)
        xB = self.modelB.rvs(self.simulations, self.random_state)

        if variant == "A":
            return ci_interval((xB - xA), interval_length, ci_method)
        elif variant == "B":
            return ci_interval((xA - xB), interval_length, ci_method)
        else:
            return (ci_interval((xB - xA), interval_length, ci_method),
                    ci_interval((xA - xB), interval_length, ci_method))

    def expected_loss_relative_ci(self, method="MC", variant="A",
                                  interval_length=0.9, ci_method="ETI"):
        r"""
        Compute credible intervals on the relative difference distribution of
        :math:`Z = (B-A)/A` and/or :math:`Z = (A-B)/B`.

        * If ``variant == "A"``, :math:`Z = (B-A)/A`
        * If ``variant == "B"``, :math:`Z = (A-B)/B`
        * If ``variant == "all"``, both.

        Parameters
        ----------
        method : str (default="MC")
            The method of computation.

        variant : str (default="A")
            The chosen variant. Options are "A", "B", "all".

        interval_length : float (default=0.9)
            Compute ``interval_length``\% credible interval. This is a value in
            [0, 1].

        ci_method : str (default="ETI")
            Method to compute credible intervals. Supported methods are Highest
            Density interval (``method="HDI``) and Equal-tailed interval
            (``method="ETI"``). Currently, ``method="HDI`` is only available
            for ``method="MC"``.

        Returns
        -------
        expected_loss_relative_ci : np.ndarray or tuple of np.ndarray
        """
        check_ab_method(method=method, method_options=("MC"),
                        variant=variant, interval_length=interval_length)

        xA = self.modelA.rvs(self.simulations, self.random_state)
        xB = self.modelB.rvs(self.simulations, self.random_state)

        if variant == "A":
            return ci_interval((xB - xA)/xA, interval_length, ci_method)
        elif variant == "B":
            return ci_interval((xA - xB)/xB, interval_length, ci_method)
        else:
            return (ci_interval((xB - xA)/xA, interval_length, ci_method),
                    ci_interval((xA - xB)/xB, interval_length, ci_method))


class ParetoMVTest(BayesMVTest):
    """
    Bayesian Multivariate testing with prior Pareto distribution.

    Parameters
    ----------
    models : object
        The gamma models.

    simulations : int or None (default=1000000)
        Number of Monte Carlo simulations.

    random_state : int or None (default=None)
        The seed used by the random number generator.
    """
    def __init__(self, models, simulations=None, random_state=None,
                 n_jobs=None):
        super().__init__(models, simulations, random_state, n_jobs)

    def probability(self, method="exact", control="A", variant="B", lift=0):
        """
        Compute the error probability or *chance to beat control*, i.e.,
        :math:`P[variant > control + lift]`.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        control : str (default="A")
            The control variant.

        variant : str (default="B")
            The tested variant.

        lift : float (default=0.0)
           The amount of uplift.

        Returns
        -------
        probability : float
        """
        check_mv_method(method=method, method_options=("exact", "MC"),
                        control=control, variant=variant,
                        variants=self.models.keys(), lift=lift)

        model_control = self.models[control]
        model_variant = self.models[variant]

        if method == "exact":
            bA = model_variant.scale_posterior
            aA = model_variant.shape_posterior

            bB = model_control.scale_posterior
            aB = model_control.shape_posterior

            return probability_to_beat(aB, bB, aA, bA)
        else:
            x0 = model_control.rvs(self.simulations, self.random_state)
            x1 = model_variant.rvs(self.simulations, self.random_state)

        return (x1 > x0 + lift).mean()

    def probability_vs_all(self, method="quad", variant="B", lift=0,
                           mlhs_samples=1000):
        r"""
        Compute the error probability or *chance to beat all* variations. For
        example, given variants "A", "B", "C" and "D", and choosing
        variant="B", we compute :math:`P[B > \max(A, C, D) + lift]`.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="MLHS")
            The method of computation. Options are "MC" (Monte Carlo),
            "MLHS" (Monte Carlo + Median Latin Hypercube Sampling) and "quad"
            (numerical integration).

        variant : str (default="B")
            The chosen variant.

        lift : float (default=0.0)
           The amount of uplift.

        mlhs_samples : int (default=1000)
            Number of samples for MLHS method.

        Returns
        -------
        probability_vs_all : float
        """
        check_mv_method(method=method, method_options=("MC", "MLHS", "quad"),
                        control=None, variant=variant,
                        variants=self.models.keys(), lift=lift)

        # exclude variant
        variants = list(self.models.keys())
        variants.remove(variant)

        if method == "MC":
            # generate samples from all models in parallel
            xvariant = self.models[variant].rvs(self.simulations,
                                                self.random_state)

            xall = [self.models[v].rvs(self.simulations, self.random_state) for
                    v in variants]
            maxall = np.maximum.reduce(xall)

            return (xvariant > maxall + lift).mean()
        elif method == "quad":
            # prepare parameters
            variant_params = [(self.models[v].shape_posterior,
                              self.models[v].scale_posterior)
                              for v in variants]

            a = self.models[variant].shape_posterior
            b = self.models[variant].scale_posterior

            m = np.max([self.models[v].scale_posterior for v in variants])
            n = self.models[variant].ppf(0.99999999)
            return integrate.quad(func=func_mv_prob, a=max(b, m), b=n, args=(
                a, b, variant_params))[0]
        else:
            r = np.arange(mlhs_samples)
            np.random.shuffle(r)
            v = (r - 0.5) / mlhs_samples
            v = v[v >= 0]
            x = self.models[variant].ppf(v)

            return np.nanmean(np.prod([self.models[v].cdf(x)
                              for v in variants], axis=0))

    def expected_loss(self, method="exact", control="A", variant="B", lift=0):
        r"""
        Compute the expected loss. This is the expected uplift lost by choosing
        a given variant, i.e., :math:`\mathrm{E}[\max(control - variant -
        lift, 0)]`.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        control : str (default="A")
            The control variant.

        variant : str (default="B")
            The tested variant.

        lift : float (default=0.0)
           The amount of uplift.

        Returns
        -------
        expected_loss : float
        """
        check_mv_method(method=method, method_options=("exact", "MC"),
                        control=control, variant=variant,
                        variants=self.models.keys(), lift=lift)

        model_control = self.models[control]
        model_variant = self.models[variant]

        if method == "exact":
            bA = model_variant.scale_posterior
            aA = model_variant.shape_posterior

            bB = model_control.scale_posterior
            aB = model_control.shape_posterior

            return expected_loss(aA, bA, aB, bB)
        else:
            x0 = model_control.rvs(self.simulations, self.random_state)
            x1 = model_variant.rvs(self.simulations, self.random_state)

            return np.maximum(x0 - x1, 0).mean()

    def expected_loss_ci(self, method="MC", control="A", variant="B",
                         interval_length=0.9, ci_method="ETI"):
        r"""
        Compute credible intervals on the difference distribution of
        :math:`Z = control-variant`.

        Parameters
        ----------
        method : str (default="MC")
            The method of computation.

        control : str (default="A")
            The control variant.

        variant : str (default="B")
            The tested variant.

        interval_length : float (default=0.9)
            Compute ``interval_length``\% credible interval. This is a value in
            [0, 1].

        ci_method : str (default="ETI")
            Method to compute credible intervals. Supported methods are Highest
            Density interval (``method="HDI``) and Equal-tailed interval
            (``method="ETI"``). Currently, ``method="HDI`` is only available
            for ``method="MC"``.

        Returns
        -------
        expected_loss_ci : np.ndarray or tuple of np.ndarray
        """
        check_mv_method(method=method, method_options=("MC"),
                        control=control, variant=variant,
                        variants=self.models.keys(),
                        interval_length=interval_length)

        model_control = self.models[control]
        model_variant = self.models[variant]

        x0 = model_control.rvs(self.simulations, self.random_state)
        x1 = model_variant.rvs(self.simulations, self.random_state)

        return ci_interval((x0 - x1), interval_length, ci_method)

    def expected_loss_relative(self, method="exact", control="A", variant="B"):
        r"""
        Compute expected relative loss for choosing a variant. This can be seen
        as the negative expected relative improvement or uplift, i.e.,
        :math:`\mathrm{E}[(control - variant) / variant]`.

        Parameters
        ----------
        method : str (default="exact")
            The method of computation. Options are "exact" and "MC".

        control : str (default="A")
            The control variant.

        variant : str (default="B")
            The tested variant.

        Returns
        -------
        expected_loss_relative : float
        """
        check_mv_method(method=method, method_options=("exact", "MC"),
                        control=control, variant=variant,
                        variants=self.models.keys())

        model_control = self.models[control]
        model_variant = self.models[variant]

        if method == "exact":
            bA = model_variant.scale_posterior
            aA = model_variant.shape_posterior

            bB = model_control.scale_posterior
            aB = model_control.shape_posterior

            return aB * bB / (aB - 1) * aA / (bA * (aA + 1)) - 1
        else:
            x0 = model_control.rvs(self.simulations, self.random_state)
            x1 = model_variant.rvs(self.simulations, self.random_state)

            return ((x0 - x1) / x1).mean()

    def expected_loss_relative_vs_all(self, method="quad", control="A",
                                      variant="B", mlhs_samples=1000):
        r"""
        Compute the expected relative loss against all variations. For example,
        given variants "A", "B", "C" and "D", and choosing variant="B",
        we compute :math:`\mathrm{E}[(\max(A, C, D) - B) / B]`.

        Parameters
        ----------
        method : str (default="MLHS")
            The method of computation. Options are "MC" (Monte Carlo),
            "MLHS" (Monte Carlo + Median Latin Hypercube Sampling) and "quad"
            (numerical integration).

        variant : str (default="B")
            The chosen variant.

        mlhs_samples : int (default=1000)
            Number of samples for MLHS method.

        Returns
        -------
        expected_loss_relative_vs_all : float
        """
        check_mv_method(method=method, method_options=("MC", "MLHS", "quad"),
                        control=None, variant=variant,
                        variants=self.models.keys())

        # exclude variant
        variants = list(self.models.keys())
        variants.remove(variant)

        if method == "MC":
            # generate samples from all models in parallel
            xvariant = self.models[variant].rvs(self.simulations,
                                                self.random_state)

            xall = [self.models[v].rvs(self.simulations, self.random_state) for
                    v in variants]
            maxall = np.maximum.reduce(xall)

            return (maxall / xvariant).mean() - 1
        else:
            if method == "quad":
                # prepare parameters
                variant_params = [(self.models[v].shape_posterior,
                                  self.models[v].scale_posterior)
                                  for v in variants]

                n = np.max([self.models[v].ppf(0.99999999) for v in variants])
                m = np.max([self.models[v].scale_posterior for v in variants])

                e_max = integrate.quad(func=func_mv_elr, a=m, b=n, args=(
                    variant_params))[0]
            else:
                e_max = self._expected_value_max_mlhs(variants, mlhs_samples)

            a = self.models[variant].shape_posterior
            b = self.models[variant].scale_posterior
            e_inv_x = a / (b * (a + 1))

            return e_max * e_inv_x - 1

    def expected_loss_relative_ci(self, method="MC", control="A", variant="B",
                                  interval_length=0.9, ci_method="ETI"):
        r"""
        Compute credible intervals on the relative difference distribution of
        :math:`Z = (control - variant) / variant`.

        Parameters
        ----------
        method : str (default="MC")
            The method of computation.

        control : str (default="A")
            The control variant.

        variant : str (default="B")
            The tested variant.

        interval_length : float (default=0.9)
            Compute ``interval_length``\% credible interval. This is a value in
            [0, 1].

        ci_method : str (default="ETI")
            Method to compute credible intervals. Supported methods are Highest
            Density interval (``method="HDI``) and Equal-tailed interval
            (``method="ETI"``). Currently, ``method="HDI`` is only available
            for ``method="MC"``.

        Returns
        -------
        expected_loss_relative_ci : np.ndarray or tuple of np.ndarray
        """
        check_mv_method(method=method, method_options=("MC"), control=control,
                        variant=variant, variants=self.models.keys(),
                        interval_length=interval_length)

        model_control = self.models[control]
        model_variant = self.models[variant]

        x0 = model_control.rvs(self.simulations, self.random_state)
        x1 = model_variant.rvs(self.simulations, self.random_state)

        return ci_interval((x0 - x1) / x1, interval_length, ci_method)

    def expected_loss_vs_all(self, method="quad", variant="B", lift=0,
                             mlhs_samples=1000):
        r"""
        Compute the expected loss against all variations. For example, given
        variants "A", "B", "C" and "D", and choosing variant="B", we compute
        :math:`\mathrm{E}[\max(\max(A, C, D) - B, 0)]`.

        If ``lift`` is positive value, the computation method must be Monte
        Carlo sampling.

        Parameters
        ----------
        method : str (default="quad")
            The method of computation. Options are "MC" (Monte Carlo),
            "MLHS" (Monte Carlo + Median Latin Hypercube Sampling) and "quad"
            (numerical integration).

        variant : str (default="B")
            The chosen variant.

        lift : float (default=0.0)
           The amount of uplift.

        mlhs_samples : int (default=1000)
            Number of samples for MLHS method.

        Returns
        -------
        expected_loss_vs_all : float
        """
        check_mv_method(method=method, method_options=("MC", "MLHS", "quad"),
                        control=None, variant=variant,
                        variants=self.models.keys(), lift=lift)

        variants = list(self.models.keys())

        if method == "MC":
            # exclude variant
            variants.remove(variant)

            # generate samples from all models in parallel
            xvariant = self.models[variant].rvs(self.simulations,
                                                self.random_state)

            xall = [self.models[v].rvs(self.simulations, self.random_state) for
                    v in variants]
            maxall = np.maximum.reduce(xall)

            return np.maximum(maxall - xvariant - lift, 0).mean()
        else:
            m = np.max([self.models[v].scale_posterior for v in variants])
            n = np.max([self.models[v].ppf(0.99999999) for v in variants])

            # exclude variant
            variants.remove(variant)

            # prepare parameters
            variant_params = [(self.models[v].shape_posterior,
                              self.models[v].scale_posterior)
                              for v in variants]

            a = self.models[variant].shape_posterior
            b = self.models[variant].scale_posterior

            if method == "quad":
                return integrate.quad(func=func_mv_el, a=m, b=n, args=(
                    a, b, variant_params))[0]
            else:
                r = np.arange(mlhs_samples)
                np.random.shuffle(r)
                v = (r - 0.5) / mlhs_samples
                v = v[v >= 0]

                # ppf of distribution of max(x0, x1, ..., xn), where x_i
                # follows a gamma distribution
                x = np.array([optimize.brentq(f=func_mv_ppf,
                             args=(variant_params, p), a=m, b=n, xtol=1e-4,
                             rtol=1e-4) for p in v])

                p = x * (1 - (b / x) ** a)
                q = a * b / (a - 1) * (1 - (b / x) ** (a - 1))
                return np.nanmean(p - q)

    def _expected_value_max_mlhs(self, variants, mlhs_samples):
        """Compute expected value of the maximum of gamma random variables."""
        r = np.arange(mlhs_samples)
        np.random.shuffle(r)
        v = (r - 0.5) / mlhs_samples
        v = v[v >= 0][..., np.newaxis]

        variant_params = [(self.models[v].shape_posterior,
                          self.models[v].scale_posterior)
                          for v in variants]

        n = len(variant_params)
        aa, bb = map(np.array, zip(*variant_params))
        cc = aa * bb / (aa - 1)

        xx = stats.pareto(b=aa - 1, scale=bb).ppf(v)

        return np.sum([cc[i] * np.prod([
                      stats.pareto(b=aa[j], scale=bb[j]).cdf(xx[:, i])
                      for j in range(n) if j != i], axis=0)
                      for i in range(n)], axis=0).mean()
