"""Модуль визуализации графа зависимостей."""
import os
import shutil
import subprocess
from src.graph import DependencyGraph

PLANTUML_CMD = "plantuml"
PLANTUML_JAR = "plantuml.jar"


def generate_plantuml_text(graph: DependencyGraph) -> str:
    """Генерация текста PlantUML.

    Args:
        graph: Граф зависимостей.

    Returns:
        Строка в формате PlantUML.
    """
    lines = ["@startuml"]
    for pkg, deps in graph.graph.items():
        if not deps:
            lines.append(f"[{pkg}]")
        for dep in deps:
            lines.append(f"[{pkg}] --> [{dep}]")
    lines.append("@enduml")
    return "\n".join(lines)


def _get_plantuml_command(puml_file: str) -> list:
    """Определение команды для запуска PlantUML.

    Args:
        puml_file: Путь к файлу .puml.

    Returns:
        Список аргументов для subprocess или пустой список.
    """
    if shutil.which(PLANTUML_CMD):
        return [PLANTUML_CMD, "-tpng", puml_file]

    if os.path.exists(PLANTUML_JAR):
        return ["java", "-jar", PLANTUML_JAR, "-tpng", puml_file]

    return []


def save_visualization(graph: DependencyGraph, output_file: str) -> None:
    """Сохранение визуализации в PNG.

    Args:
        graph: Граф зависимостей.
        output_file: Имя выходного файла.
    """
    puml_text = generate_plantuml_text(graph)
    puml_file = output_file.replace(".png", ".puml")

    with open(puml_file, "w", encoding="utf-8") as file:
        file.write(puml_text)

    print(f"PlantUML text saved to {puml_file}")

    command = _get_plantuml_command(puml_file)

    if not command:
        print(
            "Error: PlantUML not found. Install it via package manager "
            "or place 'plantuml.jar' in the project root."
        )
        return

    try:
        subprocess.run(command, check=True, capture_output=True)
        print(f"PNG image saved to {output_file}")
    except subprocess.CalledProcessError as error:
        print(f"PlantUML error: {error.stderr.decode()}")
