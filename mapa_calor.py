import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 1. Cargar la imagen del plano arquitectónico
# Asegúrate de colocar el nombre de tu archivo de imagen
image_path = 'plano_balzay.jpg' 
img = Image.open(image_path)
width, height = img.size

# 2. Coordenadas relativas (%) de los 8 puntos sobre el plano
points_coords = {
    1: (6.5,  18.0),   # Punto 1
    2: (4.0,  63.0),   # Punto 2
    3: (18.5, 81.0),   # Punto 3
    4: (32.0, 52.0),   # Punto 4
    5: (36.5, 81.0),   # Punto 5
    6: (49.5, 81.0),   # Punto 6
    7: (57.5, 48.0),   # Punto 7
    8: (54.0, 15.0)    # Punto 8
}

# 3. Datos completos de RSSI por punto extraídos del inventario
# Incluye todas las lecturas de APs, bandas y canales registrados
all_measurements = {
    1: [-44, -44, -45, -46, -54, -54],
    2: [-41, -41, -45, -45, -64],
    3: [-45, -45, -45, -45, -62, -62],
    4: [-44, -47, -44, -48, -64, -64],
    5: [-44, -47, -48, -48, -64, -64],
    6: [-39, -39, -39, -40, -66, -66],
    7: [-47, -47, -48, -48, -64, -64],
    8: [-42, -43, -43, -43, -64, -64]
}

# OPCIÓN A: Usar el valor Promedio de todas las redes detectadas por punto
rssi_values = np.array([np.mean(all_measurements[p]) for p in sorted(all_measurements.keys())])

# (Si prefieres usar el valor Máximo de cada punto, descomenta la siguiente línea):
# rssi_values = np.array([np.max(all_measurements[p]) for p in sorted(all_measurements.keys())])

# Convertir coordenadas a píxeles
x_pts = np.array([coords[0] * width / 100.0 for coords in points_coords.values()])
y_pts = np.array([coords[1] * height / 100.0 for coords in points_coords.values()])

# 4. Generación de la malla para interpolación espacial
grid_x, grid_y = np.meshgrid(
    np.linspace(0, width, width // 2),
    np.linspace(0, height, height // 2)
)

# Algoritmo IDW (Inverse Distance Weighting) para simular propagación de radio
def idw_interpolation(x, y, values, gx, gy, power=2.5):
    dist = np.hypot(gx[..., np.newaxis] - x, gy[..., np.newaxis] - y)
    dist = np.maximum(dist, 1e-6)  # Evitar división entre cero
    weights = 1.0 / (dist ** power)
    weights /= np.sum(weights, axis=-1, keepdims=True)
    return np.sum(weights * values, axis=-1)

# Generar la superficie de cobertura interpolada
grid_z = idw_interpolation(x_pts, y_pts, rssi_values, grid_x, grid_y, power=2.5)

# 5. Estilo visual profesional para informe en LaTeX
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

# Plano arquitectónico de fondo
ax.imshow(img, extent=[0, width, height, 0])

# Ajuste dinámico de la escala de color para acentuar variaciones de señal
vmin, vmax = np.min(rssi_values) - 3, np.max(rssi_values) + 3
cmap = plt.cm.turbo

# Superposición de la capa del mapa de calor
contour = ax.imshow(
    grid_z,
    extent=[0, width, height, 0],
    cmap=cmap,
    alpha=0.55,
    origin='upper',
    vmin=vmin,
    vmax=vmax
)

# 6. Colocar los marcadores y anotaciones con el RSSI promedio/representativo
for i, (p_id, (px, py)) in enumerate(points_coords.items()):
    x_px = px * width / 100.0
    y_px = py * height / 100.0
    val = rssi_values[i]
    num_mues = len(all_measurements[p_id])
    
    # Dibujar punto de medición
    ax.scatter(x_px, y_px, c='black', s=55, zorder=5, marker='o')
    ax.scatter(x_px, y_px, c='white', s=25, zorder=6, marker='o')
    
    # Etiqueta con valor promedio e indicación de muestras consideradas
    ax.annotate(
        f"P{p_id}: {val:.1f} dBm\n({num_mues} redes)",
        (x_px, y_px),
        xytext=(8, -14),
        textcoords='offset points',
        fontsize=8,
        fontweight='bold',
        color='black',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.8, alpha=0.9),
        zorder=7
    )

# 7. Barra de escala lateral (Colorbar)
cbar = fig.colorbar(contour, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label('Nivel de Señal RSSI Promedio (dBm)', fontsize=10, fontweight='bold', labelpad=10)
cbar.ax.tick_params(labelsize=9)

# Cuadro descriptivo formal
ax.text(
    0.01, 0.96, 'Caracterización Radioeléctrica: RSSI Promedio Multisistema',
    transform=ax.transAxes,
    fontsize=10,
    fontweight='bold',
    bbox=dict(boxstyle="square,pad=0.4", fc="white", ec="gray", lw=0.7)
)

# Formato final limpio
ax.axis('off')
plt.tight_layout()

# 8. Exportar PNG de alta resolución (300 DPI)
plt.savefig('mapa_calor_rssi_completo.png', dpi=300, bbox_inches='tight', pad_inches=0.05)
plt.show()
