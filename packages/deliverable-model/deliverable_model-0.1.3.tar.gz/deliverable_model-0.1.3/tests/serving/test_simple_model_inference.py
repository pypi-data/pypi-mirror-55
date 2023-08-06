from deliverable_model.serving import SimpleModelInference


def test_serving(datadir):
    deliverable_model = SimpleModelInference(datadir)

    request = ["abc", "cba"]

    response = list(deliverable_model.parse(request))

    expected = [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]

    assert [i[1] for i in response] == expected
