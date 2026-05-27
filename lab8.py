"""
Lab 8 - MM3014 Teoría de Probabilidades
Etapas 3 y 4: Simulaciones de Monte Carlo

Parámetros globales:
    N = 100  estampas distintas en el álbum
    S = 7    estampas por sobre
    R = 10,000 simulaciones
    Semilla = 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ──────────────────────────────────────────────
# Parámetros globales
# ──────────────────────────────────────────────
N      = 100       # Número de estampas distintas
S      = 7         # Estampas por sobre
R      = 10_000    # Simulaciones
SEED   = 2026
PRECIO = 9.50      # Q por sobre
BUDGET = 1_000.0   # Q presupuesto total

rng = np.random.default_rng(SEED)

# ══════════════════════════════════════════════
# ██  ETAPA 3 — Presupuesto y costo
# ══════════════════════════════════════════════

def comprar_sobre(coleccion: set, rng_local) -> tuple[int, int]:
    """
    Compra un sobre con S estampas aleatorias (con reemplazo entre posiciones del sobre,
    pero cada estampa es un número en [0, N-1]).
    Devuelve (nuevas_distintas, repetidas_en_este_sobre).
    """
    estampas = rng_local.integers(0, N, size=S)
    nuevas = 0
    for e in estampas:
        if e not in coleccion:
            coleccion.add(e)
            nuevas += 1
    repetidas = S - nuevas
    return nuevas, repetidas


# ── 3.1  Simulación con presupuesto suelto (sobre a sobre) ────────────────────

def simular_etapa3_sueltos(R, rng_local):
    """
    Compra sobres sueltos hasta agotar el presupuesto o completar el álbum.
    Retorna arrays: completado, n_sobres, n_distintas
    """
    completado  = np.zeros(R, dtype=int)
    n_sobres    = np.zeros(R, dtype=int)
    n_distintas = np.zeros(R, dtype=int)

    for i in range(R):
        coleccion = set()
        gasto     = 0.0
        sobres    = 0

        while (gasto + PRECIO <= BUDGET) and (len(coleccion) < N):
            comprar_sobre(coleccion, rng_local)
            gasto  += PRECIO
            sobres += 1

        completado[i]  = 1 if len(coleccion) == N else 0
        n_sobres[i]    = sobres
        n_distintas[i] = len(coleccion)

    return completado, n_sobres, n_distintas


# ── 3.2  Simulación con caja de 104 sobres (Q 975) ───────────────────────────

SOBRES_CAJA  = 104
COSTO_CAJA   = 975.0

def simular_etapa3_caja(R, rng_local):
    """
    Compra exactamente 104 sobres (la caja completa) y verifica si se completó el álbum.
    """
    completado = np.zeros(R, dtype=int)

    for i in range(R):
        coleccion = set()
        for _ in range(SOBRES_CAJA):
            comprar_sobre(coleccion, rng_local)
        completado[i] = 1 if len(coleccion) == N else 0

    return completado


# ── 3.3  Estrategia mixta: caja + sobres sueltos ──────────────────────────────

def simular_etapa3_mixta(R, rng_local):
    """
    Estrategia: comprar 1 caja (Q 975) + sobres sueltos con el resto del presupuesto.
    Presupuesto restante = Q 1000 - Q 975 = Q 25  → máx 2 sobres sueltos.
    """
    resto_presupuesto = BUDGET - COSTO_CAJA       # Q 25
    sobres_extra_max  = int(resto_presupuesto // PRECIO)   # 2 sobres

    completado  = np.zeros(R, dtype=int)
    n_sobres    = np.zeros(R, dtype=int)

    for i in range(R):
        coleccion = set()
        sobres    = 0

        # Fase 1: caja
        for _ in range(SOBRES_CAJA):
            comprar_sobre(coleccion, rng_local)
            sobres += 1

        # Fase 2: sobres sueltos extras
        gasto_extra = 0.0
        while (gasto_extra + PRECIO <= resto_presupuesto) and (len(coleccion) < N):
            comprar_sobre(coleccion, rng_local)
            gasto_extra += PRECIO
            sobres      += 1

        completado[i] = 1 if len(coleccion) == N else 0
        n_sobres[i]   = sobres

    return completado, n_sobres, sobres_extra_max


# ── 3.4  Pregunta 1: cálculo exacto ──────────────────────────────────────────

def preguntas_etapa3():
    max_sobres_presupuesto = int(BUDGET // PRECIO)
    min_sobres_teorico     = int(np.ceil(N / S))   # sin repetidos
    print("=" * 60)
    print("ETAPA 3 — Preguntas de análisis")
    print("=" * 60)
    print(f"\nPregunta 1:")
    print(f"  Máx sobres con Q{BUDGET:.0f}  : {max_sobres_presupuesto}")
    print(f"  Mín sobres teórico (sin rep.): {min_sobres_teorico}")
    print(f"  Estampas máx obtenibles (Q1000): {max_sobres_presupuesto * S}")
    if max_sobres_presupuesto * S >= N:
        print(f"  → En teoría SÍ alcanzaría (si no hubiera repetidos).")
    else:
        print(f"  → En teoría NO alcanzaría aunque no hubiese repetidos.")


# ── 3.5  Ejecutar y reportar Etapa 3 ─────────────────────────────────────────

def etapa3():
    print("\n" + "═" * 60)
    print("  ETAPA 3: Incorporación del presupuesto y costo")
    print("═" * 60)

    preguntas_etapa3()

    # Simulaciones
    rng_local = np.random.default_rng(SEED)

    print("\n[Simulando sobres sueltos…]")
    comp_s, sob_s, dist_s = simular_etapa3_sueltos(R, rng_local)

    rng_local2 = np.random.default_rng(SEED)
    print("[Simulando caja de 104 sobres…]")
    comp_c = simular_etapa3_caja(R, rng_local2)

    rng_local3 = np.random.default_rng(SEED)
    print("[Simulando estrategia mixta (caja + sueltos)…]")
    comp_m, sob_m, extra_max = simular_etapa3_mixta(R, rng_local3)

    # ── Resultados sobres sueltos
    prob_s = comp_s.mean()
    E_sobres_s = sob_s.mean()
    mask_no = comp_s == 0
    E_dist_no_comp = dist_s[mask_no].mean() if mask_no.any() else float('nan')

    print("\n── Sobres sueltos (presupuesto Q1000) ──")
    print(f"  P(completar álbum)              : {prob_s:.4f}  ({prob_s*100:.2f} %)")
    print(f"  E[sobres comprados]             : {E_sobres_s:.2f}")
    print(f"  E[estampas distintas | no comp.]: {E_dist_no_comp:.2f}")

    # ── Resultados caja
    prob_c = comp_c.mean()
    print(f"\n── Caja 104 sobres (Q{COSTO_CAJA:.0f}) ──")
    print(f"  P(completar álbum)              : {prob_c:.4f}  ({prob_c*100:.2f} %)")
    print(f"  ¿Conviene la caja? {'SÍ' if prob_c > prob_s else 'NO'} "
          f"(Δp = {(prob_c - prob_s)*100:+.2f} pp)")

    # ── Resultados mixta
    prob_m = comp_m.mean()
    print(f"\n── Estrategia mixta (caja Q975 + hasta {extra_max} sobres sueltos) ──")
    print(f"  Presupuesto restante tras caja  : Q{BUDGET - COSTO_CAJA:.2f}")
    print(f"  Sobres sueltos extra máx posibles: {extra_max}")
    print(f"  P(completar álbum)              : {prob_m:.4f}  ({prob_m*100:.2f} %)")
    print(f"  E[sobres totales]               : {sob_m.mean():.2f}")

    # ── Gráfica Etapa 3
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Etapa 3 — Proporción de completar el álbum", fontsize=14, fontweight='bold')

    escenarios = [
        ("Sobres sueltos\n(Q1000)", prob_s, 1 - prob_s),
        (f"Caja 104 sobres\n(Q{COSTO_CAJA:.0f})", prob_c, 1 - prob_c),
        (f"Mixta\n(caja + {extra_max} sueltos)", prob_m, 1 - prob_m),
    ]
    colores = ["#2196F3", "#4CAF50", "#FF9800"]

    for ax, (titulo, p_si, p_no), color in zip(axes, escenarios, colores):
        barras = ax.bar(["Completó", "No completó"], [p_si, p_no],
                        color=[color, "#BDBDBD"], edgecolor='white', linewidth=1.2)
        ax.set_title(titulo, fontsize=11)
        ax.set_ylim(0, 1.05)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        ax.set_ylabel("Proporción")
        for barra, val in zip(barras, [p_si, p_no]):
            ax.text(barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 0.01,
                    f"{val*100:.1f}%", ha='center', va='bottom', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("etapa3_barras.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\n[Gráfica guardada como etapa3_barras.png]")


# ══════════════════════════════════════════════
# ██  ETAPA 4 — Intercambio de repetidas
# ══════════════════════════════════════════════

def simular_con_intercambio_hasta_completar(K: int, R: int, rng_local) -> np.ndarray:
    """
    Simula hasta completar el álbum con regla de intercambio:
    cada K repetidas acumuladas → 1 estampa nueva (elegida entre las faltantes).
    Retorna array con número de sobres por simulación.
    """
    n_sobres_arr = np.zeros(R, dtype=int)

    for i in range(R):
        coleccion  = set(range(N))   # faltantes = complemento
        faltantes  = set(range(N))
        coleccion  = set()
        repetidas_acum = 0
        sobres     = 0

        while len(coleccion) < N:
            estampas = rng_local.integers(0, N, size=S)
            sobres  += 1
            for e in estampas:
                if e not in coleccion:
                    coleccion.add(e)
                else:
                    repetidas_acum += 1

            # Intercambios: cada K repetidas → 1 faltante
            if K > 0:
                canjes = repetidas_acum // K
                repetidas_acum = repetidas_acum % K
                faltantes_lista = list(set(range(N)) - coleccion)
                canjes = min(canjes, len(faltantes_lista))
                if canjes > 0:
                    elegidas = rng_local.choice(faltantes_lista,
                                                size=canjes, replace=False)
                    for e in elegidas:
                        coleccion.add(e)

        n_sobres_arr[i] = sobres

    return n_sobres_arr


def simular_con_intercambio_M_fijos(K: int, M: int, R: int, rng_local) -> float:
    """
    Simula exactamente M sobres con regla de intercambio K.
    Retorna proporción de simulaciones donde se completó el álbum.
    """
    exitos = 0

    for _ in range(R):
        coleccion      = set()
        repetidas_acum = 0

        for _ in range(M):
            if len(coleccion) == N:
                break
            estampas = rng_local.integers(0, N, size=S)
            for e in estampas:
                if e not in coleccion:
                    coleccion.add(e)
                else:
                    repetidas_acum += 1

            if K > 0:
                canjes = repetidas_acum // K
                repetidas_acum = repetidas_acum % K
                faltantes_lista = list(set(range(N)) - coleccion)
                canjes = min(canjes, len(faltantes_lista))
                if canjes > 0:
                    elegidas = rng_local.choice(faltantes_lista,
                                                size=canjes, replace=False)
                    for e in elegidas:
                        coleccion.add(e)

        if len(coleccion) == N:
            exitos += 1

    return exitos / R


def etapa4():
    print("\n" + "═" * 60)
    print("  ETAPA 4: Efecto del intercambio de repetidas")
    print("═" * 60)

    Ks = [1, 2, 5, 10]

    # ── Parte A: Hasta completar el álbum ────────────────────────────────────
    print("\n── Parte A: Sobres hasta completar álbum por K ──")

    # Caso sin intercambio (referencia): K = ∞ → nunca hay canje
    rng_ref = np.random.default_rng(SEED)
    sobres_ref = simular_con_intercambio_hasta_completar(0, R, rng_ref)  # K=0 → sin intercambio
    media_ref  = sobres_ref.mean()
    std_ref    = sobres_ref.std()
    print(f"\n  K=∞ (sin intercambio): media={media_ref:.2f}, std={std_ref:.2f}")

    resultados_A = {}
    for K in Ks:
        rng_k = np.random.default_rng(SEED)
        sobres_k = simular_con_intercambio_hasta_completar(K, R, rng_k)
        media_k  = sobres_k.mean()
        std_k    = sobres_k.std()
        reduccion = (media_ref - media_k) / media_ref * 100
        resultados_A[K] = sobres_k
        print(f"  K={K:2d}: media={media_k:.2f}, std={std_k:.2f}, "
              f"reducción={reduccion:.1f}%")

    # Pregunta 2 de análisis: ahorro en Q para K=2
    K2_media  = resultados_A[2].mean()
    ahorro_s  = media_ref - K2_media
    ahorro_Q  = ahorro_s * PRECIO
    print(f"\n  Pregunta 2: Ahorro promedio K=2 vs sin intercambio: "
          f"{ahorro_s:.2f} sobres ≈ Q{ahorro_Q:.2f}")

    # Gráfica A: Histogramas superpuestos
    fig, ax = plt.subplots(figsize=(10, 5))
    colores_K = {1: "#E91E63", 2: "#9C27B0", 5: "#2196F3", 10: "#4CAF50"}
    bins = np.arange(0, 250, 3)

    ax.hist(sobres_ref, bins=bins, alpha=0.35, label="Sin intercambio",
            color="#607D8B", density=True)
    for K in Ks:
        ax.hist(resultados_A[K], bins=bins, alpha=0.55,
                label=f"K={K}", color=colores_K[K], density=True)

    ax.set_xlabel("Número de sobres para completar el álbum", fontsize=11)
    ax.set_ylabel("Densidad", fontsize=11)
    ax.set_title("Etapa 4A — Distribución de sobres necesarios según K", fontsize=13, fontweight='bold')
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig("etapa4A_histogramas.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\n[Gráfica guardada como etapa4A_histogramas.png]")

    # ── Parte B: Probabilidad de éxito vs M ──────────────────────────────────
    print("\n── Parte B: P(éxito) vs M por K ──")

    M_vals = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    probs  = {K: [] for K in Ks}
    probs_ref = []

    for M in M_vals:
        # Sin intercambio
        rng_r = np.random.default_rng(SEED + M)
        probs_ref.append(simular_con_intercambio_M_fijos(0, M, R, rng_r))
        for K in Ks:
            rng_k = np.random.default_rng(SEED + M + K)
            probs[K].append(simular_con_intercambio_M_fijos(K, M, R, rng_k))

    # Tabla de resultados
    header = f"{'M':>4} | {'Sin intercambio':>16} | " + " | ".join(f"{'K='+str(K):>6}" for K in Ks)
    print("\n  " + header)
    print("  " + "-" * len(header))
    for j, M in enumerate(M_vals):
        fila = f"{M:>4} | {probs_ref[j]:>16.4f} | " + " | ".join(f"{probs[K][j]:>6.4f}" for K in Ks)
        print("  " + fila)

    # Umbrales 50%, 75%, 90%
    umbrales = [0.50, 0.75, 0.90]
    print("\n  Sobres mínimos para alcanzar cada umbral de probabilidad:")
    print(f"  {'K':>6} | {'50%':>5} | {'75%':>5} | {'90%':>5}")
    print("  " + "-" * 32)

    todos = {"Sin intercambio": probs_ref}
    todos.update({f"K={K}": probs[K] for K in Ks})

    for nombre, p_lista in todos.items():
        fila = f"  {nombre:>15} |"
        for umbral in umbrales:
            alcanza = [M for M, p in zip(M_vals, p_lista) if p >= umbral]
            fila += f" {alcanza[0] if alcanza else '>70':>5} |"
        print(fila)

    # Pregunta 3: M=45, diferencias entre K
    idx_45 = M_vals.index(45)
    p_k10 = probs[10][idx_45]
    p_k5  = probs[5][idx_45]
    p_k1  = probs[1][idx_45]
    print(f"\n  Pregunta 3 (M=45):")
    print(f"    K=10 → {p_k10:.4f}   K=5 → {p_k5:.4f}   K=1 → {p_k1:.4f}")
    print(f"    Δ(K10→K5) = {(p_k5 - p_k10)*100:.2f} pp")
    print(f"    Δ(K5→K1)  = {(p_k1 - p_k5)*100:.2f} pp")

    # Costo efectivo por estampa nueva por canje
    print(f"\n  Pregunta 5 — Costo efectivo por canje:")
    for K in Ks:
        costo_por_nueva = K * PRECIO / S
        print(f"    K={K:2d}: Q{costo_por_nueva:.4f} por estampa nueva obtenida por canje")

    # Gráfica B: P(éxito) vs M
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(M_vals, probs_ref, 'o--', color="#607D8B",
            label="Sin intercambio", linewidth=1.5)
    for K in Ks:
        ax.plot(M_vals, probs[K], 'o-', color=colores_K[K],
                label=f"K={K}", linewidth=2)

    ax.axhline(0.50, color='gray', linestyle=':', linewidth=1, alpha=0.6)
    ax.axhline(0.75, color='gray', linestyle=':', linewidth=1, alpha=0.6)
    ax.axhline(0.90, color='gray', linestyle=':', linewidth=1, alpha=0.6)
    ax.text(M_vals[-1] + 0.3, 0.50, "50%", va='center', color='gray', fontsize=9)
    ax.text(M_vals[-1] + 0.3, 0.75, "75%", va='center', color='gray', fontsize=9)
    ax.text(M_vals[-1] + 0.3, 0.90, "90%", va='center', color='gray', fontsize=9)

    ax.set_xlabel("Número de sobres M", fontsize=11)
    ax.set_ylabel("P(completar el álbum)", fontsize=11)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax.set_title("Etapa 4B — Probabilidad de éxito vs. sobres comprados, por K",
                 fontsize=13, fontweight='bold')
    ax.legend(loc='lower right')
    ax.set_xlim(M_vals[0] - 1, M_vals[-1] + 2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig("etapa4B_prob_vs_M.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\n[Gráfica guardada como etapa4B_prob_vs_M.png]")


# ══════════════════════════════════════════════
# ██  MAIN
# ══════════════════════════════════════════════

if __name__ == "__main__":
    etapa3()
    etapa4()
    print("\n✓ Simulaciones completadas.")