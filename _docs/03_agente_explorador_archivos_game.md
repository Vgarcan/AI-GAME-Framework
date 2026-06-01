# 03, Implementación práctica de un agente explorador de archivos con GAME

## Tabla de contenidos

1. [Objetivo del capítulo](#objetivo-del-capítulo)
2. [Dónde encaja este capítulo dentro de la guía](#dónde-encaja-este-capítulo-dentro-de-la-guía)
3. [Qué vamos a construir](#qué-vamos-a-construir)
4. [Por qué empezar con un agente explorador de archivos](#por-qué-empezar-con-un-agente-explorador-de-archivos)
5. [Diseño GAME del agente](#diseño-game-del-agente)
6. [Estructura mental del agente](#estructura-mental-del-agente)
7. [Paso 1, definir los Goals](#paso-1-definir-los-goals)
8. [Paso 2, definir las funciones reales](#paso-2-definir-las-funciones-reales)
9. [Paso 3, convertir funciones en Actions](#paso-3-convertir-funciones-en-actions)
10. [Paso 4, registrar las Actions en el ActionRegistry](#paso-4-registrar-las-actions-en-el-actionregistry)
11. [Paso 5, preparar el Environment](#paso-5-preparar-el-environment)
12. [Paso 6, preparar el AgentLanguage](#paso-6-preparar-el-agentlanguage)
13. [Paso 7, crear el Agent](#paso-7-crear-el-agent)
14. [Paso 8, ejecutar el agente](#paso-8-ejecutar-el-agente)
15. [Código completo del ejemplo](#código-completo-del-ejemplo)
16. [Cómo fluye una ejecución real](#cómo-fluye-una-ejecución-real)
17. [Qué ocurre en memoria durante la ejecución](#qué-ocurre-en-memoria-durante-la-ejecución)
18. [Por qué necesitamos una acción terminal](#por-qué-necesitamos-una-acción-terminal)
19. [Errores comunes al implementar este agente](#errores-comunes-al-implementar-este-agente)
20. [Cómo mejorar este agente en una versión profesional](#cómo-mejorar-este-agente-en-una-versión-profesional)
21. [Relación con Django, APIs y proyectos reales](#relación-con-django-apis-y-proyectos-reales)
22. [Resumen del capítulo](#resumen-del-capítulo)
23. [Próximo capítulo recomendado](#próximo-capítulo-recomendado)

---

## Objetivo del capítulo

En los capítulos anteriores vimos primero la idea general del **GAME Framework** y después los componentes principales de un framework simple para construir agentes.

Ahora vamos a dar un paso más práctico.

El objetivo de este capítulo es construir mentalmente y en código un primer agente completo usando GAME. El agente será sencillo, pero suficientemente realista para entender cómo se conectan las piezas.

Vamos a construir un **agente explorador de archivos**, capaz de:

1. Recibir una tarea del usuario.
2. Listar archivos disponibles en un directorio.
3. Leer archivos concretos.
4. Guardar en memoria las decisiones del agente y los resultados del entorno.
5. Terminar la ejecución con un resumen.

Este ejemplo es importante porque refleja una situación muy común en desarrollo de software. Muchas herramientas de IA para programación necesitan inspeccionar archivos, entender el proyecto, decidir qué leer y luego producir una respuesta o proponer cambios.

Un agente de este tipo puede ser la base de herramientas más avanzadas como:

1. Un asistente que lee documentación técnica.
2. Un agente que analiza un proyecto Django.
3. Un agente que resume scripts Python.
4. Un agente que revisa errores en logs.
5. Un agente que prepara documentación de un repositorio.
6. Un agente que ayuda a mantener una base de conocimiento local.

---

## Dónde encaja este capítulo dentro de la guía

Hasta ahora tenemos esta progresión:

1. **Capítulo 01**, introducción al framework, GAME y Agent Loop.
2. **Capítulo 02**, construcción conceptual del framework simple, `Goal`, `Action`, `ActionRegistry`, `Memory`, `Environment`, `AgentLanguage` y `Agent`.
3. **Capítulo 03**, implementación práctica de un agente usando esas piezas.

Este capítulo ya no se queda solo en la arquitectura. Aquí empezamos a ver cómo un diseño GAME se convierte en un agente funcional.

La idea no es copiar código sin entenderlo. La idea es ver cómo una decisión de diseño se convierte en una clase, una función o una responsabilidad concreta.

---

## Qué vamos a construir

Vamos a construir un agente llamado:

```text
File Explorer Agent
```

En español podemos llamarlo:

```text
Agente Explorador de Archivos
```

Su misión será recibir peticiones como esta:

```text
Dime qué archivos Python hay en este directorio y resume para qué sirve cada uno.
```

El agente no debería responder inmediatamente sin mirar nada. Primero debería pensar qué acciones tiene disponibles.

Por ejemplo, una ejecución razonable sería:

```text
Usuario:
Dime qué archivos Python hay en este directorio y resume para qué sirve cada uno.

Agente:
Decide usar list_files.

Environment:
Devuelve una lista de archivos.

Agente:
Decide leer main.py.

Environment:
Devuelve el contenido de main.py.

Agente:
Decide leer utils.py.

Environment:
Devuelve el contenido de utils.py.

Agente:
Decide terminar con un resumen.
```

Este comportamiento parece simple, pero contiene todas las piezas importantes de un agente:

1. Objetivo.
2. Herramientas.
3. Decisión.
4. Ejecución.
5. Resultado.
6. Memoria.
7. Nueva decisión.
8. Finalización.

Eso es un Agent Loop real.

---

## Por qué empezar con un agente explorador de archivos

Un agente explorador de archivos es un buen primer ejemplo porque tiene un entorno fácil de entender.

No necesitamos todavía bases de datos, APIs externas, autenticación, permisos complejos ni llamadas a servicios de terceros. El agente solo interactúa con el sistema de archivos.

Aun así, el ejemplo nos permite practicar conceptos profesionales:

| Concepto | Cómo aparece en este agente |
|---|---|
| Separación de responsabilidades | El agente decide, el environment ejecuta |
| Abstracción | Las acciones se describen como objetos |
| Registro de herramientas | El ActionRegistry centraliza las herramientas |
| Gestión de estado | La Memory guarda lo ocurrido |
| Control de ejecución | max_iterations evita bucles infinitos |
| Finalización controlada | terminate marca el final del loop |
| Manejo de errores | read_file puede devolver errores si el archivo no existe |

También es un caso muy cercano al trabajo real de un developer. Cuando tú usas una IA para ayudarte con un proyecto, muchas veces la IA necesita hacer exactamente esto:

1. Ver qué archivos existen.
2. Leer algunos archivos.
3. Entender relaciones entre ellos.
4. Hacer una recomendación.
5. Proponer cambios.

Por eso este ejemplo es pequeño, pero no es artificial.

---

## Diseño GAME del agente

Antes de programar, diseñamos el agente usando GAME.

Recordemos:

| Letra | Componente | Pregunta principal |
|---|---|---|
| G | Goals | Qué intenta conseguir el agente |
| A | Actions | Qué puede hacer el agente |
| M | Memory | Qué recuerda el agente |
| E | Environment | Dónde ejecuta sus acciones |

Para nuestro agente explorador de archivos, el diseño sería el siguiente.

### G, Goals

El agente tiene dos goals principales:

1. Explorar archivos del directorio actual, listando y leyendo archivos cuando sea necesario.
2. Terminar la sesión cuando la tarea esté completa, proporcionando un resumen útil.

Esto significa que el agente no existe solo para ejecutar comandos. Existe para ayudar al usuario a entender archivos.

### A, Actions

El agente tendrá tres acciones iniciales:

| Acción | Propósito | Terminal |
|---|---|---|
| `list_files` | Devuelve la lista de archivos del directorio | No |
| `read_file` | Lee el contenido de un archivo específico | No |
| `terminate` | Termina el loop con un mensaje final | Sí |

Estas acciones son pequeñas, concretas y fáciles de razonar.

### M, Memory

La memoria guardará:

1. La tarea original del usuario.
2. Cada decisión tomada por el agente.
3. Cada resultado devuelto por el entorno.
4. El mensaje final de terminación.

Esto permite que el agente no pierda contexto entre una iteración y la siguiente.

### E, Environment

El entorno será el sistema de archivos local.

Eso significa que cuando el agente diga:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "main.py"
  }
}
```

El Environment será quien realmente intente abrir `main.py`, leerlo y devolver su contenido.

---

## Estructura mental del agente

Podemos imaginar el agente como una pequeña máquina de decisión.

```text
Tarea del usuario
    ↓
Memoria actual
    ↓
Goals disponibles
    ↓
Actions disponibles
    ↓
Prompt para el LLM
    ↓
El LLM elige una Action
    ↓
El Environment ejecuta la Action
    ↓
El resultado se guarda en Memory
    ↓
El ciclo se repite
```

Esta estructura es la parte más importante del capítulo.

Un error común cuando se empieza con agentes es pensar que el agente es solo “un prompt grande”. En realidad, el prompt es solo una parte. El agente completo necesita una arquitectura alrededor:

1. Una forma de describir herramientas.
2. Una forma de ejecutar herramientas.
3. Una forma de guardar contexto.
4. Una forma de parar.
5. Una forma de cambiar componentes sin reescribir todo.

Eso es lo que nos da este framework.

---

## Paso 1, definir los Goals

Primero definimos los objetivos del agente.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Goal:
    """
    Represents one goal or instruction for the agent.

    Attributes:
        priority: Determines the order in which goals are presented.
        name: Short identifier for the goal.
        description: Human readable explanation of what the agent should do.
    """

    priority: int
    name: str
    description: str
```

Ahora creamos los goals del agente explorador de archivos:

```python
goals = [
    Goal(
        priority=1,
        name="Explore Files",
        description="Explore files in the current directory by listing and reading them when needed."
    ),
    Goal(
        priority=2,
        name="Terminate",
        description="Terminate the session when the task is complete with a helpful summary."
    )
]
```

Aquí estamos haciendo algo muy importante. Estamos separando las instrucciones del agente de la lógica de ejecución.

En un script mal diseñado podríamos meter estas reglas directamente en un prompt enorme. Pero al convertirlas en objetos, podemos:

1. Reordenarlas por prioridad.
2. Reutilizarlas en otros agentes.
3. Añadir o quitar goals sin tocar el loop.
4. Crear goals comunes para todos nuestros agentes.

Por ejemplo, más adelante podríamos tener un goal global de seguridad:

```python
Goal(
    priority=0,
    name="Safety",
    description="Never modify or delete files unless the user has explicitly approved the change."
)
```

Ese goal podría aplicarse a muchos agentes diferentes.

---

## Paso 2, definir las funciones reales

Ahora necesitamos funciones normales de Python.

Estas funciones son las que realmente harán el trabajo.

```python
import os
from typing import List


def list_files() -> List[str]:
    """
    Return a list of files and folders in the current directory.

    This function is intentionally simple for the first version of the framework.
    Later, we could add filtering, security checks, ignored folders and metadata.
    """

    return os.listdir(".")
```

La función `list_files` no sabe nada sobre agentes, goals, memoria ni LLMs. Solo lista archivos.

Eso es bueno. Una función debe tener una responsabilidad clara.

Ahora definimos `read_file`:

```python
def read_file(file_name: str) -> str:
    """
    Read the content of a file from the current directory.

    Args:
        file_name: Name of the file to read.

    Returns:
        The file content as text, or an error message if the file cannot be read.
    """

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except UnicodeDecodeError:
        return f"Error: {file_name} could not be decoded as UTF-8 text."
    except Exception as exc:
        return f"Error: {str(exc)}"
```

Y ahora la función `terminate`:

```python
def terminate(message: str) -> str:
    """
    Terminate the agent loop and return a final summary message.

    Args:
        message: Final message for the user.

    Returns:
        The same message, so the environment can store it as the action result.
    """

    return message
```

La función `terminate` parece muy simple, pero en diseño de agentes es muy importante. Sirve para que el agente tenga una forma explícita de decir:

```text
He terminado la tarea.
```

Sin una acción terminal, el agente podría seguir iterando hasta llegar al límite máximo.

---

## Paso 3, convertir funciones en Actions

Ahora convertimos esas funciones normales en Actions.

Una `Action` no es solo una función. Es una descripción completa de una herramienta.

```python
from typing import Any, Callable, Dict


class Action:
    """
    Represents a tool that the agent can choose and the environment can execute.

    Attributes:
        name: Name used by the LLM to invoke the action.
        function: Python callable that performs the real work.
        description: Explanation of when and why the action should be used.
        parameters: JSON schema describing the expected arguments.
        terminal: Whether this action should stop the agent loop.
    """

    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict,
        terminal: bool = False,
    ):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters
        self.terminal = terminal

    def execute(self, **args) -> Any:
        """
        Execute the underlying Python function with keyword arguments.
        """

        return self.function(**args)
```

Ahora podemos definir la acción `list_files`:

```python
list_files_action = Action(
    name="list_files",
    function=list_files,
    description="Returns a list of files and folders in the current directory.",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    },
    terminal=False,
)
```

Como `list_files` no necesita argumentos, su schema está vacío.

Ahora definimos `read_file`:

```python
read_file_action = Action(
    name="read_file",
    function=read_file,
    description="Reads the content of a specified file in the current directory.",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Name of the file to read."
            }
        },
        "required": ["file_name"]
    },
    terminal=False,
)
```

Aquí el schema sí importa. Le estamos diciendo al modelo que para llamar a `read_file`, necesita proporcionar `file_name`.

Finalmente definimos `terminate`:

```python
terminate_action = Action(
    name="terminate",
    function=terminate,
    description="Terminates the agent loop and returns a final message for the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Final summary message for the user."
            }
        },
        "required": ["message"]
    },
    terminal=True,
)
```

La clave es esta línea:

```python
terminal=True
```

Eso convierte esta herramienta en una señal de parada para el Agent Loop.

---

## Paso 4, registrar las Actions en el ActionRegistry

Ahora necesitamos un registro centralizado de acciones.

```python
from typing import List, Optional


class ActionRegistry:
    """
    Stores and retrieves actions by name.

    The agent uses this registry to find the real Action object after the LLM
    has selected a tool name.
    """

    def __init__(self):
        self.actions = {}

    def register(self, action: Action) -> None:
        """
        Register an action using its name as the lookup key.
        """

        self.actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        """
        Return an action by name, or None if the action does not exist.
        """

        return self.actions.get(name)

    def get_actions(self) -> List[Action]:
        """
        Return all registered actions.
        """

        return list(self.actions.values())
```

Ahora registramos las acciones:

```python
action_registry = ActionRegistry()

action_registry.register(list_files_action)
action_registry.register(read_file_action)
action_registry.register(terminate_action)
```

Esto permite que el agente trabaje de forma genérica.

En vez de tener un código así:

```python
if tool_name == "list_files":
    result = list_files()
elif tool_name == "read_file":
    result = read_file(file_name)
elif tool_name == "terminate":
    result = terminate(message)
```

Podemos hacer esto:

```python
action = action_registry.get_action(tool_name)
result = action.execute(**args)
```

Ese cambio parece pequeño, pero es una mejora arquitectónica muy grande.

Significa que el Agent Loop no necesita conocer cada herramienta específica. Solo necesita saber cómo buscar una acción y ejecutarla.

---

## Paso 5, preparar el Environment

El Environment es quien ejecuta acciones y devuelve resultados formateados.

```python
import time
import traceback
from typing import Any


class Environment:
    """
    Executes actions and formats their results.

    The environment is the bridge between the agent's abstract action choice
    and the real world where the action actually happens.
    """

    def execute_action(self, action: Action, args: dict) -> dict:
        """
        Execute an action safely and return a structured result.
        """

        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as exc:
            return {
                "tool_executed": False,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }

    def format_result(self, result: Any) -> dict:
        """
        Wrap the raw result in metadata.
        """

        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
```

Este diseño tiene varias ventajas:

1. Los errores se capturan en un único sitio.
2. Todos los resultados tienen una estructura parecida.
3. El agente puede guardar resultados consistentes en memoria.
4. Más adelante podemos crear otros entornos.

Por ejemplo:

```text
LocalFileEnvironment
GitHubEnvironment
DjangoProjectEnvironment
GoogleDriveEnvironment
DatabaseEnvironment
```

La acción `read_file` puede mantener el mismo nombre, pero el entorno puede cambiar totalmente cómo se ejecuta.

---

## Paso 6, preparar el AgentLanguage

En este capítulo no vamos a implementar a fondo `AgentLanguage`, porque merece su propio capítulo.

Pero sí necesitamos entender su responsabilidad.

`AgentLanguage` hace dos cosas:

1. Construye el prompt que se manda al modelo.
2. Parsea la respuesta del modelo para extraer la acción elegida.

Podríamos imaginar una interfaz así:

```python
class AgentLanguage:
    """
    Responsible for formatting prompts and parsing model responses.
    """

    def construct_prompt(self, actions, environment, goals, memory):
        raise NotImplementedError

    def parse_response(self, response: str) -> dict:
        raise NotImplementedError
```

Para una primera versión sencilla, podríamos usar JSON.

El modelo debería responder con algo así:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "main.py"
  }
}
```

Entonces `parse_response` convertiría ese texto en un diccionario de Python:

```python
{
    "tool": "read_file",
    "args": {
        "file_name": "main.py"
    }
}
```

En sistemas modernos, muchas veces esto se hace con function calling o tool calling. Pero la idea de arquitectura es la misma.

El agente no debería tener lógica mezclada para cada proveedor de IA. Por eso existe `AgentLanguage`.

Así podríamos tener:

```text
JsonAgentLanguage
OpenAIFunctionCallingLanguage
OllamaJsonLanguage
LiteLLMToolCallingLanguage
```

El Agent Loop seguiría siendo el mismo.

---

## Paso 7, crear el Agent

Ahora juntamos todas las piezas en una clase `Agent`.

```python
import json
from typing import Callable, Optional


class Memory:
    """
    Stores the conversation and tool results used by the agent loop.
    """

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict) -> None:
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None):
        if limit is None:
            return self.items
        return self.items[-limit:]
```

Ahora la clase `Agent`:

```python
class Agent:
    """
    Reusable GAME agent.

    The agent owns the loop, but delegates responsibilities to the GAME components.
    """

    def __init__(
        self,
        goals,
        agent_language,
        action_registry: ActionRegistry,
        generate_response: Callable,
        environment: Environment,
    ):
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, goals, memory: Memory, actions: ActionRegistry):
        """
        Build the prompt using goals, memory, actions and environment.
        """

        return self.agent_language.construct_prompt(
            actions=actions.get_actions(),
            environment=self.environment,
            goals=goals,
            memory=memory,
        )

    def get_action(self, response: str):
        """
        Parse the LLM response and retrieve the selected action.
        """

        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        """
        Return True if the selected action is terminal.
        """

        action_def, _ = self.get_action(response)
        return action_def.terminal

    def set_current_task(self, memory: Memory, task: str) -> None:
        """
        Store the user's task as the first memory item for this run.
        """

        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict) -> None:
        """
        Store the agent decision and the environment result.
        """

        memory.add_memory({"type": "assistant", "content": response})
        memory.add_memory({"type": "user", "content": json.dumps(result)})

    def prompt_llm_for_action(self, full_prompt):
        """
        Send the prompt to the selected LLM integration.
        """

        return self.generate_response(full_prompt)

    def run(self, user_input: str, memory=None, max_iterations: int = 10) -> Memory:
        """
        Execute the agent loop.
        """

        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for _ in range(max_iterations):
            prompt = self.construct_prompt(self.goals, memory, self.actions)
            response = self.prompt_llm_for_action(prompt)

            action, invocation = self.get_action(response)

            if action is None:
                memory.add_memory({
                    "type": "system",
                    "content": f"Unknown action requested: {invocation['tool']}"
                })
                break

            result = self.environment.execute_action(action, invocation["args"])
            self.update_memory(memory, response, result)

            if self.should_terminate(response):
                break

        return memory
```

Esta clase es el corazón del framework.

Observa que `Agent.run()` no sabe qué significa `list_files`, `read_file` o `terminate`. Solo sabe ejecutar el ciclo general.

Eso es exactamente lo que queremos.

---

## Paso 8, ejecutar el agente

Una vez tenemos las piezas, podemos crear el agente:

```python
environment = Environment()
agent_language = JsonAgentLanguage()

file_explorer_agent = Agent(
    goals=goals,
    agent_language=agent_language,
    action_registry=action_registry,
    generate_response=generate_response,
    environment=environment,
)
```

Después lo ejecutamos:

```python
user_input = input("What would you like me to do? ")
final_memory = file_explorer_agent.run(user_input, max_iterations=10)
```

Y podríamos imprimir la memoria final:

```python
for item in final_memory.get_memories():
    print(f"\n{item['type'].upper()}: {item['content']}")
```

Esto nos permite inspeccionar lo que pasó dentro del loop.

Para aprender agentes, imprimir la memoria es muy útil porque puedes ver:

1. Qué pidió el usuario.
2. Qué acción eligió el agente.
3. Qué devolvió el entorno.
4. Cuándo decidió terminar.

---

## Código completo del ejemplo

Este código junta las piezas principales en un único archivo para estudiar el flujo.

No está pensado como la versión final de un paquete profesional. Está pensado como una versión didáctica para entender la arquitectura.

```python
"""
File Explorer Agent built with a simple GAME framework.

This example demonstrates how Goals, Actions, Memory and Environment
work together inside a reusable Agent Loop.
"""

import json
import os
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class Goal:
    """
    Represents one goal or instruction for the agent.
    """

    priority: int
    name: str
    description: str


class Action:
    """
    Represents a tool available to the agent.
    """

    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict,
        terminal: bool = False,
    ):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters
        self.terminal = terminal

    def execute(self, **args) -> Any:
        """
        Execute the underlying function.
        """

        return self.function(**args)


class ActionRegistry:
    """
    Stores the actions that the agent can use.
    """

    def __init__(self):
        self.actions = {}

    def register(self, action: Action) -> None:
        self.actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        return self.actions.get(name)

    def get_actions(self) -> List[Action]:
        return list(self.actions.values())


class Memory:
    """
    Stores user messages, agent decisions and environment results.
    """

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict) -> None:
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None):
        if limit is None:
            return self.items
        return self.items[-limit:]


class Environment:
    """
    Executes actions and returns structured results.
    """

    def execute_action(self, action: Action, args: dict) -> dict:
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as exc:
            return {
                "tool_executed": False,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }

    def format_result(self, result: Any) -> dict:
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }


class JsonAgentLanguage:
    """
    Very simple placeholder language layer.

    In a real implementation, construct_prompt would format the prompt for an LLM,
    and parse_response would parse the LLM response.
    """

    def construct_prompt(self, actions, environment, goals, memory):
        return {
            "goals": goals,
            "actions": actions,
            "memory": memory.get_memories(),
            "environment": str(environment.__class__.__name__),
        }

    def parse_response(self, response: str) -> dict:
        return json.loads(response)


class Agent:
    """
    Reusable GAME agent.
    """

    def __init__(
        self,
        goals,
        agent_language,
        action_registry: ActionRegistry,
        generate_response: Callable,
        environment: Environment,
    ):
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, goals, memory: Memory, actions: ActionRegistry):
        return self.agent_language.construct_prompt(
            actions=actions.get_actions(),
            environment=self.environment,
            goals=goals,
            memory=memory,
        )

    def get_action(self, response: str):
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        action_def, _ = self.get_action(response)
        return action_def.terminal

    def set_current_task(self, memory: Memory, task: str) -> None:
        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict) -> None:
        memory.add_memory({"type": "assistant", "content": response})
        memory.add_memory({"type": "user", "content": json.dumps(result)})

    def prompt_llm_for_action(self, full_prompt):
        return self.generate_response(full_prompt)

    def run(self, user_input: str, memory=None, max_iterations: int = 10) -> Memory:
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for _ in range(max_iterations):
            prompt = self.construct_prompt(self.goals, memory, self.actions)
            response = self.prompt_llm_for_action(prompt)

            action, invocation = self.get_action(response)

            if action is None:
                memory.add_memory({
                    "type": "system",
                    "content": f"Unknown action requested: {invocation['tool']}"
                })
                break

            result = self.environment.execute_action(action, invocation["args"])
            self.update_memory(memory, response, result)

            if self.should_terminate(response):
                break

        return memory


# Tool functions

def list_files() -> List[str]:
    """
    List files and folders in the current directory.
    """

    return os.listdir(".")


def read_file(file_name: str) -> str:
    """
    Read a text file from the current directory.
    """

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except UnicodeDecodeError:
        return f"Error: {file_name} could not be decoded as UTF-8 text."
    except Exception as exc:
        return f"Error: {str(exc)}"


def terminate(message: str) -> str:
    """
    End the agent loop with a final message.
    """

    return message


# Example LLM function for demonstration only

def generate_response(prompt):
    """
    Fake response generator used only for demonstration.

    In a real agent, this would call an LLM such as Ollama, OpenAI, Anthropic
    or a LiteLLM compatible provider.
    """

    memories = prompt["memory"]

    if len(memories) == 1:
        return json.dumps({"tool": "list_files", "args": {}})

    if len(memories) == 3:
        return json.dumps({"tool": "terminate", "args": {"message": "I listed the files and completed the task."}})

    return json.dumps({"tool": "terminate", "args": {"message": "Task completed."}})


# Main execution

def main():
    goals = [
        Goal(
            priority=1,
            name="Explore Files",
            description="Explore files in the current directory by listing and reading them when needed.",
        ),
        Goal(
            priority=2,
            name="Terminate",
            description="Terminate the session when the task is complete with a helpful summary.",
        ),
    ]

    action_registry = ActionRegistry()

    action_registry.register(Action(
        name="list_files",
        function=list_files,
        description="Returns a list of files and folders in the current directory.",
        parameters={"type": "object", "properties": {}, "required": []},
        terminal=False,
    ))

    action_registry.register(Action(
        name="read_file",
        function=read_file,
        description="Reads the content of a specified file in the current directory.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to read."
                }
            },
            "required": ["file_name"],
        },
        terminal=False,
    ))

    action_registry.register(Action(
        name="terminate",
        function=terminate,
        description="Terminates the agent loop and returns a final message.",
        parameters={
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Final message for the user."
                }
            },
            "required": ["message"],
        },
        terminal=True,
    ))

    agent = Agent(
        goals=goals,
        agent_language=JsonAgentLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment(),
    )

    final_memory = agent.run(
        user_input="List the files in this directory.",
        max_iterations=10,
    )

    for item in final_memory.get_memories():
        print(f"\n{item['type'].upper()}: {item['content']}")


if __name__ == "__main__":
    main()
```

---

## Cómo fluye una ejecución real

Supongamos que el usuario escribe:

```text
Dime qué archivos hay en este directorio.
```

La memoria inicial sería:

```json
[
  {
    "type": "user",
    "content": "Dime qué archivos hay en este directorio."
  }
]
```

El agente construye un prompt con:

1. Goals.
2. Actions disponibles.
3. Memory actual.
4. Environment.

El LLM responde:

```json
{
  "tool": "list_files",
  "args": {}
}
```

El Agent parsea la respuesta, busca `list_files` en el ActionRegistry y se la pasa al Environment.

El Environment ejecuta:

```python
list_files()
```

Y devuelve algo así:

```json
{
  "tool_executed": true,
  "result": ["main.py", "utils.py", "README.md"],
  "timestamp": "2026-06-01T21:00:00+0100"
}
```

Después el Agent guarda dos entradas nuevas en memoria:

```json
{
  "type": "assistant",
  "content": "{\"tool\": \"list_files\", \"args\": {}}"
}
```

```json
{
  "type": "user",
  "content": "{\"tool_executed\": true, \"result\": [\"main.py\", \"utils.py\", \"README.md\"]}"
}
```

En la siguiente iteración, el agente ya sabe que existen esos archivos.

Podría decidir leer `README.md`:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "README.md"
  }
}
```

O podría terminar si la petición solo era listar archivos:

```json
{
  "tool": "terminate",
  "args": {
    "message": "The directory contains main.py, utils.py and README.md."
  }
}
```

---

## Qué ocurre en memoria durante la ejecución

La memoria es el historial operativo del agente.

No solo guarda mensajes bonitos. Guarda el proceso completo:

1. Usuario pide una tarea.
2. Agente decide una acción.
3. Environment devuelve resultado.
4. Agente decide otra acción.
5. Environment devuelve otro resultado.
6. Agente termina.

Esto hace que cada vuelta del loop tenga más información que la anterior.

Ejemplo simplificado:

```json
[
  {
    "type": "user",
    "content": "Resume los archivos Python del proyecto."
  },
  {
    "type": "assistant",
    "content": "{\"tool\": \"list_files\", \"args\": {}}"
  },
  {
    "type": "user",
    "content": "{\"tool_executed\": true, \"result\": [\"main.py\", \"utils.py\"]}"
  },
  {
    "type": "assistant",
    "content": "{\"tool\": \"read_file\", \"args\": {\"file_name\": \"main.py\"}}"
  },
  {
    "type": "user",
    "content": "{\"tool_executed\": true, \"result\": \"import utils...\"}"
  }
]
```

Esto explica por qué la memoria no puede ser ignorada.

Sin memoria, el agente podría olvidar que ya listó archivos, leer el mismo archivo varias veces o no saber qué resultados recibió.

---

## Por qué necesitamos una acción terminal

Una acción terminal es una acción que le dice al Agent Loop:

```text
La tarea ha terminado.
```

En nuestro ejemplo, esa acción es:

```python
terminate(message)
```

Y se registra así:

```python
Action(
    name="terminate",
    function=terminate,
    description="Terminates the agent loop and returns a final message.",
    parameters={...},
    terminal=True,
)
```

El método `should_terminate` comprueba si la acción elegida es terminal:

```python
def should_terminate(self, response: str) -> bool:
    action_def, _ = self.get_action(response)
    return action_def.terminal
```

Esto es importante por seguridad y control.

Sin una acción terminal, el agente solo pararía cuando se alcanzara `max_iterations`. Eso no es ideal porque el final no sería semántico. Sería simplemente un corte técnico.

Con `terminate`, el agente puede terminar de forma intencional y explicar el resultado al usuario.

---

## Errores comunes al implementar este agente

### Error 1, mezclar decisión y ejecución

Mala práctica:

```python
if response == "list files":
    os.listdir(".")
```

Aquí el loop está demasiado acoplado a herramientas concretas.

Mejor práctica:

```python
action = registry.get_action(invocation["tool"])
result = environment.execute_action(action, invocation["args"])
```

Así el loop no necesita saber los detalles de cada herramienta.

### Error 2, no validar si la acción existe

El modelo puede equivocarse y pedir una herramienta que no existe.

Ejemplo:

```json
{
  "tool": "open_file",
  "args": {
    "file_name": "main.py"
  }
}
```

Pero nuestro registry solo tiene `read_file`.

Por eso conviene comprobar:

```python
if action is None:
    memory.add_memory({
        "type": "system",
        "content": f"Unknown action requested: {invocation['tool']}"
    })
    break
```

En una versión más avanzada, podríamos devolver ese error al modelo y permitirle corregirse.

### Error 3, no limitar iteraciones

Siempre debe existir un límite:

```python
max_iterations=10
```

Esto evita bucles infinitos.

Incluso si tienes una acción terminal, el límite sigue siendo necesario como medida de seguridad.

### Error 4, guardar memoria sin estructura

Mala práctica:

```python
memory.append(response)
memory.append(result)
```

Mejor práctica:

```python
memory.add_memory({"type": "assistant", "content": response})
memory.add_memory({"type": "user", "content": json.dumps(result)})
```

La estructura ayuda a construir prompts más consistentes.

### Error 5, no separar AgentLanguage

Si mezclas dentro del Agent la lógica de prompt y parsing, luego será más difícil cambiar de proveedor.

Por ejemplo, si hoy usas JSON manual, mañana function calling y pasado mañana Ollama con formato diferente, no quieres reescribir el Agent Loop.

Por eso `AgentLanguage` merece estar separado.

---

## Cómo mejorar este agente en una versión profesional

La versión de este capítulo es didáctica. Para una versión más profesional, podríamos añadir muchas mejoras.

### 1. Validación de parámetros

Antes de ejecutar una acción, validar que los argumentos cumplen el schema.

Por ejemplo, si `read_file` requiere `file_name`, no deberíamos ejecutar si falta.

### 2. Restricción de directorio

Nunca conviene permitir que un agente lea cualquier archivo del sistema.

Mejor sería definir un directorio raíz permitido:

```python
BASE_DIR = Path("./project_files").resolve()
```

Y comprobar que cualquier archivo leído esté dentro de ese directorio.

### 3. Ignorar carpetas peligrosas o innecesarias

En proyectos reales, normalmente ignoramos:

```text
.venv
node_modules
.git
__pycache__
dist
build
.env
```

Esto evita leer contenido innecesario o sensible.

### 4. Soporte para extensiones concretas

Podríamos permitir solo:

```text
.py
.md
.txt
.json
.yaml
.yml
```

### 5. Mejor metadata en list_files

En vez de devolver solo nombres:

```json
["main.py", "utils.py"]
```

Podríamos devolver:

```json
{
  "files": [
    {
      "name": "main.py",
      "extension": ".py",
      "size_bytes": 1520,
      "modified_at": "2026-06-01T20:00:00+0100"
    }
  ],
  "total_files": 1
}
```

Eso ayuda al agente a tomar mejores decisiones.

### 6. Acción search_in_file

Una mejora natural sería añadir:

```python
search_in_file(file_name: str, search_term: str)
```

Así el agente no necesita leer archivos completos para encontrar una palabra concreta.

### 7. Acción summarize_file

Otra acción útil sería:

```python
summarize_file(file_name: str)
```

Aunque cuidado, esa acción ya implicaría llamar a un modelo o lógica de resumen.

### 8. Integración con Django

En un proyecto Django, podríamos guardar ejecuciones del agente en modelos:

```python
class AgentRun(models.Model):
    task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
```

Y cada paso:

```python
class AgentStep(models.Model):
    run = models.ForeignKey(AgentRun, on_delete=models.CASCADE)
    action_name = models.CharField(max_length=100)
    arguments = models.JSONField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

Esto permitiría auditar lo que hizo el agente.

---

## Relación con Django, APIs y proyectos reales

Este ejemplo puede parecer un script local, pero la arquitectura se parece mucho a una app profesional.

En Django podríamos tener:

| GAME | Equivalente en una app Django |
|---|---|
| Goals | Configuración del agente en base de datos o settings |
| Actions | Servicios Python, tasks, integraciones externas |
| Memory | Modelos Django, sesiones, logs, Redis, PostgreSQL |
| Environment | Sistema donde se ejecutan acciones, filesystem, GitHub, APIs |
| AgentLanguage | Adaptador para Ollama, OpenAI, LiteLLM o tool calling |
| Agent | Servicio principal que coordina el loop |

Un ejemplo profesional sería un **Django Project Documentation Agent**.

Ese agente podría tener estas acciones:

```text
list_project_files
read_project_file
search_in_project
summarize_django_app
inspect_models
inspect_urls
inspect_views
terminate
```

Y sus goals podrían ser:

```text
Ayudar al usuario a entender un proyecto Django.
Leer solo archivos relevantes.
No modificar archivos sin aprobación.
Producir resúmenes claros para documentación técnica.
Terminar cuando haya respondido a la petición del usuario.
```

Con esta arquitectura, no tendríamos que reescribir el Agent Loop. Solo cambiaríamos las acciones, los goals y el environment.

Eso es exactamente el valor del framework.

---

## Resumen del capítulo

En este capítulo hemos construido una versión práctica de un agente explorador de archivos usando GAME.

Los puntos clave son:

1. El agente no debe ser un script lleno de condicionales.
2. Los Goals definen qué intenta conseguir el agente.
3. Las Actions describen herramientas disponibles.
4. El ActionRegistry permite buscar acciones por nombre.
5. El Environment ejecuta las acciones reales y devuelve resultados estructurados.
6. La Memory guarda el historial de usuario, decisiones y resultados.
7. El AgentLanguage separa el formato de comunicación con el modelo.
8. El Agent Loop coordina todo.
9. La acción `terminate` permite terminar de forma explícita.
10. `max_iterations` protege contra bucles infinitos.

La idea más importante es esta:

```text
El Agent Loop permanece estable, mientras que los componentes GAME cambian según el agente que quieras construir.
```

Ese es el salto de un script experimental a un framework reutilizable.

---

## Próximo capítulo recomendado

El próximo capítulo debería centrarse en **AgentLanguage**, porque es una de las piezas más importantes para conectar el framework con modelos reales.

Título sugerido:

```text
04, AgentLanguage, cómo construir prompts y parsear respuestas del modelo
```

En ese capítulo podemos cubrir:

1. Qué es `AgentLanguage`.
2. Por qué no conviene mezclar prompt engineering dentro del Agent Loop.
3. Cómo construir un prompt con goals, actions y memory.
4. Cómo pedir respuestas JSON al modelo.
5. Cómo parsear respuestas.
6. Cómo manejar errores de formato.
7. Cómo adaptar esto a Ollama.
8. Cómo adaptar esto a LiteLLM.
9. Cómo se relaciona con function calling y tool calling.
10. Cómo preparar la base para agentes más profesionales.
