import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, '..'))
csv_path = os.path.join(base_dir, 'data', 'song_data.csv')
output_dir = os.path.join(base_dir, 'figures')
os.makedirs(output_dir, exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 9

df = pd.read_csv(csv_path)
df_dedup = df.drop_duplicates()

# 2x2 figura létrehozása
fig, axs = plt.subplots(2, 2, figsize=(11, 7.5), dpi=300)

# PANEL A: Célváltozó eloszlása
ax_a = axs[0, 0]
ax_a.hist(df['song_popularity'], bins=40, color='#1DB954', alpha=0.55, label=f'Eredeti minta (N=18 835, $\mu$={df["song_popularity"].mean():.1f})', edgecolor='white')
ax_a.hist(df_dedup['song_popularity'], bins=40, color='#191414', alpha=0.5, label=f'Dedublikált minta (N=14 926, $\mu$={df_dedup["song_popularity"].mean():.1f})', edgecolor='white')
ax_a.axvline(df['song_popularity'].mean(), color='#1DB954', linestyle='--', linewidth=1.8)
ax_a.axvline(df_dedup['song_popularity'].mean(), color='#191414', linestyle=':', linewidth=1.8)
ax_a.set_title('(A) A song_popularity eloszlása és a slágertorzulás', fontsize=10.5, fontweight='bold')
ax_a.set_xlabel('Népszerűség (0–100)', fontsize=9)
ax_a.set_ylabel('Gyakoriság (darab)', fontsize=9)
ax_a.legend(fontsize=8, frameon=True, facecolor='white', loc='upper left')

# PANEL B: Korrelációs mátrix
ax_b = axs[0, 1]
key_cols = ['danceability', 'loudness', 'energy', 'acousticness', 'instrumentalness', 'audio_valence', 'song_popularity']
corr_sub = df[key_cols].corr()
cax = ax_b.matshow(corr_sub, cmap='coolwarm', vmin=-0.75, vmax=0.75)
fig.colorbar(cax, ax=ax_b, fraction=0.046, pad=0.04)

ax_b.set_xticks(range(len(key_cols)))
ax_b.set_yticks(range(len(key_cols)))
labels_short = ['dance', 'loud', 'energy', 'acoust', 'instr', 'valence', 'POPULARITY']
ax_b.set_xticklabels(labels_short, rotation=35, ha='left', fontsize=8)
ax_b.set_yticklabels(labels_short, fontsize=8)

for i in range(len(key_cols)):
    for j in range(len(key_cols)):
        val = corr_sub.iloc[i, j]
        color = 'white' if abs(val) > 0.45 else 'black'
        ax_b.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=7.5, fontweight='bold' if j==6 or i==6 else 'normal')
ax_b.set_title('(B) Pearson-korrelációk és multikollinearitás', fontsize=10.5, fontweight='bold', pad=18)

# PANEL C: Kategóriánkénti Danceability és Loudness
ax_c = axs[1, 0]
bins = [-1, 19, 39, 59, 79, 100]
labels = ['0–19', '20–39', '40–59', '60–79', '80–100']
df['pop_cat'] = pd.cut(df['song_popularity'], bins=bins, labels=labels)
cat_means = df.groupby('pop_cat', observed=False).agg(
    dance=('danceability', 'mean'),
    loud=('loudness', 'mean')
).reset_index()

x = np.arange(len(labels))
width = 0.35
ax_c1 = ax_c
ax_c2 = ax_c.twinx()

rects1 = ax_c1.bar(x - width/2, cat_means['dance'], width, color='#2ecc71', alpha=0.85, label='Danceability')
rects2 = ax_c2.bar(x + width/2, cat_means['loud'], width, color='#e74c3c', alpha=0.85, label='Loudness [dB]')
ax_c1.set_ylim(0.5, 0.75)
ax_c2.set_ylim(-10, -4)
ax_c1.set_xticks(x)
ax_c1.set_xticklabels(labels, fontsize=8.5)
ax_c1.set_xlabel('Népszerűségi kategória', fontsize=9)
ax_c1.set_ylabel('Átlagos táncolhatóság (0–1)', fontsize=8.5, color='#27ae60')
ax_c2.set_ylabel('Átlagos hangerő (dB)', fontsize=8.5, color='#c0392b')
ax_c.set_title('(C) Táncolhatóság és hangerő ugrása a slágereknél', fontsize=10.5, fontweight='bold')

for rect in rects1:
    h = rect.get_height()
    ax_c1.text(rect.get_x() + rect.get_width()/2., h + 0.005, f'{h:.2f}', ha='center', va='bottom', fontsize=7.5)
for rect in rects2:
    h = rect.get_height()
    ax_c2.text(rect.get_x() + rect.get_width()/2., h + 0.15, f'{h:.1f}', ha='center', va='bottom', fontsize=7.5)

# PANEL D: Duplikációk torzító hatása
ax_d = axs[1, 1]
features_comp = ['danceability', 'loudness', 'instrumentalness', 'acousticness', 'energy']
p_orig = df[features_comp].apply(lambda s: s.corr(df['song_popularity']))
p_dedup = df_dedup[features_comp].apply(lambda s: s.corr(df_dedup['song_popularity']))
x_d = np.arange(len(features_comp))
ax_d.bar(x_d - width/2, p_orig, width, label='Eredeti (duplikált)', color='#e67e22', alpha=0.85)
ax_d.bar(x_d + width/2, p_dedup, width, label='Dedublikált (tiszta)', color='#3498db', alpha=0.85)
ax_d.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax_d.set_xticks(x_d)
ax_d.set_xticklabels(['dance', 'loudness', 'instrum.', 'acoustic', 'energy'], fontsize=8.5)
ax_d.set_ylabel('Pearson r a népszerűséggel', fontsize=9)
ax_d.set_title('(D) A duplikációk torzítása a korrelációkra', fontsize=10.5, fontweight='bold')
ax_d.legend(fontsize=8, frameon=True, facecolor='white', loc='lower right')

for i in range(len(features_comp)):
    v1, v2 = p_orig.iloc[i], p_dedup.iloc[i]
    ax_d.text(x_d[i] - width/2, v1 + (0.005 if v1>=0 else -0.015), f'{v1:+.2f}', ha='center', fontsize=7.5)
    ax_d.text(x_d[i] + width/2, v2 + (0.005 if v2>=0 else -0.015), f'{v2:+.2f}', ha='center', fontsize=7.5)

plt.suptitle('EDA ÖSSZEFOGLALÓ DASHBOARD – SPOTIFY DALNÉPSZERŰSÉG ADATHALMAZ', fontsize=12, fontweight='bold', y=0.995)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'dashboard_eda_summary.png'), bbox_inches='tight')
plt.close()
print(f"Dashboard kép elkészült: {os.path.join(output_dir, 'dashboard_eda_summary.png')}")
