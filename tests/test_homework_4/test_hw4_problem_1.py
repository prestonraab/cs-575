from SIR_model import SIR_simulation

def test_hw4_problem_1() -> None:
    # Question
    # For a population of at least 1000 and only one agent initially infections
    # select values for m, p, and gamma so that at the peak
    # of the epidemic more than 80% of the population is infectious
    
    # What I expect
    minimum_population_size: int = 1000
    peak_number_infectious: float = 0.8*1000

    # When
    ## Modify these values
    m = 1       # Probability of meeting
    p = 0.4     # Transmission rate
    gamma = 0.02 # Recovery rate
    N = 1000
    s0 = N-1
    i0 = 1
    r0 = 0
    dt = 0.1
    duration = 140
    my_simulation: SIR_simulation = SIR_simulation(m,
                                        p,
                                        gamma,
                                        dt,
                                        duration,
                                        s0,
                                        i0,
                                        r0)
    my_simulation.run_simulation()
    # Then
    infectious_history = my_simulation.I
    print(max(infectious_history))
    assert N >= minimum_population_size
    assert infectious_history[0] < 2
    assert max(infectious_history) > peak_number_infectious

if __name__ == "__main__":
    test_hw4_problem_1()
