r"""
=================
globalepistasis
=================

Implements global epistasis models based on `Otwinoski et al (2018)`_.

.. contents:: Contents
   :local:
   :depth: 2

Definition of models
---------------------

The models are defined as follows. Let :math:`v` be a variant. We convert
:math:`v` into a binary representation with respect to some wildtype
sequence. This representation is a vector :math:`\mathbf{b}\left(v\right)`
with element :math:`b\left(v\right)_m` equal to 1 if the variant has mutation
:math:`m` and 0 otherwise, and :math:`m` ranging over all :math:`M` mutations
observed in the overall set of variants (so :math:`\mathbf{b}\left(v\right)`
is of length :math:`M`). Variants can be converted into this binary form
using :class:`dms_variants.binarymap.BinaryMap`.

We define a *latent effect* for each mutation :math:`m`, which we denote as
:math:`\beta_m`. The latent effects of mutations contribute additively to the
*latent phenotype*, and the latent phenotype of the wildtype sequence is
:math:`\beta_{\rm{wt}}`. So the *latent phenotype* of variant :math:`v` is:

.. math::
   :label: latent_phenotype

   \phi\left(v\right) = \beta_{\rm{wt}} +
                        \sum_{m=1}^M \beta_m b\left(v\right)_m.

The predicted *observed phenotype* :math:`p\left(v\right)` is a function of the
latent phenotype:

.. math::
   :label: observed_phenotype

   p\left(v\right) = g\left(\phi\left(v\right)\right)

where :math:`g` is the *global epistasis function*.

We define epistasis models with the following global epistasis functions:

Non-epistatic model
+++++++++++++++++++++
This model has no epistasis, so the observed phenotype is just the latent
phenotype. In other words:

.. math::
   :label: noepistasis

   g\left(x\right) = x.

This model is implemented as :class:`NoEpistasis`.

Monotonic spline epistasis model
+++++++++++++++++++++++++++++++++
This is the model used in `Otwinoski et al (2018)`_. It transforms
the latent phenotype to the observed phenotype using monotonic I-splines with
linear extrapolation outside the spline boundaries:

.. math::
   :label: monotonicspline

   g\left(x\right)
   =
   \begin{cases}
   c_{\alpha} + \sum_{m=1}^M \alpha_{m} I_m\left(x\right)
     & \rm{if\;} L \le x \le U, \\
   c_{\alpha} + \sum_{m=1}^M \alpha_m
     \left[I_m\left(L\right) + \left(x - L\right)
           \left.\frac{\partial I_m\left(y\right)}
                      {\partial y}\right\rvert_{y=L}
     \right]
     & \rm{if\;} x < L, \\
   c_{\alpha} + \sum_{m=1}^M \alpha_m
     \left[I_m\left(U\right) + \left(x - U\right)
           \left.\frac{\partial I_m\left(y\right)}
                      {\partial y}\right\rvert_{y=U}
     \right]
     & \rm{if\;} x > U,
   \end{cases}

where :math:`c_{\alpha}` is an arbitrary number giving the *minimum*
observed phenotype, the :math:`\alpha_m` coefficients are all :math:`\ge 0`,
:math:`I_m` indicates a family of I-splines defined via
:class:`dms_variants.ispline.Isplines_total`, and :math:`L` and :math:`U` are
the lower and upper bounds on the regions over which the I-splines are defined.
Note how when :math:`x` is outside the range of the I-splines, we linearly
extrapolate :math:`g` from its range boundaries to calculate.

This model is implemented as :class:`MonotonicSplineEpistasis`. By default,
the I-splines are of order 3 and are defined on a mesh of four evenly spaced
points such that the total number of I-splines is :math:`M=5` (although these
options can be adjusted when initializing a :class:`MonotonicSplineEpistasis`
model).

The latent effects are scaled so that their mean absolute value is one,
and the latent phenotype of the wildtype is set to zero.

Fitting of models
-------------------
For each variant :math:`v`, we have an experimentally measured functional
score :math:`y_v` and optionally an estimate of the error (variance)
:math:`\sigma^2_{y_v}` in this functional score measurement. If no error
estimates are available, then we set :math:`\sigma^2_{y_v} = 0`.

The goal of the fitting is to parameterize the model so the observed phenotype
:math:`p\left(v\right)` predicted by the model is as close as possible to the
measured functional score :math:`y_v`. Following `Otwinoski et al (2018)`_,
we assume the likelihood of measuring a functional score :math:`y_v` is
normally distributed around the model prediction :math:`p\left(v\right)`
with variance :math:`\sigma^2_{y_v} + \sigma^2_{\rm{HOC}}`, where
:math:`\sigma^2_{\rm{HOC}}` is the un-modeled *house-of-cards epistasis*
(although in practice it could also represent experimental noise not
capture in the variance estimates). So the overall log likelihood of
the model is

.. math::
   :label: loglik

   \mathcal{L} = \sum_{v=1}^V \ln\left[N\left(y_v \mid p\left(v\right),
                 \sigma^2_{y_v} + \sigma^2_{\rm{HOC}}\right)\right]

where :math:`V` is the number of variants and :math:`N` is the normal
distribution defined by

.. math::
   :label: normaldist

   N\left(y \mid \mu, \sigma^2\right) = \frac{1}{\sqrt{2 \pi \sigma^2}} \exp
                    \left(-\frac{\left(y - \mu\right)^2}{2 \sigma^2}\right).

To fit the model, we maximize the log likelihood in Eq. :eq:`loglik` with
respect to all model parameters: the latent effects :math:`\beta_m` of all
mutations, the latent phenotype :math:`\beta_{\rm{wt}}` of the wildtype
sequence, the house-of-cards epistasis :math:`\sigma^2_{\rm{HOC}}`,
and any parameters that define the global epistasis function :math:`g`.

Details of fitting
-------------------------

Fitting workflow
+++++++++++++++++
The fitting workflow is essentially the same as that described in
`Otwinoski et al (2018)`_:

 1. The latent effects are fit under an additive (non-epistatic) model
    using least squares.
 2. If there are any parameters in the epistasis function, they are set
    to reasonable initial values. For :class:`MonotonicSplineEpistasis`
    this involves setting the mesh to go from 0 to 1,
    setting :math:`c_{\alpha}` to the minimum functional
    score and setting the weights :math:`\alpha_m` to equal values such
    that the max of the epistasis function is the same as the maximum
    functional score.
 3. The overall model is fit by maximum likelihood.
 4. For :class:`MonotonicSplineEpistasis`, the latent effects and wildtype
    latent phenotype are rescaled so that the mean absolute value latent
    effect is one and the wildtype latent phenotype is zero.

Vector representation of :math:`\beta_{\rm{wt}}`
+++++++++++++++++++++++++++++++++++++++++++++++++
For the purposes of the optimization (and in the equations below), we change
how :math:`\beta_{\rm{wt}}` is represented to simplify the calculations.
Specifically, to the binary encoding :math:`\mathbf{b}\left(v\right)` of
each variant, we append a 1 so that the encodings are now of length
:math:`M + 1`. We then define :math:`\beta_{M + 1} = \beta_{\rm{wt}}`.
Then Eq. :eq:`latent_phenotype` can be rewritten as

.. math::
   :label: latent_phenotype_wt_vec

   \phi\left(v\right) = \sum_{m=1}^{M+1} \beta_m b\left(v\right)_m

enabling :math:`\beta_{\rm{wt}}` to just be handled like the other
:math:`\beta_m` parameters.

Optimization
++++++++++++
The optimization is performed by :meth:`AbstractEpistasis.fit`.
There are several options to that method about how to do the optimization;
by default it uses a L-BFGS-B algorithm with exact gradients
calculated as below.

Gradients
+++++++++++

For the optimization, we use the following gradients:

.. math::
   :label: dlatent_phenotype_dlatent_effect

   \frac{\partial \phi\left(v\right)}{\partial \beta_m} =
   b\left(v_m\right)

.. math::
   :label: dobserved_phenotype_dlatent_effect

   \frac{\partial p\left(v\right)}{\partial \beta_m}
   &=& \left.\frac{\partial g\left(x\right)}{\partial x}
       \right\rvert_{x = \phi\left(v\right)} \times
       \frac{\partial \phi\left(v\right)}{\partial \beta_m} \\
   &=& \left.\frac{\partial g\left(x\right)}{\partial x}
       \right\rvert_{x = \phi\left(v\right)} \times b\left(v_m\right)

.. math::
   :label: dnormaldist_dmu

   \frac{\partial \ln\left[N\left(y \mid \mu, \sigma^2\right)\right]}
        {\partial \mu} =
   \frac{y - \mu}{\sigma^2}

.. math::
   :label: dloglik_dlatent_effect

   \frac{\partial \mathcal{L}}{\partial \beta_m}
   &=& \sum_{v=1}^V \frac{\partial \ln\left[N\left(y_v \mid p\left(v\right),
                          \sigma_{y_v}^2 + \sigma^2_{\rm{HOC}}\right)\right]}
                         {\partial p\left(v\right)} \times
                    \frac{\partial p\left(v\right)}{\partial \beta_m} \\
   &=& \sum_{v=1}^V \frac{y_v - p\left(v\right)}
                         {\sigma_{y_v}^2 + \sigma^2_{\rm{HOC}}} \times
                    \frac{\partial p\left(v\right)}{\partial \beta_m}

.. math::
   :label: dnormaldist_dsigma2

   \frac{\partial \ln\left[N\left(y \mid \mu, \sigma^2\right)\right]}
        {\partial \sigma^2} = \frac{1}{2}\left[\left(\frac{y - \mu}{\sigma^2}
                                                     \right)^2 -
                                              \frac{1}{\sigma^2}\right]

.. math::
   :label: dloglik_depistasis_HOC

   \frac{\partial \mathcal{L}}{\partial \sigma^2_{\rm{HOC}}} = \sum_{v=1}^V
   \frac{1}{2} \left[\left(\frac{y_v - p\left(v\right)}
                                {\sigma_{y_v}^2 + \sigma_{\rm{HOC}}^2}\right)^2
                     - \frac{1}{\sigma_{y_v}^2 + \sigma_{\rm{HOC}}^2} \right]

For derivatives of log likelihood with respect to the parameters of
:math:`g` as defined in Eq. :eq:`monotonicspline`:

.. math::

   \frac{g\left(x\right)}{\partial c_{\alpha}} = 1

.. math::

   \frac{g\left(x\right)}{\partial \alpha_m} = I_m\left(x\right)

.. math::
   :label: dloglik_dcalpha

   \frac{\mathcal{L}}{\partial c_{\alpha}}
   &=&
   \frac{\mathcal{L}}{\partial p\left(v\right)}
   \frac{\partial p\left(v\right)}{\partial c_{\alpha}} \\
   &=& \sum_{v=1}^V \frac{y_v - p\left(v\right)}
                         {\sigma_{y_v}^2 + \sigma^2_{\rm{HOC}}}

.. math::
   :label: dloglik_dalpham

   \frac{\mathcal{L}}{\partial \alpha_m}
   &=&
   \frac{\mathcal{L}}{\partial p\left(v\right)}
   \frac{\partial p\left(v\right)}{\partial \alpha_m} \\
   &=& \sum_{v=1}^V \frac{y_v - p\left(v\right)}
                         {\sigma_{y_v}^2 + \sigma^2_{\rm{HOC}}}
       I_m\left(\phi\left(v\right)\right)


API implementing models
--------------------------

.. _`Otwinoski et al (2018)`: https://www.pnas.org/content/115/32/E7550

"""


import abc
import collections

import numpy

import pandas as pd

import scipy.optimize
import scipy.sparse
import scipy.stats

import dms_variants.ispline


class EpistasisFittingError(Exception):
    """Error fitting an epistasis model."""

    pass


class AbstractEpistasis(abc.ABC):
    """Abstract base class for epistasis models.

    Parameters
    ----------
    binarymap : :class:`dms_variants.binarymap.BinaryMap`
        Contains the variants, their functional scores, and score variances.

    Note
    ----
    This is an abstract base class. It implements most of the epistasis model
    functionality, but does not define the actual functional form of
    the global epistasis function :meth:`AbstractEpistasis.epistasis_func`.

    """

    _NEARLY_ZERO = 1e-8
    """float: lower bound for parameters that should be > 0."""

    def __init__(self,
                 binarymap,
                 ):
        """See main class docstring."""
        self._binarymap = binarymap
        self._nlatent = self.binarymap.binarylength  # number latent effects
        self._cache = {}  # cache computed values

        # initialize params
        self._latenteffects = numpy.zeros(self._nlatent + 1, dtype='float')
        self.epistasis_HOC = 1.0
        self._epistasis_func_params = self._init_epistasis_func_params

    # ------------------------------------------------------------------------
    # Methods / properties to set and get model parameters that are fit.
    # The setters must clear appropriate elements from the cache.
    # ------------------------------------------------------------------------
    @property
    def _latenteffects(self):
        r"""numpy.ndarray: Latent effects of mutations and wildtype.

        The :math:`\beta_m` values followed by :math:`\beta_{\rm{wt}}` for
        the representation in Eq. :eq:`latent_phenotype_wt_vec`.

        """
        return self._latenteffects_val

    @_latenteffects.setter
    def _latenteffects(self, val):
        if not (isinstance(val, numpy.ndarray) and
                len(val) == self._nlatent + 1):
            raise ValueError(f"invalid value for `_latenteffects`: {val}")
        if (not hasattr(self, '_latenteffects_val')) or (self._latenteffects
                                                         != val).any():
            self._cache = {}
            self._latenteffects_val = val.copy()
            self._latenteffects_val.flags.writeable = False

    @property
    def epistasis_HOC(self):
        r"""float: House of cards epistasis, :math:`\sigma^2_{\rm{HOC}}`."""
        return self._epistasis_HOC_val

    @epistasis_HOC.setter
    def epistasis_HOC(self, val):
        if val <= 0:
            raise ValueError(f"`epistasis_HOC` must be > 0: {val}")
        if (not hasattr(self, '_epistasis_HOC_val')) or (val !=
                                                         self.epistasis_HOC):
            for key in list(self._cache.keys()):
                if key not in {'_latent_phenotypes', '_observed_phenotypes',
                               '_dobserved_phenotype_dlatent',
                               '_isplines_total'}:
                    del self._cache[key]
            self._epistasis_HOC_val = val

    @property
    def _epistasis_func_params(self):
        """numpy.ndarray: :meth:`AbstractEpistasis.epistasis_func` params."""
        return self._epistasis_func_params_val

    @_epistasis_func_params.setter
    def _epistasis_func_params(self, val):
        if len(val) != len(self._epistasis_func_param_names):
            raise ValueError('invalid length for `_epistasis_func_params`')
        if ((not hasattr(self, '_epistasis_func_params_val')) or
                (val != self._epistasis_func_params).any()):
            for key in list(self._cache.keys()):
                if key not in {'_latent_phenotypes', '_variances',
                               '_isplines_total'}:
                    del self._cache[key]
            self._epistasis_func_params_val = val.copy()
            self._epistasis_func_params_val.flags.writeable = False

    # ------------------------------------------------------------------------
    # Methods / properties to get model parameters in useful formats
    # ------------------------------------------------------------------------
    @property
    def binarymap(self):
        """:class:`dms_variants.binarymap.BinaryMap`: Variants to model.

        The binary map is set during initialization of the model.

        """
        return self._binarymap

    @property
    def _binary_variants(self):
        r"""scipy.sparse.csr.csr_matrix: Binary variants with 1 in last column.

        As in Eq. :eq:`latent_phenotype_wt_vec` with :math:`\beta_{M+1}`.
        So this is a :math:`V` by :math:`M + 1` matrix.

        """
        if not hasattr(self, '_binary_variants_val'):
            # add column as here: https://stackoverflow.com/a/41947378
            self._binary_variants_val = scipy.sparse.hstack(
                [self.binarymap.binary_variants,
                 numpy.ones(self.binarymap.nvariants, dtype='int8')[:, None],
                 ],
                format='csr',
                )
        return self._binary_variants_val

    @property
    def nparams(self):
        """int: Total number of parameters in model."""
        return (len(self._latenteffects) +  # latent effects, wt latent pheno
                1 +  # HOC epistasis
                len(self._epistasis_func_params)  # params of epistasic func
                )

    @property
    def latent_phenotype_wt(self):
        r"""float: Latent phenotype of wildtype.

        :math:`\beta_{\rm{wt}}` in Eq. :eq:`latent_phenotype`.

        """
        return self._latenteffects[self._nlatent]

    @property
    def epistasis_func_params_dict(self):
        """OrderedDict: :meth:`AbstractEpistasis.epistasis_func` param values.

        Maps names of parameters defining the global epistasis function to
        current values. These parameters are all arguments to
        :meth:`AbstractEpistasis.epistasis_func` **except** `latent_phenotype`
        (which is the function input, not a parameter defining the function).

        """
        if not self._epistasis_func_param_names:
            return collections.OrderedDict()
        assert (len(self._epistasis_func_params) ==
                len(self._epistasis_func_param_names))
        return collections.OrderedDict(zip(self._epistasis_func_param_names,
                                           self._epistasis_func_params))

    # ------------------------------------------------------------------------
    # Methods to get phenotypes / mutational effects given current model state
    # ------------------------------------------------------------------------
    def phenotypes_frombinary(self,
                              binary_variants,
                              phenotype,
                              *,
                              wt_col=False,
                              ):
        """Phenotypes from binary variant representations.

        Parameters
        ----------
        binary_variants : scipy.sparse.csr.csr_matrix or numpy.ndarray
            Binary variants in form used by
            :class:`dms_variants.binarymap.BinaryMap`.
        phenotype : {'latent', 'observed'}
            Calculate the latent or observed phenotype.
        wt_col : bool
            Set to `True` if `binary_variants` contains a terminal
            column of ones to enable calculations in the form given
            by Eq. :eq:`latent_phenotype_wt_vec`.

        Returns
        --------
        numpy.ndarray
            Latent phenotypes calculated using Eq. :eq:`latent_phenotype`.

        """
        if len(binary_variants.shape) != 2:
            raise ValueError(f"`binary_variants` not 2D:\n{binary_variants}")
        if binary_variants.shape[1] != self._nlatent + int(wt_col):
            raise ValueError(f"variants wrong length: {binary_variants.shape}")

        if wt_col:
            assert len(self._latenteffects) == binary_variants.shape[1]
            latent = binary_variants.dot(self._latenteffects)
        else:
            assert (len(self._latenteffects) - 1) == binary_variants.shape[1]
            latent = (binary_variants.dot(self._latenteffects[: -1]) +
                      self.latent_phenotype_wt)

        if phenotype == 'latent':
            return latent
        elif phenotype == 'observed':
            return self.epistasis_func(latent)
        else:
            return ValueError(f"invalid `phenotype` of {phenotype}")

    @property
    def latent_effects_df(self):
        """pandas.DataFrame: Latent effects of mutations.

        For each single mutation in :attr:`AbstractEpistasis.binarymap`,
        gives the current predicted latent effect of that mutation.

        """
        assert len(self.binarymap.all_subs) == len(self._latenteffects) - 1
        return pd.DataFrame({'mutation': self.binarymap.all_subs,
                             'latent_effect': self._latenteffects[: -1]})

    def add_phenotypes_to_df(self,
                             df,
                             *,
                             substitutions_col=None,
                             latent_phenotype_col='latent_phenotype',
                             observed_phenotype_col='observed_phenotype',
                             phenotype_col_overwrite=False,
                             unknown_as_nan=False,
                             ):
        """Add predicted phenotypes to data frame of variants.

        Parameters
        ----------
        df : pandas.DataFrame
            Data frame containing variants.
        substitutions_col : str or None
            Column in `df` giving variants as substitution strings in format
            that can be processed by :attr:`AbstractEpistasis.binarymap`.
            If `None`, defaults to the `substitutions_col` attribute of
            that binary map.
        latent_phenotype_col : str
            Column added to `df` containing predicted latent phenotypes.
        observed_phenotype_col : str
            Column added to `df` containing predicted observed phenotypes.
        phenotype_col_overwrite : bool
            If the specified latent or observed phenotype column already
            exist in `df`, overwrite it? If `False`, raise an error.
        unknown_as_nan : bool
            If some of the substitutions in a variant are not present in
            the model (not in :attr:`AbstractEpistasis.binarymap`) set the
            phenotypes to `nan` (not a number)? If `False`, raise an error.

        Returns
        -------
        pandas.DataFrame
            A copy of `df` with the phenotypes added. Phenotypes are predicted
            based on the current state of the model.

        """
        if substitutions_col is None:
            substitutions_col = self.binarymap.substitutions_col
        if substitutions_col not in df.columns:
            raise ValueError('`df` lacks `substitutions_col` '
                             f"{substitutions_col}")
        if 3 != len({substitutions_col, latent_phenotype_col,
                     observed_phenotype_col}):
            raise ValueError('repeated name among `latent_phenotype_col`, '
                             '`observed_phenotype_col`, `substitutions_col`')
        for col in [latent_phenotype_col, observed_phenotype_col]:
            if col in df.columns and not phenotype_col_overwrite:
                if not phenotype_col_overwrite:
                    raise ValueError(f"`df` already contains column {col}")

        # build binary variants as csr matrix
        row_ind = []  # row indices of elements that are one
        col_ind = []  # column indices of elements that are one
        nan_variant_indices = []  # indices of variants that are nan
        for ivariant, subs in enumerate(df[substitutions_col].values):
            try:
                for isub in self.binarymap.sub_str_to_indices(subs):
                    row_ind.append(ivariant)
                    col_ind.append(isub)
            except ValueError:
                if unknown_as_nan:
                    nan_variant_indices.append(ivariant)
                else:
                    raise ValueError('Variant has substitutions not in model:'
                                     f"\n{subs}\nMaybe use `unknown_as_nan`?")
        binary_variants = scipy.sparse.csr_matrix(
                            (numpy.ones(len(row_ind), dtype='int8'),
                             (row_ind, col_ind)),
                            shape=(len(df), self.binarymap.binarylength),
                            dtype='int8')

        df = df.copy()
        for col, phenotype in [(latent_phenotype_col, 'latent'),
                               (observed_phenotype_col, 'observed')]:
            vals = self.phenotypes_frombinary(binary_variants, phenotype)
            assert len(vals) == len(df)
            vals = vals.copy()  # needed because vals not might be writable
            vals[nan_variant_indices] = numpy.nan
            df[col] = vals
        return df

    @property
    def phenotypes_df(self):
        """pandas.DataFrame: Phenotypes of variants used to fit model.

        For each variant in :attr:`AbstractEpistasis.binarymap`, gives
        the current predicted latent and observed phenotype as well
        as the functional score and its variance.

        """
        return pd.DataFrame(
                {self.binarymap.substitutions_col:
                    self.binarymap.substitution_variants,
                 'func_score': self.binarymap.func_scores,
                 'func_score_var': self.binarymap.func_scores_var,
                 'latent_phenotype': self._latent_phenotypes,
                 'observed_phenotype': self._observed_phenotypes,
                 })

    def enrichments(self, observed_phenotypes, base=2):
        r"""Calculated enrichment ratios from observed phenotypes.

        Note
        ----
        In many cases, the functional scores used to fit the model are the
        logarithm (most commonly base 2) of experimentally observed enrichments
        For example, this is how functional scores are calculated by
        :meth:`dms_variants.codonvarianttable.CodonVariantTable.func_scores`.
        In that case, the predicted enrichment value :math:`E\left(v\right)`
        for each variant :math:`v` can be computed from the observed phenotype
        :math:`p\left(v\right)` as:

        .. math::

           E\left(v\right) = B^{p\left(v\right) - p\left(\rm{wt}\right)}

        where :math:`p\left(\rm{wt}\right)` is the observed phenotype
        of wildtype, and :math:`B` is the base for the exponent (by default
        :math:`B = 2`).

        Parameters
        ----------
        observed_phenotypes : float or numpy.ndarray
            The observed phenotypes.
        base : float
            The base for the exponent used to convert observed phenotypes
            to enrichments.

        Returns
        -------
        float or numpy.ndarray
            The enrichments.

        """
        observed_phenotype_wt = float(self.epistasis_func(
                numpy.array([self.latent_phenotype_wt])))
        return base**(observed_phenotypes - observed_phenotype_wt)

    # ------------------------------------------------------------------------
    # Methods / properties used for model fitting. Many of these are properties
    # that store the current state for the variants we are fitting, using the
    # cache so that they don't have to be re-computed needlessly.
    # ------------------------------------------------------------------------
    def fit(self, *, use_grad=True, optimize_method='L-BFGS-B', ftol=1e-7):
        """Fit all model params to maximum likelihood values.

        Parameters
        ----------
        use_grad : bool
            Use analytical gradients to help with fitting.
        optimize_method : {'L-BFGS-B', 'TNC'}
            Optimization method used by `scipy.optimize.minimize`.
        ftol : float
            Function convergence tolerance for optimization, used by
            `scipy.optimize.minimize`.

        Returns
        -------
        scipy.optimize.OptimizeResult
            The results of optimizing the full model.

        """
        # least squares fit of latent effects for reasonable initial values
        self._fit_latent_leastsquares()

        # prescale parameters to desired range
        self._prescale_params()

        # optimize full model by maximum likelihood
        optres = scipy.optimize.minimize(
                        fun=self._loglik_by_allparams,
                        jac=self._dloglik_by_allparams if use_grad else None,
                        x0=self._allparams,
                        method=optimize_method,
                        bounds=self._allparams_bounds,
                        options={'ftol': ftol},
                        )
        if not optres.success:
            raise EpistasisFittingError(
                    f"Fitting of {self.__class__.__name__} failed after "
                    f"{optres.nit} iterations. Message:\n{optres.message}\n"
                    f"{optres}")
        self._allparams = optres.x

        # postscale parameters to desired range
        self._postscale_params()

        return optres

    @property
    def loglik(self):
        """float: Current log likelihood as defined in Eq. :eq:`loglik`."""
        key = 'loglik'
        if key not in self._cache:
            self._cache[key] = self._loglik_by_variant.sum()
        return self._cache[key]

    def _loglik_by_allparams(self, allparams, negative=True):
        """(Negative) log likelihood after setting all parameters.

        Note
        ----
        Calling this method alters the interal model parameters, so only
        use if you understand what you are doing.

        Parameters
        ----------
        allparams : numpy.ndarray
            Parameters used to set :meth:`AbstractEpistasis._allparams`.
        negative : bool
            Return negative log likelihood. Useful if using a minimizer to
            optimize.

        Returns
        -------
        float
            (Negative) log likelihood after setting parameters to `allparams`.

        """
        self._allparams = allparams
        if negative:
            return -self.loglik
        else:
            return self.loglik

    def _loglik_by_epistasis_func_params(self, epistasis_func_params,
                                         negative=True):
        """(Negative) log likelihood after setting epistasis func params.

        Note
        ----
        Calling this method alters the interal model parameters, so only
        use if you understand what you are doing.

        Parameters
        ----------
        epistasis_func_params : numpy.ndarray
            Used to set :meth:`AbstractEpistasis._epistasis_func_params`.
        negative : bool
            Return negative log likelihood. Useful if using a minimizer to
            optimize.

        Returns
        -------
        float
            (Negative) log likelihood after setting epistasis func params
            to `epistasis_func_params`.

        """
        self._epistasis_func_params = epistasis_func_params
        if negative:
            return -self.loglik
        else:
            return self.loglik

    def _dloglik_by_allparams(self, allparams, negative=True):
        """(Negative) derivative of log likelihood with respect to all params.

        Note
        ----
        Calling this method alters the interal model parameters, so only
        use if you understand what you are doing.

        Parameters
        ----------
        allparams: numpy.ndarray
            Parameters used to set :meth:`AbstractEpistasis._allparams`.
        negative : bool
            Return negative log likelihood. Useful if using a minimizer to
            optimize.

        Returns
        --------
        numpy.ndarray
            (Negative) derivative of log likelihood with respect to
            :meth:`AbstractEpistasis._allparams`.

        """
        self._allparams = allparams
        val = numpy.concatenate((self._dloglik_dlatent,
                                 [self._dloglik_depistasis_HOC],
                                 self._dloglik_depistasis_func_params,
                                 )
                                )
        assert val.shape == (self.nparams,)
        if negative:
            return -val
        else:
            return val

    def _dloglik_by_epistasis_func_params(self, epistasis_func_params,
                                          negative=True):
        """(Negative) derivative of log likelihood by epistasis func params.

        Note
        ----
        Calling this method alters the interal model parameters, so only
        use if you understand what you are doing.

        Parameters
        ----------
        epistasis_func_params : numpy.ndarray
            Used to set :meth:`AbstractEpistasis._epistasis_func_params`.
        negative : bool
            Return negative log likelihood. Useful if using a minimizer to
            optimize.

        Returns
        --------
        numpy.ndarray
            (Negative) derivative of log likelihood with respect to
            :meth:`AbstractEpistasis._epistasis_func_params`.

        """
        self._epistasis_func_params = epistasis_func_params
        if negative:
            return -self._dloglik_depistasis_func_params
        else:
            return self._dloglik_depistasis_func_params

    @property
    def _allparams(self):
        """numpy.ndarray: All model parameters in a single array.

        Note
        ----
        This property should only be used for purposes in which it is
        necessary to get or set all params in a single vector (typically
        for model optimiziation), **not** to access the values of specific
        parameters, since the order of parameters in the array may change
        in future implementations.

        """
        val = numpy.concatenate((self._latenteffects,
                                 [self.epistasis_HOC],
                                 self._epistasis_func_params,
                                 )
                                )
        assert val.shape == (self.nparams,)
        return val

    @_allparams.setter
    def _allparams(self, val):
        if val.shape != (self.nparams,):
            raise ValueError(f"invalid `_allparams`: {val}")
        self._latenteffects = val[: len(self._latenteffects)]
        self.epistasis_HOC = val[len(self._latenteffects)]
        if len(self._epistasis_func_params):
            self._epistasis_func_params = val[len(self._latenteffects) + 1:]

    @property
    def _allparams_bounds(self):
        """list: Bounds for :meth:`AbstractEpistasis._allparams`.

        Can be passed to `scipy.optimize.minimize`.

        """
        bounds = ([(None, None)] * len(self._latenteffects) +
                  [(self._NEARLY_ZERO, None)] +  # HOC epistasis must be > 0
                  self._epistasis_func_param_bounds
                  )
        assert len(bounds) == len(self._allparams)
        return bounds

    @property
    def _loglik_by_variant(self):
        """numpy.ndarray: Log likelihoods per variant (Eq. :eq:`loglik`)."""
        key = '_loglik_by_variant'
        if key not in self._cache:
            standard_devs = numpy.sqrt(self._variances)
            if not (standard_devs > 0).all():
                raise ValueError('standard deviations not all > 0')
            self._cache[key] = scipy.stats.norm.logpdf(
                                    self.binarymap.func_scores,
                                    loc=self._observed_phenotypes,
                                    scale=standard_devs)
        return self._cache[key]

    @property
    def _latent_phenotypes(self):
        """numpy.ndarray: Latent phenotypes, Eq. :eq:`latent_phenotype`."""
        key = '_latent_phenotypes'
        if key not in self._cache:
            self._cache[key] = self.phenotypes_frombinary(
                                binary_variants=self._binary_variants,
                                phenotype='latent',
                                wt_col=True,
                                )
        return self._cache[key]

    @property
    def _observed_phenotypes(self):
        """numpy.ndarray: Observed phenotypes, Eq. :eq:`observed_phenotype`."""
        key = '_observed_phenotypes'
        if key not in self._cache:
            self._cache[key] = self.epistasis_func(self._latent_phenotypes)
        return self._cache[key]

    @property
    def _variances(self):
        r"""numpy.ndarray: Functional score variance plus HOC epistasis.

        :math:`\sigma_{y_v}^2 + \sigma_{\rm{HOC}}^2` in Eq. :eq:`loglik`.

        """
        key = '_variances'
        if key not in self._cache:
            if self.binarymap.func_scores_var is not None:
                var = self.binarymap.func_scores_var + self.epistasis_HOC
            else:
                var = numpy.full(self.binarymap.nvariants, self.epistasis_HOC)
            if (var <= 0).any():
                raise ValueError('variance <= 0')
            self._cache[key] = var
        return self._cache[key]

    @property
    def _dobserved_phenotypes_dlatent(self):
        """scipy.parse.csr_matrix: Derivative observed pheno by latent effects.

        See Eq. :eq:`dobserved_phenotype_dlatent_effect`. This is a
        :math:`M + 1` by :math:`V` matrix.

        """
        key = '_dobserved_phenotype_dlatent'
        if key not in self._cache:
            self._cache[key] = (
                    self._binary_variants
                    .transpose()  # convert from V by M to M by V
                    .multiply(self._depistasis_func_dlatent(
                                self._latent_phenotypes))
                    )
            assert self._cache[key].shape == (self._nlatent + 1,
                                              self.binarymap.nvariants)
        return self._cache[key]

    @property
    def _func_score_minus_observed_pheno_over_variance(self):
        r"""numpy.ndarray: Scores minus observed phenotypes over variance.

        The quantity :math:`\frac{y_v - p\left(v\right)}
        {\sigma_{y_v}^2 + \sigma^2_{\rm{HOC}}}`, which appears in Eq.
        :eq:`dloglik_dlatent_effect` and :eq:`dloglik_depistasis_HOC`.

        """
        key = '_func_score_minus_observed_pheno_over_variance'
        if key not in self._cache:
            self._cache[key] = (self.binarymap.func_scores -
                                self._observed_phenotypes) / self._variances
        return self._cache[key]

    @property
    def _dloglik_dlatent(self):
        """numpy.ndarray: Derivative log likelihood by latent effects.

        See Eq. :eq:`dloglik_dlatent_effect`.

        """
        key = '_dloglik_dlatent'
        if key not in self._cache:
            self._cache[key] = self._dobserved_phenotypes_dlatent.dot(
                    self._func_score_minus_observed_pheno_over_variance)
            assert self._cache[key].shape == (self._nlatent + 1,)
        return self._cache[key]

    @property
    def _dloglik_depistasis_HOC(self):
        """float: Derivative of log likelihood by HOC epistasis.

        See Eq. :eq:`dloglik_depistasis_HOC`.

        """
        key = '_dloglik_depistasis_HOC'
        if key not in self._cache:
            self._cache[key] = (
                0.5 *
                (self._func_score_minus_observed_pheno_over_variance**2 -
                 1 / self._variances).sum()
                )
        return self._cache[key]

    def _fit_latent_leastsquares(self):
        """Fit latent effects and HOC epistasis by least squares.

        Note
        ----
        This is a useful way to quickly get "reasonable" initial values for
        `_latenteffects` and `epistasis_HOC`.

        """
        # fit by least squares
        fitres = scipy.sparse.linalg.lsqr(
                    A=self._binary_variants,
                    b=self.binarymap.func_scores,
                    x0=self._latenteffects,
                    )

        # use fit result to update latenteffects
        self._latenteffects = fitres[0]

        # estimate HOC epistasis as residuals not from func_score variance
        residuals2 = fitres[3]**2
        if self.binarymap.func_scores_var is None:
            self.epistasis_HOC = max(residuals2 / self.binarymap.nvariants,
                                     self._NEARLY_ZERO)
        else:
            self.epistasis_HOC = max((residuals2 -
                                      self.binarymap.func_scores_var.sum()
                                      ) / self.binarymap.nvariants,
                                     self._NEARLY_ZERO)

    # ------------------------------------------------------------------------
    # Abstract methods for global epistasis func, must implement in subclasses
    # ------------------------------------------------------------------------
    @abc.abstractmethod
    def epistasis_func(self, latent_phenotype):
        """Global epistasis function :math:`g` in Eq. :eq:`observed_phenotype`.

        Note
        ----
        This is an abstract method for the :class:`AbstractEpistasis` class.
        The actual functional forms for specific models are defined in
        concrete subclasses. Those concrete implementations will also have
        additional parameters used by the function.

        """
        return NotImplementedError

    @abc.abstractmethod
    def _depistasis_func_dlatent(self, latent_phenotype):
        """Get derivative of epistasis function by latent phenotype.

        Note
        ----
        This is the derivative of :meth:`AbstractEpistasis.epistasis_func`
        with respect to the latent phenotype. It is an abstract method;
        the actual functional forms for specific models are defined in
        concrete subclasses.

        """
        return NotImplementedError

    @property
    @abc.abstractmethod
    def _dloglik_depistasis_func_params(self):
        """numpy.ndarray: Derivative log likelihood by epistasis func params.

        Note
        ----
        Derivative of :meth:`AbstractEpistasis.loglik` with respect to
        :meth:`AbstractEpistasis._epistasis_func_params`. It is an abstract
        property, the actual functional forms for specific models are defined
        in concrete subclasses.

        """
        return NotImplementedError

    @property
    @abc.abstractmethod
    def _epistasis_func_param_names(self):
        """list: Names of :meth:`AbstractEpistasis.epistasis_func_params`.

        Note
        ----
        This is an abstract property; the actual bounds for specific models are
        defined in concrete subclasses.

        """
        return NotImplementedError

    @property
    @abc.abstractmethod
    def _epistasis_func_param_bounds(self):
        """list: Bounds for the epistasis function parameters.

        For each entry in :meth:`AbstractEpistasis._epistasis_func_param_names`
        a 2-tuple gives the lower and upper bound for optimization by
        `scipy.optimize.minimize`.

        Note
        ----
        This is an abstract property; the actual bounds for specific models are
        defined in concrete subclasses.

        """
        return NotImplementedError

    @property
    @abc.abstractmethod
    def _init_epistasis_func_params(self):
        """numpy.ndarray: Init :meth:`AbstractEpistasis._epistasis_func_params`

        Note
        ----
        This is an abstract property; the actual bounds for specific models are
        defined in concrete subclasses.

        """
        return NotImplementedError

    @abc.abstractmethod
    def _prescale_params(self):
        """Rescale parameters prior to the global fitting.

        Note
        ----
        This is an abstract method, the actula pre-scaling is done in concrete
        subclasses.

        """
        return NotImplementedError

    @abc.abstractmethod
    def _postscale_params(self):
        """Rescale parameters after the global fitting.

        Note
        ----
        This is an abstract method, the actula pre-scaling is done in concrete
        subclasses.

        """
        return NotImplementedError


class NoEpistasis(AbstractEpistasis):
    """Non-epistatic model.

    Note
    ----
    Model when there is no epistasis, which is when the global epistasis
    function :math:`g` is defined by Eq. :eq:`noepistasis`.

    This is a concrete subclass of :class:`AbstractEpistasis`, so see the docs
    of that abstract base class for details on most properties and methods.

    Parameters
    ----------
    binarymap : :class:`dms_variants.binarymap.BinaryMap`
        Contains the variants, their functional scores, and score variances.

    """

    def epistasis_func(self, latent_phenotype):
        """Apply :math:`g` in Eq. :eq:`noepistasis`.

        Parameters
        -----------
        latent_phenotype : numpy.ndarray
            Latent phenotype(s) of one or more variants.

        Returns
        -------
        numpy.ndarray
            Observed phenotype(s) after transforming the latent phenotypes
            using the global epistasis function.

        """
        return latent_phenotype

    def _depistasis_func_dlatent(self, latent_phenotype):
        """Get derivative of epistasis function by latent phenotype.

        Parameters
        -----------
        latent_phenotype : numpy.ndarray
            Latent phenotype(s) of one or more variants.

        Returns
        -------
        numpy.ndarray
            Derivative of :meth:`NoEpistasis.epistasis_func` with respect to
            latent phenotype evaluated at `latent_phenotype`.

        """
        return numpy.ones(latent_phenotype.shape, dtype='float')

    @property
    def _dloglik_depistasis_func_params(self):
        """numpy.ndarray: Derivative of log likelihood by epistasis fun params.

        For :class:`NoEpistasis` models, this is just an empty array as there
        are no epistasis function parameters.

        """
        assert len(self.epistasis_func_params_dict) == 0
        return numpy.array([], dtype='float')

    @property
    def _epistasis_func_param_names(self):
        """list: Epistasis function parameter names.

        For :class:`NoEpistasis`, this is just an emptly list as there are
        no epistasis function parameters.

        """
        return []

    @property
    def _epistasis_func_param_bounds(self):
        """list: Bounds for the epistasis function parameters.

        For :class:`NoEpistasis` models, this is just an empty list as
        there are no epistasis function parameters.

        """
        bounds_d = {}
        return [bounds_d[name] for name in self._epistasis_func_param_names]

    @property
    def _init_epistasis_func_params(self):
        """numpy.ndarray: Initial :meth:`NoEpistasis._epistasis_func_params`.

        For :class:`NoEpistasis` models, this is just an empty array as
        there are no epistasis function parameters.

        """
        init_d = {}
        return numpy.array([init_d[name] for name in
                            self._epistasis_func_param_names],
                           dtype='float')

    def _prescale_params(self):
        """Do nothing, as no need to prescale for :class:`NoEpistasis`."""
        pass

    def _postscale_params(self):
        """Do nothing, as no need to postscale for :class:`NoEpistasis`."""
        pass


class MonotonicSplineEpistasis(AbstractEpistasis):
    """Monotonic spline global epistasis model.

    Note
    ----
    Models global epistasis function :math:`g` via monotonic splines as
    defined in Eq. :eq:`monotonicspline`.

    This is a concrete subclass of :class:`AbstractEpistasis`, so see the docs
    of that abstract base class for details on most properties and methods.

    Parameters
    ----------
    binarymap : :class:`dms_variants.binarymap.BinaryMap`
        Contains the variants, their functional scores, and score variances.
    spline_order : int
        Order of the I-splines defining the global epistasis function.
    meshpoints : int
        Number of evenly spaced mesh points for the I-spline defining the
        global epistasis function.

    """

    def __init__(self,
                 binarymap,
                 *,
                 spline_order=3,
                 meshpoints=4,
                 ):
        """See main class docstring."""
        if not (isinstance(meshpoints, int) and meshpoints > 1):
            raise ValueError('`meshpoints` must be int > 1')
        self._mesh = numpy.linspace(0, 1, meshpoints)
        self._spline_order = spline_order
        super().__init__(binarymap)

    @property
    def _isplines_total(self):
        """:class:`dms_variants.ispline.Isplines_total`: I-splines.

        The I-spline family is defined with the current values of
        the latent phenotypes as `x`.

        """
        key = '_isplines_total'
        if key not in self._cache:
            self._cache[key] = dms_variants.ispline.Isplines_total(
                                        order=self._spline_order,
                                        mesh=self._mesh,
                                        x=self._latent_phenotypes)
        return self._cache[key]

    def epistasis_func(self, latent_phenotype):
        """Apply :math:`g` in Eq. :eq:`monotonicspline`.

        Parameters
        -----------
        latent_phenotype : numpy.ndarray
            Latent phenotype(s) of one or more variants.

        Returns
        -------
        numpy.ndarray
            Observed phenotype(s) after transforming the latent phenotypes
            using the global epistasis function.

        """
        if not isinstance(latent_phenotype, numpy.ndarray):
            raise ValueError('`latent_phenotype` not numpy array')
        if ((latent_phenotype.shape == self._latent_phenotypes.shape) and
                (latent_phenotype == self._latent_phenotypes).all()):
            return self._isplines_total.Itotal(weights=self.alpha_ms,
                                               w_lower=self.c_alpha)
        else:
            return dms_variants.ispline.Isplines_total(
                        order=self._spline_order,
                        mesh=self._mesh,
                        x=latent_phenotype).Itotal(weights=self.alpha_ms,
                                                   w_lower=self.c_alpha)

    def _depistasis_func_dlatent(self, latent_phenotype):
        """Get derivative of epistasis function by latent phenotype.

        Parameters
        -----------
        latent_phenotype : float or numpy.ndarray
            Latent phenotype(s) of one or more variants.

        Returns
        -------
        float or numpy.ndarray
            Derivative of :meth:`MonotonicSplineEpistasis.epistasis_func` with
            with respect to latent phenotype evaluated at `latent_phenotype`.

        """
        return self._isplines_total.dItotal_dx(weights=self.alpha_ms)

    @property
    def _dloglik_depistasis_func_params(self):
        r"""numpy.ndarray: Derivative of epistasis function by its params.

        Derivative of :meth:`AbstractEpistasis.loglik` with respect to
        :meth:`AbstractEpistasis._epistasis_func_params`.

        Note
        ----
        See Eqs. and :eq:`dloglik_dcalpha` and :eq:`dloglik_dalpham`.

        """
        assert self._epistasis_func_params[0] == self.c_alpha
        assert (self._epistasis_func_params[1:] == self.alpha_ms).all()
        dlog_dobs = self._func_score_minus_observed_pheno_over_variance
        dcalpha = dlog_dobs.dot(
                self._isplines_total.dItotal_dw_lower())
        dalpham = dlog_dobs.dot(
                self._isplines_total.dItotal_dweights(self.alpha_ms,
                                                      self.c_alpha))
        deriv = numpy.append(dcalpha, dalpham)
        assert deriv.shape == self._epistasis_func_params.shape
        return deriv

    @property
    def _epistasis_func_param_names(self):
        r"""list: Epistasis function parameter names.

        These are the :math:`c_{\alpha}` and :math:`\alpha_m` parameters
        in Eq. :eq:`monotonicspline`.

        """
        return ['c_alpha'] + [f"alpha_{m}" for m in
                              range(1, self._isplines_total.n + 1)]

    @property
    def _epistasis_func_param_bounds(self):
        r"""list: Bounds for the epistasis function parameters.

        There is no bound on :math:`c_{\alpha}`, and the :math:`\alpha_m`
        parameters must be > 0.

        """
        bounds_d = {'c_alpha': (None, None)}
        for m in range(1, self._isplines_total.n + 1):
            bounds_d[f"alpha_{m}"] = (self._NEARLY_ZERO, None)
        return [bounds_d[name] for name in self._epistasis_func_param_names]

    @property
    def _init_epistasis_func_params(self):
        r"""numpy.ndarray: Initial values for epistasis func parameters.

        :math:`c_{alpha}` is set to the minimum observed phenotype in the
        actual data, and all :math:`\alpha_m` values are set to
        :math:`\left[\max\left(y_v\right) - \min\left(y_v\right)\right] / M`
        so that the range of :math:`g` over 0 to 1 goes from the smallest
        to largest observed phenotype.

        """
        func_score_min = min(self.binarymap.func_scores)
        func_score_max = max(self.binarymap.func_scores)
        init_d = {'c_alpha': func_score_min}
        for m in range(1, self._isplines_total.n + 1):
            init_d[f"alpha_{m}"] = ((func_score_max - func_score_min) /
                                    self._isplines_total.n)
        return numpy.array([init_d[name] for name in
                            self._epistasis_func_param_names],
                           dtype='float')

    @property
    def c_alpha(self):
        r"""float: :math:`c_{\alpha}` in Eq. :eq:`monotonicspline`."""
        return self.epistasis_func_params_dict['c_alpha']

    @property
    def alpha_ms(self):
        r"""numpy.ndarray: :math:`\alpha_m` in Eq. :eq:`monotonicspline`."""
        return numpy.array([self.epistasis_func_params_dict[f"alpha_{m}"]
                            for m in range(1, self._isplines_total.n + 1)],
                           dtype='float')

    def _prescale_params(self):
        """Rescale latent effects so latent phenotypes are within mesh."""
        rescale_min, rescale_max = min(self._mesh), max(self._mesh)
        rescalerange = rescale_max - rescale_min
        assert rescalerange > 0
        currentrange = (self._latent_phenotypes.max() -
                        self._latent_phenotypes.min())
        if currentrange <= 0:
            raise ValueError(f"bad latent phenotype range: {currentrange}")
        # rescale so latent phenotypes span desired range
        self._latenteffects = self._latenteffects * rescalerange / currentrange
        assert numpy.allclose(
                self._latent_phenotypes.max() - self._latent_phenotypes.min(),
                rescalerange)
        # change wildtype latent phenotype so latent phenotypes have right min
        self._latenteffects = numpy.append(
                self._latenteffects[: -1],
                (self._latenteffects[-1] + rescale_min -
                 self._latent_phenotypes.min()))
        assert numpy.allclose(rescale_min, self._latent_phenotypes.min())
        assert numpy.allclose(rescale_max, self._latent_phenotypes.max())

    def _postscale_params(self):
        """Rescale parameters after global epistasis fitting.

        The parameters are re-scaled so that:
          - The mean absolute value latent effect is 1.
          - The latent phenotype of wildtype is 0.

        """
        # make mean absolute latent effect equal to one
        mean_abs_latent_effect = numpy.abs(self._latenteffects[: -1]).mean()
        if mean_abs_latent_effect == 0:
            raise ValueError('latent effects are all 0')
        oldloglik = self.loglik
        self._latenteffects = self._latenteffects / mean_abs_latent_effect
        self._mesh = self._mesh / mean_abs_latent_effect
        assert numpy.allclose(1, numpy.abs(self._latenteffects[: -1]).mean())

        # make latent phenotype of wildtype equal to 0
        self._mesh = self._mesh - self._latenteffects[-1]
        self._latenteffects = numpy.append(self._latenteffects[: -1], 0.0)
        assert (0 ==
                self.phenotypes_frombinary(numpy.zeros((1, self._nlatent)),
                                           'latent')
                ).all()

        # make sure log likelihood hasn't changed too much
        if not numpy.allclose(self.loglik, oldloglik):
            raise EpistasisFittingError('post-scaling latent effects changed '
                                        f"loglik {oldloglik} to {self.loglik}")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
