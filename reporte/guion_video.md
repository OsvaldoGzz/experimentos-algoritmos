# Guion orientativo — aproximadamente 7 minutos

No leas todo el código. Explica la idea y muestra la función correspondiente.

- **0:00–0:35.** Muestra el repositorio público y sus carpetas. Di: «Comparo algoritmos que buscan soluciones de maneras distintas: paralelismo, decisiones voraces y mejoras de rutas».
- **0:35–1:20.** Ejecuta `py codigo/experimentos.py` en vivo. Explica que los CSV guardan mediciones y los PNG muestran resultados. Mientras corre, muestra `estimate_pi`: genera puntos y cuenta los que caen dentro de un cuarto de círculo. La proporción multiplicada por cuatro aproxima pi.
- **1:20–2:05.** Abre `e1_speedup.png`. Explica `T(1)/T(p)` y compara con la línea ideal. Di lo que realmente muestre tu ejecución, aunque usar más procesos resulte más lento.
- **2:05–2:45.** Muestra los tres objetos del reporte. Con capacidad cinco, A y B dan valor siete; C da quince. El más ligero no necesariamente aprovecha mejor la capacidad.
- **2:45–3:40.** Muestra `cambio` y `dos_opt`. «Invierto una parte de la ruta y la acepto si reduce distancia. Repito hasta que ya no encuentro una mejora». Abre las dos gráficas del ejercicio 3. Explica que óptimo local no garantiza el mejor recorrido posible.
- **3:40–4:50.** Muestra la aceptación `exp(-delta/temperatura)`. «Al principio puedo aceptar empeoramientos para salir de una solución local. Al enfriarse, eso se vuelve menos probable». Abre convergencia y tiempo/calidad. Explica los resultados, sin prometer que un esquema siempre gana.
- **4:50–6:15.** Muestra el histograma del ejercicio 5. Explica que dividiste el costo del recorrido entre el óptimo exacto de cada instancia. El uno es ideal y el dos es el límite teórico. Muestra la comparación de métodos y el efecto de mejorar MST con 2-opt.
- **6:15–7:00.** Muestra los CSV generados al acabar la ejecución. Concluye con tres ideas: más procesos no garantizan más velocidad; empezar bien puede ahorrar mejoras; combinar construcción y mejora puede producir buenas rutas.

Ensaya una vez para comprobar que ejecución y explicación caben en ocho minutos. Si tu equipo
tarda mucho, empieza ejecutando al inicio del video y usa ese tiempo para explicar los métodos.
La ejecución debe terminar y debes mostrar sus archivos; no presentes una ejecución incompleta
como finalizada. Ajusta muestras o repeticiones solo si actualizas también el reporte.
