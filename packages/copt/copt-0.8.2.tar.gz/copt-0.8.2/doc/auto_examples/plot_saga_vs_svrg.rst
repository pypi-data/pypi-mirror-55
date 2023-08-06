.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_saga_vs_svrg.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_saga_vs_svrg.py:


SAGA vs SVRG
===========================================

A comparison between two variance-reduced stochastic gradient methods:
SAGA (implemented in :func:`copt.minimize_saga`) and SVRG (implemented in
:func:`copt.minimize_svrg`). The problem solved in this case is the sum of a
logistic regression and an L1 norm (sometimes referred to as sparse logistic)



.. image:: /auto_examples/images/sphx_glr_plot_saga_vs_svrg_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

      0%|          | 0/100 [00:00<?, ?it/s]    SAGA:   0%|          | 0/100 [00:00<?, ?it/s]    SAGA:   0%|          | 0/100 [00:00<?, ?it/s, tol=5.67]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=5.67]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=3.23]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=1.93]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.911]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.538]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.258]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.146]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.0786]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.0433]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.0254]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.0152]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.00925]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.0058]     SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.00354]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.00246]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.00159]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.00111]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.000722]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.000518]    SAGA:   1%|1         | 1/100 [00:00<01:25,  1.16it/s, tol=0.000328]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=0.000328]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=0.000246]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=0.000153]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=0.000112]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=7.76e-05]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=5.33e-05]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=3.79e-05]    SAGA:  20%|##        | 20/100 [00:00<00:48,  1.66it/s, tol=2.58e-05]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=1.78e-05]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=1.18e-05]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=8.51e-06]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=5.81e-06]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=4.23e-06]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=2.88e-06]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=2.02e-06]    SAGA:  20%|##        | 20/100 [00:01<00:48,  1.66it/s, tol=1.31e-06]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=1.31e-06]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=9.87e-07]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=6.8e-07]     SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=4.69e-07]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=3.4e-07]     SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=2.38e-07]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=1.65e-07]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=1.09e-07]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=7.98e-08]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=5.6e-08]     SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=3.94e-08]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=2.78e-08]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=1.96e-08]    SAGA:  35%|###5      | 35/100 [00:01<00:27,  2.36it/s, tol=1.35e-08]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=1.35e-08]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=9.65e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=6.77e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=4.92e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=3.35e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=2.46e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=1.67e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=1.19e-09]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=8.81e-10]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=5.85e-10]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=4.32e-10]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=2.98e-10]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=2.08e-10]    SAGA:  48%|####8     | 48/100 [00:01<00:15,  3.34it/s, tol=1.55e-10]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.55e-10]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.03e-10]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=7.4e-11]     SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=5.27e-11]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=3.69e-11]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=2.71e-11]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.87e-11]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.33e-11]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=9.27e-12]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=6.86e-12]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=4.53e-12]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=3.4e-12]     SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=2.25e-12]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.66e-12]    SAGA:  61%|######1   | 61/100 [00:01<00:08,  4.71it/s, tol=1.17e-12]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.17e-12]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=7.93e-13]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=6.04e-13]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=4.1e-13]     SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=2.93e-13]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=2.01e-13]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.4e-13]     SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=9.91e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=6.67e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=4.82e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=3.04e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.96e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.21e-14]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=7.27e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=3.61e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.97e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.42e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.06e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.03e-15]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=1.1e-15]     SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=9.91e-16]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=7.85e-16]    SAGA:  75%|#######5  | 75/100 [00:01<00:03,  6.63it/s, tol=9.36e-16]    SAGA:  97%|#########7| 97/100 [00:01<00:00,  9.35it/s, tol=9.36e-16]    SAGA:  97%|#########7| 97/100 [00:01<00:00,  9.35it/s, tol=8.42e-16]    SAGA:  97%|#########7| 97/100 [00:01<00:00,  9.35it/s, tol=7.54e-16]    SAGA:  97%|#########7| 97/100 [00:01<00:00,  9.35it/s, tol=6.67e-16]    SAGA: 100%|##########| 100/100 [00:01<00:00, 66.16it/s, tol=6.67e-16]





|


.. code-block:: default

    import copt as cp
    import matplotlib.pyplot as plt
    import numpy as np

    # .. construct (random) dataset ..
    n_samples, n_features = 1000, 200
    np.random.seed(0)
    X = np.random.randn(n_samples, n_features)
    y = np.random.rand(n_samples)

    # .. objective function and regularizer ..
    f = cp.utils.LogLoss(X, y)
    g = cp.utils.L1Norm(1.0 / n_samples)

    # .. callbacks to track progress ..
    cb_saga = cp.utils.Trace(lambda x: f(x) + g(x))
    cb_svrg = cp.utils.Trace(lambda x: f(x) + g(x))

    # .. run the SAGA and SVRG algorithms ..
    step_size = 1.0 / (3 * f.max_lipschitz)
    result_saga = cp.minimize_saga(
        f.partial_deriv,
        X,
        y,
        np.zeros(n_features),
        prox=g.prox_factory(n_features),
        step_size=step_size,
        callback=cb_saga,
        tol=0,
        max_iter=100,
    )

    result_svrg = cp.minimize_svrg(
        f.partial_deriv,
        X,
        y,
        np.zeros(n_features),
        prox=g.prox_factory(n_features),
        step_size=step_size,
        callback=cb_svrg,
        tol=0,
        max_iter=100,
    )


    # .. plot the result ..
    fmin = min(np.min(cb_saga.trace_fx), np.min(cb_svrg.trace_fx))
    plt.title("Comparison of full gradient optimizers")
    plt.plot(cb_saga.trace_fx - fmin, lw=4, label="SAGA")
    # .. for SVRG we multiply the number of iterations by two to ..
    # .. account for computation of the snapshot gradient ..
    plt.plot(
        2 * np.arange(len(cb_svrg.trace_fx)), cb_svrg.trace_fx - fmin, lw=4, label="SVRG"
    )
    plt.ylabel("Function suboptimality", fontweight="bold")
    plt.xlabel("number of gradient evaluations", fontweight="bold")
    plt.yscale("log")
    plt.ylim(ymin=1e-16)
    plt.xlim((0, 50))
    plt.legend()
    plt.grid()
    plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  3.669 seconds)

**Estimated memory usage:**  101 MB


.. _sphx_glr_download_auto_examples_plot_saga_vs_svrg.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_saga_vs_svrg.py <plot_saga_vs_svrg.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_saga_vs_svrg.ipynb <plot_saga_vs_svrg.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
