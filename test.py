def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)

# TODO: look for values
#def test_parameters(cldf_dataset):
#    assert len(list(cldf_dataset["ParameterTable"])) == 499


#def test_languages(cldf_dataset):
#    assert len(list(cldf_dataset["LanguageTable"])) == 9