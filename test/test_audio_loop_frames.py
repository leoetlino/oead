import pytest
import oead


@pytest.mark.parametrize("cls", [oead.audio.Amta, oead.audio.Fwav])
def test_set_loop_end_frame(cls):
    asset = cls()

    asset.loop_end_frame = 20
    asset.loop_start_frame = 10

    assert asset.loop_start_frame == 10
    assert asset.loop_end_frame == 20
