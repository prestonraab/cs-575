from SIR_model import SIR_simulation

def test_hw4_problem3() -> None:
    # Question
    # For a population of at least 1000 and at least 20% of the agents initially infections
    # select values for m, p, and gamma so that at the the end of the epidemic 
    # between 40% and 50% of the population was never infectious
    
    # What I expect
    minimum_population_size: int = 1000
    
    # When
    
    ## Modify these values
    m = 1       # Probability of meeting
    p = 0.4     # Transmission rate
    gamma = 0.4 # Recovery rate
    N = 1000
    i0 = 200
    s0 = N-i0
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
    assert N >= minimum_population_size
    assert infectious_history[0] >= 0.2*N
    susceptible_history = my_simulation.S
    print(susceptible_history[-1])
    assert susceptible_history[-1] >= 0.4*N and susceptible_history[-1] <= 0.5*N


if __name__ == "__main__":
    test_hw4_problem3()