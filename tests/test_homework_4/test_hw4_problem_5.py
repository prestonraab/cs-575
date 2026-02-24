from SIR_model import SIR_simulation

def test_hw4_problem5() -> None:
    # Question
    # For a population of at least 1000 and only one agent initially infections
    # select values for m, p, and gamma so that at least 40% of the population is 
    # never infectious, at least 40% of the population has recovered,
    # and no more than 10% of the population is infectious at
    # any one time. Set the simluation duration to 300.
    
    # What I expect
    minimum_population_size: int = 1000
    
    # When
    
    ## Modify these values
    m = 1       # Probability of meeting
    p = 0.15     # Transmission rate
    gamma = 0.1 # Recovery rate
    N = 1000
    s0 = N-1
    i0 = 1
    r0 = 0
    dt = 0.1
    duration = 300
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
    assert N >= minimum_population_size
    assert max(infectious_history) <= 0.1 * N 
    susceptible_history = my_simulation.S
    recovered_history = my_simulation.R
    assert recovered_history[-1] >= 0.4*N
