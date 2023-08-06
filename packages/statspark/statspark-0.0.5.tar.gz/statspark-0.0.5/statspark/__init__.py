
__version__ = '0.0.5'


from statspark.config import (
    get_option,
    options,
    set_option
)
from statspark.qgf import qgf
from statspark.r_inspired import (
    # classes
    Interval, Pipe,
    # functions
    add_intercept,
    additive_terms,
    csum_N_pois,
    dcast,
    determine_type,
    dist_to_point,
    dpmf,
    fft_curve,
    gauss_seidel,
    get_p_thres,
    get_response,
    hsm,
    impute_em,
    kde, kde_mult,
    logarithmic_scoring,
    npmap,
    plot_lm,
    plot_op,
    plot_qq, plot_rf, plot_rlev, plot_sl,
    produce_roc_table,
    random_word,
    rpmf
)
