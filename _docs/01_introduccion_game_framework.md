# 01. Introducción al GAME Framework para diseñar agentes de IA

## Tabla de contenidos

1. [Propósito de esta guía](#1-propósito-de-esta-guía)
2. [Por qué necesitamos un framework para agentes de IA](#2-por-qué-necesitamos-un-framework-para-agentes-de-ia)
3. [Qué es un agente de IA](#3-qué-es-un-agente-de-ia)
4. [Qué es el GAME Framework](#4-qué-es-el-game-framework)
5. [Vista general de GAME](#5-vista-general-de-game)
6. [G, Goals e Instructions](#6-g-goals-e-instructions)
7. [A, Actions](#7-a-actions)
8. [M, Memory](#8-m-memory)
9. [E, Environment](#9-e-environment)
10. [Cómo GAME se conecta con el Agent Loop](#10-cómo-game-se-conecta-con-el-agent-loop)
11. [Actions y Environment, una diferencia fundamental](#11-actions-y-environment-una-diferencia-fundamental)
12. [Ejemplo conceptual, Proactive Coder Agent](#12-ejemplo-conceptual-proactive-coder-agent)
13. [Ejemplo práctico, File Explorer Agent](#13-ejemplo-práctico-file-explorer-agent)
14. [Por qué simular un agente antes de programarlo](#14-por-qué-simular-un-agente-antes-de-programarlo)
15. [Beneficios del enfoque GAME](#15-beneficios-del-enfoque-game)
16. [Errores comunes al diseñar agentes sin framework](#16-errores-comunes-al-diseñar-agentes-sin-framework)
17. [Relación con buenas prácticas de desarrollo de software](#17-relación-con-buenas-prácticas-de-desarrollo-de-software)
18. [Resumen del capítulo](#18-resumen-del-capítulo)
19. [Próximo capítulo sugerido](#19-próximo-capítulo-sugerido)

---

## 1. Propósito de esta guía

Esta guía tiene como objetivo explicar, en español y de forma progresiva, cómo diseñar agentes de inteligencia artificial usando el **GAME Framework**.

La intención no es solamente aprender una técnica aislada, sino construir una forma profesional de pensar sobre agentes de IA antes de escribir código. Cuando empezamos a trabajar con agentes, es muy tentador abrir Python, crear unas funciones, llamar a un modelo de lenguaje y esperar que el sistema funcione. Ese enfoque puede servir para experimentos pequeños, pero rápidamente se vuelve difícil de mantener.

El GAME Framework nos ayuda a evitar ese problema. Nos obliga a responder preguntas importantes desde el principio:

1. ¿Qué debe conseguir el agente?
2. ¿Qué instrucciones debe seguir?
3. ¿Qué herramientas puede usar?
4. ¿Qué información debe recordar?
5. ¿Dónde ejecuta realmente sus acciones?
6. ¿Cómo sabe cuándo debe continuar y cuándo debe terminar?

En esta primera parte vamos a centrarnos en la introducción general al framework y en sus cuatro componentes principales:

```text
G = Goals / Instructions
A = Actions
M = Memory
E = Environment
```

La idea es que este documento sirva como el primer capítulo de una guía más grande sobre construcción de agentes de IA.

---

## 2. Por qué necesitamos un framework para agentes de IA

Un agente de IA no es simplemente un chatbot. Un chatbot normalmente recibe una pregunta y genera una respuesta. Un agente, en cambio, puede tomar decisiones, elegir acciones, usar herramientas, observar resultados, actualizar su memoria y repetir el proceso hasta completar una tarea.

Esto introduce más poder, pero también más riesgo y complejidad.

Por ejemplo, imagina que queremos construir un agente capaz de analizar un proyecto Django. Este agente podría:

1. Listar los archivos del proyecto.
2. Leer `models.py`.
3. Leer `views.py`.
4. Revisar `urls.py`.
5. Detectar si hay vistas sin permisos.
6. Proponer mejoras.
7. Pedir aprobación antes de modificar código.
8. Aplicar cambios si el usuario acepta.

Si programamos todo esto de forma improvisada, podemos acabar con un script lleno de condiciones, prompts gigantes, funciones mezcladas y lógica difícil de depurar.

El problema no es que el agente use IA. El problema es que, sin arquitectura, el comportamiento del agente queda desordenado.

Un framework nos ayuda a separar responsabilidades. Esto es igual que en desarrollo web. En Django no metemos toda la aplicación en un único archivo. Separamos modelos, vistas, URLs, formularios, servicios, plantillas, permisos y configuración. Con agentes pasa algo parecido. Necesitamos separar objetivos, herramientas, memoria, entorno y loop de ejecución.

El GAME Framework nos da esa estructura.

---

## 3. Qué es un agente de IA

Un agente de IA es un sistema que usa un modelo de lenguaje para decidir qué hacer a continuación dentro de un proceso.

Una forma sencilla de entenderlo es esta:

```text
Usuario da una tarea
        ↓
El agente interpreta la tarea
        ↓
El agente decide una acción
        ↓
El entorno ejecuta la acción
        ↓
El agente observa el resultado
        ↓
El resultado se guarda en memoria
        ↓
El agente decide el siguiente paso
```

Este ciclo se repite hasta que el agente cumple su objetivo o llega a una condición de parada.

Por ejemplo, si le pedimos a un agente:

```text
Revisa este proyecto y dime qué archivos Python contiene.
```

El agente podría decidir:

```json
{
  "tool": "list_files",
  "args": {}
}
```

El entorno ejecuta esa acción y devuelve:

```json
{
  "tool_executed": true,
  "result": ["main.py", "utils.py", "models.py"]
}
```

Después el agente puede decidir leer uno de esos archivos:

```json
{
  "tool": "read_file",
  "args": {
    "file_name": "main.py"
  }
}
```

Aquí ya no estamos hablando de una simple conversación. Estamos hablando de un sistema que decide, actúa, observa y continúa.

---

## 4. Qué es el GAME Framework

El **GAME Framework** es una metodología para diseñar agentes de IA dividiendo su arquitectura en cuatro partes principales:

| Letra | Componente | Pregunta principal |
| --- | --- | --- |
| G | Goals / Instructions | ¿Qué debe conseguir el agente y cómo debe comportarse? |
| A | Actions | ¿Qué acciones puede elegir el agente? |
| M | Memory | ¿Qué información conserva el agente entre pasos? |
| E | Environment | ¿Dónde y cómo se ejecutan realmente las acciones? |

GAME no es necesariamente una librería concreta. Es una forma de diseñar. Podemos implementarlo en Python, JavaScript, Django, Flask, una aplicación de consola, una API o incluso en una simulación conversacional.

La ventaja de GAME es que nos permite pensar primero y programar después.

Antes de escribir una clase `Agent`, una función `run()` o una integración con Ollama, OpenAI, LiteLLM o cualquier otro proveedor, podemos diseñar el comportamiento del agente en papel:

```text
Goals:
Analizar un proyecto y proponer mejoras pequeñas.

Actions:
Listar archivos, leer archivos, buscar texto, proponer cambios, terminar.

Memory:
Recordar la tarea del usuario, archivos leídos, decisiones tomadas y resultados.

Environment:
Sistema de archivos local del proyecto.
```

Una vez definido eso, la implementación se vuelve mucho más clara.

---

## 5. Vista general de GAME

El framework puede visualizarse así:

```text
                 ┌──────────────────────┐
                 │        Goals         │
                 │ Qué quiere conseguir │
                 └──────────┬───────────┘
                            │
                            ↓
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│    Memory    │ →  │        Agent         │ →  │       Actions        │
│ Qué recuerda │    │ Decide el siguiente  │    │ Qué puede intentar   │
│              │ ←  │ paso del loop        │ ←  │ hacer                │
└──────────────┘    └──────────┬───────────┘    └──────────┬───────────┘
                               │                           │
                               ↓                           ↓
                    ┌──────────────────────┐    ┌──────────────────────┐
                    │     Environment      │ ←  │ Acción seleccionada  │
                    │ Ejecuta y devuelve   │    │ con argumentos       │
                    │ resultados           │    └──────────────────────┘
                    └──────────────────────┘
```

Cada componente tiene una responsabilidad clara.

Los **Goals** dirigen el comportamiento.

Las **Actions** definen qué opciones tiene el agente.

La **Memory** mantiene contexto entre iteraciones.

El **Environment** ejecuta realmente las acciones y devuelve resultados.

Esta separación es la base de un agente mantenible.

---

## 6. G, Goals e Instructions

La letra **G** representa **Goals** e **Instructions**.

Los **Goals** describen qué intenta conseguir el agente. Las **Instructions** describen cómo debe intentar conseguirlo, qué restricciones debe respetar y qué estilo de comportamiento debe seguir.

En muchos diseños, goals e instructions aparecen juntos porque ambos condicionan el comportamiento del agente.

Por ejemplo, un goal podría ser:

```text
Identificar posibles mejoras en un proyecto de software.
```

Pero eso no es suficiente. El agente necesita instrucciones:

```text
Lee primero la estructura del proyecto.
No modifiques archivos sin aprobación.
Propón cambios pequeños.
Evita romper interfaces existentes.
Termina con un resumen claro.
```

Sin estas instrucciones, el agente podría hacer algo peligroso o poco útil, como editar muchos archivos sin entender el proyecto.

### 6.1 Goals como objetivos de alto nivel

Un objetivo de alto nivel responde a la pregunta:

```text
¿Qué resultado queremos conseguir?
```

Ejemplos:

| Tipo de agente | Goal |
| --- | --- |
| Agente de documentación | Explicar cómo está organizado un proyecto |
| Agente de código | Proponer mejoras pequeñas y seguras |
| Agente de soporte | Ayudar al usuario a diagnosticar un error |
| Agente de RPA | Analizar un proceso y detectar pasos automatizables |
| Agente de archivos | Listar, leer y resumir archivos de un directorio |

### 6.2 Instructions como reglas de comportamiento

Las instrucciones responden a la pregunta:

```text
¿Cómo debe intentar cumplir el objetivo?
```

Ejemplo para un agente de código:

```text
1. Lista primero los archivos del proyecto.
2. Lee solo los archivos necesarios.
3. No leas más de cinco archivos por ejecución.
4. Propón tres mejoras pequeñas.
5. Pide confirmación antes de editar.
6. Si editas, modifica un archivo cada vez.
7. Termina con un resumen de cambios.
```

Estas instrucciones convierten un agente genérico en un agente controlado.

### 6.3 Goals con prioridad

En una implementación más formal podemos representar un goal como objeto:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Goal:
    """Representa un objetivo o instrucción del agente.

    Attributes:
        priority: Prioridad del objetivo. Un número más bajo puede significar mayor prioridad.
        name: Nombre corto del objetivo.
        description: Explicación detallada del objetivo o instrucción.
    """

    priority: int
    name: str
    description: str
```

Ejemplo:

```python
file_management_goal = Goal(
    priority=1,
    name="file_management",
    description="""
    Gestionar archivos del directorio actual:
    1. Listar archivos cuando sea necesario.
    2. Leer contenido cuando sea útil.
    3. Buscar dentro de archivos si el usuario necesita información concreta.
    4. Explicar los resultados de forma clara.
    """
)
```

Esto evita tener todas las instrucciones mezcladas en un único prompt gigante. También permite reutilizar goals entre agentes diferentes.

---

## 7. A, Actions

La letra **A** representa **Actions**.

Las acciones son las capacidades que el agente puede elegir. Son el conjunto de herramientas disponibles.

Un agente no debería poder hacer cualquier cosa. Debe tener una lista controlada de acciones.

Por ejemplo, un agente de archivos podría tener estas acciones:

```text
list_files()
read_file(file_name)
search_in_file(file_name, search_term)
terminate(message)
```

Un agente de código podría tener estas:

```text
list_project_files()
read_project_file(file_name)
edit_project_file(file_name, changes)
run_tests()
ask_user_approval(proposal)
terminate(message)
```

Un agente de investigación podría tener estas:

```text
search_web(query)
read_page(url)
summarize_page(content)
save_note(note)
terminate(message)
```

### 7.1 Las Actions son una interfaz

Una acción describe lo que el agente puede intentar hacer, pero no necesariamente contiene toda la lógica del mundo real.

Por ejemplo:

```text
read_file(file_name)
```

Esta acción significa:

```text
El agente puede pedir leer un archivo.
```

Pero no explica todavía si el archivo está en local, en GitHub, en Google Drive, en S3 o en una base de datos.

Esa diferencia la veremos al hablar de Environment.

### 7.2 Una Action como objeto

Podemos representar una acción con una clase:

```python
from typing import Any, Callable, Dict

class Action:
    """Representa una herramienta disponible para el agente.

    Cada acción contiene un nombre, una función real, una descripción,
    un esquema de parámetros y una indicación de si termina el loop.
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
        """Ejecuta la función asociada a la acción."""
        return self.function(**args)
```

Esta clase permite que cada acción tenga metadatos. No solo guardamos la función, también guardamos el nombre, la descripción, los parámetros esperados y si la acción debe cerrar el loop.

### 7.3 Parámetros como contrato

Un punto importante es que las acciones suelen describirse con un esquema de parámetros.

Ejemplo:

```python
read_file_action = Action(
    name="read_file",
    function=read_file,
    description="Lee el contenido de un archivo concreto.",
    parameters={
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Nombre del archivo que se quiere leer."
            }
        },
        "required": ["file_name"]
    },
    terminal=False
)
```

Esto funciona como un contrato entre el modelo y el sistema.

El modelo no debería inventar argumentos. Debe elegir una acción y pasar los argumentos esperados.

---

## 8. M, Memory

La letra **M** representa **Memory**.

La memoria es la información que el agente conserva entre una iteración y otra del loop.

Sin memoria, el agente no sabría qué ha hecho antes. Podría leer el mismo archivo varias veces, olvidar errores, repetir acciones o perder el objetivo original del usuario.

### 8.1 Qué puede guardar la memoria

La memoria puede guardar muchos tipos de información:

| Información | Ejemplo |
| --- | --- |
| Tarea original | “Revisa los archivos Python del proyecto” |
| Decisiones del agente | “Voy a listar archivos primero” |
| Acciones ejecutadas | `list_files()` |
| Resultados del entorno | Lista de archivos devuelta |
| Errores | Archivo no encontrado |
| Archivos ya leídos | `main.py`, `utils.py` |
| Propuestas hechas | “Añadir validación de entrada” |
| Decisiones del usuario | “Acepto la segunda propuesta” |

### 8.2 Memoria conversacional simple

Una implementación básica puede ser una lista:

```python
from typing import Dict, List, Optional

class Memory:
    """Memoria simple basada en una lista de mensajes."""

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Añade una entrada a la memoria."""
        self.items.append(memory)

    def get_memories(self, limit: Optional[int] = None) -> List[Dict]:
        """Devuelve las memorias disponibles.

        Si se proporciona limit, devuelve solo las últimas entradas.
        """
        if limit is None:
            return self.items
        return self.items[-limit:]
```

Aunque parece una clase muy simple, es una buena decisión arquitectónica.

Hoy podemos guardar memoria en una lista. Mañana podríamos guardarla en PostgreSQL, Redis, un archivo JSON, una tabla de Django o una base de datos vectorial.

Mientras el resto del agente siga usando:

```python
memory.add_memory(...)
memory.get_memories(...)
```

podemos cambiar la implementación interna sin romper el loop principal.

### 8.3 Memoria como historial del loop

En un agente tipo GAME, cada vuelta del loop suele añadir dos cosas a memoria:

```text
1. La decisión del agente.
2. El resultado de la acción ejecutada.
```

Ejemplo:

```json
{
  "type": "assistant",
  "content": "{\"tool\": \"list_files\", \"args\": {}}"
}
```

Luego:

```json
{
  "type": "user",
  "content": "{\"tool_executed\": true, \"result\": [\"main.py\", \"utils.py\"]}"
}
```

Aunque el resultado lo genera el entorno, se suele añadir como mensaje de tipo usuario o herramienta para que el modelo lo vea en la siguiente iteración.

---

## 9. E, Environment

La letra **E** representa **Environment**.

El Environment es el entorno donde las acciones se ejecutan realmente.

Si las Actions son la interfaz, el Environment es la implementación.

Por ejemplo, la acción puede ser:

```text
read_file(file_name)
```

Pero el entorno decide cómo se lee ese archivo.

Podríamos tener distintos entornos:

| Environment | Implementación de `read_file` |
| --- | --- |
| LocalFileEnvironment | Lee archivos del disco local |
| GitHubEnvironment | Lee archivos de un repositorio GitHub |
| DjangoStorageEnvironment | Lee archivos usando el storage de Django |
| S3Environment | Lee archivos desde Amazon S3 |
| MockEnvironment | Devuelve resultados simulados para pruebas |

### 9.1 Environment como puente con el mundo real

El agente decide. El entorno ejecuta.

Esto es importante porque el modelo de lenguaje no debería tener acceso directo e ilimitado al sistema. El entorno actúa como capa de control.

Ejemplo:

```python
import time
import traceback
from typing import Any

class Environment:
    """Ejecuta acciones y formatea resultados para el agente."""

    def execute_action(self, action: Action, args: dict) -> dict:
        """Ejecuta una acción y captura errores de forma controlada."""
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def format_result(self, result: Any) -> dict:
        """Devuelve el resultado con metadatos útiles."""
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }
```

Esta clase centraliza la ejecución, los errores y el formato de respuesta.

### 9.2 Por qué Environment mejora la seguridad

Separar Environment permite aplicar reglas de seguridad.

Por ejemplo:

1. Bloquear lectura fuera del directorio permitido.
2. Impedir edición de archivos sensibles.
3. Registrar todas las acciones ejecutadas.
4. Limitar el número de acciones por ejecución.
5. Validar argumentos antes de ejecutar.
6. Pedir confirmación humana antes de acciones peligrosas.

En un proyecto real, esto es fundamental.

Un agente que puede editar archivos, ejecutar comandos o llamar APIs necesita límites claros.

---

## 10. Cómo GAME se conecta con el Agent Loop

El **Agent Loop** es el motor de ejecución del agente.

GAME define las piezas. El loop las hace funcionar juntas.

Un loop básico puede verse así:

```text
1. Recibir tarea del usuario.
2. Añadir la tarea a memoria.
3. Construir un prompt con goals, actions y memory.
4. Enviar el prompt al modelo.
5. Parsear la respuesta del modelo.
6. Identificar la acción elegida.
7. Ejecutar la acción en el environment.
8. Guardar el resultado en memory.
9. Comprobar si debe terminar.
10. Repetir si no ha terminado.
```

En pseudocódigo:

```python
def run_agent(user_input):
    memory.add_memory({"type": "user", "content": user_input})

    for iteration in range(max_iterations):
        prompt = construct_prompt(goals, actions, memory)
        response = call_llm(prompt)
        invocation = parse_response(response)
        action = action_registry.get_action(invocation["tool"])
        result = environment.execute_action(action, invocation["args"])
        memory.add_memory({"type": "assistant", "content": response})
        memory.add_memory({"type": "user", "content": result})

        if action.terminal:
            break
```

Lo importante es que el loop puede permanecer igual aunque cambiemos el tipo de agente.

Podemos cambiar goals, actions, memory o environment, pero el mecanismo básico sigue siendo el mismo.

---

## 11. Actions y Environment, una diferencia fundamental

Una de las ideas más importantes de GAME es separar **qué puede hacer el agente** de **cómo se ejecuta realmente**.

### 11.1 Actions responden a “qué”

Las Actions dicen:

```text
Estas son las capacidades disponibles.
```

Ejemplo:

```text
read_file(file_name)
```

Esto significa que el agente puede pedir leer un archivo.

### 11.2 Environment responde a “cómo”

El Environment dice:

```text
Así se ejecuta esa capacidad en este contexto concreto.
```

Ejemplo:

```python
def read_file(file_name: str) -> str:
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()
```

Pero en otro entorno podría ser:

```python
def read_file(file_name: str) -> str:
    return github_client.get_file_contents(file_name)
```

La acción conceptual es la misma, pero el entorno cambia.

### 11.3 Analogía con desarrollo web

Esto se parece a una interfaz o contrato.

Imagina que en Django tienes un servicio:

```python
def send_notification(user, message):
    ...
```

Tu aplicación sabe que puede enviar notificaciones, pero la implementación puede cambiar:

| Implementación | Descripción |
| --- | --- |
| EmailNotificationService | Envía correos |
| SlackNotificationService | Envía mensajes a Slack |
| ConsoleNotificationService | Imprime en consola para pruebas |
| MockNotificationService | Simula envío durante tests |

Con agentes pasa lo mismo.

El agente sabe que puede usar `read_file`, pero el entorno decide si se lee desde local, GitHub, S3 o una base de datos.

---

## 12. Ejemplo conceptual, Proactive Coder Agent

Un ejemplo útil para entender GAME es un agente llamado **Proactive Coder**.

Este agente analiza un codebase, detecta patrones y propone mejoras pequeñas que pueda implementar con bajo riesgo.

### 12.1 Goals

```text
1. Identificar posibles mejoras en el proyecto.
2. Asegurarse de que las mejoras sean útiles y relevantes.
3. Mantener los cambios pequeños y autocontenidos.
4. Evitar romper interfaces existentes.
5. Implementar solo cambios aprobados por el usuario.
```

### 12.2 Instructions

```text
1. Elegir un archivo del proyecto.
2. Leer archivos relacionados.
3. Leer como máximo cinco archivos.
4. Proponer tres ideas implementables en dos o tres funciones.
5. Pedir al usuario que seleccione una propuesta.
6. Listar los archivos que habría que modificar.
7. Aplicar cambios archivo por archivo.
8. Terminar con un resumen.
```

### 12.3 Actions

```text
list_project_files()
read_project_file(file_name)
ask_user_approval(proposal)
edit_project_file(file_name, changes)
terminate(message)
```

### 12.4 Memory

```text
Memoria conversacional con:
1. Tarea original del usuario.
2. Archivos listados.
3. Archivos leídos.
4. Propuestas generadas.
5. Decisión del usuario.
6. Cambios aplicados.
```

### 12.5 Environment

```text
Sistema local de archivos del proyecto.
Más adelante podría cambiarse por GitHub Actions, una API o un entorno de desarrollo remoto.
```

Este diseño permite pensar el agente antes de programarlo.

---

## 13. Ejemplo práctico, File Explorer Agent

Un ejemplo más sencillo es un agente explorador de archivos.

Su tarea es ayudar al usuario a listar, leer y resumir archivos.

### 13.1 GAME del File Explorer Agent

| Componente | Diseño |
| --- | --- |
| Goals | Explorar archivos y terminar con un resumen útil |
| Actions | `list_files`, `read_file`, `terminate` |
| Memory | Historial de tarea, acciones y resultados |
| Environment | Directorio local donde se ejecuta el script |

### 13.2 Goals

```python
goals = [
    Goal(
        priority=1,
        name="Explore Files",
        description="Explorar archivos del directorio actual listándolos y leyéndolos cuando sea necesario."
    ),
    Goal(
        priority=2,
        name="Terminate",
        description="Terminar la sesión cuando la tarea esté completa con un resumen útil."
    )
]
```

### 13.3 Actions

```python
def list_files() -> list[str]:
    """Lista los archivos del directorio actual."""
    return os.listdir(".")


def read_file(file_name: str) -> str:
    """Lee el contenido de un archivo."""
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def terminate(message: str) -> str:
    """Finaliza el loop del agente con un mensaje."""
    return message
```

### 13.4 Acción terminal

La acción `terminate` debe marcarse como terminal:

```python
terminate_action = Action(
    name="terminate",
    function=terminate,
    description="Finaliza la ejecución del agente con un mensaje de resumen.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    },
    terminal=True
)
```

Esto permite que el agente termine de forma controlada.

---

## 14. Por qué simular un agente antes de programarlo

Una práctica muy útil es simular el agente en una conversación antes de implementarlo.

La simulación consiste en dar al modelo sus goals y actions, y pedirle que en cada paso responda solo con la siguiente acción. Después, nosotros actuamos como environment y devolvemos el resultado.

Ejemplo de prompt de simulación:

```text
Quiero simular un agente de IA diseñado con GAME.

Goals:
1. Listar archivos del proyecto.
2. Leer archivos relevantes.
3. Resumir cómo encajan entre sí.
4. Terminar con una conclusión útil.

Actions:
1. list_files()
2. read_file(file_name)
3. terminate(message)

En cada paso, responde solo con la acción que quieres ejecutar.
Después espera a que yo te devuelva el resultado.
```

El agente podría responder:

```json
{
  "tool": "list_files",
  "args": {}
}
```

Nosotros devolveríamos:

```json
{
  "tool_executed": true,
  "result": ["main.py", "utils.py", "README.md"]
}
```

El agente entonces decidiría el siguiente paso.

Esta simulación permite descubrir problemas antes de programar:

1. Actions insuficientes.
2. Goals demasiado vagos.
3. Falta de memoria necesaria.
4. Ausencia de una acción terminal.
5. Errores en el formato esperado.
6. Comportamientos inseguros.
7. Necesidad de pedir aprobación humana.

Simular primero ahorra tiempo porque permite validar el diseño del agente sin haber escrito todavía toda la implementación.

---

## 15. Beneficios del enfoque GAME

GAME aporta varios beneficios importantes.

### 15.1 Claridad

Cada componente tiene una responsabilidad clara.

```text
Goals dirigen.
Actions ofrecen capacidades.
Memory conserva contexto.
Environment ejecuta.
Agent Loop coordina.
```

### 15.2 Modularidad

Podemos cambiar una parte sin romperlo todo.

Por ejemplo, podemos cambiar `LocalFileEnvironment` por `GitHubEnvironment` sin cambiar la lógica principal del agente.

### 15.3 Reutilización

El mismo loop puede servir para agentes distintos.

```text
File Agent
Research Agent
Coding Agent
Django Documentation Agent
RPA Process Agent
```

Cada uno puede tener goals y actions diferentes, pero compartir la misma estructura base.

### 15.4 Escalabilidad

A medida que el agente crece, la separación de componentes evita que el código se convierta en un bloque inmanejable.

### 15.5 Seguridad

Al limitar las actions y controlar el environment, reducimos el riesgo de que el agente haga cosas no deseadas.

### 15.6 Facilidad de testing

Podemos probar actions, memory y environment por separado.

También podemos crear un `MockEnvironment` para simular respuestas sin tocar archivos reales.

---

## 16. Errores comunes al diseñar agentes sin framework

Cuando no usamos una estructura como GAME, es común caer en estos errores.

### 16.1 Prompt gigante y difícil de mantener

Todo se mete en una única instrucción enorme. Al principio funciona, pero después se vuelve difícil saber qué parte del prompt controla qué comportamiento.

### 16.2 Herramientas mezcladas con lógica del loop

El loop acaba lleno de condiciones:

```python
if tool_name == "list_files":
    ...
elif tool_name == "read_file":
    ...
elif tool_name == "edit_file":
    ...
```

Esto no escala bien.

### 16.3 Sin memoria clara

El agente no sabe qué ha hecho antes o depende de una memoria implícita mal organizada.

### 16.4 Sin acciones terminales

El agente no tiene una forma clara de terminar. Esto puede causar loops largos, repetitivos o infinitos.

### 16.5 Sin separación entre acción y ejecución

El agente mezcla la decisión con la implementación concreta. Esto hace que sea difícil cambiar de entorno.

### 16.6 Sin control de seguridad

El agente puede ejecutar acciones peligrosas sin validación suficiente.

---

## 17. Relación con buenas prácticas de desarrollo de software

GAME no es solo una técnica para IA. También refleja principios clásicos de ingeniería de software.

| Principio | Cómo aparece en GAME |
| --- | --- |
| Separation of Concerns | Goals, Actions, Memory y Environment están separados |
| Dependency Injection | El Agent recibe componentes externos en el constructor |
| Interface vs Implementation | Actions definen capacidades, Environment las ejecuta |
| Open Closed Principle | Podemos añadir actions sin reescribir el loop |
| Single Responsibility Principle | Cada clase tiene una responsabilidad principal |
| Testability | Podemos probar componentes de forma aislada |
| Reusability | El mismo loop sirve para agentes diferentes |
| Error Handling | Environment centraliza errores de ejecución |

Esto conecta directamente con desarrollo profesional.

Un agente bien diseñado no debería ser una colección de prompts sueltos. Debería ser un sistema con arquitectura.

---

## 18. Resumen del capítulo

El GAME Framework es una metodología para diseñar agentes de IA de forma estructurada.

Sus cuatro componentes son:

| Componente | Significado | Responsabilidad |
| --- | --- | --- |
| G | Goals / Instructions | Definir qué debe conseguir el agente y cómo debe comportarse |
| A | Actions | Definir qué herramientas puede elegir el agente |
| M | Memory | Guardar contexto entre iteraciones |
| E | Environment | Ejecutar acciones y devolver resultados |

La idea clave es separar diseño, decisión y ejecución.

El agente no debería ser un script improvisado. Debería tener una arquitectura donde:

```text
Los goals guían.
Las actions limitan lo que puede hacer.
La memory mantiene continuidad.
El environment conecta con el mundo real.
El loop coordina todo.
```

Esta separación permite construir agentes más claros, seguros, reutilizables y fáciles de mantener.

---

## 19. Próximo capítulo sugerido

El siguiente capítulo debería centrarse en la implementación del framework en Python.

Título sugerido:

```text
02. Implementando los componentes base del GAME Framework en Python
```

Contenido sugerido:

1. Crear la clase `Goal`.
2. Crear la clase `Action`.
3. Crear `ActionRegistry`.
4. Crear `Memory`.
5. Crear `Environment`.
6. Explicar cómo cada clase representa una parte de GAME.
7. Preparar la base para construir la clase `Agent` en el capítulo siguiente.

