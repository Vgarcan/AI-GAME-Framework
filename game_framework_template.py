"""
GAME Framework Template
=======================

Esqueleto reutilizable para crear agentes usando el GAME Framework.

GAME:
    G = Goals / Objetivos e instrucciones
    A = Actions / Herramientas disponibles
    M = Memory / Memoria
    E = Environment / Entorno de ejecución

Este archivo está pensado como punto de partida para proyectos de estudio,
POCs o pequeños frameworks internos.
"""

from __future__ import annotations

import json
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class Goal:
    """
    Representa un objetivo o instrucción del agente.
    """

    priority: int
    name: str
    description: str


class Action:
    """
    Representa una herramienta que el agente puede usar.
    """

    def __init__(
        self,
        name: str,
        function: Callable[..., Any],
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        terminal: bool = False,
    ) -> None:
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters or {
            "type": "object",
            "properties": {},
            "required": [],
        }
        self.terminal = terminal

    def execute(self, **args: Any) -> Any:
        """
        Ejecuta la función asociada a esta acción.
        """
        return self.function(**args)

    def to_prompt_schema(self) -> Dict[str, Any]:
        """
        Devuelve una representación de la acción para el prompt.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "terminal": self.terminal,
        }


class ActionRegistry:
    """
    Registro central de acciones disponibles para un agente.
    """

    def __init__(self) -> None:
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action) -> None:
        """
        Añade una acción al registro.
        """
        self._actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        """
        Recupera una acción por nombre.
        """
        return self._actions.get(name)

    def get_actions(self) -> List[Action]:
        """
        Devuelve todas las acciones registradas.
        """
        return list(self._actions.values())


class Memory:
    """
    Memoria sencilla basada en una lista de mensajes.
    """

    def __init__(self) -> None:
        self.items: List[Dict[str, str]] = []

    def add_memory(self, memory: Dict[str, str]) -> None:
        """
        Añade una entrada a la memoria.
        """
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Devuelve las memorias guardadas.

        Si limit tiene valor, devuelve solo las últimas N entradas.
        """
        if limit is None:
            return self.items

        return self.items[-limit:]


class Environment:
    """
    Ejecuta acciones y devuelve resultados estructurados.
    """

    def execute_action(self, action: Action, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una acción y captura errores.
        """
        try:
            result = action.execute(**args)
            return self.format_result(result)

        except Exception as exc:
            return {
                "tool_executed": False,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "timestamp": self.current_timestamp(),
            }

    def format_result(self, result: Any) -> Dict[str, Any]:
        """
        Formatea el resultado de una acción.
        """
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": self.current_timestamp(),
        }

    def current_timestamp(self) -> str:
        """
        Devuelve una marca temporal.
        """
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")


class AgentLanguage:
    """
    Clase base para construir prompts y parsear respuestas.
    """

    def construct_prompt(
        self,
        goals: List[Goal],
        actions: List[Action],
        memory: Memory,
        environment: Environment,
    ) -> str:
        raise NotImplementedError

    def parse_response(self, response: str) -> Dict[str, Any]:
        raise NotImplementedError


class JsonAgentLanguage(AgentLanguage):
    """
    Lenguaje simple donde el modelo responde con JSON.

    Formato esperado:
        {
            "tool": "action_name",
            "args": {}
        }
    """

    def construct_prompt(
        self,
        goals: List[Goal],
        actions: List[Action],
        memory: Memory,
        environment: Environment,
    ) -> str:
        sorted_goals = sorted(goals, key=lambda goal: goal.priority)

        goals_text = "\n".join(
            f"{goal.priority}. {goal.name}: {goal.description}"
            for goal in sorted_goals
        )

        actions_text = json.dumps(
            [action.to_prompt_schema() for action in actions],
            indent=2,
            ensure_ascii=False,
        )

        memory_text = json.dumps(
            memory.get_memories(limit=20),
            indent=2,
            ensure_ascii=False,
        )

        return f"""
You are an AI agent using the GAME Framework.

GOALS:
{goals_text}

AVAILABLE ACTIONS:
{actions_text}

MEMORY:
{memory_text}

RESPONSE FORMAT:
You must respond only with valid JSON using this schema:

{{
  "tool": "action_name",
  "args": {{}}
}}

Choose exactly one action.
Do not include markdown.
Do not include explanations outside the JSON.
""".strip()

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Convierte la respuesta JSON del modelo en una invocación.
        """
        try:
            invocation = json.loads(response)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"The model did not return valid JSON. Raw response: {response}"
            ) from exc

        if "tool" not in invocation:
            raise ValueError("The response must include a 'tool' field.")

        if "args" not in invocation:
            invocation["args"] = {}

        if not isinstance(invocation["args"], dict):
            raise ValueError("The 'args' field must be an object.")

        return invocation


class Agent:
    """
    Agente reutilizable basado en GAME.
    """

    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[str], str],
        environment: Environment,
    ) -> None:
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def set_current_task(self, memory: Memory, task: str) -> None:
        """
        Guarda la petición inicial del usuario.
        """
        memory.add_memory({
            "type": "user",
            "content": task,
        })

    def construct_prompt(self, memory: Memory) -> str:
        """
        Construye el prompt completo para el modelo.
        """
        return self.agent_language.construct_prompt(
            goals=self.goals,
            actions=self.actions.get_actions(),
            memory=memory,
            environment=self.environment,
        )

    def get_action(self, response: str) -> tuple[Action, Dict[str, Any]]:
        """
        Parsea la respuesta y recupera la acción solicitada.
        """
        invocation = self.agent_language.parse_response(response)
        action_name = invocation["tool"]

        action = self.actions.get_action(action_name)

        if action is None:
            raise ValueError(f"Unknown action requested by model: {action_name}")

        return action, invocation

    def update_memory(
        self,
        memory: Memory,
        response: str,
        result: Dict[str, Any],
    ) -> None:
        """
        Guarda la decisión del agente y el resultado del entorno.
        """
        memory.add_memory({
            "type": "assistant",
            "content": response,
        })

        memory.add_memory({
            "type": "environment",
            "content": json.dumps(result, ensure_ascii=False),
        })

    def run(
        self,
        user_input: str,
        memory: Optional[Memory] = None,
        max_iterations: int = 10,
    ) -> Memory:
        """
        Ejecuta el loop principal del agente.
        """
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(1, max_iterations + 1):
            print(f"\n--- Iteration {iteration} ---")

            prompt = self.construct_prompt(memory)

            response = self.generate_response(prompt)
            print(f"Agent decision: {response}")

            action, invocation = self.get_action(response)

            result = self.environment.execute_action(
                action=action,
                args=invocation["args"],
            )
            print(f"Action result: {result}")

            self.update_memory(memory, response, result)

            if action.terminal:
                print("Terminal action executed. Stopping agent loop.")
                break

        return memory


def say(message: str) -> str:
    """
    Acción sencilla de ejemplo.
    """
    return message


def terminate(message: str) -> str:
    """
    Acción terminal de ejemplo.
    """
    return message


def generate_response(prompt: str) -> str:
    """
    Placeholder para conectar tu modelo de IA.

    Sustituye esta función por una llamada real a Ollama, LiteLLM,
    OpenAI, Anthropic o tu propio endpoint.
    """
    print("\nPROMPT SENT TO MODEL:")
    print(prompt)

    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": "Template ejecutado correctamente. Sustituye generate_response por tu cliente LLM."
        }
    })


def build_template_agent() -> Agent:
    """
    Crea un agente mínimo usando el template.
    """

    goals = [
        Goal(
            priority=1,
            name="Responder al usuario",
            description="Ayudar al usuario usando las acciones disponibles.",
        ),
        Goal(
            priority=2,
            name="Terminar correctamente",
            description="Usar la acción terminate cuando la tarea esté completada.",
        ),
    ]

    registry = ActionRegistry()

    registry.register(Action(
        name="say",
        function=say,
        description="Devuelve un mensaje al usuario.",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Mensaje que se devolverá al usuario.",
                }
            },
            "required": ["message"],
        },
        terminal=False,
    ))

    registry.register(Action(
        name="terminate",
        function=terminate,
        description="Termina el loop del agente con un mensaje final.",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Mensaje final para el usuario.",
                }
            },
            "required": ["message"],
        },
        terminal=True,
    ))

    return Agent(
        goals=goals,
        agent_language=JsonAgentLanguage(),
        action_registry=registry,
        generate_response=generate_response,
        environment=Environment(),
    )


if __name__ == "__main__":
    agent = build_template_agent()
    final_memory = agent.run(
        user_input="Prueba el agente usando el template GAME.",
        max_iterations=5,
    )

    print("\nFINAL MEMORY:")
    for item in final_memory.get_memories():
        print(item)
