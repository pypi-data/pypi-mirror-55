"""
################################################################################

Copyright (C) 2017-2019, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your research,
I would appreciate an acknowledgement to the use of the
"CapFit program within the pPXF Python package of Cappellari (2017),
which implements a Levenberg-Marquardt approach with the addition of
box constraints and fixed/tied variables".

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.

###############################################################################

Changelog
---------

V1.0.7: MC, Oxford, 10 October 2019
-----------------------------------

- Included complete documentation.
- Improved print formatting.
- Returns .message attribute.
- Improved xtol convergence test.
- Only accept final move if chi2 decreased.
- Strictly satisfy bounds during Jacobian computation.

V1.0.6: MC, Oxford, 11 June 2019
++++++++++++++++++++++++++++++++

- Use only free parameters for small-step convergence test.
- Explain in words convergence status when verbose != 0
- Fixed program stop when abs_step is undefined.
- Fixed capfit ignoring optional max_nfev.

V1.0.5: MC, Oxford, 28 March 2019
+++++++++++++++++++++++++++++++++

- Raise an error if the user function returns non-finite values.

V1.0.4: MC, Oxford, 30 November 2018
++++++++++++++++++++++++++++++++++++

- Allow for a scalar ``abs_step``.

V1.0.3: MC, Oxford, 20 September 2018
+++++++++++++++++++++++++++++++++++++

- Raise an error if one tries to tie parameters to themselves.
  Thanks to Kyle Westfall (Univ. Santa Cruz) for the feedback.
- Use Python 3.6 f-strings.

V1.0.2: MC, Oxford, 10 May 2018
+++++++++++++++++++++++++++++++

- Dropped legacy Python 2.7 support.

V1.0.1: MC, Oxford, 13 February 2018
++++++++++++++++++++++++++++++++++++

- Make output errors of non-free variable exactly zero.

V1.0.0: MC, Oxford, 15 June 2017
++++++++++++++++++++++++++++++++

- Written by Michele Cappellari

"""

import numpy as np
from scipy import optimize, linalg

################################################################################

def fprint(x):
    return (" {:.4g}"*len(x)).format(*x)

################################################################################

def chi2(x):
    return x @ x

################################################################################

def cov_err(jac):
    """
    Covariance and 1sigma formal errors calculation.
    See e.g. Press et al. 2007, Numerical Recipes, 3rd ed., Section 15.4.2

    """
    U, s, Vh = linalg.svd(jac, full_matrices=False)
    w = s > np.finfo(float).eps*max(jac.shape)*s[0]
    cov = (Vh[w].T/s[w]**2) @ Vh[w]
    perr = np.sqrt(np.diag(cov))

    return cov, perr

################################################################################

class capfit(object):

    """
    CapFit
    ------

    ``CapFit`` is an enhanced implementation of the nonlinear least-squares
    algorithm by Levenberg-Marquardt (LM) with the addition of a rigorous
    treatment of bound constraints. One can easily tie or fix some parameters
    without having the modify the fitting function.

    Given a function of ``n`` model parameters ``x_k`` returning the ``m``
    model residuals ``f_j(x)``, ``CapFit`` finds a local minimum of the cost
    function::

        G(x) = sum[f_j(x)^2]

        subject to:

            lb_n <= x_n <= ub_n  (bounds)
            x_k = f(x)  (tied parameters)
            x_m = a_m  (fixed parameters)

    Attribution
    -----------

    If you use this software for your research, please cite the Python package
    ``ppxf`` by `Cappellari (2017)
    <http://adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_, where this
    software was introduced. The BibTeX entry for the paper is::

        @ARTICLE{Cappellari2017,
            author = {{Cappellari}, M.},
            title = "{Improving the full spectrum fitting method:
                accurate convolution with Gauss-Hermite functions}",
            journal = {MNRAS},
            eprint = {1607.08538},
            year = 2017,
            volume = 466,
            pages = {798-811},
            doi = {10.1093/mnras/stw3020}
        }

    Usage Examples
    --------------

    .. code-block:: python

        import numpy as np
        import matplotlib.pyplot as plt

        from ppxf.capfit import capfit

        def func(p, x=None, y=None, yerr=None, a=None):
            model = p[0]*np.exp(-0.5*(x - p[1]/a)**2/p[2]**2)
            resid = (y - model)/yerr
            return resid

        a = 1.0
        np.random.seed(123)
        x = np.linspace(-3, 3, 100)
        ptrue = np.array([2., -1., 0.5])
        y = -func(ptrue, x=x, y=0, yerr=1, a=a)
        yerr = np.full_like(y, 0.1)
        y += np.random.normal(0, yerr, x.size)
        p0 = np.array([1., 1., 1.])
        kwargs = {'x': x, 'y': y, 'yerr': yerr, 'a': a}

        print("#### Unconstrained case ####")
        res = capfit(func, p0, kwargs=kwargs, verbose=1)

        print("#### Bounds on parameters ####")
        res = capfit(func, p0, kwargs=kwargs, verbose=1,
                     bounds=[(-np.inf, -0.95, 0.55), (np.inf, np.inf, np.inf)])

        print("#### Tied parameters ####")
        res = capfit(func, p0, kwargs=kwargs, tied=['', '-p[0]/2', ''], verbose=1)

        print("#### Fixed parameters ####")
        res = capfit(func, [1, 1, 0.5], kwargs=kwargs, fixed=[0, 0, 1], verbose=1)

        plt.plot(x, y, 'o')
        plt.plot(x, -func(res.x, x=x, y=0, yerr=1, a=a))

    Input Parameters
    ----------------

    fun : callable
        Function which computes the vector of residuals, with the signature
        ``fun(x, *args, **kwargs)``, i.e., the minimization proceeds with
        respect to its first argument. The argument ``x`` passed to this
        function is an 1-d darray of shape (n,).
        The function must return a 1-d array of shape (m,).
    x0 : array_like with shape (n,) or float
        Initial guess on independent variables. If float, it will be treated
        as a 1-d array with one element.
    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on independent variables. Defaults to no bounds.
        Each array must match the size of `x0` or be a scalar, in the latter
        case a bound will be the same for all variables. Use ``np.inf`` with
        an appropriate sign to disable bounds on all or some variables.
    ftol : float or None, optional
        Tolerance for termination by the change of the cost function (default
        is 1e-4). The optimization process is stopped when both
        ``prered < ftol`` and ``abs(actred) < ftol`` and additionally
        ``actred <= 2*prered``, where ``actred`` and ``prered`` are the actual
        and predicted relative changes respectively
        (as described in More' et al. 1980).
    xtol : float or None, optional
        Tolerance for termination by the change ``dx`` of the independent
        variables (default is 1e-4). The condition is
        ``norm(dx) < xtol*(xtol + norm(xs))`` where ``xs`` is the value of ``x``
        scaled according to `x_scale` parameter (see below).
        If None, the termination by this condition is disabled.
    x_scale : array_like or 'jac', optional
        Characteristic scale of each variable. Setting `x_scale` is equivalent
        to reformulating the problem in scaled variables ``xs = x/x_scale``.
        An alternative view is that the size of a trust region along j-th
        dimension is proportional to ``x_scale[j]``. Improved convergence may
        be achieved by setting `x_scale` such that a step of a given size
        along any of the scaled variables has a similar effect on the cost
        function. If set to 'jac', the scale is iteratively updated using the
        inverse norms of the columns of the Jacobian matrix (as described in
        More' et al. 1980).
    max_nfev : None or int, optional
        Maximum number of function evaluations before the termination
        (default is 100*n).
    diff_step : None, scalar or array_like, optional
        Determines the relative step size for the finite difference
        approximation of the Jacobian. The actual step is computed as
        ``diff_step*maximum(1, abs(x))`` (default=1e-4)
    abs_step : None, scalar or array_like, optional
        Determines the absolute step size for the finite difference
        approximation of the Jacobian. Default is None and ``diff_step``
        is used instead.
    tied : array_like with shape (n,), optional
        A list of string expressions. Each expression "ties" the parameter to
        other free or fixed parameters.  Any expression involving constants and
        the parameter array ``p[j]`` are permitted. Since they are totally
        constrained, tied parameters are considered to be fixed; no errors are
        computed for them.

        This is a vector with the same dimensions as ``x0``. In practice,
        for every element of ``x0`` one needs to specify either an empty string
        ``''`` implying that the parameter is free, or a string expression
        involving some of the variables ``p[j]``, where ``j`` represents the
        index of the vector of parameters. See usage example.
    verbose : {0, 1, 2}, optional
        Level of algorithm's verbosity:
            * 0 (default) : work silently.
            * 1 : display a termination report.
            * 2 : display progress during iterations.
    args, kwargs : tuple and dict, optional
        Additional arguments passed to `fun`, empty by default.
        The calling signature is ``fun(x, *args, **kwargs)``.

    Returns
    -------

    `OptimizeResult` with the following fields defined:

    x : ndarray, shape (n,)
        Solution found.
    cost : float
        Value of the cost function at the solution.
    fun : ndarray, shape (m,)
        Vector of residuals at the solution.
    jac : ndarray, shape (m, n)
        Modified Jacobian matrix at the solution, in the sense that J.T @ J
        is a Gauss-Newton approximation of the Hessian of the cost function.
    grad : ndarray, shape (m,)
        Gradient of the cost function at the solution.
    nfev : int
        Number of function evaluations done.
    njev : int or None
        Number of Jacobian evaluations done.
    status : int
        The reason for algorithm termination:
            * -1 : improper input parameters status
            *  0 : the maximum number of function evaluations is exceeded.
            *  2 : `ftol` termination condition is satisfied.
            *  3 : `xtol` termination condition is satisfied.
            *  4 : Both `ftol` and `xtol` termination conditions are satisfied.
    message : str
        Verbal description of the termination reason.
    success : bool
        True if one of the convergence criteria is satisfied (`status` > 0).

    Notes
    -----

    The present program differs from the standard Levenberg-Marquard algorithm
    as it includes bound constraints by solving a full quadratic programming
    problem at every iteration. This approach is robust and accurate, and is
    efficient when the function evaluation is at least as expensive to compute
    as the quadratic solution.

    A general textbook description of the LM algorithm *without* bounds is given in:

    - Chapter 5.2 of `Fletcher R., 1987, Practical Methods of Optimization, 2nd ed., Wiley
      <http://doi.org/10.1002/9781118723203>`_
    - Chapter 10.3 of `Nocedal J. & Wright S.J., 2006, Numerical Optimization, 2nd ed., Springer
      <http://doi.org./10.1007/978-0-387-40065-5>`_

    The original papers introducing the LM method *without* bounds are:

    - `Levenberg K., 1944, Quart. Appl. Math., 164, 2
      <https://doi.org/10.1090/qam/10666>`_
    - `Marquardt D.W., 1963, J. Soc. Indust. Appl. Math, 11, 431
      <https://doi.org/10.1137/0111030>`_

    The Jacobian scaling and convergence tests follow
    `More', J.J., Garbow, B.S. & Hillstrom, K.E. 1980, User Guide for MINPACK-1,
    Argonne National Laboratory Report ANL-80-74 <http://cds.cern.ch/record/126569>`_

    """
    def __init__(self, func, p1, abs_step=None, bounds=(-np.inf, np.inf),
                 diff_step=1e-4, fixed=None, ftol=1e-4, max_nfev=None, tied=None,
                 verbose=0, x_scale='jac', xtol=1e-4, args=(), kwargs={}):

        p1 = np.array(p1, dtype=float)  # Make copy to leave input unchanged
        bounds = np.asarray([np.resize(b, p1.size) for b in bounds])
        assert np.all(bounds[0] < bounds[1]), "Must be lower bound < upper bound"
        p1 = p1.clip(*bounds)   # Make initial guess feasible

        fixed = np.full(p1.size, False) if fixed is None else np.asarray(fixed)
        if tied is None:
            tied = np.full(p1.size, '')
        else:
            assert np.all([f'p[{j}]' not in td for j, td in enumerate(tied)]), \
                "Parameters cannot be tied to themselves"
        assert len(p1) == len(fixed) == len(tied), \
            "`x0`, `fixed` and `tied` must have the same size"

        self.nfev = self.njev = 0
        self.diff_step = diff_step
        self.abs_step = None if abs_step is None else abs_step*np.ones_like(p1)
        self.tied = np.asarray([a.strip() for a in tied])
        self.free = (np.asarray(fixed) == 0) & (self.tied == '')
        self.args = args
        self.kwargs = kwargs
        self.max_nfev = 100*self.free.sum() if max_nfev is None else max_nfev
        self.ftol = ftol
        self.xtol = xtol
        self.verbose = verbose

        f1 = self.call(func, p1)
        assert f1.ndim == 1, "The fitting function must return a vector of residuals"
        J1 = self.fdjac(func, p1, f1, bounds)
        dd = linalg.norm(J1, axis=0)
        mx = np.max(dd)
        eps = np.finfo(float).eps
        dd[dd < eps*(eps + mx)] = 1  # As More'+80
        lam = 0.01*mx**2  # 0.01*max(diag(J1.T @ J1))

        if verbose == 2:
            print(f"\nStart lam: {lam:.4g}  chi2: {chi2(f1):.4g}\nStart p:" + fprint(p1))

        while(True):

            if isinstance(x_scale, str) and x_scale == 'jac':
                dd = np.maximum(dd, linalg.norm(J1, axis=0))
            else:
                dd = np.ones_like(p1)/x_scale

            # Solve the LM system without explicitly creating J1.T @ J1
            dn = dd/np.max(dd)
            A = np.vstack([J1, np.diag(np.sqrt(lam)*dn)])
            b = np.append(-f1, np.zeros_like(p1))
            h = optimize.lsq_linear(A, b, bounds=bounds-p1, method='bvls').x

            p2 = p1 + h
            f2 = self.call(func, p2)

            # Actual versus predicted chi2 reduction
            actred = 1 - chi2(f2)/chi2(f1)
            prered = 1 - chi2(f1 + J1 @ h)/chi2(f1)
            ratio = actred/prered

            status = self.check_conv(lam, f2, p2, h, dn, actred, prered)

            if status != -1:
                if actred > 0:
                    p1, f1 = p2, f2
                if self.verbose:
                    print(f"\n{self.message}\nFinal iter: {self.njev}  "
                          f"Func calls: {self.nfev}  chi2: {chi2(f1):.4g}  "
                          f"Status: {status}\nFinal p:" + fprint(p1) + "\n")
                break

            # eq.(5.2.7) of Fletcher (1987)
            # Algorithm 4.1 in Nocedal & Wright (2006)
            if ratio < 0.25:
                lam *= 4
            elif ratio > 0.75:
                lam /= 2

            if ratio > 0.0001:  # Successful step: move on
                J2 = self.fdjac(func, p2, f2, bounds)
                p1, f1, J1 = p2, f2, J2

        self.x = p1
        self.cost = 0.5*chi2(f1)  # as in least_squares()
        self.fun = f1
        self.jac = J1
        self.grad = J1.T @ f1
        self.status = status
        self.success = status > 0
        self.cov, self.x_err = cov_err(J1)
        self.x_err[~self.free] = 0

################################################################################

    def fdjac(self, func, pars, f, bounds):

        self.njev += 1
        jac = np.zeros([f.size, pars.size])
        if self.abs_step is None:
            h = self.diff_step*np.maximum(1.0, np.abs(pars))  # as in least_squares()
        else:
            h = self.abs_step.copy()

        x = pars + h
        hits = (x < bounds[0]) | (x > bounds[1])

        # Respect bounds in finite differences
        if np.any(hits):
            dist = np.abs(bounds - pars)
            fits = np.abs(h) <= np.maximum(*dist)
            h[hits & fits] *= -1
            forward = (dist[1] >= dist[0]) & ~fits
            backward = (dist[1] < dist[0]) & ~fits
            h[forward] = dist[1, forward]
            h[backward] = -dist[0, backward]

        # Compute derivative for free parameters
        w = np.flatnonzero(self.free)
        for j in w:
            pars1 = pars.copy()
            pars1[j] += h[j]
            f1 = self.call(func, pars1)
            jac[:, j] = (f1 - f)/h[j]

        return jac

################################################################################

    def call(self, func, p):

        self.nfev += 1
        w = np.flatnonzero(self.tied != '')
        for j in w:   # loop can be empty
            exec(f'p[{j}] = {self.tied[j]}')
        resid = func(p, *self.args, **self.kwargs)
        assert np.all(np.isfinite(resid)), \
            "The fitting function returned infinite residuals"

        return resid

################################################################################

    def check_conv(self, lam, f, p, h, dn, actred, prered):

        status = -1
        if self.nfev > self.max_nfev:
            self.message = "Terminating on function evaluations count"
            status = 0

        if prered < self.ftol and abs(actred) < self.ftol and actred <= 2*prered: # (More'+80)
            self.message = "Terminating on small function variation (ftol)"
            status = 2

        if linalg.norm((dn*h)[self.free]) < self.xtol*(self.xtol + linalg.norm((dn*p)[self.free])):
            if status == 2:
                self.message = "Both ftol and xtol convergence test are satisfied"
                status = 4
            else:
                self.message = "Terminating on small step (xtol)"
                status = 3

        if self.verbose == 2:
            print(f"\niter: {self.njev}  lam: {lam:.4g}  chi2: {chi2(f):.4g}"
                  f"  ratio: {actred/prered:.4g}\np:" + fprint(p) + "\nh:" + fprint(h))

        return status

################################################################################
