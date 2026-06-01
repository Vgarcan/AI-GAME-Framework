# 02. Construcción de un Framework Simple para Agentes con GAME

## Tabla de contenidos

1. [Objetivo del capítulo](#1-objetivo-del-capítulo)
2. [De diseñar agentes a construir un framework](#2-de-diseñar-agentes-a-construir-un-framework)
3. [Por qué necesitamos un framework](#3-por-qué-necesitamos-un-framework)
4. [La idea central: el loop permanece, los componentes cambian](#4-la-idea-central-el-loop-permanece-los-componentes-cambian)
5. [Estructura general del framework](#5-estructura-general-del-framework)
6. [Componente G: Goals](#6-componente-g-goals)
7. [Componente A: Actions](#7-componente-a-actions)
8. [ActionRegistry: el registro de herramientas](#8-actionregistry-el-registro-de-herramientas)
9. [Componente M: Memory](#9-componente-m-memory)
10. [Componente E: Environment](#10-componente-e-environment)
11. [AgentLanguage: el traductor entre el agente y el modelo](#11-agentlanguage-el-traductor-entre-el-agente-y-el-modelo)
12. [La clase Agent como orquestador](#12-la-clase-agent-como-orquestador)
13. [El flujo completo de una iteración](#13-el-flujo-completo-de-una-iteración)
14. [Ejemplo conceptual: agente explorador de archivos](#14-ejemplo-conceptual-agente-explorador-de-archivos)
15. [Relación con buenas prácticas de software](#15-relación-con-buenas-prácticas-de-software)
16. [Errores comunes al construir este framework](#16-errores-comunes-al-construir-este-framework)
17. [Resumen del capítulo](#17-resumen-del-capítulo)
18. [Preparación para el siguiente capítulo](#18-preparación-para-el-siguiente-capítulo)

---

## 1. Objetivo del capítulo

En el capítulo anterior presentamos el **GAME Framework** como una forma de diseñar agentes de inteligencia artificial antes de escribir código. Vimos que GAME divide el diseño del agente en cuatro piezas principales:

| Letra | Componente | Pregunta principal |
| --- | --- | --- |
| G | Goals | ¿Qué quiere conseguir el agente y bajo qué instrucciones? |
| A | Actions | ¿Qué herramientas puede usar el agente? |
| M | Memory | ¿Qué recuerda el agente entre iteraciones? |
| E | Environment | ¿Dónde se ejecutan realmente las acciones? |

En este capítulo vamos a dar el siguiente paso. Ya no vamos a hablar solo de diseño conceptual. Vamos a empezar a traducir ese diseño a una arquitectura de código.

El objetivo no es crear todavía un agente perfecto ni una librería completa de producción. El objetivo es entender cómo podríamos construir un **framework simple y reutilizable** para agentes, donde cada componente de GAME tenga una representación clara en Python.

La idea importante es esta:

> Queremos que la forma en la que diseñamos el agente sea parecida a la forma en la que lo programamos.

Si diseñamos el agente con Goals, Actions, Memory y Environment, nuestro código debería tener clases o módulos que representen esas mismas responsabilidades.

---

## 2. De diseñar agentes a construir un framework

Cuando empiezas a crear agentes, es normal escribir algo rápido. Por ejemplo, podrías tener un script con este tipo de estructura:

```python
# Ejemplo simplificado de un agente improvisado
user_task = input("¿Qué quieres hacer? ")

while True:
    response = call_llm(user_task)

    if "list_files" in response:
        result = os.listdir(".")
    elif "read_file" in response:
        result = read_file("main.py")
    elif "finish" in response:
        break

    user_task += str(result)
```

Este tipo de código puede servir para probar una idea, pero tiene varios problemas:

1. La lógica del agente está mezclada con la ejecución de herramientas.
2. Las acciones están hardcodeadas dentro del loop.
3. La memoria no tiene una interfaz clara.
4. Es difícil cambiar de entorno, por ejemplo de archivos locales a GitHub.
5. Es difícil crear otro agente sin copiar y modificar mucho código.
6. El loop principal crece demasiado rápido.

Un framework intenta resolver este problema separando responsabilidades.

En lugar de hacer que el loop sepa todos los detalles, el loop solo debe saber hacer lo esencial:

1. Construir un prompt.
2. Pedir al modelo una decisión.
3. Interpretar la acción elegida.
4. Ejecutar la acción en un entorno.
5. Guardar el resultado en memoria.
6. Repetir o terminar.

Todo lo demás debería estar encapsulado en componentes intercambiables.

---

## 3. Por qué necesitamos un framework

Al principio, crear un framework parece añadir complejidad. En lugar de una función simple, empezamos a crear clases como `Goal`, `Action`, `Memory`, `Environment`, `ActionRegistry` y `Agent`.

La pregunta lógica es:

> ¿No estamos complicando algo que podría ser más simple?

La respuesta es: sí, al principio hay más estructura. Pero esa estructura tiene una razón. Estamos pagando una pequeña complejidad inicial para ganar claridad, reutilización y escalabilidad.

Esto es muy parecido a lo que ocurre en desarrollo web.

Podrías crear una web pequeña con un único archivo HTML, un poco de JavaScript y algo de CSS dentro del mismo documento. Para una prueba rápida, funciona. Pero si el proyecto crece, ese archivo se convierte en un problema.

Por eso usamos estructuras como:

```text
project/
    app/
        models.py
        views.py
        services.py
        urls.py
        templates/
        static/
```

No hacemos esto porque nos guste crear carpetas. Lo hacemos porque cada pieza tiene una responsabilidad.

Con agentes ocurre lo mismo. Un agente puede empezar como un script pequeño, pero si queremos crear varios agentes, conectar herramientas, usar memoria, controlar errores y cambiar de entorno, necesitamos una arquitectura.

---

## 4. La idea central: el loop permanece, los componentes cambian

La clave del framework es esta:

> El agent loop debe ser estable. Lo que debe cambiar son los componentes GAME.

Es decir, el loop principal debería ser prácticamente el mismo para un agente de archivos, un agente de investigación, un agente de código o un agente de documentación Django.

Lo que cambia son las piezas que se le conectan.

| Tipo de agente | Goals | Actions | Memory | Environment |
| --- | --- | --- | --- | --- |
| Agente de archivos | Explorar y resumir archivos | Listar, leer, buscar | Historial de archivos leídos | Sistema de archivos local |
| Agente de investigación | Buscar y resumir información | Buscar web, leer páginas, resumir | Historial de fuentes | Internet o API de búsqueda |
| Agente de código | Analizar y modificar código | Leer archivos, editar, ejecutar tests | Cambios propuestos y resultados | Repositorio local o GitHub |
| Agente Django | Documentar un proyecto | Leer modelos, vistas, urls, settings | Contexto del proyecto | Proyecto Django local |

El loop, en cambio, sigue el mismo patrón:

```text
Recibir tarea
Construir prompt
Pedir decisión al LLM
Parsear acción
Ejecutar acción
Guardar resultado
Repetir o terminar
```

Esta separación es lo que nos permite crear agentes especializados sin reescribir toda la lógica cada vez.

---

## 5. Estructura general del framework

Una versión simple del framework puede tener esta estructura conceptual:

```text
game/
    core.py
    actions.py
    memory.py
    environment.py
    language.py
    agent.py
```

Cada archivo tendría una responsabilidad clara:

| Archivo | Responsabilidad |
| --- | --- |
| `core.py` | Definir conceptos básicos como `Goal` |
| `actions.py` | Definir `Action` y `ActionRegistry` |
| `memory.py` | Definir cómo se guarda y recupera la memoria |
| `environment.py` | Definir cómo se ejecutan las acciones |
| `language.py` | Definir cómo se construyen prompts y se parsean respuestas |
| `agent.py` | Definir el loop principal del agente |

En una primera implementación, podríamos tenerlo todo en un solo archivo para aprender. Pero desde el punto de vista profesional, separar estos módulos ayuda mucho a mantener el código.

Una posible representación mental sería esta:

```text
Agent
    usa Goals
    usa ActionRegistry
    usa Memory
    usa Environment
    usa AgentLanguage
    usa generate_response
```

El agente no debería saber demasiados detalles internos. Su responsabilidad es coordinar.

---

## 6. Componente G: Goals

Los Goals representan los objetivos, instrucciones y reglas que guían al agente.

Una implementación sencilla podría ser:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Goal:
    """
    Representa un objetivo o instrucción de alto nivel para el agente.

    Attributes:
        priority: Prioridad del objetivo. Un número menor puede significar mayor prioridad.
        name: Nombre corto del objetivo.
        description: Explicación detallada del objetivo o regla.
    """

    priority: int
    name: str
    description: str
```

Usamos `@dataclass` porque `Goal` es principalmente una estructura de datos. No necesita mucha lógica interna. Solo necesita agrupar información de forma clara.

Usamos `frozen=True` para que el objeto sea inmutable después de crearlo. Esto ayuda a evitar cambios accidentales durante la ejecución.

Ejemplo:

```python
file_explorer_goal = Goal(
    priority=1,
    name="explore_files",
    description="""
    Explorar los archivos del directorio actual cuando el usuario lo solicite.
    El agente debe listar archivos antes de leerlos y debe explicar sus hallazgos
    de forma clara al finalizar.
    """
)
```

### Por qué los Goals no deberían ser solo texto suelto

Podríamos tener todos los objetivos en un único prompt enorme, pero eso se vuelve difícil de mantener.

Por ejemplo:

```python
system_prompt = """
Eres un agente que explora archivos. Debes listar archivos, leer contenido,
resumir información, no hacer cambios peligrosos, terminar cuando acabes...
"""
```

Esto funciona al principio, pero cuando el agente crece, el prompt se convierte en una pared de texto. Con objetos `Goal`, podemos ordenar, filtrar, reutilizar y combinar instrucciones.

Por ejemplo:

```python
goals = [
    Goal(1, "safety", "No modificar archivos sin aprobación del usuario."),
    Goal(2, "exploration", "Listar archivos antes de leer contenido específico."),
    Goal(3, "summary", "Terminar con un resumen claro de lo encontrado."),
]
```

Esto es más fácil de mantener y se puede convertir después en un prompt estructurado.

### Goals como qué y cómo

En este framework, la palabra `Goal` puede incluir dos cosas:

1. Qué quiere conseguir el agente.
2. Cómo debe comportarse para conseguirlo.

Ejemplo de qué:

```text
Encontrar archivos Python relevantes dentro del proyecto.
```

Ejemplo de cómo:

```text
No leer más de cinco archivos antes de producir un resumen.
```

Ambos pueden vivir como Goals porque ambos condicionan el comportamiento del agente.

---

## 7. Componente A: Actions

Las Actions representan lo que el agente puede hacer.

Una acción no es solamente una función. En el framework, una acción agrupa varias cosas:

| Parte | Significado |
| --- | --- |
| `name` | Nombre que el modelo usará para invocar la acción |
| `function` | Función Python que se ejecutará realmente |
| `description` | Explicación para que el modelo sepa cuándo usarla |
| `parameters` | Esquema de argumentos que acepta la acción |
| `terminal` | Indica si esta acción termina el loop |

Una implementación básica sería:

```python
from typing import Any, Callable, Dict


class Action:
    """
    Representa una herramienta disponible para el agente.

    Una Action describe qué puede hacer el agente y contiene la función
    Python que se ejecutará cuando el agente elija esta herramienta.
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
        Ejecuta la función asociada a la acción.

        Args:
            **args: Argumentos dinámicos definidos por el modelo.

        Returns:
            El resultado devuelto por la función asociada.
        """
        return self.function(**args)
```

### Ejemplo de acción simple

Imagina una función que lista archivos:

```python
import os
from typing import List


def list_files() -> List[str]:
    """
    Devuelve la lista de archivos en el directorio actual.
    """
    return os.listdir(".")
```

Ahora la convertimos en una Action:

```python
list_files_action = Action(
    name="list_files",
    function=list_files,
    description="Devuelve una lista de archivos en el directorio actual.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    terminal=False,
)
```

El modelo no necesita saber cómo funciona `os.listdir`. Solo necesita saber que existe una herramienta llamada `list_files`, qué hace y qué parámetros necesita.

### Ejemplo de acción con parámetros

Ahora una función para leer un archivo:

```python
def read_file(file_name: str) -> str:
    """
    Lee el contenido de un archivo de texto.

    Args:
        file_name: Nombre del archivo a leer.

    Returns:
        Contenido del archivo como texto.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()
```

La acción quedaría así:

```python
read_file_action = Action(
    name="read_file",
    function=read_file,
    description="Lee el contenido de un archivo concreto del directorio actual.",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Nombre del archivo que se quiere leer.",
            }
        },
        "required": ["file_name"],
    },
    terminal=False,
)
```

La parte de `parameters` funciona como un contrato. Define qué argumentos son válidos para esta acción.

En agentes modernos, esta idea se parece mucho al uso de **tool calling** o **function calling**. El modelo decide una herramienta y proporciona argumentos estructurados.

---

## 8. ActionRegistry: el registro de herramientas

Si tenemos muchas acciones, necesitamos una forma limpia de registrarlas y buscarlas por nombre. Para eso usamos `ActionRegistry`.

```python
from typing import List, Optional


class ActionRegistry:
    """
    Registro centralizado de acciones disponibles para un agente.

    Permite registrar acciones y recuperarlas por nombre cuando el modelo
    decide qué herramienta quiere usar.
    """

    def __init__(self):
        self.actions = {}

    def register(self, action: Action) -> None:
        """
        Registra una nueva acción.

        Args:
            action: Instancia de Action que se quiere añadir al registro.
        """
        self.actions[action.name] = action

    def get_action(self, name: str) -> Optional[Action]:
        """
        Busca una acción por nombre.

        Args:
            name: Nombre de la acción.

        Returns:
            La Action encontrada o None si no existe.
        """
        return self.actions.get(name)

    def get_actions(self) -> List[Action]:
        """
        Devuelve todas las acciones registradas.
        """
        return list(self.actions.values())
```

### Por qué esto mejora el diseño

Sin `ActionRegistry`, el loop podría acabar lleno de condicionales:

```python
if tool_name == "list_files":
    result = list_files()
elif tool_name == "read_file":
    result = read_file(**args)
elif tool_name == "search_in_file":
    result = search_in_file(**args)
elif tool_name == "terminate":
    result = terminate(**args)
```

Esto se vuelve incómodo en cuanto añadimos más herramientas.

Con `ActionRegistry`, el proceso es mucho más limpio:

```python
action = registry.get_action(tool_name)
result = action.execute(**args)
```

El loop ya no necesita saber todas las acciones posibles. Solo necesita pedir al registro la acción correspondiente.

### Ejemplo completo de registro

```python
registry = ActionRegistry()

registry.register(list_files_action)
registry.register(read_file_action)
```

Más adelante podríamos añadir nuevas acciones sin tocar el loop:

```python
registry.register(search_in_file_action)
registry.register(write_file_action)
registry.register(run_tests_action)
```

Esto es extensibilidad.

---

## 9. Componente M: Memory

La memoria permite que el agente recuerde lo que ha ocurrido en iteraciones anteriores.

Sin memoria, el agente solo vería la tarea actual. No recordaría qué archivos ya ha leído, qué errores han ocurrido, qué acción eligió antes o qué información le devolvió el entorno.

Una implementación sencilla sería:

```python
from typing import Dict, List, Optional


class Memory:
    """
    Memoria básica del agente.

    Guarda una lista de mensajes o eventos producidos durante el loop.
    Esta versión usa memoria en RAM, pero la interfaz permite cambiar
    la implementación en el futuro.
    """

    def __init__(self):
        self.items = []

    def add_memory(self, memory: Dict) -> None:
        """
        Añade una entrada a la memoria.

        Args:
            memory: Diccionario que representa un mensaje o evento.
        """
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Devuelve las memorias guardadas.

        Args:
            limit: Número máximo de memorias a devolver.

        Returns:
            Lista de entradas de memoria.
        """
        if limit is None:
            return self.items

        return self.items[-limit:]
```

### Por qué no usar directamente una lista

Podríamos hacer esto:

```python
memory = []
memory.append({"type": "user", "content": "Explora este proyecto"})
```

Pero envolver la lista en una clase tiene ventajas:

1. Podemos cambiar la forma de almacenar memoria sin cambiar el loop.
2. Podemos añadir filtros.
3. Podemos limitar el número de mensajes.
4. Podemos guardar memoria en una base de datos.
5. Podemos crear memoria vectorial más adelante.
6. Podemos añadir métodos para resumir memoria antigua.

Por ejemplo, hoy la memoria puede estar en RAM. Mañana podría estar en Django:

```python
class DatabaseMemory(Memory):
    def add_memory(self, memory: Dict) -> None:
        AgentMemory.objects.create(**memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict]:
        queryset = AgentMemory.objects.order_by("-created_at")
        if limit:
            queryset = queryset[:limit]
        return [item.to_message() for item in queryset]
```

El agente seguiría usando:

```python
memory.add_memory(...)
memory.get_memories(...)
```

Eso es abstracción.

### Memoria como lista de mensajes

Aunque internamente la memoria pueda estar en una base de datos, en un grafo o en un vector store, al final el modelo normalmente necesita recibir contexto en forma de mensajes o texto.

Por eso es útil que `get_memories()` devuelva una lista preparada para construir el prompt.

Ejemplo:

```python
memory.add_memory({"type": "user", "content": "Resume los archivos Python."})
memory.add_memory({"type": "assistant", "content": '{"tool": "list_files", "args": {}}'})
memory.add_memory({"type": "user", "content": '{"result": ["main.py", "utils.py"]}'})
```

En la siguiente iteración, el agente podrá ver que ya listó los archivos.

---

## 10. Componente E: Environment

El Environment es el puente entre el agente y el mundo real.

La Action describe qué puede hacer el agente. El Environment ejecuta esa acción realmente.

Esto es muy importante.

Una acción llamada `read_file` puede existir en diferentes entornos:

| Environment | Qué hace `read_file` realmente |
| --- | --- |
| LocalFileEnvironment | Lee un archivo del disco local |
| GitHubEnvironment | Lee un archivo desde un repositorio GitHub |
| GoogleDriveEnvironment | Lee un documento desde Google Drive |
| DjangoStorageEnvironment | Lee un archivo gestionado por Django Storage |

La acción conceptual es la misma, pero la implementación real puede cambiar.

Una implementación sencilla de Environment sería:

```python
import time
import traceback
from typing import Any, Dict


class Environment:
    """
    Ejecuta acciones y devuelve resultados estructurados.

    El Environment controla la ejecución real de las herramientas y captura
    errores para que el agente pueda continuar de forma controlada.
    """

    def execute_action(self, action: Action, args: Dict) -> Dict:
        """
        Ejecuta una acción con sus argumentos.

        Args:
            action: Action que se quiere ejecutar.
            args: Argumentos elegidos por el agente.

        Returns:
            Diccionario con el resultado o información del error.
        """
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as error:
            return {
                "tool_executed": False,
                "error": str(error),
                "traceback": traceback.format_exc(),
            }

    def format_result(self, result: Any) -> Dict:
        """
        Formatea el resultado de una acción.

        Args:
            result: Resultado devuelto por la función ejecutada.

        Returns:
            Diccionario con metadatos útiles.
        """
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
```

### Por qué el Environment devuelve diccionarios

Es mejor devolver resultados estructurados que texto suelto.

Resultado menos útil:

```text
Archivo leído correctamente.
```

Resultado más útil:

```json
{
    "tool_executed": true,
    "result": "Contenido del archivo...",
    "timestamp": "2026-06-01T21:00:00+0100"
}
```

Esto ayuda al agente a razonar mejor porque puede distinguir:

1. Si la herramienta se ejecutó o falló.
2. Cuál fue el resultado.
3. Cuándo ocurrió.
4. Qué error apareció si algo salió mal.

### El Environment también centraliza errores

En lugar de capturar errores dentro del loop principal, los capturamos en el Environment.

Esto mantiene el loop limpio.

```python
try:
    result = action.execute(**args)
except Exception as error:
    return {
        "tool_executed": False,
        "error": str(error),
        "traceback": traceback.format_exc(),
    }
```

El agente no se cae inmediatamente si una herramienta falla. Recibe un resultado de error y puede decidir qué hacer en la siguiente iteración.

---

## 11. AgentLanguage: el traductor entre el agente y el modelo

`AgentLanguage` es una pieza muy importante, aunque a veces se entiende tarde.

Su trabajo es traducir entre dos mundos:

1. El mundo interno del framework, con objetos `Goal`, `Action`, `Memory` y `Environment`.
2. El mundo del LLM, que necesita recibir prompts y devolver respuestas interpretables.

En términos simples, `AgentLanguage` hace dos cosas:

```text
Construir el prompt que se envía al modelo.
Parsear la respuesta del modelo para extraer la acción elegida.
```

Una interfaz conceptual podría ser:

```python
class AgentLanguage:
    """
    Define cómo el framework se comunica con el modelo.
    """

    def construct_prompt(self, actions, environment, goals, memory):
        """
        Construye el prompt o estructura de mensajes para el LLM.
        """
        raise NotImplementedError

    def parse_response(self, response):
        """
        Extrae la invocación de herramienta desde la respuesta del LLM.
        """
        raise NotImplementedError
```

### Por qué separar AgentLanguage

Porque no todos los modelos o proveedores trabajan igual.

Algunos modelos soportan tool calling real. Otros solo devuelven texto. Otros pueden funcionar mejor con JSON. Otros pueden requerir un formato específico.

Podríamos tener varias implementaciones:

```text
FunctionCallingAgentLanguage
JsonAgentLanguage
OllamaJsonAgentLanguage
OpenAICompatibleAgentLanguage
MarkdownActionLanguage
```

Esto encaja muy bien con tu aprendizaje de Ollama, LiteLLM y APIs compatibles con OpenAI.

El mismo agente podría usar distintas formas de comunicarse con el modelo sin cambiar el loop principal.

### Ejemplo de respuesta esperada en JSON

Un agente sin tool calling nativo podría devolver algo así:

```json
{
    "tool": "read_file",
    "args": {
        "file_name": "main.py"
    }
}
```

`AgentLanguage.parse_response()` convertiría ese texto en un diccionario Python:

```python
{
    "tool": "read_file",
    "args": {
        "file_name": "main.py"
    }
}
```

Luego el agente puede buscar `read_file` en el `ActionRegistry`.

---

## 12. La clase Agent como orquestador

La clase `Agent` une todas las piezas.

No debería contener toda la lógica del mundo. Su trabajo es orquestar.

Una versión simplificada podría ser:

```python
import json
from typing import Callable, List, Optional


class Agent:
    """
    Orquestador principal del framework.

    Ejecuta el loop del agente usando los componentes GAME:
    Goals, Actions, Memory y Environment.
    """

    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable,
        environment: Environment,
    ):
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, memory: Memory):
        """
        Construye el prompt usando AgentLanguage.
        """
        return self.agent_language.construct_prompt(
            actions=self.actions.get_actions(),
            environment=self.environment,
            goals=self.goals,
            memory=memory,
        )

    def get_action(self, response):
        """
        Interpreta la respuesta del modelo y recupera la acción registrada.
        """
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, action: Action) -> bool:
        """
        Comprueba si la acción elegida debe finalizar el loop.
        """
        return action.terminal

    def update_memory(self, memory: Memory, response: str, result: dict) -> None:
        """
        Guarda la decisión del agente y el resultado de la acción.
        """
        memory.add_memory({"type": "assistant", "content": response})
        memory.add_memory({"type": "user", "content": json.dumps(result)})

    def run(self, user_input: str, memory: Optional[Memory] = None, max_iterations: int = 10) -> Memory:
        """
        Ejecuta el agent loop.

        Args:
            user_input: Tarea inicial del usuario.
            memory: Memoria opcional existente.
            max_iterations: Límite máximo de iteraciones para evitar loops infinitos.

        Returns:
            Memoria final después de ejecutar el agente.
        """
        memory = memory or Memory()
        memory.add_memory({"type": "user", "content": user_input})

        for _ in range(max_iterations):
            prompt = self.construct_prompt(memory)
            response = self.generate_response(prompt)

            action, invocation = self.get_action(response)

            if action is None:
                memory.add_memory({
                    "type": "system",
                    "content": "Error: la acción solicitada no existe en el registro.",
                })
                break

            result = self.environment.execute_action(action, invocation["args"])
            self.update_memory(memory, response, result)

            if self.should_terminate(action):
                break

        return memory
```

### Qué hace realmente Agent

La clase `Agent` no debería saber cómo listar archivos, cómo llamar a GitHub, cómo guardar memoria en PostgreSQL o cómo parsear todos los formatos posibles.

Solo coordina:

```text
Prompt
Respuesta
Acción
Ejecución
Memoria
Terminación
```

Esto es una buena señal de diseño. La clase principal tiene una responsabilidad clara.

---

## 13. El flujo completo de una iteración

Una sola vuelta del loop ocurre así:

```text
1. Memory entrega el contexto actual.
2. Goals indican qué debe intentar conseguir el agente.
3. ActionRegistry entrega la lista de herramientas disponibles.
4. AgentLanguage construye el prompt.
5. generate_response envía el prompt al LLM.
6. El LLM responde con una acción y argumentos.
7. AgentLanguage parsea la respuesta.
8. ActionRegistry busca la Action correspondiente.
9. Environment ejecuta la Action.
10. Memory guarda la decisión y el resultado.
11. Agent comprueba si la acción era terminal.
12. El loop continúa o finaliza.
```

En forma de diagrama:

```text
User Task
    ↓
Memory + Goals + Actions + Environment
    ↓
AgentLanguage.construct_prompt()
    ↓
generate_response(prompt)
    ↓
LLM chooses action
    ↓
AgentLanguage.parse_response()
    ↓
ActionRegistry.get_action()
    ↓
Environment.execute_action()
    ↓
Memory.add_memory()
    ↓
Continue or terminate
```

Este flujo es la columna vertebral del framework.

---

## 14. Ejemplo conceptual: agente explorador de archivos

Para aterrizar la idea, pensemos en un agente simple que explora archivos.

### Goals

```python
goals = [
    Goal(
        priority=1,
        name="explore_files",
        description="Listar y leer archivos del directorio cuando el usuario lo pida.",
    ),
    Goal(
        priority=2,
        name="terminate",
        description="Terminar la sesión con un resumen claro cuando la tarea esté completa.",
    ),
]
```

### Funciones reales

```python
import os
from typing import List


def list_files() -> List[str]:
    """
    Lista los archivos del directorio actual.
    """
    return os.listdir(".")


def read_file(file_name: str) -> str:
    """
    Lee el contenido de un archivo.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def terminate(message: str) -> str:
    """
    Devuelve el mensaje final del agente.
    """
    return message
```

### Registro de acciones

```python
registry = ActionRegistry()

registry.register(Action(
    name="list_files",
    function=list_files,
    description="Lista los archivos del directorio actual.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    terminal=False,
))

registry.register(Action(
    name="read_file",
    function=read_file,
    description="Lee el contenido de un archivo concreto.",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Nombre del archivo que se desea leer.",
            }
        },
        "required": ["file_name"],
    },
    terminal=False,
))

registry.register(Action(
    name="terminate",
    function=terminate,
    description="Termina el loop con un mensaje final para el usuario.",
    parameters={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Resumen final de la tarea realizada.",
            }
        },
        "required": ["message"],
    },
    terminal=True,
))
```

### Creación del agente

```python
file_explorer_agent = Agent(
    goals=goals,
    agent_language=agent_language,
    action_registry=registry,
    generate_response=generate_response,
    environment=Environment(),
)
```

### Ejecución

```python
memory = file_explorer_agent.run(
    user_input="Dime qué archivos Python hay en este directorio y resume su propósito.",
    max_iterations=10,
)
```

El agente podría hacer algo como:

```text
Iteración 1:
    Acción elegida: list_files
    Resultado: ["main.py", "utils.py", "README.md"]

Iteración 2:
    Acción elegida: read_file
    Argumentos: {"file_name": "main.py"}
    Resultado: contenido de main.py

Iteración 3:
    Acción elegida: read_file
    Argumentos: {"file_name": "utils.py"}
    Resultado: contenido de utils.py

Iteración 4:
    Acción elegida: terminate
    Argumentos: {"message": "He revisado main.py y utils.py..."}
    Resultado: mensaje final
```

---

## 15. Relación con buenas prácticas de software

Este framework no es solo una técnica para agentes. También es una buena práctica de arquitectura de software.

### Separación de responsabilidades

Cada componente tiene una función clara:

| Componente | Responsabilidad |
| --- | --- |
| Goal | Definir objetivos e instrucciones |
| Action | Definir una capacidad disponible |
| ActionRegistry | Registrar y buscar acciones |
| Memory | Guardar contexto e historial |
| Environment | Ejecutar acciones y devolver resultados |
| AgentLanguage | Formatear prompts y parsear respuestas |
| Agent | Coordinar el loop |

Esto evita que una sola clase haga demasiado.

### Inyección de dependencias

La clase `Agent` recibe sus dependencias desde fuera:

```python
Agent(
    goals=goals,
    agent_language=agent_language,
    action_registry=registry,
    generate_response=generate_response,
    environment=environment,
)
```

Esto significa que podemos cambiar piezas sin modificar la clase `Agent`.

Por ejemplo, podríamos cambiar:

```python
generate_response=openai_generate_response
```

por:

```python
generate_response=ollama_generate_response
```

El loop seguiría igual.

### Extensibilidad

Para añadir una nueva herramienta, no deberíamos tocar el loop. Solo registramos una acción nueva:

```python
registry.register(Action(
    name="search_in_file",
    function=search_in_file,
    description="Busca una palabra dentro de un archivo.",
    parameters={...},
    terminal=False,
))
```

Esto es mucho mejor que editar condicionales cada vez.

### Testabilidad

Al separar componentes, es más fácil probar cada parte.

Podemos probar `Memory` sin llamar a ningún modelo.

Podemos probar `Environment` con acciones falsas.

Podemos probar `ActionRegistry` registrando herramientas dummy.

Podemos probar `AgentLanguage` con respuestas de ejemplo.

Esto es especialmente importante si algún día quieres convertir esto en un proyecto serio, reutilizable o incluso vendible.

---

## 16. Errores comunes al construir este framework

### Error 1: meter demasiada lógica dentro de Agent

La clase `Agent` no debería saber cómo funcionan todas las herramientas. Si empieza a tener muchos `if`, algo está mal.

Mala señal:

```python
if tool == "read_file":
    ...
elif tool == "search_web":
    ...
elif tool == "query_database":
    ...
```

Mejor enfoque:

```python
action = registry.get_action(tool)
result = environment.execute_action(action, args)
```

### Error 2: no definir acciones terminales

Si el agente no tiene una forma clara de terminar, puede quedar atrapado en un loop.

Por eso es útil tener una acción como:

```python
terminate(message: str)
```

Y registrarla con:

```python
terminal=True
```

Además, siempre conviene usar `max_iterations` como medida de seguridad.

### Error 3: usar memoria sin estructura

Guardar texto suelto sin formato puede dificultar que el agente razone bien.

Menos recomendable:

```python
memory.append("Leí main.py")
```

Más recomendable:

```python
memory.add_memory({
    "type": "assistant",
    "content": '{"tool": "read_file", "args": {"file_name": "main.py"}}',
})
```

O incluso mejor, usar una estructura más explícita en futuras versiones.

### Error 4: acciones con descripciones vagas

El modelo necesita saber cuándo usar cada acción.

Descripción débil:

```text
Lee cosas.
```

Descripción mejor:

```text
Lee el contenido de un archivo del directorio actual. El nombre del archivo debe haber sido obtenido previamente con list_files.
```

La calidad de las descripciones afecta directamente a la calidad de las decisiones del agente.

### Error 5: no manejar errores del entorno

Las herramientas pueden fallar. Un archivo puede no existir. Una API puede devolver error. Una base de datos puede no responder.

El framework debe devolver errores de forma estructurada:

```json
{
    "tool_executed": false,
    "error": "FileNotFoundError: main.py not found"
}
```

Así el agente puede decidir si intenta otra acción, pide aclaración o termina con una explicación.

---

## 17. Resumen del capítulo

En este capítulo hemos empezado a convertir el GAME Framework en una arquitectura de código.

La idea principal es que los componentes GAME no solo sirven para pensar. También pueden convertirse en clases y módulos reales.

Hemos visto estos componentes:

| Componente | Clase o pieza sugerida |
| --- | --- |
| Goals | `Goal` |
| Actions | `Action` |
| Registro de acciones | `ActionRegistry` |
| Memory | `Memory` |
| Environment | `Environment` |
| Lenguaje del agente | `AgentLanguage` |
| Loop principal | `Agent` |

El principio más importante es:

> El loop principal debe permanecer estable. Lo que cambia de un agente a otro son los componentes GAME.

Esto nos permite crear agentes diferentes cambiando sus objetivos, acciones, memoria, entorno o lenguaje, sin reescribir toda la lógica de ejecución.

También hemos conectado esta arquitectura con buenas prácticas profesionales como:

1. Separación de responsabilidades.
2. Inyección de dependencias.
3. Extensibilidad.
4. Testabilidad.
5. Manejo estructurado de errores.
6. Control de loops mediante acciones terminales y límites de iteración.

---

## 18. Preparación para el siguiente capítulo

En el siguiente capítulo podemos empezar a construir el framework en código de forma más práctica.

Una buena continuación sería:

```text
03. Implementación de las clases base del Framework GAME
```

En ese capítulo podemos crear una primera estructura real de proyecto:

```text
game_framework/
    game/
        __init__.py
        core.py
        actions.py
        memory.py
        environment.py
        language.py
        agent.py
    examples/
        file_explorer.py
    README.md
```

Y empezar a implementar paso a paso:

1. `Goal`
2. `Action`
3. `ActionRegistry`
4. `Memory`
5. `Environment`
6. Una primera versión de `AgentLanguage`
7. Una primera versión de `Agent`
8. Un ejemplo ejecutable con un agente explorador de archivos

La clave será mantener el código simple, comentado y fácil de entender, pero con una estructura profesional desde el principio.
