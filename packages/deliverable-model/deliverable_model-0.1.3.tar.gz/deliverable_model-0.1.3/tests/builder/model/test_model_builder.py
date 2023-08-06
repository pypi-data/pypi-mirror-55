import filecmp

from deliverable_model.builder.model.model_builder import ModelBuilder


def test_build(datadir, tmpdir):
    model_builder = ModelBuilder()

    model_builder.add_keras_h5_model(datadir / "fixture" / "keras_h5_model")
    
    model_builder.save()

    config = model_builder.serialize(tmpdir)

    assert config == {'version': '1.0', 'type': 'keras_h5_model'}

    dircmp_obj = filecmp.dircmp(datadir / "expected", tmpdir)
    assert not dircmp_obj.diff_files

    assert model_builder.get_dependency() == ["tensorflow"]
