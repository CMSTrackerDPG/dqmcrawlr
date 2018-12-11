from dqmcrawlr.dataset import get_dataset, get_available_datasets


def test_get_available_datasets():
    datasets = get_available_datasets(321012)

    assert "/Commissioning/Run2018D-PromptReco-v2/DQMIO" in datasets
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" in datasets
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" in datasets
    assert "/ZeroBias/Run2018D-PromptReco-v2/DQMIO" in datasets


def test_single_dataset():
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" == get_dataset(321012, "Express")


def test_multipe_dataset():
    """
    generated with:

    for run in RunInfo.objects.all().filter(problem_categories=10):
        print("assert '{}' == get_dataset([{}, '{}'])".format(run.type.dataset, run.run_number, run.type.reco))

    """

    assert "/Cosmics/Run2018E-PromptReco-v1/DQMIO" == get_dataset(325680, "Prompt")
    assert "/StreamExpress/Run2018D-Express-v1/DQMIO" == get_dataset(324878, "Express")
    assert "/StreamExpressCosmics/Run2018D-Express-v1/DQMIO" == get_dataset(
        324231, "Express"
    )
    assert "/ZeroBias/Run2018D-PromptReco-v2/DQMIO" == get_dataset(323954, "Prompt")
    assert "/Cosmics/Run2018D-PromptReco-v2/DQMIO" == get_dataset(323109, "Prompt")
    assert "/ZeroBias/Run2018C-PromptReco-v3/DQMIO" == get_dataset(320065, "Prompt")
    assert "/StreamExpress/Run2018C-Express-v1/DQMIO" == get_dataset(319909, "Express")
    assert "/StreamExpressCosmics/Run2018C-Express-v1/DQMIO" == get_dataset(
        319882, "Express"
    )


def test_heavy_ion():
    # TODO
    pass
