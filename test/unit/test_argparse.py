import pytest

from tuxrun.argparse import filter_artefacts, setup_parser


def test_timeouts_parser():
    assert setup_parser().parse_args(["--timeouts", "boot=1"]).timeouts == {"boot": 1}
    assert setup_parser().parse_args(
        ["--timeouts", "boot=1", "deploy=42"]
    ).timeouts == {"boot": 1, "deploy": 42}

    with pytest.raises(SystemExit):
        setup_parser().parse_args(["--timeouts", "boot=a"])

    with pytest.raises(SystemExit):
        setup_parser().parse_args(["--timeouts", "booting=1"])


def test_downloads_rejects_the_same_name_twice(capsys):
    with pytest.raises(SystemExit):
        setup_parser().parse_args(
            [
                "--device",
                "usbg-bcm2711-rpi-4-b",
                "--downloads",
                "https://e.com/download?id=A",
                "--downloads",
                "https://e.com/download?id=B",
            ]
        )
    assert "downloaded twice" in capsys.readouterr().err


def test_uboot_is_bios():
    options = setup_parser().parse_args(
        ["--device", "qemu-arm64", "--uboot", "https://example.com/u-boot.bin"]
    )
    assert options.bios == "https://example.com/u-boot.bin"
    assert filter_artefacts(options)["bios"] == "https://example.com/u-boot.bin"


def test_filter_artefacts_with_a_dash_in_the_name():
    options = setup_parser().parse_args(
        [
            "--device",
            "fvp-morello-android",
            "--ap-romfw",
            "https://example.com/ap.bin",
            "--scp-fw",
            "https://example.com/scp.bin",
        ]
    )
    artefacts = filter_artefacts(options)
    assert artefacts["ap_romfw"] == "https://example.com/ap.bin"
    assert artefacts["scp_fw"] == "https://example.com/scp.bin"
