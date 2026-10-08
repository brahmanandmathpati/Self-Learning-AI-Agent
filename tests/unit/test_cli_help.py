"""The CLI prints help and lists every command."""

from sla.cli import build_parser, main


def test_no_command_prints_help(capsys):
    assert main([]) == 1
    assert "usage: sla" in capsys.readouterr().out


def test_parser_name_and_commands(capsys):
    assert build_parser().prog == "sla"
    main([])
    out = capsys.readouterr().out
    for cmd in ("train", "evaluate", "pipeline", "ablation", "baseline", "reflect", "runs", "dashboard"):
        assert cmd in out
