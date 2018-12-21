from dqmcrawlr.dqm import DQMSession


def test_get_available_datasets():
    dqm_session = DQMSession()
    datasets = dqm_session.get_available_datasets(321012)

    assert "/Commissioning/Run2018D-PromptReco-v2/DQMIO" in datasets
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" in datasets
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" in datasets
    assert "/ZeroBias/Run2018D-PromptReco-v2/DQMIO" in datasets


def test_single_dataset():
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" == DQMSession().get_dataset(
        321012, "Express"
    )


def test_get_lumisections():
    assert "534" == DQMSession().get_lumisections(322222, "Prompt")


def test_multipe_dataset():
    """
    generated with:

    for run in RunInfo.objects.all().filter(problem_categories=10):
        print("assert '{}' == get_dataset([{}, '{}'])".format(
            run.type.dataset, run.run_number, run.type.reco)
        )
    """

    session = DQMSession()

    assert "/Cosmics/Run2018E-PromptReco-v1/DQMIO" == session.get_dataset(
        325680, "Prompt"
    )
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" == session.get_dataset(
        324878, "Express"
    )
    assert "/StreamExpressCosmics/Run2018D-Express-v1/DQMIO" == session.get_dataset(
        324231, "Express"
    )
    assert "/ZeroBias/Run2018D-PromptReco-v2/DQMIO" == session.get_dataset(
        323954, "Prompt"
    )
    assert "/Cosmics/Run2018D-PromptReco-v2/DQMIO" == session.get_dataset(
        323109, "Prompt"
    )
    assert "/ZeroBias/Run2018C-PromptReco-v3/DQMIO" == session.get_dataset(
        320065, "Prompt"
    )
    assert "/StreamExpress/Run2018C-Express-v1/DQMIO" == session.get_dataset(
        319909, "Express"
    )
    assert "/StreamExpressCosmics/Run2018C-Express-v1/DQMIO" == session.get_dataset(
        319882, "Express"
    )


def test_rereco():
    session = DQMSession()

    assert "/SingleTrack/Run2017G-17Nov2017-v1/DQMIO" == session.get_dataset(
        306645, "reReco"
    )
    assert "/SingleTrack/Run2017G-17Nov2017-v1/DQMIO" == session.get_dataset(
        306631, "reReco"
    )
    assert "/SingleTrack/Run2017G-17Nov2017-v1/DQMIO" == session.get_dataset(
        306584, "reReco"
    )


def test_heavy_ion():
    session = DQMSession()

    assert "/StreamHIExpress/HIRun2018A-Express-v1/DQMIO" == session.get_dataset(
        327564, "Express"
    )
    assert "/StreamHIExpress/HIRun2018A-Express-v1/DQMIO" == session.get_dataset(
        327489, "Express"
    )
    assert "/HIMinimumBias1/HIRun2018A-PromptReco-v2/DQMIO" == session.get_dataset(
        327489, "Prompt"
    )
