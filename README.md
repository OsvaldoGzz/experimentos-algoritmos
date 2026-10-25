# Comparación sencilla de algoritmos

Autor: Osvaldo González Martínez — 2043042

## Ejecutar en Windows (VS Code o PowerShell)

1. Descomprime el proyecto y abre su carpeta en VS Code.
2. Abre Terminal > Nueva terminal.
3. Instala la dependencia:

```bash
py -m pip install -r requirements.txt
```

4. Ejecuta desde la carpeta del proyecto:

```bash
py codigo/experimentos.py
```

En Linux o macOS usa `python3` en lugar de `py`. Requiere Python 3.10 o posterior.
Ejecuta como archivo, no pegues el programa en una celda o consola interactiva: utiliza procesos.
Al finalizar se regeneran las gráficas y los CSV. El ejercicio 5 tarda más porque calcula
100 óptimos exactos. Los tiempos y el speedup cambian según el equipo y su carga.

## Organización propuesta

- `codigo/experimentos.py`: los cinco ejercicios, con funciones sencillas.
- `graficas/`: ocho imágenes PNG.
- `resultados/`: tablas CSV y resumen de resultados.
- `reporte/reporte.md`: reporte con gráficas y análisis.
- `reporte/guion_video.md`: guía para una demo de menos de ocho minutos.
- `requirements.txt`: dependencia.

**La consigna recibida menciona una estructura exacta, pero no incluye el árbol de carpetas.
Esta estructura es provisional: compárala con la que entregue el docente.**

## Antes de entregar

Crea un repositorio público y sube el contenido de esta carpeta. Añade su URL al reporte.
Graba la ejecución en tu computadora y añade el enlace del video al reporte.
Las gráficas incluidas corresponden a una ejecución del entorno de preparación. Para reportar
el rendimiento de tu computadora, vuelve a ejecutar y actualiza los números del reporte con
`resultados/resumen.txt`. No interpretes los tiempos incluidos como mediciones de tu PC.

## Decisiones para poder explicarlo

Se usan distancias euclidianas, que cumplen la desigualdad triangular. El TSP siempre regresa
a la primera ciudad. La mochila es 0/1. La búsqueda 2-opt usa primera mejora y termina cuando
ninguna inversión válida reduce el costo. Recocido devuelve la mejor ruta que encontró,
no solamente la última que visitó. En MST puro se compara el **tour construido a partir del
árbol**, no el peso del árbol (un árbol no es un tour del TSP).

El óptimo de nueve ciudades se obtiene probando las 8! permutaciones restantes al fijar
la ciudad cero. No se afirma optimalidad global en los experimentos de treinta ciudades.
Las semillas hacen repetibles los datos, pero no los tiempos. El enfriamiento usa el mismo
presupuesto de 3000 movimientos, temperaturas inicial/final 30 y 0.01, y la misma ruta
inicial por ensayo. La comparación final vuelve a ejecutar todos los métodos sobre las
mismas cien instancias de nueve ciudades: no mezcla costos de tamaños distintos.
