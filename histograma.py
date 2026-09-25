import matplotlib.pyplot as plt
import numpy as np

# Datos extraídos del inventario (APs únicos / BSSID por canal)
# 2.4 GHz: Canales 1, 3, 6, 9, 11
canales_24 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
aps_24 =     [2,   0,   1,   0,   0,   2,   0,   0,   1,   0,    4,    0,    0] 

# 5 GHz: Canales 44, 52, 60, 100, 108, 120, 157
canales_5 = ['44', '52', '60', '100', '108', '120', '157']
aps_5 =     [1,    1,    1,    1,     1,     1,     1]

# Configurar la figura con dos subgráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Histograma 2.4 GHz
ax1.bar(canales_24, aps_24, color='#3498db', edgecolor='black')
ax1.set_title('Distribución de APs por Canal - Banda 2.4 GHz', fontsize=14, fontweight='bold')
ax1.set_xlabel('Número de Canal', fontsize=12)
ax1.set_ylabel('Cantidad de APs (BSSID)', fontsize=12)
ax1.set_yticks(range(0, 6))
ax1.grid(axis='y', linestyle='--', alpha=0.7)
# Resaltar canales no solapados (1, 6, 11)
for i in [0, 5, 10]:
    ax1.get_xticklabels()[i].set_fontweight("bold")
    ax1.get_xticklabels()[i].set_color("red")
a
# Histograma 5 GHz
ax2.bar(canales_5, aps_5, color='#2ecc71', edgecolor='black', width=0.5)
ax2.set_title('Distribución de APs por Canal - Banda 5 GHz', fontsize=14, fontweight='bold')
ax2.set_xlabel('Número de Canal (Principal)', fontsize=12)
ax2.set_ylabel('Cantidad de APs (BSSID)', fontsize=12)
ax2.set_yticks(range(0, 4))
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
