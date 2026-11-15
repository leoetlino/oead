import struct

import pytest
import oead


def make_fstm(channels):
    stm = oead.audio.Fstm()
    stm.endian = oead.Endianness.Little
    data = bytearray(stm.to_binary())
    struct.pack_into("<I", data, 8, 0x40000)
    stm = oead.audio.Fstm(bytes(data))

    info = stm.info
    stream_info = info.stream_info
    stream_info.encoding = oead.audio.SampleFormat.PCMS8
    stream_info.channel_count = len(channels)
    stream_info.frame_count = len(channels[0])
    info.stream_info = stream_info
    stm.info = info
    stm.samples = channels
    return stm


@pytest.mark.parametrize("channels", [
    [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]],
    [[0] * 5, [0] * 5, [0] * 5],
])
def test_bfstm_identical_channels_are_aligned(channels):
    stm = make_fstm(channels)

    reparsed = oead.audio.Fstm(bytes(stm.to_binary()))

    assert [list(channel[:5]) for channel in reparsed.samples] == channels
