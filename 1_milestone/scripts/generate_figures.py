"""
Vizualizációkat generáló szkript az 1. mérföldkő dokumentációhoz.
Generálja a legfontosabb magyarázó ábrákat png formátumban.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Beállítások
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

output_dir = '1_milestone/figures'
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv('1_milestone/song_data.csv')
df_dedup = df.drop_duplicates()

# -------------------------------------------------------------
# 1. ÁBRA: song_popularity eloszlása (Eredeti vs Dedublikált)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
ax.hist(df['song_popularity'], bins=50, color='#1DB954', alpha=0.6, label='Eredeti adatállomány (N=18 835)', edgecolor='white')
ax.hist(df_dedup['song_popularity'], bins=50, color='#191414', alpha=0.5, label='Duplikációk nélkül (N=14 926)', edgecolor='white')
ax.axvline(df['song_popularity'].mean(), color='#1DB954', linestyle='--', linewidth=2, label=f'Eredeti átlag: {df["song_popularity"].mean():.1f}')
ax.axvline(df_dedup['song_popularity'].mean(), color='#191414', linestyle=':', linewidth=2, label=f'Dedublikált átlag: {df_dedup["song_popularity"].mean():.1f}')
ax.set_title('A célváltozó (song_popularity) eloszlása és a duplikációk hatása', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Népszerűség (0 - 100)', fontsize=10)
ax.set_ylabel('Gyakoriság (darab)', fontsize=10)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig1_popularity_distribution.png'))
plt.close()

# -------------------------------------------------------------
# 2. ÁBRA: Korrelációs mátrix hőtérkép
# -------------------------------------------------------------
num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != 'song_popularity'] + ['song_popularity']
corr_mat = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
cax = ax.matshow(corr_mat, cmap='coolwarm', vmin=-0.8, vmax=0.8)
fig.colorbar(cax, fraction=0.046, pad=0.04)

ax.set_xticks(range(len(num_cols)))
ax.set_yticks(range(len(num_cols)))
ax.set_xticklabels(num_cols, rotation=45, ha='left', fontsize=8)
ax.set_yticklabels(num_cols, fontsize=8)

for i in range(len(num_cols)):
    for j in range(len(num_cols)):
        val = corr_mat.iloc[i, j]
        color = 'white' if abs(val) > 0.45 else 'black'
        ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=7)

ax.set_title('Zenei jellemzők és népszerűség Pearson-korrelációs mátrixa', fontsize=12, fontweight='bold', pad=25)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig2_correlation_heatmap.png'))
plt.close()

# -------------------------------------------------------------
# 3. ÁBRA: Danceability és Loudness a népszerűségi sávokban
# -------------------------------------------------------------
bins = [-1, 19, 39, 59, 79, 100]
labels = ['0–19', '20–39', '40–59', '60–79', '80–100']
df['pop_cat'] = pd.cut(df['song_popularity'], bins=bins, labels=labels)

cat_stats = df.groupby('pop_cat', observed=False).agg(
    mean_dance=('danceability', 'mean'),
    mean_loud=('loudness', 'mean'),
    count=('song_popularity', 'count')
).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

# Danceability
bars1 = ax1.bar(cat_stats['pop_cat'], cat_stats['mean_dance'], color='#2ecc71', edgecolor='#27ae60', alpha=0.85)
ax1.set_ylim(0.5, 0.75)
ax1.set_title('Átlagos táncolhatóság (danceability)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Népszerűségi kategória', fontsize=9)
ax1.set_ylabel('Érték (0 - 1.0)', fontsize=9)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f'{yval:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

# Loudness
bars2 = ax2.bar(cat_stats['pop_cat'], cat_stats['mean_loud'], color='#e74c3c', edgecolor='#c0392b', alpha=0.85)
ax2.set_ylim(-9.5, -4.5)
ax2.set_title('Átlagos hangerő (loudness, dB)', fontsize=11, fontweight='bold')
ax2.set_xlabel('Népszerűségi kategória', fontsize=9)
ax2.set_ylabel('Hangerő (dB)', fontsize=9)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.2f} dB', ha='center', va='bottom', fontsize=8, fontweight='bold')

plt.suptitle('Kulcsfontosságú jellemzők változása népszerűségi kategóriák szerint', fontsize=12, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig3_danceability_loudness_by_cat.png'))
plt.close()

# -------------------------------------------------------------
# 4. ÁBRA: Duplikációk torzító hatása a korrelációkra
# -------------------------------------------------------------
features_comp = ['danceability', 'loudness', 'instrumentalness', 'acousticness', 'energy', 'audio_valence']
p_orig = df[features_comp].apply(lambda x: x.corr(df['song_popularity']))
p_dedup = df_dedup[features_comp].apply(lambda x: x.corr(df_dedup['song_popularity']))

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
x = np.arange(len(features_comp))
width = 0.35

ax.bar(x - width/2, p_orig, width, label='Eredeti (duplikált adatokkal)', color='#e67e22', alpha=0.9)
ax.bar(x + width/2, p_dedup, width, label='Dedublikált (tiszta adatokkal)', color='#3498db', alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels(features_comp, fontsize=9, rotation=15)
ax.set_ylabel('Pearson-korreláció a song_popularity-vel', fontsize=9)
ax.set_title('A duplikációk torzító hatása a zenei jellemzők és népszerűség korrelációjára', fontsize=11, fontweight='bold', pad=12)
ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax.legend(frameon=True, facecolor='white')
for i in range(len(features_comp)):
    ax.text(x[i] - width/2, p_orig.iloc[i] + (0.005 if p_orig.iloc[i] >= 0 else -0.015), f'{p_orig.iloc[i]:.3f}', ha='center', fontsize=7.5)
    ax.text(x[i] + width/2, p_dedup.iloc[i] + (0.005 if p_dedup.iloc[i] >= 0 else -0.015), f'{p_dedup.iloc[i]:.3f}', ha='center', fontsize=7.5)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig4_duplicate_bias_comparison.png'))
plt.close()

# -------------------------------------------------------------
# 5. ÁBRA: Ütemmutató (time_signature) megoszlása
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
ts_counts = df['time_signature'].value_counts().sort_index()
bars = ax.bar([str(int(k)) for k in ts_counts.index], ts_counts.values, color='#9b59b6', edgecolor='#8e44ad', alpha=0.85)
ax.set_yscale('log')
ax.set_title('Az ütemmutatók (time_signature) eloszlása (logaritmikus skála)', fontsize=11, fontweight='bold', pad=10)
ax.set_xlabel('Ütemmutató értéke', fontsize=9)
ax.set_ylabel('Gyakoriság (darab, log skála)', fontsize=9)
for bar in bars:
    yval = bar.get_height()
    pct = (yval / len(df)) * 100
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.2, f'{yval:,}\n({pct:.2f}%)', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig5_time_signature_dist.png'))
plt.close()

print("Minden ábra sikeresen legenerálva a figures mappába!")
