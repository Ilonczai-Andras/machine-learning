import pandas as pd
import numpy as np

df = pd.read_csv('1_milestone/song_data.csv')
num_cols = df.select_dtypes(include=[np.number]).columns

stats = []
for c in num_cols:
    s = df[c]
    stats.append({
        'Feature': c,
        'Count': len(s),
        'Mean': s.mean(),
        'Std': s.std(),
        'Min': s.min(),
        'Q25': s.quantile(0.25),
        'Median': s.median(),
        'Q75': s.quantile(0.75),
        'Max': s.max(),
        'Skew': s.skew()
    })

stats_df = pd.DataFrame(stats)
print(stats_df.to_string(index=False))

# Check duplicates detail
dups_all = df.duplicated().sum()
dups_subset = df.duplicated(subset=[c for c in df.columns if c != 'song_name']).sum()
print(f"\nExact duplicates (all cols): {dups_all}")
print(f"Duplicates excluding song_name: {dups_subset}")

# Correlation matrix with song_popularity
corrs_p = df[num_cols].corr(method='pearson')['song_popularity'].drop('song_popularity')
corrs_s = df[num_cols].corr(method='spearman')['song_popularity'].drop('song_popularity')
corr_summary = pd.DataFrame({'Pearson': corrs_p, 'Spearman': corrs_s}).sort_values(by='Pearson', ascending=False)
print("\nCorrelations with song_popularity:")
print(corr_summary.to_string())

# Audio feature inter-correlations (top pairs)
corr_matrix = df[num_cols].corr()
pairs = []
for i in range(len(num_cols)):
    for j in range(i + 1, len(num_cols)):
        c1, c2 = num_cols[i], num_cols[j]
        pairs.append((c1, c2, corr_matrix.loc[c1, c2]))
pairs.sort(key=lambda x: abs(x[2]), reverse=True)
print("\nTop 10 strongest feature correlations:")
for c1, c2, val in pairs[:10]:
    print(f"{c1} <-> {c2}: {val:.4f}")
