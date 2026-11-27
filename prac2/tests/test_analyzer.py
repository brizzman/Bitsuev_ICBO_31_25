"""Тесты анализатора графа."""
import json
from src.config import Config
from src.analyzer import build_transitive_graph


def test_build_graph_cycle(tmp_path) -> None:
    """Тест обработки циклических зависимостей."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({
        "A": ["B"],
        "B": ["C"],
        "C": ["A"]
    }))
    
    config = Config(
        package="A", source=str(test_file), test_mode=True,
        version="latest", output="out.png", ascii_mode=False,
        max_depth=-1
    )
    
    graph = build_transitive_graph(config)
    assert "A" in graph.graph
    assert "B" in graph.graph["A"]
    assert "C" in graph.graph["B"]
    assert "A" in graph.graph["C"]


def test_build_graph_max_depth(tmp_path) -> None:
    """Тест ограничения максимальной глубины."""
    test_file = tmp_path / "data.json"
    test_file.write_text(json.dumps({
        "A": ["B"],
        "B": ["C"],
        "C": ["D"]
    }))
    
    config = Config(
        package="A", source=str(test_file), test_mode=True,
        version="latest", output="out.png", ascii_mode=False,
        max_depth=1
    )
    
    graph = build_transitive_graph(config)
    assert "B" in graph.graph["A"]
    assert "C" not in graph.graph
