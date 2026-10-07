# MCP de Unreal 5.8 + Claude Code
Tags: #unreal #mcp #claude-code #automatizacion #ue58
Volver: [[00_MOC_Unreal]] · Relacionado: [[Pipeline_ComfyUI_ClaudeCode_MCP]]

> [!warning] Desconectado el 2026-10-07 por decisión de Álvaro
> Claude **no** controla Unreal. Álvaro hace las cosas en el editor y Claude le explica cómo hacerlas y le da tips.
> Se borró `.mcp.json` del vault y el cliente `scripts/ue_mcp.js`. En `UE58_Cine_Template` se desactivaron los plugins MCP y el autostart.
> Esta nota queda solo como referencia de lo que es el plugin.

Investigado leyendo el código fuente del plugin (`Engine/Plugins/Experimental/ModelContextProtocol`) y probándolo en vivo el 2026-10-07.

## Qué es
Plugin **experimental** de Epic ("Unreal MCP", *Anthropic MCP server implementation for Unreal Engine*). Levanta un servidor HTTP **dentro del editor** al que se conecta un LLM (Claude Code) para inspeccionar y modificar el proyecto.
- Sin editor abierto no hay servidor.
- Aviso que muestra el log: lo que se envía al LLM es "Licensed Technology" bajo la EULA de UE; responsabilidad tuya que el proveedor no lo use para entrenar.

## Activarlo en un proyecto
1. `.uproject` → plugins `ModelContextProtocol` + los toolsets que quieras (`EditorToolset`, `ConfigSettingsToolset`, `NiagaraToolsets`, `PCGToolset`… o `AllToolsets`).
2. `Config/DefaultEditorPerProjectUserSettings.ini`:
   ```ini
   [/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
   bAutoStartServer=True
   ServerPortNumber=8000
   ```
   (también se cambia en Editor Preferences → Model Context Protocol, o con `-ModelContextProtocolPort=N` al lanzar).
3. Al abrir el editor, en el log: `Starting MCP server on port 8000`.

## Conectarlo a Claude Code
```bash
claude mcp add --transport http --scope project unreal http://localhost:8000/mcp
```
Crea `.mcp.json` en la raíz del vault (ya hecho). Las herramientas aparecen **al iniciar una sesión nueva** de Claude Code (hay que aprobar el servidor la primera vez).

## Cómo funciona por dentro
- Transporte MCP "streamable HTTP": `POST /mcp` (JSON-RPC), `GET /mcp` (SSE), `DELETE /mcp` (cerrar sesión).
- `initialize` devuelve cabecera **`Mcp-Session-Id`**; todas las peticiones siguientes deben llevarla (si falta → 400).
- Valida `Origin` (anti DNS-rebinding): solo localhost o sin Origin.
- Con `bEnableToolSearch=True` (default) solo expone **3 meta-tools**: `list_toolsets`, `describe_toolset`, `call_tool`. El LLM descubre el resto bajo demanda (ahorra contexto).
- (Había un cliente de prueba en Node, `scripts/ue_mcp.js`; borrado el 2026-10-07.)

## Qué puede hacer (toolsets probados con mi plantilla)
| Toolset | Para qué me sirve |
|---|---|
| `EditorAppToolset` | **CaptureViewport** (Claude "ve" la escena, con anotaciones de actores), cámara del viewport, selección, PIE, abrir editores de assets, buscar CVars |
| `SceneTools` | Cargar nivel, añadir actores desde clase/asset, buscar actores, carpetas del outliner, trazar rayos, merge de actores, level instances |
| `ActorTools` | Transformaciones, componentes, jerarquías, look_at, tags, labels |
| `ObjectTools` | Leer/escribir **cualquier propiedad** de cualquier objeto (listar, get, set, reset) |
| `AssetTools` | Buscar, cargar, guardar, duplicar, mover, borrar assets; leer/escribir ficheros de texto bajo `/Game` |
| `MaterialTools` | Crear materiales/funciones/MPC, añadir y conectar nodos, recompilar |
| `MaterialInstanceTools`, `TextureTools`, `StaticMeshTools`, `SkeletalMeshTools`, `BlueprintTools`, `DataTable`/`CurveTable` | Edición de esos tipos de asset |
| `PrimitiveTools` | Añadir cubos/esferas/conos/cilindros a un actor (blockouts) |
| `NiagaraToolset_System` | **Niagara completo**: crear sistemas desde plantilla, añadir emisores/módulos/renderers, leer y escribir inputs del stack, ver errores de compilación |
| `NiagaraToolset_Component` | Variables de usuario de un componente Niagara en el nivel |
| `PCGToolset` | Construir y modificar grafos PCG |
| `ConfigSettingsToolset` | Leer/editar secciones de config (Project Settings) |
| `ProgrammaticToolset` | `execute_tool_script`: Python **sandboxed** que solo encadena llamadas a otras tools (no es Python libre del editor) |
| `LogsToolset` | Leer el Output Log |

## Límites que encontré
- **No hay Sequencer** en los toolsets que activé (existe `SequencerAnimMixerToolset`, sin probar) → animación con keys = Python del editor.
- **No hay ejecución de Python libre ni de comandos de consola**. Para eso: script Python headless (ver abajo) o abrirlo a mano en el editor.
- Experimental: puede cambiar entre hotfixes de 5.8.

## Estrategia combinada que funciona
- **MCP** → lo interactivo: mirar la escena (CaptureViewport), colocar/ajustar actores, materiales, Niagara.
- **Python headless** → lo masivo/repetible (presets MRG, niveles, secuencias):
  `UnrealEditor-Cmd.exe <proyecto.uproject> -run=pythonscript -script="C:/ruta/script.py" -unattended`
  Ver [[UE58_Python_API_Aprendizajes]].
