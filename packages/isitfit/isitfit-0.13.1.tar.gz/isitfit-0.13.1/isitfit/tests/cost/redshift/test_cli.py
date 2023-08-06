from isitfit.cost.redshift.cli import cost_analyze, cost_optimize

def test_costCore(mocker):
    mockee_list = [
      'isitfit.cost.redshift.iterator.RedshiftPerformanceIterator',
      'isitfit.cost.redshift.analyzer.Analyzer',
      'isitfit.cost.redshift.reporter.ReporterAnalyze',
      'isitfit.cost.redshift.reporter.ReporterOptimize',
    ]
    for mockee_single in mockee_list:
      mocker.patch(mockee_single, autospec=True)

    # run and test
    cost_analyze(None)
    assert True # no exception

    cost_analyze([1])
    assert True # no exception

    cost_optimize()
    assert True # no exception
