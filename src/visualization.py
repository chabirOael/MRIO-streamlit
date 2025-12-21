"""
Visualization functions for MRIO emissions decomposition analysis.
"""
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe
from matplotlib.patches import FancyBboxPatch


def fmt_kg(x):
    return f"{x:,.0f} kg"


def percent(x, total):
    return 0.0 if total == 0 else 100.0 * x / total


colors = {
    'direct': '#2E5090',
    'domestic': '#E67E22',
    'foreign': '#27AE60',
    'accent': '#95A5A6',
    'background': '#FAFBFC',
    'text_dark': '#2C3E50',
    'text_light': '#7F8C8D'
}


def create_enhanced_donut(direct, domestic_indirect, foreign_indirect, country, sector_name, stressor, unit_label="per 1 M€ final demand"):
    sizes = [direct, domestic_indirect, foreign_indirect]
    labels = [f"{country} (Direct)", f"{country} (Indirect)", "Rest of world (Indirect)"]
    chart_colors = [colors['direct'], colors['domestic'], colors['foreign']]

    fig = plt.figure(figsize=(14, 8), facecolor='white')
    ax_donut = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=3)

    wedges, texts, autotexts = ax_donut.pie(
        sizes,
        labels=[None]*len(labels),
        autopct=lambda p: f"{p:.1f}%\n{fmt_kg(p/100 * sum(sizes))}" if p > 2 else "",
        startangle=90,
        counterclock=False,
        colors=chart_colors,
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3, antialiased=True),
        pctdistance=0.75
    )

    for i, autotext in enumerate(autotexts):
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')
        autotext.set_path_effects([pe.withStroke(linewidth=3.5, foreground=chart_colors[i], alpha=0.8)])

    center_circle = plt.Circle((0, 0), 0.50, color='white', linewidth=2, edgecolor=colors['accent'], alpha=0.95)
    ax_donut.add_artist(center_circle)

    ax_donut.text(0, 0.15, country, ha="center", va="center", fontsize=28, fontweight='bold', color=colors['text_dark'])

    total_emissions = sum(sizes)
    ax_donut.text(0, -0.05, "Total", ha="center", va="center", fontsize=11, color=colors['text_light'], style='italic')
    ax_donut.text(0, -0.22, fmt_kg(total_emissions), ha="center", va="center", fontsize=16, fontweight='bold', color=colors['text_dark'])

    ax_donut.axis('equal')

    legend_labels = []
    for i in range(len(labels)):
        pct = percent(sizes[i], total_emissions)
        legend_labels.append(f"{labels[i]}: {fmt_kg(sizes[i])} ({pct:.1f}%)")

    legend = ax_donut.legend(
        wedges, legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=1,
        frameon=True,
        fontsize=10,
        framealpha=0.95,
        edgecolor=colors['accent'],
        fancybox=True,
        shadow=True
    )
    legend.get_frame().set_facecolor(colors['background'])

    title_text = f"Emissions decomposition: {sector_name}"
    subtitle_text = f"{unit_label} • {stressor}"
    ax_donut.text(0.5, 1.12, title_text, transform=ax_donut.transAxes,
                  ha='center', fontsize=14, fontweight='bold', color=colors['text_dark'])
    ax_donut.text(0.5, 1.06, subtitle_text, transform=ax_donut.transAxes,
                  ha='center', fontsize=10, color=colors['text_light'], style='italic')

    ax_details = plt.subplot2grid((3, 3), (0, 2), rowspan=3)
    ax_details.axis('off')

    details_y = 0.95
    line_height = 0.10

    ax_details.text(0.5, details_y, "Detailed Breakdown",
                    ha='center', fontsize=12, fontweight='bold',
                    color=colors['text_dark'], transform=ax_details.transAxes)
    details_y -= line_height * 1.5

    def detail_row(y, color, title, value):
        ax_details.add_patch(plt.Rectangle((0.05, y - 0.04), 0.04, 0.04,
                                           facecolor=color, transform=ax_details.transAxes, clip_on=False))
        ax_details.text(0.12, y, title, fontsize=10, fontweight='bold',
                        color=colors['text_dark'], transform=ax_details.transAxes, va='center')
        y2 = y - line_height * 0.6
        ax_details.text(0.12, y2, fmt_kg(value), fontsize=11, color=color, fontweight='bold',
                        transform=ax_details.transAxes, va='center')
        ax_details.text(0.88, y2, f"{percent(value, total_emissions):.1f}%",
                        fontsize=10, color=colors['text_light'],
                        transform=ax_details.transAxes, va='center', ha='right')
        return y2 - line_height * 1.3

    details_y = detail_row(details_y, colors['direct'],   "Direct (on-site intensity)", direct)
    details_y = detail_row(details_y, colors['domestic'], "Domestic supply chain",       domestic_indirect)
    details_y = detail_row(details_y, colors['foreign'],  "Foreign supply chain",        foreign_indirect)

    fancy_box = FancyBboxPatch(
        (0.02, 0.08), 0.96, 0.87,
        boxstyle="round,pad=0.02",
        edgecolor=colors['accent'],
        facecolor=colors['background'],
        linewidth=1.5,
        transform=ax_details.transAxes,
        zorder=-1
    )
    ax_details.add_patch(fancy_box)

    plt.tight_layout()
    return fig

