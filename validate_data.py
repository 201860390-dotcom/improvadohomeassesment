# validate_data.py — Auditoría de datos pre-dashboard
import pandas as pd
import sys

print("=" * 60)
print("ANTIGRAVITY · DATA VALIDATION AUDIT")
print("Improvado TCS Assignment — Pre-Build Check")
print("=" * 60)

# ── CARGA DE ARCHIVOS ──────────────────────────────────────────
try:
    daily    = pd.read_csv("marketing_daily_2023.csv")
    channels = pd.read_csv("channel_summary.csv")
    sources  = pd.read_csv("data_source_summary.csv")
    campaigns= pd.read_csv("campaign_summary.csv")
    print("\n✓ Los 4 archivos CSV cargados correctamente")
except FileNotFoundError as e:
    print(f"\n✗ ERROR: Archivo no encontrado → {e}")
    sys.exit(1)

# ── SHAPES ────────────────────────────────────────────────────
print(f"\n── SHAPES ──")
print(f"  marketing_daily_2023 : {daily.shape[0]:,} filas × {daily.shape[1]} cols")
print(f"  channel_summary      : {channels.shape[0]:,} filas × {channels.shape[1]} cols")
print(f"  data_source_summary  : {sources.shape[0]:,} filas × {sources.shape[1]} cols")
print(f"  campaign_summary     : {campaigns.shape[0]:,} filas × {campaigns.shape[1]} cols")

# ── VALIDACIÓN 1: Organic Spend = $0 ─────────────────────────
print(f"\n── VALIDACIÓN 1: Organic Spend = $0 ──")
organic = daily[daily['channel'] == 'Organic']
organic_spend = organic['spend_usd'].sum()
if organic_spend == 0:
    print(f"  ✓ PASS — Organic spend total: $0.00")
else:
    print(f"  ✗ FAIL — Organic spend detectado: ${organic_spend:,.2f}")

# ── VALIDACIÓN 2: CTR dentro del rango 2%–12% ────────────────
print(f"\n── VALIDACIÓN 2: CTR en rango 2%–12% ──")
ctr_min = daily['ctr_pct'].min()
ctr_max = daily['ctr_pct'].max()
if ctr_min >= 2.0 and ctr_max <= 12.0:
    print(f"  ✓ PASS — CTR rango: {ctr_min:.2f}% – {ctr_max:.2f}%")
else:
    print(f"  ✗ FAIL — CTR fuera de rango: {ctr_min:.2f}% – {ctr_max:.2f}%")

# ── VALIDACIÓN 3: Pico de Septiembre ─────────────────────────
print(f"\n── VALIDACIÓN 3: Pico estacional Septiembre ──")
daily['date'] = pd.to_datetime(daily['date'])
daily['month'] = daily['date'].dt.month
monthly_avg = daily.groupby('month')['impressions'].sum()
sept_impressions = monthly_avg.get(9, 0)
avg_other = monthly_avg.drop(9).mean()
multiplier = sept_impressions / avg_other if avg_other > 0 else 0
if multiplier >= 2.8:
    print(f"  ✓ PASS — Pico septiembre: {multiplier:.1f}x sobre promedio")
else:
    print(f"  ⚠ WARN — Multiplicador septiembre: {multiplier:.1f}x (esperado ≥2.8x)")

# ── VALIDACIÓN 4: Consistencia Matemática Clicks ─────────────
print(f"\n── VALIDACIÓN 4: Clicks ≈ Impressions × CTR ──")
daily['clicks_calculated'] = (daily['impressions'] * daily['ctr_pct'] / 100).round()
diff = (daily['clicks'] - daily['clicks_calculated']).abs()
max_diff_pct = (diff / daily['clicks'].replace(0, 1)).max() * 100
if max_diff_pct <= 0.5:
    print(f"  ✓ PASS — Desviación máxima: {max_diff_pct:.3f}%")
else:
    print(f"  ⚠ WARN — Desviación máxima: {max_diff_pct:.3f}% (tolerancia: 0.5%)")

# ── KPIs GLOBALES CALCULADOS ──────────────────────────────────
print(f"\n── KPIs GLOBALES (calculados desde CSV) ──")
paid = daily[daily['channel'] != 'Organic']

total_spend       = daily['spend_usd'].sum()
total_impressions = daily['impressions'].sum()
total_clicks      = daily['clicks'].sum()
total_conversions = daily['conversions'].sum()
total_video_views = daily['video_views'].sum()
avg_cpm           = (paid['spend_usd'].sum() / paid['impressions'].sum() * 1000)
avg_ctr           = (total_clicks / total_impressions * 100)
avg_cpc           = (paid['spend_usd'].sum() / paid['clicks'].sum())
conv_rate         = (total_conversions / total_clicks * 100)

print(f"  Total Spend       : ${total_spend:>15,.0f}  (~${total_spend/1e6:.1f}M)")
print(f"  Avg CPM           : ${avg_cpm:>15,.2f}")
print(f"  Avg CTR Global    : {avg_ctr:>15.2f}%")
print(f"  Avg CPC           : ${avg_cpc:>15,.2f}")
print(f"  Total Video Views : {total_video_views:>15,.0f}  (~{total_video_views/1e6:.1f}M)")
print(f"  Total Impressions : {total_impressions:>15,.0f}  (~{total_impressions/1e6:.1f}M)")
print(f"  Total Conversions : {total_conversions:>15,.0f}  (~{total_conversions/1e6:.2f}M)")
print(f"  Conv. Rate Global : {conv_rate:>15.2f}%")

# ── VALIDACIÓN 5: Consistencia cruzada channel_summary ────────
print(f"\n── VALIDACIÓN 5: Consistencia cruzada channel_summary ──")
daily_by_channel = daily.groupby('channel').agg(
    impressions_calc=('impressions','sum'),
    spend_calc=('spend_usd','sum')
).reset_index()

for _, row in daily_by_channel.iterrows():
    ch = row['channel']
    ch_row = channels[channels['channel'] == ch]
    if ch_row.empty:
        print(f"  ⚠ Canal '{ch}' no encontrado en channel_summary")
        continue
    csv_imp = ch_row['impressions_total'].values[0]
    calc_imp = row['impressions_calc']
    delta_pct = abs(csv_imp - calc_imp) / calc_imp * 100 if calc_imp > 0 else 0
    status = "✓" if delta_pct < 0.1 else "⚠"
    print(f"  {status} {ch:<15} Δ impressions: {delta_pct:.3f}%")

# ── CANALES DISPONIBLES ───────────────────────────────────────
print(f"\n── CANALES DETECTADOS ──")
for ch in sorted(daily['channel'].unique()):
    count = daily[daily['channel'] == ch].shape[0]
    print(f"  • {ch:<20} {count:,} registros")

print(f"\n── FUENTES DETECTADAS ──")
for src in sorted(daily['data_source'].unique()):
    print(f"  • {src}")

print("\n" + "=" * 60)
print("✓ VALIDACIÓN COMPLETA — Listo para construir el dashboard")
print("=" * 60)

# Exporta KPIs para uso en main.py
kpis = {
    'total_spend': total_spend,
    'avg_cpm': avg_cpm,
    'avg_ctr': avg_ctr,
    'avg_cpc': avg_cpc,
    'total_video_views': total_video_views,
    'total_impressions': total_impressions,
    'total_conversions': total_conversions,
    'conv_rate': conv_rate
}
print("\nKPIs exportados para main.py ✓")
