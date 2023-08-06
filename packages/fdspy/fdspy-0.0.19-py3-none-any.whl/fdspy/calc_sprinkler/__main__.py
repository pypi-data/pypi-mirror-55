from fdspy.lib.cibse_guide_e import _dT_d_dt, _Q, _theta_c, _U
import seaborn as sns

sns.set_style("ticks", {"axes.grid": True})


if __name__ == "__main__":
    import numpy as np

    # INPUTS
    time_start = 0
    time_step = 0.1
    time_end = 10 * 60

    alpha = 0.0117e3  # [W/s2]
    r = 5.5 / 2  # Estimation
    h = 2.8
    RTI = 50
    T_d_activation = 273.15 + 77  # [K]

    # time_end = float(input("Time end [min]: ")) * 60
    # alpha = float(input("Alpha (growth factor) [W/s2]: "))
    # r = float(input("Lateral distance between fire and sprinkler heads [m]: "))
    # h = float(input("Vertical distance between sprinkler head and floor [m]: "))
    # RTI = float(input("Sprinkler RTI: "))
    # T_d_activation = float(input("Sprinkler activation temperature [C]: ")) + 273.15

    # CONTAINERS
    time = np.arange(time_start, time_end, time_step)
    Q = time * 0
    T_g = time * 0
    T_d = time * 0

    # INITIAL CONDITIONS
    T_g[0] = 273.15
    T_d[0] = 273.15

    # CALCULATION
    # calculate heat release rate
    Q = _Q(alpha, time)
    # calculate jet speed near sprinkler
    U = _U(Q, r, h)

    # calculate temperature near sprinkler
    T_g = _theta_c(Q, r, h)

    # calculate sprinkler temperature
    iter_time = enumerate(time)
    next(iter_time)
    for i, t in iter_time:
        T_d[i] = T_d[i - 1] + _dT_d_dt(U[i], T_g[i], T_d[i - 1], RTI)

    # RE-EVALUATE FIRE FOR SUPPRESSION ACTIVATION
    Q[T_d >= T_d_activation] = -1
    T_g[T_d >= T_d_activation] = -1
    T_d[T_d >= T_d_activation] = -1
    Q[Q == -1] = np.max(Q)
    T_d[T_d == -1] = np.max(T_d)
    T_g[T_g == -1] = np.max(T_g)

    print(
        "{:25}: {:7.2f} [min]".format(
            "Sprinkler activated at", np.min(time[T_d == np.max(T_d)]) / 60.0
        )
    )
    print("{:25}: {:7.2f} [kW]".format("The maximum HRR is", np.max(Q) / 1.0e3))

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style(
        "white", {"axes.grid": True, "grid.linestyle": ":", "grid.color": "0.5"}
    )
    sns.set_context("paper")
    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(3.5, 3.5), sharex="all")
    ax1.plot(time / 60, T_g - 273.15, label="Temperature (near field)", ls="-", c="k")
    ax1.plot(time / 60, T_d - 273.15, label="Temperature (sprinkler)", ls="--", c="k")
    ax0.plot(time / 60, Q / 1e6, ls="-", c="k", label="HRR")
    # plt.figure(num=1)
    # plt.subplot(211)
    # plt.plot(time/60, Q/1e6, label='HRR')
    # plt.ylabel("Heat Release Rate [MW]")
    # plt.subplot(212)
    # plt.plot(time/60, T_g-273.15, label="Temperature (near field)")
    # plt.plot(time/60, T_d-273.15, label="Temperature (sprinkler)")
    ax1.set_xlabel("Time [min]")
    ax1.set_ylabel("Temperature [$\degree C$]")
    ax1.set_xticks(np.arange(0, 11, 1))
    ax1.legend().set_visible(True)
    ax0.set_ylabel("Heat Release Rate [MW]")
    ax0.legend().set_visible(True)

    plt.tight_layout()
    # ax1.legend().set_
    plt.show()

    print("Press any key to continue.")
