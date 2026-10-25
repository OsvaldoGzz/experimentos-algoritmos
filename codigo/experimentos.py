"""Cinco experimentos. Ejecutar desde cualquier carpeta con Python 3.10+.
Las semillas permiten repetir los datos; los tiempos dependen del equipo.
"""
import csv
import itertools
import math
import multiprocessing as mp
import random
import statistics as st
import time
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
G = BASE / 'graficas'
R = BASE / 'resultados'
SEMILLA = 2043042


def guardar(nombre, filas):
    with (R / (nombre + '.csv')).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def figura(nombre, ylabel, xlabel='Método'):
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid(axis='y', alpha=.25)
    plt.tight_layout()
    plt.savefig(G / (nombre + '.png'), dpi=160)
    plt.close()


def contar_dentro(datos):
    cantidad, semilla = datos
    rng = random.Random(semilla)
    dentro = 0
    for _ in range(cantidad):
        x, y = rng.random(), rng.random()
        if x*x + y*y <= 1:
            dentro += 1
    return dentro


def estimate_pi(procesos, muestras=2_000_000):
    # Siempre los mismos 32 bloques: mismo trabajo y mismas muestras.
    bloques = 32
    tareas = [(muestras//bloques + (i < muestras % bloques), SEMILLA+i)
              for i in range(bloques)]
    inicio = time.perf_counter()
    # Se mide también crear y cerrar el grupo de procesos.
    with mp.get_context('spawn').Pool(procesos) as pool:
        dentro = sum(pool.map(contar_dentro, tareas))
    return 4*dentro/muestras, time.perf_counter()-inicio


def ejercicio1():
    filas = []
    for repeticion in range(3):
        orden = [1, 2, 4, 8]
        random.Random(SEMILLA+repeticion).shuffle(orden)
        for p in orden:
            pi, segundos = estimate_pi(p)
            filas.append(dict(repeticion=repeticion+1, procesos=p, pi=pi, segundos=segundos))
    guardar('e1_tiempos', filas)
    tiempos = [st.median(f['segundos'] for f in filas if f['procesos']==p) for p in [1,2,4,8]]
    speedup = [tiempos[0]/t for t in tiempos]
    plt.figure()
    plt.plot([1,2,4,8], speedup, 'o-', label='Medido')
    plt.plot([1,2,4,8], [1,2,4,8], '--', label='Ideal')
    plt.xticks([1,2,4,8]); plt.legend()
    figura('e1_speedup', 'Speedup = T(1) / T(p)', 'Procesos')
    return speedup


def mochila(objetos, capacidad, criterio):
    # Mochila 0/1: cada objeto se toma completo o no se toma.
    if criterio == 'peso':
        ordenados = sorted(objetos, key=lambda x: x[1])
    else:
        ordenados = sorted(objetos, key=lambda x: x[2]/x[1], reverse=True)
    elegidos, peso, valor = [], 0, 0
    for nombre, p, v in ordenados:
        if peso+p <= capacidad:
            elegidos.append(nombre); peso += p; valor += v
    return elegidos, peso, valor


def ejercicio2():
    objetos = [('A',2,3), ('B',3,4), ('C',5,15)]
    filas = []
    for criterio in ['peso', 'valor/peso']:
        elegidos, peso, valor = mochila(objetos, 5, criterio)
        filas.append(dict(metodo=criterio, objetos=' '.join(elegidos), peso=peso, valor=valor))
    guardar('e2_mochila', filas)
    plt.figure(); plt.bar([f['metodo'] for f in filas], [f['valor'] for f in filas])
    figura('e2_mochila', 'Valor total')


def distancias(n, semilla):
    rng = random.Random(semilla)
    puntos = [(rng.uniform(0,100), rng.uniform(0,100)) for _ in range(n)]
    return [[math.dist(a,b) for b in puntos] for a in puntos]


def costo(ruta, d):
    return sum(d[ruta[i]][ruta[(i+1)%len(ruta)]] for i in range(len(ruta)))


def vecino_cercano(d, inicio):
    ruta = [inicio]
    pendientes = set(range(len(d))) - {inicio}
    while pendientes:
        siguiente = min(pendientes, key=lambda j: (d[ruta[-1]][j], j))
        ruta.append(siguiente); pendientes.remove(siguiente)
    return ruta


def pares(n):
    # Mantener fija la primera ciudad elimina movimientos redundantes.
    return [(i,j) for i in range(1,n-1) for j in range(i+1,n)
            if not (i==1 and j==n-1)]


def cambio(ruta, i, j):
    return ruta[:i] + ruta[i:j+1][::-1] + ruta[j+1:]


def dos_opt(ruta, d):
    # Primera mejora: aceptar la primera inversión que reduzca la distancia.
    ruta = ruta[:]
    actual = costo(ruta,d)
    mejoras = 0
    while True:
        encontrada = False
        for i,j in pares(len(ruta)):
            nueva = cambio(ruta,i,j)
            valor = costo(nueva,d)
            if valor < actual-1e-10:
                ruta, actual = nueva, valor
                mejoras += 1; encontrada = True
                break
        if not encontrada:
            return ruta, mejoras


def ejercicio3():
    # 30 pares de ensayos en la misma instancia de 30 ciudades.
    d = distancias(30, SEMILLA)
    filas = []
    for ensayo in range(30):
        rng = random.Random(SEMILLA+ensayo)
        aleatoria = rng.sample(range(30),30)
        cercana = vecino_cercano(d, rng.randrange(30))
        for nombre, inicial in [('Aleatorio',aleatoria),('Vecino cercano',cercana)]:
            ruta, mejoras = dos_opt(inicial,d)
            filas.append(dict(ensayo=ensayo+1, metodo=nombre, mejoras=mejoras, costo=costo(ruta,d)))
    guardar('e3_busqueda_local',filas)
    for campo in ['mejoras','costo']:
        plt.figure()
        plt.boxplot([[f[campo] for f in filas if f['metodo']==m] for m in ['Aleatorio','Vecino cercano']], tick_labels=['Aleatorio','Vecino cercano'])
        figura('e3_'+campo, 'Mejoras aceptadas' if campo=='mejoras' else 'Distancia final')
    return filas


def recocido(inicial, d, esquema, semilla, iteraciones=3000):
    rng = random.Random(semilla)
    ruta = inicial[:]; actual = costo(ruta,d)
    mejor, mejor_costo = ruta[:], actual
    movimientos = pares(len(ruta))
    historia = [mejor_costo]
    # Mismos extremos y presupuesto para comparar solo el enfriamiento.
    t0, tf = 30.0, 0.01
    inicio = time.perf_counter()
    for k in range(iteraciones):
        progreso = k/(iteraciones-1)
        if esquema == 'Lineal':
            temperatura = t0+(tf-t0)*progreso
        else:
            temperatura = t0*(tf/t0)**progreso
        i,j = rng.choice(movimientos)
        nueva = cambio(ruta,i,j)
        valor = costo(nueva,d)
        delta = valor-actual
        if delta <= 0 or rng.random() < math.exp(-delta/temperatura):
            ruta, actual = nueva, valor
            if actual < mejor_costo:
                mejor, mejor_costo = ruta[:], actual
        historia.append(mejor_costo)
    return mejor, historia, time.perf_counter()-inicio


def ejercicio4():
    d = distancias(30,SEMILLA)
    filas = []; curvas = {}
    for esquema in ['Lineal','Exponencial']:
        historias = []
        for ensayo in range(20):
            rng = random.Random(SEMILLA+ensayo)
            inicial = rng.sample(range(30),30)
            ruta, historia, segundos = recocido(inicial,d,esquema,SEMILLA+1000+ensayo)
            historias.append(historia)
            filas.append(dict(ensayo=ensayo+1, esquema=esquema, segundos=segundos, costo=costo(ruta,d)))
        curvas[esquema] = [st.mean(col) for col in zip(*historias)]
    guardar('e4_recocido',filas)
    guardar('e4_convergencia',[dict(iteracion=k, **{s:curvas[s][k] for s in curvas}) for k in range(3001)])
    plt.figure()
    for esquema, curva in curvas.items(): plt.plot(curva,label=esquema)
    plt.legend(); figura('e4_convergencia','Mejor distancia encontrada (media de 20 ensayos)','Iteración')
    plt.figure()
    for esquema in curvas:
        datos = [f for f in filas if f['esquema']==esquema]
        plt.scatter([f['segundos'] for f in datos],[f['costo'] for f in datos],label=esquema,alpha=.7)
    plt.legend(); figura('e4_tiempo_calidad','Distancia final (menor es mejor)','Tiempo (segundos)')
    return filas


def mst_tour(d):
    # Prim sencillo; después recorrido en profundidad y retorno al inicio.
    n = len(d); visitados = {0}; arbol = [[] for _ in range(n)]
    while len(visitados) < n:
        _,a,b = min((d[a][b],a,b) for a in visitados for b in range(n) if b not in visitados)
        arbol[a].append(b); arbol[b].append(a); visitados.add(b)
    ruta = []
    def recorrer(nodo, padre):
        ruta.append(nodo)
        for hijo in arbol[nodo]:
            if hijo != padre: recorrer(hijo,nodo)
    recorrer(0,-1)
    return ruta


def optimo_exacto(d):
    # 8! = 40320 recorridos al fijar la ciudad 0; viable para 9 ciudades.
    return min(costo((0,)+p,d) for p in itertools.permutations(range(1,len(d))))


def ejercicio5():
    filas = []
    for ensayo in range(100):
        d = distancias(9,SEMILLA+ensayo)
        optimo = optimo_exacto(d)
        rng = random.Random(SEMILLA+ensayo)
        inicial = rng.sample(range(9),9)
        mst = mst_tour(d)
        local,_ = dos_opt(inicial,d)
        cercana,_ = dos_opt(vecino_cercano(d,rng.randrange(9)),d)
        mst_opt,_ = dos_opt(mst,d)
        rutas = {'MST puro':mst,'MST + 2-opt':mst_opt,'Local aleatorio':local,'Local vecino':cercana}
        for esquema in ['Lineal','Exponencial']:
            rutas['SA '+esquema] = recocido(inicial,d,esquema,SEMILLA+1000+ensayo)[0]
        for metodo,ruta in rutas.items():
            valor = costo(ruta,d)
            filas.append(dict(instancia=ensayo+1,metodo=metodo,costo=valor,optimo=optimo,razon=valor/optimo))
    guardar('e5_comparacion',filas)
    razones = [f['razon'] for f in filas if f['metodo']=='MST puro']
    plt.figure(); plt.hist(razones,bins=12,edgecolor='white'); plt.axvline(2,color='red',linestyle='--',label='Límite teórico 2')
    plt.xlim(.98,2.05); plt.legend(); figura('e5_razon','Número de instancias','Costo MST / Costo óptimo')
    nombres = list(rutas)
    plt.figure(figsize=(10,5))
    plt.boxplot([[f['costo'] for f in filas if f['metodo']==m] for m in nombres],tick_labels=nombres)
    plt.xticks(rotation=15); figura('e5_costos','Distancia final')
    return filas


def resumen(speedup, local, sa, mst):
    lineas = ['RESULTADOS MEDIDOS EN ESTE EQUIPO', 'Speedup 1, 2, 4, 8: '+str([round(s,3) for s in speedup])]
    for m in ['Aleatorio','Vecino cercano']:
        datos = [f for f in local if f['metodo']==m]
        lineas.append(f'{m}: mejoras medias {st.mean(f["mejoras"] for f in datos):.2f}; costo medio {st.mean(f["costo"] for f in datos):.2f}')
    for m in ['Lineal','Exponencial']:
        datos = [f for f in sa if f['esquema']==m]
        lineas.append(f'SA {m}: costo medio {st.mean(f["costo"] for f in datos):.2f}; tiempo medio {st.mean(f["segundos"] for f in datos):.5f} s')
    for m in dict.fromkeys(f['metodo'] for f in mst):
        datos = [f for f in mst if f['metodo']==m]
        lineas.append(f'{m}: costo medio {st.mean(f["costo"] for f in datos):.2f}; razón media {st.mean(f["razon"] for f in datos):.4f}; máxima {max(f["razon"] for f in datos):.4f}')
    texto = '\n'.join(lineas)
    (R/'resumen.txt').write_text(texto,encoding='utf-8')
    print(texto)


if __name__ == '__main__':
    mp.freeze_support()  # Necesario para multiprocesamiento en Windows.
    G.mkdir(exist_ok=True); R.mkdir(exist_ok=True)
    print('Ejercicio 1...'); speedup = ejercicio1()
    print('Ejercicio 2...'); ejercicio2()
    print('Ejercicio 3...'); local = ejercicio3()
    print('Ejercicio 4...'); sa = ejercicio4()
    print('Ejercicio 5 (100 instancias)...'); mst = ejercicio5()
    resumen(speedup,local,sa,mst)
