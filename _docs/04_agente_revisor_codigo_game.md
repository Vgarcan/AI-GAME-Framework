# 04, Diseño e implementación de un agente revisor de código con GAME

## Tabla de contenidos

1. [Objetivo del capítulo](#objetivo-del-capítulo)
2. [Por qué construir otro tipo de agente](#por-qué-construir-otro-tipo-de-agente)
3. [Qué agente vamos a crear](#qué-agente-vamos-a-crear)
4. [Qué problema resuelve un agente revisor de código](#qué-problema-resuelve-un-agente-revisor-de-código)
5. [Diferencia con el agente explorador de archivos](#diferencia-con-el-agente-explorador-de-archivos)
6. [Diseño GAME del agente](#diseño-game-del-agente)
7. [G, Goals e instrucciones](#g-goals-e-instrucciones)
8. [A, Actions disponibles](#a-actions-disponibles)
9. [M, Memory necesaria](#m-memory-necesaria)
10. [E, Environment del agente](#e-environment-del-agente)
11. [Flujo general del agente](#flujo-general-del-agente)
12. [Reglas de seguridad del agente](#reglas-de-seguridad-del-agente)
13. [Diseño de las clases reutilizables](#diseño-de-las-clases-reutilizables)
14. [Definición de Goals](#definición-de-goals)
15. [Funciones reales del entorno](#funciones-reales-del-entorno)
16. [Actions del agente revisor de código](#actions-del-agente-revisor-de-código)
17. [Acción para proponer mejoras](#acción-para-proponer-mejoras)
18. [Acción para pedir aprobación](#acción-para-pedir-aprobación)
19. [Acción para aplicar cambios](#acción-para-aplicar-cambios)
20. [Acción terminal](#acción-terminal)
21. [Código completo del ejemplo](#código-completo-del-ejemplo)
22. [Ejemplo de ejecución simulada](#ejemplo-de-ejecución-simulada)
23. [Qué se guarda en memoria](#qué-se-guarda-en-memoria)
24. [Errores comunes al diseñar este agente](#errores-comunes-al-diseñar-este-agente)
25. [Cómo convertirlo en un agente profesional](#cómo-convertirlo-en-un-agente-profesional)
26. [Relación con Django y desarrollo web](#relación-con-django-y-desarrollo-web)
27. [Resumen del capítulo](#resumen-del-capítulo)
28. [Próximo capítulo recomendado](#próximo-capítulo-recomendado)

---

## Objetivo del capítulo

En el capítulo anterior construimos un agente explorador de archivos. Ese agente era útil para entender cómo un agente puede listar archivos, leer contenido y terminar con un resumen.

Ahora vamos a crear otro tipo de agente usando el mismo framework.

El objetivo de este capítulo es diseñar e implementar un **agente revisor de código** usando el enfoque GAME.

Este agente no se limitará a leer archivos. Su tarea será analizar código, detectar posibles mejoras, proponer cambios pequeños y pedir aprobación antes de modificar nada.

Esto nos permite estudiar una idea muy importante en agentes de IA:

> Un agente no debería tener permiso para hacer cualquier cosa solo porque técnicamente puede hacerlo.

Un buen agente necesita límites, reglas, memoria, herramientas bien definidas y una forma clara de saber cuándo debe parar.

En este capítulo vamos a ver cómo se diseña ese comportamiento usando GAME.

---

## Por qué construir otro tipo de agente

El agente explorador de archivos nos ayudó a entender la estructura básica del framework.

Pero si solo usamos ese ejemplo, podríamos pensar que todos los agentes son simplemente herramientas de lectura.

En la práctica, muchos agentes interesantes hacen más que leer información. Por ejemplo:

1. Revisan código.
2. Proponen cambios.
3. Generan documentación.
4. Ejecutan pruebas.
5. Consultan APIs.
6. Preparan informes.
7. Comparan archivos.
8. Detectan errores.
9. Sugieren refactorizaciones.
10. Automatizan pequeñas tareas.

Por eso necesitamos otro ejemplo.

Este capítulo mostrará cómo el mismo framework puede producir un agente con un comportamiento distinto simplemente cambiando sus componentes GAME.

La clase `Agent` y el loop principal pueden seguir siendo los mismos. Lo que cambia es el diseño del agente.

---

## Qué agente vamos a crear

Vamos a diseñar un agente llamado:

```text
Code Review Agent
```

En español lo llamaremos:

```text
Agente Revisor de Código
```

Su misión será:

1. Recibir una tarea del usuario.
2. Listar archivos del proyecto.
3. Leer archivos relevantes.
4. Analizar el código.
5. Proponer mejoras pequeñas y seguras.
6. Pedir aprobación antes de editar.
7. Aplicar cambios únicamente si el usuario aprueba.
8. Terminar con un resumen claro.

Este tipo de agente es muy parecido a una versión simplificada de herramientas modernas de desarrollo asistido por IA.

La diferencia es que aquí lo vamos a diseñar desde cero, entendiendo cada pieza.

---

## Qué problema resuelve un agente revisor de código

Cuando trabajas en un proyecto de software, especialmente si estás aprendiendo o manteniendo código antiguo, es común encontrarte con preguntas como estas:

1. ¿Qué archivos son importantes?
2. ¿Dónde debería empezar a revisar?
3. ¿Hay funciones demasiado largas?
4. ¿Hay código repetido?
5. ¿Faltan validaciones?
6. ¿Hay nombres poco claros?
7. ¿Se pueden añadir comentarios o docstrings?
8. ¿Hay errores sencillos que se puedan corregir?
9. ¿Se puede mejorar la estructura sin romper nada?
10. ¿Qué cambios son seguros y pequeños?

Un agente revisor de código puede ayudarte a responder estas preguntas.

Pero debe hacerlo con cuidado.

Un mal agente podría modificar muchos archivos sin permiso, cambiar interfaces públicas, romper tests o crear cambios difíciles de revisar.

Un buen agente debería trabajar como un junior developer disciplinado:

1. Primero inspecciona.
2. Luego entiende.
3. Después propone.
4. Espera aprobación.
5. Finalmente modifica con cuidado.

Ese comportamiento es perfecto para practicar GAME.

---

## Diferencia con el agente explorador de archivos

El agente explorador de archivos tenía un objetivo sencillo:

```text
Explorar archivos y resumir contenido.
```

El agente revisor de código tiene un objetivo más delicado:

```text
Analizar código y proponer o aplicar mejoras sin romper el proyecto.
```

La diferencia principal no está solo en las herramientas. Está en las reglas.

| Aspecto | Agente explorador de archivos | Agente revisor de código |
|---|---|---|
| Tarea principal | Leer y resumir archivos | Analizar y mejorar código |
| Riesgo | Bajo | Medio |
| Puede editar | No necesariamente | Sí, pero con aprobación |
| Necesita aprobación | Normalmente no | Sí |
| Debe limitar cambios | No aplica mucho | Muy importante |
| Debe proteger interfaces | No aplica mucho | Fundamental |
| Necesita explicar cambios | Opcional | Obligatorio |

Este ejemplo nos enseña una lección importante:

> Cuanto más poder tiene un agente, más importantes son sus goals, instrucciones y límites.

---

## Diseño GAME del agente

Antes de escribir código, debemos diseñar el agente con GAME.

GAME significa:

| Letra | Componente | Pregunta principal |
|---|---|---|
| G | Goals e instrucciones | ¿Qué debe conseguir el agente y con qué reglas? |
| A | Actions | ¿Qué herramientas puede usar? |
| M | Memory | ¿Qué debe recordar durante el proceso? |
| E | Environment | ¿Dónde se ejecutan realmente las acciones? |

Vamos a aplicar esta estructura a nuestro agente revisor de código.

---

## G, Goals e instrucciones

Los goals definen qué intenta conseguir el agente.

Las instrucciones definen cómo debe intentarlo.

Para este agente podemos definir estos objetivos:

1. Revisar el código de forma segura.
2. Identificar mejoras pequeñas y concretas.
3. Evitar cambios grandes o arriesgados.
4. No modificar archivos sin aprobación del usuario.
5. Mantener las interfaces existentes.
6. Explicar claramente cualquier propuesta.
7. Terminar con un resumen útil.

Estos goals no solo dicen qué queremos. También moldean el comportamiento del agente.

Por ejemplo, no basta con decir:

```text
Mejora el código.
```

Eso es demasiado ambiguo.

Un agente podría interpretar eso como permiso para reescribir medio proyecto.

Es mejor decir:

```text
Identifica mejoras pequeñas, seguras y autocontenidas. No edites ningún archivo hasta que el usuario apruebe una propuesta concreta.
```

Este tipo de instrucción es mucho más profesional.

---

## A, Actions disponibles

Las actions definen lo que el agente puede hacer.

Para este agente necesitaremos acciones como estas:

1. `list_project_files()`, listar archivos del proyecto.
2. `read_project_file(file_name)`, leer un archivo concreto.
3. `propose_code_improvements(proposals)`, presentar mejoras al usuario.
4. `ask_user_approval(proposal_id)`, pedir aprobación para una propuesta.
5. `edit_project_file(file_name, new_content)`, modificar un archivo.
6. `terminate(message)`, terminar la ejecución.

En una primera versión podemos simplificar algunas.

Por ejemplo, `propose_code_improvements()` podría simplemente devolver una lista de propuestas al usuario. En una versión más avanzada, podría guardar esas propuestas en una base de datos o crear un objeto formal de tipo `Proposal`.

Lo importante es que cada acción tenga una responsabilidad clara.

---

## M, Memory necesaria

La memoria de este agente es más importante que en el agente explorador de archivos.

Debe recordar cosas como:

1. Qué tarea pidió el usuario.
2. Qué archivos se han listado.
3. Qué archivos se han leído.
4. Qué problemas se han encontrado.
5. Qué propuestas se han presentado.
6. Si el usuario aprobó o no una propuesta.
7. Qué archivos se han modificado.
8. Qué resultado produjo cada acción.

Sin memoria, el agente podría cometer errores como:

1. Leer el mismo archivo muchas veces.
2. Proponer cambios sin recordar qué archivo analizó.
3. Editar algo que no fue aprobado.
4. Terminar sin explicar lo que hizo.

En esta versión mantendremos una memoria sencilla basada en una lista de mensajes, igual que en capítulos anteriores.

Pero conceptualmente, este agente ya nos muestra por qué en proyectos reales podríamos necesitar una memoria más avanzada.

---

## E, Environment del agente

El environment es donde las actions se ejecutan de verdad.

En este ejemplo, el environment será local.

Eso significa que las acciones trabajarán con archivos del sistema de archivos del ordenador.

Pero el mismo diseño podría adaptarse a otros entornos:

| Environment | Qué permitiría hacer |
|---|---|
| LocalDevelopmentEnvironment | Leer y editar archivos locales |
| GitHubEnvironment | Leer archivos desde un repositorio remoto |
| DjangoProjectEnvironment | Analizar apps, modelos, vistas y urls |
| ReadOnlyEnvironment | Revisar código sin poder modificarlo |
| PullRequestEnvironment | Comentar cambios en una pull request |

Esta separación es muy importante.

La action puede llamarse igual:

```python
edit_project_file(file_name, new_content)
```

Pero el environment decide cómo se aplica ese cambio.

En local podría escribir en disco.

En GitHub podría crear un commit.

En una pull request podría añadir una sugerencia.

En un entorno de solo lectura podría rechazar la acción.

---

## Flujo general del agente

El agente debería trabajar de forma ordenada.

Un flujo razonable sería:

```text
1. Recibe la tarea del usuario.
2. Lista los archivos del proyecto.
3. Selecciona archivos relevantes.
4. Lee uno o varios archivos.
5. Analiza el contenido.
6. Propone mejoras pequeñas.
7. Pide aprobación.
8. Si el usuario aprueba, edita el archivo.
9. Si el usuario no aprueba, no modifica nada.
10. Termina con un resumen.
```

Este flujo es una versión concreta del Agent Loop.

```text
Memory + Goals + Actions
        ↓
      Prompt
        ↓
   Decisión del LLM
        ↓
      Action
        ↓
   Environment
        ↓
     Result
        ↓
     Memory
```

Cada vuelta del loop acerca al agente a su objetivo.

---

## Reglas de seguridad del agente

Como este agente puede modificar archivos, necesitamos reglas claras.

Estas reglas deberían estar dentro de los goals o instrucciones.

Reglas recomendadas:

1. No editar archivos sin aprobación explícita.
2. No modificar más de un archivo por propuesta en la versión inicial.
3. No cambiar nombres de funciones públicas sin permiso.
4. No cambiar firmas de funciones sin permiso.
5. No eliminar código sin explicar por qué.
6. No modificar archivos de configuración sensibles en la primera versión.
7. No modificar migraciones automáticamente.
8. No tocar archivos grandes sin avisar.
9. No continuar indefinidamente.
10. Terminar con un resumen de acciones tomadas.

Estas reglas no son decoración. Son parte del diseño del agente.

Un agente sin límites puede ser más peligroso que útil.

---

## Diseño de las clases reutilizables

Vamos a asumir que ya tenemos las clases base del framework:

1. `Goal`
2. `Action`
3. `ActionRegistry`
4. `Memory`
5. `Environment`
6. `AgentLanguage`
7. `Agent`

Este capítulo no intenta reconstruir todo desde cero. La idea es mostrar cómo crear un nuevo agente cambiando sus componentes.

Esto demuestra el valor del framework.

No queremos reescribir el loop.

Queremos reutilizarlo.

---

## Definición de Goals

Podemos definir los goals del agente así:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Goal:
    """
    Representa un objetivo o regla de comportamiento del agente.

    priority:
        Número usado para ordenar los goals.
        Un número más bajo puede interpretarse como mayor prioridad.

    name:
        Nombre corto del goal.

    description:
        Explicación detallada del objetivo o instrucción.
    """
    priority: int
    name: str
    description: str


code_review_goals = [
    Goal(
        priority=1,
        name="safe_code_review",
        description=(
            "Revisar el código de forma segura, identificando mejoras pequeñas, "
            "concretas y fáciles de revisar."
        )
    ),
    Goal(
        priority=2,
        name="approval_before_editing",
        description=(
            "No modificar ningún archivo hasta que el usuario apruebe una "
            "propuesta concreta de cambio."
        )
    ),
    Goal(
        priority=3,
        name="preserve_interfaces",
        description=(
            "Mantener las interfaces existentes. No cambiar nombres de funciones, "
            "argumentos, rutas o contratos públicos sin aprobación explícita."
        )
    ),
    Goal(
        priority=4,
        name="summarise_work",
        description=(
            "Terminar la sesión con un resumen claro de archivos revisados, "
            "propuestas realizadas y cambios aplicados."
        )
    ),
]
```

Fíjate en que algunos goals son objetivos y otros son restricciones.

Esto es normal.

En un agente real, los goals suelen mezclar:

1. Objetivos de negocio.
2. Reglas de seguridad.
3. Estilo de trabajo.
4. Restricciones técnicas.
5. Criterios de finalización.

---

## Funciones reales del entorno

Ahora necesitamos funciones reales.

Estas funciones son las que ejecutará el environment.

Primero necesitamos listar archivos:

```python
import os
from typing import List


def list_project_files(root_dir: str = ".") -> List[str]:
    """
    Lista archivos de un proyecto de forma sencilla.

    En una versión inicial, solo devuelve archivos del directorio actual.
    En una versión profesional, podríamos recorrer subdirectorios,
    ignorar carpetas como .git, __pycache__, node_modules o .venv,
    y filtrar por extensiones.
    """
    files = []

    for item in os.listdir(root_dir):
        full_path = os.path.join(root_dir, item)

        if os.path.isfile(full_path):
            files.append(item)

    return files
```

Después necesitamos leer archivos:

```python
def read_project_file(file_name: str) -> str:
    """
    Lee el contenido de un archivo del proyecto.

    Esta función devuelve texto porque el agente necesita enviar el contenido
    al modelo como parte del contexto.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: el archivo '{file_name}' no existe."
    except UnicodeDecodeError:
        return f"Error: el archivo '{file_name}' no se puede leer como texto UTF-8."
    except Exception as error:
        return f"Error inesperado leyendo '{file_name}': {error}"
```

También necesitamos editar archivos:

```python
def edit_project_file(file_name: str, new_content: str) -> str:
    """
    Sobrescribe el contenido de un archivo.

    En una versión real, esta función debería crear una copia de seguridad,
    mostrar un diff antes de escribir o trabajar sobre una rama Git.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(new_content)

        return f"Archivo '{file_name}' actualizado correctamente."
    except Exception as error:
        return f"Error escribiendo '{file_name}': {error}"
```

Y necesitamos terminar:

```python
def terminate(message: str) -> str:
    """
    Termina el loop del agente con un mensaje final.
    """
    return message
```

---

## Actions del agente revisor de código

Una vez que tenemos las funciones reales, debemos convertirlas en actions.

Las actions describen al agente qué puede hacer.

El código real puede ser así:

```python
from typing import Callable, Dict, Any


class Action:
    """
    Representa una herramienta disponible para el agente.

    name:
        Nombre que el modelo usará para invocar la herramienta.

    function:
        Función Python real que se ejecutará.

    description:
        Explicación para que el modelo entienda cuándo usarla.

    parameters:
        Esquema de argumentos esperados.

    terminal:
        Indica si esta acción debe terminar el loop.
    """

    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict,
        terminal: bool = False
    ):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters
        self.terminal = terminal

    def execute(self, **args) -> Any:
        """
        Ejecuta la función real asociada a esta action.
        """
        return self.function(**args)
```

Y el registry:

```python
class ActionRegistry:
    """
    Registro central de actions disponibles para un agente.
    """

    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        """
        Registra una nueva action usando su nombre como clave.
        """
        self.actions[action.name] = action

    def get_action(self, name: str):
        """
        Devuelve una action por nombre.
        """
        return self.actions.get(name)

    def get_actions(self):
        """
        Devuelve todas las actions registradas.
        """
        return list(self.actions.values())
```

---

## Acción para proponer mejoras

Una acción interesante en este agente es `propose_code_improvements`.

Esta acción no modifica archivos. Su función es estructurar propuestas.

En una primera versión puede ser muy sencilla:

```python
def propose_code_improvements(proposals: list) -> dict:
    """
    Devuelve una lista de propuestas de mejora.

    Cada propuesta debería explicar:
    1. Qué archivo afecta.
    2. Qué problema se ha encontrado.
    3. Qué cambio se recomienda.
    4. Por qué el cambio es pequeño y seguro.
    """
    return {
        "proposal_count": len(proposals),
        "proposals": proposals
    }
```

Y su action:

```python
action_registry.register(Action(
    name="propose_code_improvements",
    function=propose_code_improvements,
    description=(
        "Presenta una lista de mejoras de código pequeñas y seguras. "
        "Esta acción no modifica archivos. Solo organiza propuestas."
    ),
    parameters={
        "type": "object",
        "properties": {
            "proposals": {
                "type": "array",
                "description": "Lista de propuestas de mejora",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "file_name": {"type": "string"},
                        "problem": {"type": "string"},
                        "suggested_change": {"type": "string"},
                        "reason": {"type": "string"}
                    },
                    "required": [
                        "id",
                        "file_name",
                        "problem",
                        "suggested_change",
                        "reason"
                    ]
                }
            }
        },
        "required": ["proposals"]
    },
    terminal=False
))
```

Esta action ayuda a que el agente no pase directamente de leer código a editarlo.

Obliga a una fase intermedia de análisis y propuesta.

---

## Acción para pedir aprobación

En una conversación real, la aprobación puede venir del usuario.

En un framework local sencillo, podemos modelarla como una action:

```python
def ask_user_approval(proposal_id: str, summary: str) -> str:
    """
    Simula una petición de aprobación al usuario.

    En una aplicación real, esta función podría pausar el agente,
    mostrar la propuesta en una interfaz web y esperar una respuesta.
    """
    return (
        f"Se requiere aprobación para la propuesta {proposal_id}: {summary}. "
        "El agente debe esperar confirmación explícita antes de editar."
    )
```

Su action:

```python
action_registry.register(Action(
    name="ask_user_approval",
    function=ask_user_approval,
    description=(
        "Solicita aprobación del usuario para una propuesta concreta. "
        "Debe usarse antes de cualquier edición de archivo."
    ),
    parameters={
        "type": "object",
        "properties": {
            "proposal_id": {
                "type": "string",
                "description": "Identificador de la propuesta"
            },
            "summary": {
                "type": "string",
                "description": "Resumen claro del cambio propuesto"
            }
        },
        "required": ["proposal_id", "summary"]
    },
    terminal=False
))
```

Esta action representa un patrón muy profesional:

> El agente puede recomendar, pero no debe actuar sobre cambios sensibles sin aprobación.

---

## Acción para aplicar cambios

La action de edición es la más delicada.

Debe existir, pero con restricciones claras.

```python
action_registry.register(Action(
    name="edit_project_file",
    function=edit_project_file,
    description=(
        "Edita un archivo del proyecto reemplazando su contenido. "
        "Solo debe usarse después de aprobación explícita del usuario."
    ),
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Nombre del archivo a modificar"
            },
            "new_content": {
                "type": "string",
                "description": "Nuevo contenido completo del archivo"
            }
        },
        "required": ["file_name", "new_content"]
    },
    terminal=False
))
```

En una versión profesional, esta acción no debería sobrescribir directamente el archivo sin más.

Mejoras recomendadas:

1. Crear copia de seguridad.
2. Calcular un diff.
3. Guardar el cambio en una rama Git.
4. Ejecutar tests.
5. Permitir rollback.
6. Registrar auditoría del cambio.
7. Pedir confirmación adicional para archivos críticos.

Pero para aprender, esta versión es suficiente.

---

## Acción terminal

Todo agente necesita una forma clara de terminar.

```python
action_registry.register(Action(
    name="terminate",
    function=terminate,
    description="Termina la ejecución del agente con un resumen final.",
    parameters={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Resumen final para el usuario"
            }
        },
        "required": ["message"]
    },
    terminal=True
))
```

La propiedad importante es:

```python
terminal=True
```

Cuando el agente invoca esta action, el loop sabe que debe parar.

Esto evita agentes que continúan indefinidamente.

---

## Código completo del ejemplo

A continuación tienes una versión compacta y comentada del agente revisor de código.

Este código asume que en capítulos anteriores ya existen las piezas principales del framework, pero para que el ejemplo sea fácil de estudiar, incluye las partes necesarias.

```python
"""
Agente revisor de código usando una arquitectura inspirada en GAME.

Este ejemplo está pensado para estudiar la estructura del agente.
No debe usarse directamente sobre proyectos importantes sin añadir medidas
profesionales como backups, diffs, Git, tests y confirmación real del usuario.
"""

import os
import json
import time
import traceback
from dataclasses import dataclass
from typing import Any, Callable, Dict, List


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
    Representa una herramienta disponible para el agente.
    """

    def __init__(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict,
        terminal: bool = False
    ):
        self.name = name
        self.function = function
        self.description = description
        self.parameters = parameters
        self.terminal = terminal

    def execute(self, **args) -> Any:
        """
        Ejecuta la función Python asociada a la action.
        """
        return self.function(**args)


class ActionRegistry:
    """
    Registro de actions disponibles.
    """

    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        self.actions[action.name] = action

    def get_action(self, name: str):
        return self.actions.get(name)

    def get_actions(self):
        return list(self.actions.values())


class Memory:
    """
    Memoria simple basada en una lista de mensajes.
    """

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        self.items.append(memory)

    def get_memories(self, limit: int = None):
        if limit is None:
            return self.items

        return self.items[-limit:]


class Environment:
    """
    Ejecuta actions y devuelve resultados estructurados.
    """

    def execute_action(self, action: Action, args: dict) -> dict:
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as error:
            return {
                "tool_executed": False,
                "error": str(error),
                "traceback": traceback.format_exc()
            }

    def format_result(self, result: Any) -> dict:
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }


class SimpleJsonAgentLanguage:
    """
    Lenguaje simple para construir prompts y parsear respuestas JSON.

    En una versión real, este componente podría usar function calling,
    tool calling de OpenAI, LiteLLM, Ollama con JSON mode o cualquier
    estrategia compatible.
    """

    def construct_prompt(
        self,
        actions: List[Action],
        goals: List[Goal],
        memory: Memory
    ) -> str:
        ordered_goals = sorted(goals, key=lambda goal: goal.priority)

        goals_text = "\n".join(
            f"{goal.priority}. {goal.name}: {goal.description}"
            for goal in ordered_goals
        )

        actions_text = "\n".join(
            f"Action: {action.name}\nDescription: {action.description}\nParameters: {action.parameters}"
            for action in actions
        )

        memory_text = json.dumps(memory.get_memories(), indent=2)

        return f"""
You are a code review agent.

Goals:
{goals_text}

Available actions:
{actions_text}

Memory:
{memory_text}

Return only valid JSON using this format:
{{
  "tool": "action_name",
  "args": {{}}
}}
"""

    def parse_response(self, response: str) -> dict:
        return json.loads(response)


class Agent:
    """
    Clase principal del agente.

    El loop se mantiene igual aunque cambiemos goals, actions,
    environment o agent language.
    """

    def __init__(
        self,
        goals: List[Goal],
        agent_language: SimpleJsonAgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[str], str],
        environment: Environment
    ):
        self.goals = goals
        self.agent_language = agent_language
        self.actions = action_registry
        self.generate_response = generate_response
        self.environment = environment

    def construct_prompt(self, memory: Memory) -> str:
        return self.agent_language.construct_prompt(
            actions=self.actions.get_actions(),
            goals=self.goals,
            memory=memory
        )

    def set_current_task(self, memory: Memory, task: str):
        memory.add_memory({"type": "user", "content": task})

    def get_action(self, response: str):
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def update_memory(self, memory: Memory, response: str, result: dict):
        memory.add_memory({"type": "assistant", "content": response})
        memory.add_memory({"type": "environment", "content": result})

    def should_terminate(self, action: Action) -> bool:
        return action.terminal

    def run(self, user_input: str, memory=None, max_iterations: int = 10):
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(max_iterations):
            prompt = self.construct_prompt(memory)

            print(f"\nIteration {iteration + 1}")
            print("Agent thinking...")

            response = self.generate_response(prompt)
            print(f"Agent decision: {response}")

            action, invocation = self.get_action(response)

            if action is None:
                result = {
                    "tool_executed": False,
                    "error": f"Unknown action: {invocation.get('tool')}"
                }
                self.update_memory(memory, response, result)
                continue

            result = self.environment.execute_action(action, invocation["args"])
            print(f"Action result: {result}")

            self.update_memory(memory, response, result)

            if self.should_terminate(action):
                break

        return memory


# Funciones reales del agente

def list_project_files(root_dir: str = ".") -> List[str]:
    """
    Lista archivos simples del directorio actual.
    """
    return [
        item for item in os.listdir(root_dir)
        if os.path.isfile(os.path.join(root_dir, item))
    ]


def read_project_file(file_name: str) -> str:
    """
    Lee un archivo de texto.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: el archivo '{file_name}' no existe."
    except UnicodeDecodeError:
        return f"Error: el archivo '{file_name}' no se puede leer como UTF-8."
    except Exception as error:
        return f"Error inesperado: {error}"


def propose_code_improvements(proposals: list) -> dict:
    """
    Devuelve propuestas de mejora estructuradas.
    """
    return {
        "proposal_count": len(proposals),
        "proposals": proposals
    }


def ask_user_approval(proposal_id: str, summary: str) -> str:
    """
    Solicita aprobación para una propuesta.

    En este ejemplo solo devuelve un mensaje.
    En una aplicación real, aquí se pausaría el agente hasta recibir respuesta.
    """
    return (
        f"Aprobación requerida para {proposal_id}: {summary}. "
        "No se debe editar ningún archivo hasta recibir confirmación explícita."
    )


def edit_project_file(file_name: str, new_content: str) -> str:
    """
    Edita un archivo reemplazando todo su contenido.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(new_content)

        return f"Archivo '{file_name}' actualizado correctamente."
    except Exception as error:
        return f"Error escribiendo '{file_name}': {error}"


def terminate(message: str) -> str:
    """
    Termina el agente con un resumen.
    """
    return message


# Este generate_response es solo una simulación.
# En un proyecto real llamaría a Ollama, LiteLLM, OpenAI, Anthropic u otro modelo.
def generate_response(prompt: str) -> str:
    """
    Simulación de una respuesta del modelo.

    Esta función existe para que el ejemplo sea ejecutable sin depender de una API.
    """
    return json.dumps({
        "tool": "terminate",
        "args": {
            "message": "Simulación finalizada. Conecta esta función a un LLM real para ejecutar el agente."
        }
    })


def build_code_review_agent() -> Agent:
    """
    Construye el agente revisor de código.
    """
    goals = [
        Goal(
            priority=1,
            name="safe_code_review",
            description="Revisar código de forma segura y proponer mejoras pequeñas."
        ),
        Goal(
            priority=2,
            name="approval_before_editing",
            description="No editar archivos sin aprobación explícita del usuario."
        ),
        Goal(
            priority=3,
            name="preserve_interfaces",
            description="No romper interfaces existentes ni cambiar firmas públicas sin permiso."
        ),
        Goal(
            priority=4,
            name="final_summary",
            description="Terminar con un resumen claro del trabajo realizado."
        )
    ]

    action_registry = ActionRegistry()

    action_registry.register(Action(
        name="list_project_files",
        function=list_project_files,
        description="Lista los archivos disponibles en el proyecto.",
        parameters={
            "type": "object",
            "properties": {
                "root_dir": {"type": "string"}
            },
            "required": []
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="read_project_file",
        function=read_project_file,
        description="Lee el contenido de un archivo del proyecto.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {"type": "string"}
            },
            "required": ["file_name"]
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="propose_code_improvements",
        function=propose_code_improvements,
        description="Presenta propuestas de mejora sin modificar archivos.",
        parameters={
            "type": "object",
            "properties": {
                "proposals": {"type": "array"}
            },
            "required": ["proposals"]
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="ask_user_approval",
        function=ask_user_approval,
        description="Solicita aprobación antes de aplicar una propuesta.",
        parameters={
            "type": "object",
            "properties": {
                "proposal_id": {"type": "string"},
                "summary": {"type": "string"}
            },
            "required": ["proposal_id", "summary"]
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="edit_project_file",
        function=edit_project_file,
        description="Edita un archivo. Solo debe usarse tras aprobación explícita.",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {"type": "string"},
                "new_content": {"type": "string"}
            },
            "required": ["file_name", "new_content"]
        },
        terminal=False
    ))

    action_registry.register(Action(
        name="terminate",
        function=terminate,
        description="Termina la ejecución del agente con un resumen final.",
        parameters={
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            },
            "required": ["message"]
        },
        terminal=True
    ))

    return Agent(
        goals=goals,
        agent_language=SimpleJsonAgentLanguage(),
        action_registry=action_registry,
        generate_response=generate_response,
        environment=Environment()
    )


if __name__ == "__main__":
    agent = build_code_review_agent()
    final_memory = agent.run(
        "Revisa este proyecto y propón una mejora pequeña y segura.",
        max_iterations=5
    )

    print("\nFinal memory:")
    for item in final_memory.get_memories():
        print(item)
```

---

## Ejemplo de ejecución simulada

Una ejecución real podría verse así:

```text
Usuario:
Revisa este proyecto y propón una mejora pequeña y segura.
```

Primera decisión del agente:

```json
{
  "tool": "list_project_files",
  "args": {}
}
```

Resultado del environment:

```json
{
  "tool_executed": true,
  "result": ["main.py", "utils.py", "models.py"],
  "timestamp": "2026-06-01T21:00:00+0100"
}
```

Segunda decisión:

```json
{
  "tool": "read_project_file",
  "args": {
    "file_name": "utils.py"
  }
}
```

Resultado:

```json
{
  "tool_executed": true,
  "result": "def divide(a, b):\n    return a / b\n",
  "timestamp": "2026-06-01T21:00:02+0100"
}
```

Tercera decisión:

```json
{
  "tool": "propose_code_improvements",
  "args": {
    "proposals": [
      {
        "id": "P001",
        "file_name": "utils.py",
        "problem": "La función divide no valida división por cero.",
        "suggested_change": "Añadir una validación para b == 0 y lanzar ValueError con un mensaje claro.",
        "reason": "Es un cambio pequeño, seguro y mejora el manejo de errores."
      }
    ]
  }
}
```

Cuarta decisión:

```json
{
  "tool": "ask_user_approval",
  "args": {
    "proposal_id": "P001",
    "summary": "Añadir validación de división por cero en utils.py."
  }
}
```

El agente no debería editar hasta que el usuario apruebe.

Si el usuario aprueba, entonces podría hacer:

```json
{
  "tool": "edit_project_file",
  "args": {
    "file_name": "utils.py",
    "new_content": "def divide(a, b):\n    if b == 0:\n        raise ValueError('b cannot be zero')\n    return a / b\n"
  }
}
```

Finalmente:

```json
{
  "tool": "terminate",
  "args": {
    "message": "Revisión completada. Se revisó utils.py, se propuso añadir validación de división por cero y el cambio fue aplicado tras aprobación."
  }
}
```

---

## Qué se guarda en memoria

La memoria debería guardar una secuencia de eventos.

Por ejemplo:

```json
[
  {
    "type": "user",
    "content": "Revisa este proyecto y propón una mejora pequeña."
  },
  {
    "type": "assistant",
    "content": "{\"tool\": \"list_project_files\", \"args\": {}}"
  },
  {
    "type": "environment",
    "content": {
      "tool_executed": true,
      "result": ["main.py", "utils.py"]
    }
  },
  {
    "type": "assistant",
    "content": "{\"tool\": \"read_project_file\", \"args\": {\"file_name\": \"utils.py\"}}"
  },
  {
    "type": "environment",
    "content": {
      "tool_executed": true,
      "result": "def divide(a, b): return a / b"
    }
  }
]
```

Esto permite que el agente razone en la siguiente vuelta.

Por ejemplo, después de leer `utils.py`, el agente ya puede saber:

1. Qué archivo leyó.
2. Qué función contiene.
3. Qué riesgo detectó.
4. Qué propuesta puede hacer.

Sin memoria, cada decisión sería aislada.

Con memoria, el agente puede construir una cadena de trabajo.

---

## Errores comunes al diseñar este agente

### Error 1, permitir edición demasiado pronto

Un error típico es dar al agente una action de edición y no crear una regla clara de aprobación.

Mala instrucción:

```text
Mejora el código del proyecto.
```

Mejor instrucción:

```text
Revisa el código, propone una mejora pequeña y no edites ningún archivo hasta recibir aprobación explícita del usuario.
```

### Error 2, no limitar el tamaño del cambio

Si no limitamos el alcance, el agente puede proponer cambios demasiado grandes.

Regla recomendada:

```text
Cada propuesta debe afectar a un máximo de uno o dos archivos en la primera versión del agente.
```

### Error 3, no tener acción terminal

Sin acción terminal, el agente puede seguir leyendo archivos o proponiendo cosas indefinidamente.

La action `terminate` es necesaria.

### Error 4, no registrar qué se ha aprobado

Si el usuario aprueba una propuesta, esa aprobación debe quedar en memoria.

De lo contrario, el agente podría editar algo sin poder justificar por qué.

### Error 5, mezclar análisis y ejecución

Analizar código y editar código son pasos distintos.

Un agente profesional debería separar:

1. Lectura.
2. Análisis.
3. Propuesta.
4. Aprobación.
5. Edición.
6. Verificación.
7. Resumen.

---

## Cómo convertirlo en un agente profesional

Este ejemplo es didáctico.

Para usarlo como base profesional, habría que añadir varias mejoras.

### 1. Sistema de diff

Antes de editar, el agente debería mostrar qué va a cambiar.

Ejemplo:

```text
Antes:
def divide(a, b):
    return a / b

Después:
def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b
```

Esto ayuda al usuario a aprobar con conocimiento.

### 2. Integración con Git

El agente debería trabajar en una rama separada.

Por ejemplo:

```text
feature/agent-code-review-p001
```

Así los cambios no afectan directamente al código principal.

### 3. Backups automáticos

Antes de editar, el agente podría crear una copia:

```text
utils.py.bak
```

O guardar el contenido anterior en memoria persistente.

### 4. Ejecución de tests

Después de editar, el agente debería ejecutar tests.

Acciones posibles:

```python
run_tests()
run_linter()
run_type_checker()
```

En un proyecto Django, podría ejecutar:

```bash
python manage.py test
```

### 5. Control de archivos permitidos

No todos los archivos deberían poder editarse.

Podríamos bloquear:

1. `.env`
2. Archivos de credenciales.
3. Migraciones generadas.
4. Configuración de producción.
5. Archivos binarios.
6. Archivos muy grandes.

### 6. Interfaz web

En una aplicación Django, las propuestas podrían mostrarse en una página web.

El usuario podría ver:

1. Archivo afectado.
2. Problema detectado.
3. Cambio sugerido.
4. Diff.
5. Botón para aprobar.
6. Botón para rechazar.
7. Botón para pedir una alternativa.

Esto convertiría el agente en una herramienta usable.

---

## Relación con Django y desarrollo web

Este agente encaja muy bien con un proyecto Django.

Podrías crear una app llamada:

```text
code_reviewer
```

Dentro podrías tener:

```text
code_reviewer/
    agents/
        code_review_agent.py
    services/
        file_reader.py
        diff_builder.py
        git_service.py
        test_runner.py
    models.py
    views.py
    urls.py
    templates/
        code_reviewer/
            proposal_list.html
            proposal_detail.html
```

Modelos posibles:

```python
from django.db import models


class CodeReviewSession(models.Model):
    """
    Representa una sesión de revisión de código iniciada por el usuario.
    """
    task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)


class CodeProposal(models.Model):
    """
    Representa una propuesta generada por el agente.
    """
    session = models.ForeignKey(CodeReviewSession, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    problem = models.TextField()
    suggested_change = models.TextField()
    approved = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

Este enfoque convierte el agente en algo más que un script.

Lo convierte en una aplicación mantenible.

Y eso es importante para tu perfil como desarrollador, porque demuestra que sabes pasar de una idea de IA a una arquitectura de software real.

---

## Resumen del capítulo

En este capítulo hemos creado un segundo tipo de agente usando el mismo framework GAME.

El agente revisor de código demuestra que podemos reutilizar la arquitectura base y cambiar el comportamiento cambiando los componentes del diseño.

Hemos visto que:

1. Los goals definen objetivos y restricciones.
2. Las actions representan herramientas disponibles.
3. La memory guarda decisiones, resultados y aprobaciones.
4. El environment ejecuta realmente las acciones.
5. La edición de archivos requiere reglas de seguridad.
6. La aprobación humana es fundamental cuando el agente puede modificar código.
7. La action terminal evita loops infinitos.
8. El mismo framework puede producir agentes muy distintos.

La idea más importante es esta:

> Un agente con capacidad de modificar código debe ser diseñado con límites claros, trazabilidad y aprobación humana.

Este capítulo muestra cómo el GAME Framework ayuda a construir ese comportamiento de forma modular.

---

## Próximo capítulo recomendado

El siguiente capítulo recomendado sería:

```text
05, Simulación de agentes GAME antes de programar
```

Ese capítulo debería explicar cómo probar un diseño de agente en una conversación antes de escribir código real.

Podríamos incluir:

1. Cómo escribir un prompt de simulación.
2. Cómo actuar como environment manualmente.
3. Cómo detectar actions que faltan.
4. Cómo comprobar si los goals son demasiado vagos.
5. Cómo probar errores controlados.
6. Cómo guardar buenos y malos ejemplos.
7. Cómo convertir la simulación en tests para el agente.

Este tema es importante porque antes de programar un agente complejo, conviene comprobar si su diseño funciona.
