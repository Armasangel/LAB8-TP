"""
===========================================================
  SIMULACIÓN MONTE CARLO — ÁLBUM FIFA 2026
  Problema del Coleccionista de Cupones (Coupon Collector)
===========================================================
Parámetros reales del álbum:
  - N_real = 980  estampas diferentes
  - S_real = 7    estampas por sobre
  - Precio individual: Q 9.50
  - Precio caja (104 sobres): Q 975.00

Parámetros para la simulación (versión reducida):
  - N = 100   estampas diferentes
  - S = 7     estampas por sobre
  - R = 10000 repeticiones
  - Semilla  = 2026
===========================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import log
import math

# ─────────────────────────────────────────────
#  PARÁMETROS
# ─────────────────────────────────────────────
N    = 100     # Total de estampas diferentes (versión reducida)
S    = 7       # Estampas por sobre
R    = 10000   # Número de simulaciones
SEED = 2026    # Semilla

# Parámetros reales del álbum FIFA 2026
N_real     = 980
S_real     = 7
P_individual = 9.50    # Quetzales por sobre individual
P_caja_sobres = 104    # Sobres por caja
P_caja_precio = 975.0  # Precio de la caja en Quetzales


# ─────────────────────────────────────────────
#  VALOR TEÓRICO  E[sobres] = (N/S) * H_N
#  H_N ≈ ln(N) + γ,   γ = 0.5772156649
# ─────────────────────────────────────────────
GAMMA = 0.5772156649          # Constante de Euler-Mascheroni
H_N   = log(N) + GAMMA        # Número armónico aproximado
E_sobres_teorico = (N / S) * H_N

print("=" * 60)
print("  SIMULACIÓN MONTE CARLO — ÁLBUM FIFA 2026")
print("=" * 60)
print(f"\n[PARÁMETROS DE SIMULACIÓN]")
print(f"  N (estampas únicas)     : {N}")
print(f"  S (estampas por sobre)  : {S}")
print(f"  R (simulaciones)        : {R:,}")
print(f"  Semilla                 : {SEED}")
print(f"\n[VALOR TEÓRICO]")
print(f"  H_N  = ln({N}) + {GAMMA:.7f} = {H_N:.6f}")
print(f"  E[sobres] = ({N}/{S}) × {H_N:.6f} = {E_sobres_teorico:.4f} sobres")
print()


# ─────────────────────────────────────────────
#  SIMULACIÓN
# ─────────────────────────────────────────────
rng = np.random.default_rng(SEED)

resultados_sobres    = np.zeros(R, dtype=int)
resultados_repetidas = np.zeros(R, dtype=int)

for sim in range(R):
    obtenidas  = np.zeros(N, dtype=bool)   # arreglo booleano de estampas
    n_sobres   = 0
    repetidas  = 0
    unicas     = 0                          # cuántas distintas llevamos

    while unicas < N:
        # Comprar un sobre: S estampas aleatorias SIN repetición dentro del sobre
        sobre = rng.choice(N, size=S, replace=False)
        n_sobres += 1

        for sticker in sobre:
            if obtenidas[sticker]:
                repetidas += 1
            else:
                obtenidas[sticker] = True
                unicas += 1

    resultados_sobres[sim]    = n_sobres
    resultados_repetidas[sim] = repetidas


# ─────────────────────────────────────────────
#  ESTADÍSTICAS
# ─────────────────────────────────────────────
media_sobres   = resultados_sobres.mean()
std_sobres     = resultados_sobres.std(ddof=1)
mediana_sobres = np.median(resultados_sobres)
p5, p95        = np.percentile(resultados_sobres, [5, 95])

media_rep      = resultados_repetidas.mean()
std_rep        = resultados_repetidas.std(ddof=1)

print("=" * 60)
print("  RESULTADOS EMPÍRICOS (10 000 simulaciones)")
print("=" * 60)

print(f"\n── Sobres necesarios para completar el álbum ──")
print(f"  Media muestral         : {media_sobres:.4f}")
print(f"  Desviación estándar    : {std_sobres:.4f}")
print(f"  Mediana                : {mediana_sobres:.1f}")
print(f"  Percentil  5 %         : {p5:.1f}")
print(f"  Percentil 95 %         : {p95:.1f}")
print(f"  Mínimo observado       : {resultados_sobres.min()}")
print(f"  Máximo observado       : {resultados_sobres.max()}")

print(f"\n── Estampas repetidas acumuladas ──")
print(f"  Media muestral         : {media_rep:.4f}")
print(f"  Desviación estándar    : {std_rep:.4f}")

print(f"\n── Comparación Empírico vs Teórico ──")
print(f"  E[sobres] teórico      : {E_sobres_teorico:.4f}")
print(f"  E[sobres] empírico     : {media_sobres:.4f}")
print(f"  Diferencia relativa    : {abs(media_sobres - E_sobres_teorico)/E_sobres_teorico*100:.3f} %")


# ─────────────────────────────────────────────
#  PROYECCIÓN AL ÁLBUM REAL (FIFA 2026)
# ─────────────────────────────────────────────
# Usamos el factor de escala: media_simulada / E_teorico_N100
# y lo aplicamos al E_teórico real
H_N_real = log(N_real) + GAMMA
E_sobres_real = (N_real / S_real) * H_N_real

# Costo esperado con precio individual
costo_individual = E_sobres_real * P_individual

# Costo optimizando cajas completas + individuales al final
cajas_necesarias = int(E_sobres_real // P_caja_sobres)
sobres_restantes = E_sobres_real - cajas_necesarias * P_caja_sobres
costo_optimo = cajas_necesarias * P_caja_precio + sobres_restantes * P_individual

print(f"\n{'=' * 60}")
print(f"  PROYECCIÓN ÁLBUM REAL (N={N_real}, S={S_real})")
print(f"{'=' * 60}")
print(f"  H_N_real                : {H_N_real:.6f}")
print(f"  E[sobres] teórico real  : {E_sobres_real:.1f} sobres")
print(f"  Costo (solo individuales): Q {costo_individual:,.2f}")
print(f"  Costo (cajas + indiv.)  : Q {costo_optimo:,.2f}")
print(f"    → {cajas_necesarias} caja(s) × Q{P_caja_precio:.2f}"
      f" + {sobres_restantes:.0f} sobres × Q{P_individual:.2f}")


# ─────────────────────────────────────────────
#  MÉTRICAS ADICIONALES
# ─────────────────────────────────────────────

# 1. Probabilidad de necesitar más de 30 sobres
umbral = 30
prob_mas_30 = (resultados_sobres > umbral).mean()
print(f"P(sobres > {umbral})               : {prob_mas_30:.4f}  ({prob_mas_30*100:.2f}%)")

# 2. Mínimo teórico de sobres si no hubiera repetidas (ni dentro ni entre sobres)
# Para cubrir N estampas con S por sobre sin ninguna repetición: ceil(N/S)
min_teorico = math.ceil(N / S)
print(f"Mínimo teórico de sobres (sin rep.) : {min_teorico}  (= ceil({N}/{S}))")

# 3. Valor esperado teórico de estampas repetidas
# Total de estampas abiertas en promedio = E[sobres] * S
# Repetidas esperadas = total abiertas - N (las únicas)
total_abiertas_esperadas = E_sobres_teorico * S
E_repetidas_teorico = total_abiertas_esperadas - N
print(f"E[estampas repetidas] teórico       : {E_repetidas_teorico:.4f}")
print(f"  (= E[sobres]×S − N  =  {E_sobres_teorico:.4f}×{S} − {N})")

# 4. Interpretación de la desviación estándar de sobres
print(f"\nInterpretación de σ (desviación estándar de sobres):")
print(f"  σ empírica = {std_sobres:.4f}")
print(f"  En el 68% de las simulaciones, los sobres necesarios cayeron en:")
print(f"    [{media_sobres - std_sobres:.2f},  {media_sobres + std_sobres:.2f}]  (μ ± 1σ)")
print(f"  En el 95% de las simulaciones, cayeron en:")
print(f"    [{media_sobres - 2*std_sobres:.2f},  {media_sobres + 2*std_sobres:.2f}]  (μ ± 2σ)")
print(f"  Coeficiente de variación (σ/μ): {std_sobres/media_sobres:.4f}  "
      f"→ variabilidad del {std_sobres/media_sobres*100:.2f}% respecto a la media")



# ─────────────────────────────────────────────
#  PROBLEMA 2: PROBABILIDAD DE COMPLETAR CON M SOBRES FIJOS
# ─────────────────────────────────────────────

valores_M = [20, 25, 30, 35, 40, 45, 50, 60, 70, 80]
rng2 = np.random.default_rng(SEED)

proporciones = []

for M in valores_M:
    exitos = 0
    for _ in range(R):
        obtenidas = np.zeros(N, dtype=bool)
        for _ in range(M):
            sobre = rng2.choice(N, size=S, replace=False)
            for sticker in sobre:
                obtenidas[sticker] = True
        if obtenidas.all():
            exitos += 1
    proporciones.append(exitos / R)

# ── Tabla de resultados ──
print("=" * 60)
print("  PROBLEMA 2: P(Completar álbum | M sobres)")
print("=" * 60)
print(f"\n{'M':<8} {'Proporción':>12} {'Porcentaje':>12}")
print("-" * 34)
for M, prop in zip(valores_M, proporciones):
    print(f"{M:<8} {prop:>12.4f} {prop*100:>11.2f}%")

# ── Umbral 50% y 90% ──
M50 = next((M for M, p in zip(valores_M, proporciones) if p >= 0.50), None)
M90 = next((M for M, p in zip(valores_M, proporciones) if p >= 0.90), None)
print(f"Primer M con P ≥ 50% : M = {M50}  (P = {proporciones[valores_M.index(M50)]:.4f})" if M50 else "Primer M con P ≥ 50% : No alcanzado en los valores de M probados")
print(f"Primer M con P ≥ 90% : M = {M90}  (P = {proporciones[valores_M.index(M90)]:.4f})" if M90 else f"Primer M con P ≥ 90% : No alcanzado — máximo fue {max(proporciones)*100:.2f}% con M={valores_M[proporciones.index(max(proporciones))]}")

# ── Comparación con mediana del Problema 1 ──
if M50:
    print(f"\nMediana de sobres necesarios (Problema 1) : {mediana_sobres:.1f}")
    print(f"Primer M con P(M) ≥ 0.50                  : {M50}")
if M50:
    print(f"Mediana de sobres necesarios (Problema 1) : {mediana_sobres:.1f}")
    print(f"Primer M con P(M) ≥ 0.50                  : {M50}")
    print(f"  → Diferencia: {abs(M50 - mediana_sobres):.1f} sobres")
else:
    print("P(M) = 0.50 no se alcanzó en los valores de M evaluados.")

# ── Gráfica de barras ──
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#161b22")

colores = ["#238636" if p >= 0.90 else "#f0a500" if p >= 0.50 else "#c0392b"
           for p in proporciones]

bars = ax.bar([str(m) for m in valores_M], [p * 100 for p in proporciones],
              color=colores, edgecolor="#0d1117", linewidth=0.6, width=0.6)

# Etiquetas encima de cada barra
for bar, prop in zip(bars, proporciones):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2,
            f"{prop*100:.1f}%", ha="center", va="bottom",
            color="white", fontsize=9, fontweight="bold")

# Líneas de referencia
ax.axhline(50, color="#f0e68c", linewidth=1.6, linestyle="--", label="Umbral 50%")
ax.axhline(90, color="#79c0ff", linewidth=1.6, linestyle="--", label="Umbral 90%")

# Leyenda de colores
from matplotlib.patches import Patch
leyenda_colores = [
    Patch(facecolor="#c0392b", label="P < 50%"),
    Patch(facecolor="#f0a500", label="50% ≤ P < 90%"),
    Patch(facecolor="#238636", label="P ≥ 90%"),
]
ax.legend(handles=leyenda_colores, framealpha=0.25, facecolor="#21262d",
          edgecolor="#30363d", labelcolor="white", fontsize=10, loc="upper left")

ax.set_title(
    f"P(Completar álbum | M sobres)  —  N={N}, S={S}, R={R:,} simulaciones",
    color="white", fontsize=13, fontweight="bold", pad=14
)
ax.set_xlabel("M  (sobres comprados)", color="#c9d1d9", fontsize=11)
ax.set_ylabel("Probabilidad estimada (%)", color="#c9d1d9", fontsize=11)
ax.set_ylim(0, 108)
ax.tick_params(colors="#c9d1d9")
for spine in ax.spines.values():
    spine.set_edgecolor("#30363d")
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

plt.tight_layout()
plt.savefig("prob2_barras_album_fifa2026.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
print("\n[✓] Gráfica guardada como 'prob2_barras_album_fifa2026.png'")
print("=" * 60)

# ─────────────────────────────────────────────
#  HISTOGRAMA
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#161b22")

# Histograma
n_bins = min(80, int(np.sqrt(R)))
counts, bins, patches = ax.hist(
    resultados_sobres,
    bins=n_bins,
    color="#238636",
    edgecolor="#0d1117",
    linewidth=0.4,
    alpha=0.85,
    label="Distribución simulada"
)

# Gradiente de color por frecuencia
max_count = counts.max()
cmap = plt.cm.get_cmap("YlGn")
for patch, c in zip(patches, counts):
    patch.set_facecolor(cmap(0.3 + 0.7 * c / max_count))

# Líneas verticales
ax.axvline(media_sobres, color="#f0e68c", linewidth=2.2,
           linestyle="-", label=f"Media empírica = {media_sobres:.2f}")
ax.axvline(E_sobres_teorico, color="#ff7b54", linewidth=2.2,
           linestyle="--", label=f"E[sobres] teórico = {E_sobres_teorico:.2f}")
ax.axvline(mediana_sobres, color="#79c0ff", linewidth=1.6,
           linestyle=":", label=f"Mediana = {mediana_sobres:.1f}")

# Banda de percentiles
ax.axvspan(p5, p95, alpha=0.08, color="#58a6ff",
           label=f"IC 90% [{p5:.0f} – {p95:.0f}]")

# Etiquetas y formato
ax.set_title(
    f"Distribución del N.° de Sobres para Completar el Álbum\n"
    f"(N={N} estampas, S={S}/sobre, R={R:,} simulaciones, semilla={SEED})",
    color="white", fontsize=13, pad=14, fontweight="bold"
)
ax.set_xlabel("Número de sobres comprados", color="#c9d1d9", fontsize=11)
ax.set_ylabel("Frecuencia", color="#c9d1d9", fontsize=11)

ax.tick_params(colors="#c9d1d9")
for spine in ax.spines.values():
    spine.set_edgecolor("#30363d")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

legend = ax.legend(framealpha=0.25, facecolor="#21262d",
                   edgecolor="#30363d", labelcolor="white", fontsize=10)

# Anotación de estadísticas
stats_text = (
    f"μ = {media_sobres:.2f}  |  σ = {std_sobres:.2f}\n"
    f"Teórico: {E_sobres_teorico:.2f}  |  Error: {abs(media_sobres-E_sobres_teorico)/E_sobres_teorico*100:.2f}%"
)
ax.text(0.98, 0.97, stats_text,
        transform=ax.transAxes, fontsize=9,
        verticalalignment="top", horizontalalignment="right",
        color="#c9d1d9",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#21262d",
                  edgecolor="#30363d", alpha=0.8))

plt.tight_layout()
plt.savefig("histograma_album_fifa2026.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
print("\n[✓] Histograma guardado como 'histograma_album_fifa2026.png'")
print("=" * 60)