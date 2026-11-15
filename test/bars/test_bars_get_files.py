import pytest
import oead

from utils import make_test_cases

cases, cases_data = make_test_cases("bars/files/*.bars")

@pytest.mark.parametrize("file", cases)
def test_bars_get_file(file):
    res = oead.audio.Bars(cases_data[file])
    for asset in res.files:
        assert res.get_file(asset.meta.asset_name) is not None
def test_bars_get_file_missing_name():
    res = oead.audio.Bars()
    for name in ("First", "Third"):
        meta = oead.audio.Amta()
        meta.asset_name = name
        res.add_file(meta, None)

    assert res.get_file("First").meta.asset_name == "First"
    assert res.get_file("Third").meta.asset_name == "Third"
    # CRC32 of "NotInArchive" sorts between those of "First" and "Third".
    with pytest.raises(oead.InvalidDataError, match="Name not found"):
        res.get_file("NotInArchive")


def test_bars_set_files_updates_hashes():
    res = oead.audio.Bars()
    res.version = 0x101
    for name in ("First", "Third"):
        meta = oead.audio.Amta()
        meta.asset_name = name
        res.add_file(meta, None)

    files = res.files
    files[0].meta.asset_name = "Beta"
    files[1].meta.asset_name = "Alpha"
    res.files = files

    for bars in (res, oead.audio.Bars(res.to_binary())):
        for name in ("Alpha", "Beta"):
            assert bars.get_file(name).meta.asset_name == name
        with pytest.raises(oead.InvalidDataError, match="Name not found"):
            bars.get_file("First")
