from Three_body_2D_Rick import *
from three_body_data_generator import runSimulation


def saveAndRun(config: Config):
    config.save()
    runSimulation(config, init="config", noFail = True)


def setup_periodic():
    maxRange = 20
    stepSize = 1e-4

    orbit = Config(
        name="orbit",
        range=(0, maxRange),
        step_size=stepSize,
        iterations=1,
        initial_x=[0, 1, -1],
        initial_y=[0, 0, 0],
        initial_vx=[0, 0, 0],
        initial_vy=[0, 1, -1],
    )

    # http://three-body.ipb.ac.rs/sol.php?id=1
    figure8 = Config(
        name="figure8",
        range=(0, maxRange),
        step_size=stepSize,
        iterations=1,
        initial_x=[-0.97000436, 0, 0.97000436],
        initial_y=[0.24308753, 0, -0.24308753],
        initial_vx=[0.4662036850, -0.93240737, 0.4662036850],
        initial_vy=[0.4323657300, -0.86473146, 0.4323657300],
    )

    # Warning: Unstable
    # http://three-body.ipb.ac.rs/bsol.php?id=16
    BrouckeR1 = Config(
        name="BrouckeR1",
        range=(0, maxRange),
        step_size=stepSize,
        iterations=1,
        initial_x=[0.8083106230, -0.4954148566, -0.3128957664],
        initial_y=[0, 0, 0],
        initial_vx=[0, 0, 0],
        initial_vy=[0.9901979166, -2.7171431768, 1.7269452602],
    )

    # http://three-body.ipb.ac.rs/bsol.php?id=21
    BrouckeR6 = Config(
        name="BrouckeR6",
        range=(0, maxRange),
        step_size=stepSize,
        iterations=1,
        initial_x=[0.8469642946, -0.5727221998, -0.2742420948],
        initial_y=[0, 0, 0],
        initial_vx=[0, 0, 0],
        initial_vy=[1.0275065708, -1.8209307202, 0.7934241494],
    )

    # http://three-body.ipb.ac.rs/bsol.php?id=6
    BrouckeA7 = Config(
        name="BrouckeA7",
        range=(0, maxRange),
        step_size=stepSize,
        iterations=1,
        initial_x=[-0.1095519101, 1.6613533905, -1.5518014804],
        initial_y=[0, 0, 0],
        initial_vx=[0, 0, 0],
        initial_vy=[0.9913358338, -0.1569959746, -0.8343398592],
    )

    saveAndRun(orbit)
    saveAndRun(figure8)
    #saveAndRun(BrouckeR1)
    saveAndRun(BrouckeR6)
    saveAndRun(BrouckeA7)


def setup_tests():
    numTests = 10
    stepSize = 1e-4
    maxRange = 2.5

    tests = Config(
        name="tests", range=(0, maxRange), step_size=stepSize, iterations=numTests
    )
    saveAndRun(tests)


def main():
    setup_periodic()
    setup_tests()


if __name__ == "__main__":
    main()
