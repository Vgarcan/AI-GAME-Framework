# 05. Template reutilizable del framework GAME para crear agentes

## Tabla de contenidos

1. [Objetivo de este capítulo](#1-objetivo-de-este-capítulo)
2. [Qué vamos a construir](#2-qué-vamos-a-construir)
3. [Estructura mental del template](#3-estructura-mental-del-template)
4. [Estructura recomendada de carpetas](#4-estructura-recomendada-de-carpetas)
5. [Snippet base completo](#5-snippet-base-completo)
6. [Cómo adaptar el template a otro agente](#6-cómo-adaptar-el-template-a-otro-agente)
7. [Ejemplo de adaptación rápida](#7-ejemplo-de-adaptación-rápida)
8. [Buenas prácticas profesionales](#8-buenas-prácticas-profesionales)
9. [Checklist antes de crear un nuevo agente](#9-checklist-antes-de-crear-un-nuevo-agente)
10. [Siguiente evolución posible](#10-siguiente-evolución-posible)

---

## 1. Objetivo de este capítulo

En los capítulos anteriores hemos visto tres cosas importantes:

1. Qué es el **GAME Framework**.
2. Cómo se puede convertir GAME en clases de Python.
3. Cómo crear agentes concretos usando el mismo loop.

Ahora vamos a convertir todo eso en un **template reutilizable**.

La idea no es crear un framework final de producción todavía. La idea es tener un esqueleto limpio que puedas copiar en cualquier proyecto y adaptar rápidamente.

Por ejemplo, con este template podrías crear:

| Tipo de agente | Qué cambiarías |
|---|---|
| Agente explorador de archivos | Actions de lectura y listado de archivos |
| Agente revisor de código | Actions para leer código, proponer cambios y editar |
| Agente documental | Actions para leer Markdown, PDF o DOCX |
| Agente Django | Actions para inspeccionar apps, models, views y urls |
| Agente RPA | Actions para consultar SOPs, validar reglas y generar excepciones |
| Agente de investigación | Actions para buscar, resumir y guardar fuentes |

La clave es que el **loop principal no cambia**.

Cambian las piezas GAME.

---

## 2. Qué vamos a construir

Queremos una plantilla que tenga estas piezas:

```text
game_framework_template.py

G:
    Goal

A:
    Action
    ActionRegistry

M:
    Memory

E:
    Environment

Language:
    AgentLanguage
    JsonAgentLanguage

Core:
    Agent
```

La idea es separar responsabilidades:

| Componente | Responsabilidad |
|---|---|
| `Goal` | Define lo que el agente quiere conseguir |
| `Action` | Define una herramienta disponible |
| `ActionRegistry` | Guarda y recupera acciones por nombre |
| `Memory` | Conserva el historial del agente |
| `Environment` | Ejecuta acciones y captura errores |
| `AgentLanguage` | Construye prompts y parsea respuestas |
| `Agent` | Ejecuta el loop principal |
| `generate_response` | Conecta con el modelo de IA |

Este diseño refleja directamente el GAME Framework.

---

## 3. Estructura mental del template

Antes de mirar el código, conviene entender el flujo:

```text
Usuario pide una tarea
        ↓
Agent guarda la tarea en Memory
        ↓
Agent construye un prompt usando:
    Goals
    Actions
    Memory
    Environment
        ↓
LLM responde con una acción en JSON
        ↓
AgentLanguage parsea la respuesta
        ↓
ActionRegistry busca la acción
        ↓
Environment ejecuta la acción
        ↓
Memory guarda decisión y resultado
        ↓
Se repite hasta terminal=True o max_iterations
```

Esto es el **Agent Loop**.

Lo importante es que el agente no ejecuta herramientas directamente. El agente decide, el entorno ejecuta.

---

## 4. Estructura recomendada de carpetas

Para un proyecto pequeño, puedes empezar con un solo archivo:

```text
project/
    game_framework_template.py
```

Para un proyecto más profesional, podrías separarlo así:

```text
project/
    game/
        __init__.py
        core.py
        goals.py
        actions.py
        memory.py
        environment.py
        language.py
        agent.py

    agents/
        file_explorer_agent.py
        code_reviewer_agent.py
        django_doc_agent.py

    main.py
```

En una app Django reutilizable, podrías tener algo como:

```text
ai_agents/
    __init__.py
    apps.py

    core/
        goals.py
        actions.py
        memory.py
        environment.py
        language.py
        agent.py

    agents/
        documentation_agent.py
        code_reviewer_agent.py

    services/
        llm_client.py

    management/
        commands/
            run_agent.py
```

Pero para estudiar y experimentar, lo mejor es empezar simple.

---

## 5. Snippet base completo

Este snippet está pensado como plantilla base.

La versión incluida aquí no depende todavía de OpenAI, Ollama ni LiteLLM. En lugar de eso, la función `generate_response()` está preparada como placeholder para que tú conectes el modelo que quieras.

```python
"""
GAME Framework Template
=======================

Este archivo contiene un esqueleto reutilizable para crear agentes usando el
GAME Framework.

GAME significa:

G = Goals / Objetivos e instrucciones
A = Actions / Herramientas disponibles
M = Memory / Memoria del agente
E = Environment / Entorno donde se ejecutan las acciones

La idea principal es que el loop del agente sea reutilizable y que cada agente
nuevo se cree cambiando sus goals, actions, memory, environment o language.
"""

from __future__ import annotations

import json
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


# ============================================================
# G: GOALS
# ============================================================

@dataclass(frozen=True)
class Goal:
    """
    Representa un objetivo o instrucción del agente.

    priority:
        Sirve para ordenar los goals. Un número más bajo puede entenderse
        como más importante.

    name:
        Nombre corto del goal.

    description:
        Explicación de lo que el agente debe conseguir o cómo debe comportarse.
    """

    priority: int
    name: str
    description: str


# ============================================================
# A: ACTIONS
# ============================================================

class Action:
    """
    Representa una herramienta que el agente puede usar.

    Una acción contiene:
        - name: nombre que usará el modelo para invocarla
        - function: función Python real que se ejecutará
        - description: explicación para el modelo
        - parameters: esquema de argumentos esperados
        - terminal: indica si esta acción termina el loop del agente
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
        Devuelve una representación simple de la acción para incluirla
        en el prompt del modelo.
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

    Evita tener if/else dentro del loop principal.
    """

    def __init__(self) -> None:
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action) -> None:
        """
        Añade una nueva acción al registro.
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


# ============================================================
# M: MEMORY
# ============================================================

class Memory:
    """
    Memoria sencilla basada en una lista de mensajes.

    Esta versión guarda todo en RAM. Más adelante puede cambiarse por:
        - SQLite
        - PostgreSQL
        - Redis
        - Vector database
        - Django models
        - Archivos JSON
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
        Devuelve las memorias.

        Si limit tiene valor, devuelve solo las últimas N entradas.
        """
        if limit is None:
            return self.items

        return self.items[-limit:]


# ============================================================
# E: ENVIRONMENT
# ============================================================

class Environment:
    """
    El entorno ejecuta las acciones.

    El agente decide qué acción ejecutar.
    El Environment se encarga de ejecutarla realmente y devolver un resultado
    estructurado.
    """

    def execute_action(self, action: Action, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una acción y captura errores de forma segura.
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
        Da formato estándar al resultado de una acción.
        """
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": self.current_timestamp(),
        }

    def current_timestamp(self) -> str:
        """
        Devuelve una marca temporal sencilla.
        """
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")


# ============================================================
# LANGUAGE
# ============================================================

class AgentLanguage:
    """
    Clase base para definir cómo se comunica el agente con el modelo.

    Responsabilidades:
        1. Construir el prompt.
        2. Parsear la respuesta del modelo.
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
    Implementación simple donde el modelo debe responder con JSON.

    Formato esperado:

    {
        "tool": "nombre_de_la_accion",
        "args": {
            "parametro": "valor"
        }
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
        Convierte la respuesta JSON del modelo en una invocación de acción.
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


# ============================================================
# CORE AGENT
# ============================================================

class Agent:
    """
    Agente reutilizable basado en GAME.

    Esta clase contiene el loop principal.
    No debería depender de un caso de uso concreto.
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
        Guarda la petición inicial del usuario en memoria.
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
        Parsea la respuesta del modelo y recupera la acción correspondiente.
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
        Guarda en memoria la decisión del agente y el resultado del entorno.
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
        Ejecuta el loop del agente.
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


# ============================================================
# EXAMPLE ACTIONS
# ============================================================

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


# ============================================================
# PLACEHOLDER LLM FUNCTION
# ============================================================

def generate_response(prompt: str) -> str:
    """
    Placeholder para conectar tu modelo de IA.

    Aquí podrías llamar a:
        - Ollama
        - LiteLLM
        - OpenAI API
        - Anthropic
        - Un modelo local
        - Un endpoint propio

    De momento devolvemos una acción terminal fija para probar el framework.
    """

    print("\nPROMPT SENT TO MODEL:")
    print(prompt)

    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": "Template ejecutado correctamente. Sustituye generate_response por tu cliente LLM."
        }
    })


# ============================================================
# FACTORY FUNCTION
# ============================================================

def build_template_agent() -> Agent:
    """
    Crea un agente mínimo usando el template.

    Esta función es útil porque centraliza la configuración del agente.
    Para crear otro agente, puedes copiar esta función y cambiar:
        - goals
        - actions
        - environment
        - agent_language
        - generate_response
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


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    agent = build_template_agent()
    final_memory = agent.run(
        user_input="Prueba el agente usando el template GAME.",
        max_iterations=5,
    )

    print("\nFINAL MEMORY:")
    for item in final_memory.get_memories():
        print(item)
```

---

## 6. Cómo adaptar el template a otro agente

Para crear otro agente no deberías tocar el `Agent.run()`.

Normalmente solo cambias cinco cosas:

```text
1. Goals
2. Actions
3. ActionRegistry
4. Environment
5. generate_response
```

Por ejemplo, para crear un agente de documentación:

```python
goals = [
    Goal(
        priority=1,
        name="Analizar documentación",
        description="Leer archivos Markdown y explicar cómo se relacionan."
    ),
    Goal(
        priority=2,
        name="Responder con claridad",
        description="Dar respuestas útiles, estructuradas y fáciles de estudiar."
    ),
    Goal(
        priority=3,
        name="Terminar",
        description="Finalizar con un resumen cuando la tarea esté completada."
    ),
]
```

Después defines sus acciones:

```python
def list_markdown_files() -> list[str]:
    """Devuelve los archivos Markdown disponibles."""
    ...

def read_markdown_file(file_name: str) -> str:
    """Lee un archivo Markdown concreto."""
    ...

def summarize_document(content: str) -> str:
    """Resume el contenido de un documento."""
    ...
```

Y las registras:

```python
registry.register(Action(
    name="list_markdown_files",
    function=list_markdown_files,
    description="Lista los archivos Markdown disponibles.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    terminal=False,
))
```

La clase `Agent` no cambia.

---

## 7. Ejemplo de adaptación rápida

Supongamos que quieres crear un agente para revisar archivos Python.

Podrías definir estas acciones:

```python
def list_python_files() -> list[str]:
    """Lista archivos Python del proyecto."""
    ...

def read_python_file(file_name: str) -> str:
    """Lee un archivo Python."""
    ...

def propose_improvement(file_name: str, content: str) -> str:
    """Propone una mejora para el archivo."""
    ...

def terminate(message: str) -> str:
    """Termina el agente."""
    return message
```

Y estos goals:

```python
goals = [
    Goal(
        priority=1,
        name="Revisar código",
        description="Leer archivos Python y encontrar mejoras pequeñas."
    ),
    Goal(
        priority=2,
        name="No modificar sin aprobación",
        description="Nunca editar archivos sin autorización explícita del usuario."
    ),
    Goal(
        priority=3,
        name="Mantener cambios seguros",
        description="Proponer cambios pequeños, reversibles y fáciles de probar."
    ),
]
```

Este sería otro agente completamente distinto, pero usando el mismo framework.

---

## 8. Buenas prácticas profesionales

### 8.1. No mezclar decisión con ejecución

El agente decide.

El entorno ejecuta.

Esto mantiene el diseño limpio.

Mal diseño:

```python
if model_says_read_file:
    open(file)
```

Mejor diseño:

```python
action, args = agent.get_action(response)
result = environment.execute_action(action, args)
```

---

### 8.2. Toda acción debe tener descripción clara

El modelo no sabe usar bien una herramienta si la descripción es vaga.

Descripción débil:

```text
Read file
```

Descripción mejor:

```text
Reads the content of a specific file from the current project directory.
The file_name argument must match one of the files returned by list_files.
```

---

### 8.3. Usar acciones terminales

No dependas de que el modelo “decida parar” escribiendo texto libre.

Crea una acción terminal:

```python
Action(
    name="terminate",
    function=terminate,
    description="Terminates the agent loop with a final message.",
    parameters={...},
    terminal=True,
)
```

Esto hace el loop más controlable.

---

### 8.4. Usar límites de iteraciones

Todo agente debe tener límite.

```python
agent.run(user_input, max_iterations=10)
```

Esto evita loops infinitos.

---

### 8.5. Guardar resultados estructurados

El entorno debe devolver algo consistente:

```json
{
  "tool_executed": true,
  "result": "...",
  "timestamp": "2026-06-01T20:00:00+0100"
}
```

Esto hace más fácil depurar, testear y auditar.

---

### 8.6. Separar conectores externos

No metas llamadas a APIs externas directamente en el loop.

Mejor:

```text
Agent
    usa Environment

Environment
    usa Services

Services
    llaman APIs externas
```

Ejemplo:

```text
DjangoDocumentationAgent
    ↓
DjangoEnvironment
    ↓
RepositoryService
    ↓
GitHub API / local filesystem
```

---

## 9. Checklist antes de crear un nuevo agente

Antes de programar un nuevo agente, responde estas preguntas:

```text
[ ] ¿Cuál es el objetivo principal del agente?
[ ] ¿Qué instrucciones limitan su comportamiento?
[ ] ¿Qué acciones necesita?
[ ] ¿Qué acciones son peligrosas?
[ ] ¿Alguna acción requiere aprobación humana?
[ ] ¿Qué memoria necesita entre iteraciones?
[ ] ¿Dónde se ejecutan realmente las acciones?
[ ] ¿Cómo se capturan errores?
[ ] ¿Cuándo debe terminar el loop?
[ ] ¿Cuál es el máximo de iteraciones?
[ ] ¿Qué formato debe devolver el modelo?
[ ] ¿Cómo se validará la respuesta del modelo?
[ ] ¿Cómo se probará el agente sin tocar datos reales?
```

Esta checklist es especialmente importante si el agente puede:

```text
Leer archivos
Modificar archivos
Enviar emails
Hacer llamadas a APIs
Crear registros en base de datos
Ejecutar comandos
Interactuar con servicios externos
```

---

## 10. Siguiente evolución posible

Este template es una base. A partir de aquí se puede mejorar en varias direcciones.

### 10.1. Integración con Ollama

Podrías sustituir `generate_response()` por una llamada a Ollama:

```python
from ollama import Client

client = Client(host="http://192.168.2.132:11434")

def generate_response(prompt: str) -> str:
    response = client.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]
```

### 10.2. Integración con LiteLLM

También puedes usar LiteLLM para cambiar de proveedor más fácilmente:

```python
from litellm import completion

def generate_response(prompt: str) -> str:
    response = completion(
        model="ollama/llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["choices"][0]["message"]["content"]
```

### 10.3. Memoria persistente

La clase `Memory` se puede sustituir por:

```text
JsonFileMemory
SQLiteMemory
DjangoModelMemory
VectorMemory
HybridMemory
```

Lo importante es conservar el mismo método:

```python
add_memory(...)
get_memories(...)
```

Así el agente no necesita saber cómo se guarda la memoria.

### 10.4. Validación de acciones

Más adelante conviene validar que los argumentos recibidos cumplen el esquema de la acción.

Por ejemplo:

```python
action.validate_args(invocation["args"])
```

Esto evitaría errores cuando el modelo devuelve argumentos incompletos o incorrectos.

### 10.5. Entornos especializados

Puedes crear entornos distintos:

```text
LocalFileEnvironment
GitHubEnvironment
DjangoEnvironment
RPAEnvironment
BrowserEnvironment
DatabaseEnvironment
```

El mismo agente conceptual podría funcionar en diferentes entornos.

---

## Conclusión

Este template convierte el GAME Framework en un esqueleto reutilizable.

La idea más importante es:

```text
El loop del agente debe ser estable.
Las piezas GAME deben ser intercambiables.
```

Eso significa que no necesitas crear un agente desde cero cada vez. Puedes usar el mismo núcleo y cambiar únicamente:

```text
Goals
Actions
Memory
Environment
AgentLanguage
generate_response
```

Este patrón es lo que permite pasar de scripts improvisados a una arquitectura de agentes más profesional, modular y mantenible.
