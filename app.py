
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="NewsIntel India | Cyber Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# DARK CYBERSECURITY THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #080b10;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #202938;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    .subtitle {
        color: #8b9bb0;
        font-size: 15px;
        margin-top: -12px;
        margin-bottom: 22px;
    }

    .section-title {
        color: #f1f5f9;
        font-size: 20px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background: #101722;
        border: 1px solid #253144;
        border-radius: 12px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9caec4;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #0b1018;
        border: 1px solid #1f2a3a;
        border-radius: 12px;
        padding: 6px;
    }

    .footer {
        color: #64748b;
        font-size: 12px;
        border-top: 1px solid #202938;
        padding-top: 14px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "raw"
    / "NewsIntel_final.csv"
)


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


def normalize_column_name(name):
    """Make column names easier to match across CSV versions."""
    return (
        str(name)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
        .replace("/", " ")
    )


COLUMN_ALIASES = {
    "date": [
        "date",
        "incident date",
        "incident date reported",
        "reported date",
        "timestamp",
    ],
    "victim": [
        "victim",
        "victim target",
        "victim or target",
        "organization",
        "organisation",
        "company",
        "target",
        "name",
    ],
    "country": [
        "country",
        "target country",
    ],
    "location": [
        "city or region",
        "state or region",
        "location",
        "city",
        "region",
        "state",
        "geography",
    ],
    "sector": [
        "sector",
        "industry",
        "victim sector",
    ],
    "attack_type": [
        "attack type",
        "type of attack",
        "incident type",
        "threat type",
        "attack",
    ],
    "summary": [
        "summary",
        "description",
        "details",
        "incident summary",
        "notes",
    ],
    "source": [
        "source",
        "source url",
        "url",
        "reference",
        "references",
    ],
    "status": [
        "verification status",
        "status",
        "verification",
        "confidence",
    ],
    "latitude": [
        "latitude",
        "lat",
    ],
    "longitude": [
        "longitude",
        "lon",
        "lng",
        "long",
    ],
}


def standardize_columns(df):
    """Rename recognized CSV headers to consistent internal names."""
    df = df.copy()
    normalized_lookup = {
        normalize_column_name(col): col for col in df.columns
    }

    rename_map = {}

    for standard_name, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_column_name(alias)

            if normalized_alias in normalized_lookup:
                original_name = normalized_lookup[normalized_alias]
                rename_map[original_name] = standard_name
                break

    return df.rename(columns=rename_map)


if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Please put NewsIntel_final.csv inside "
        "'data/raw/' in your project folder."
    )
    st.code("NewsIntel/data/raw/NewsIntel_final.csv")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

df = standardize_columns(df)

# Add missing optional fields so the dashboard can still run.
for col in [
    "date",
    "victim",
    "country",
    "location",
    "sector",
    "attack_type",
    "summary",
    "source",
    "status",
    "latitude",
    "longitude",
]:
    if col not in df.columns:
        df[col] = pd.NA

# Normalize data types.
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

for col in ["latitude", "longitude"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in [
    "victim",
    "country",
    "location",
    "sector",
    "attack_type",
    "summary",
    "source",
    "status",
]:
    df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    df[col] = df[col].replace("", "Unknown")

# Keep incidents within the requested timeline.
START_DATE = pd.Timestamp("2024-07-01")
END_DATE = pd.Timestamp("2026-07-31")

timeline_df = df[
    df["date"].between(START_DATE, END_DATE, inclusive="both")
].copy()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("# 🛡️ NewsIntel India")
st.markdown(
    '<div class="subtitle">'
    "Cyber Threat Intelligence Dashboard · India-focused incident monitoring"
    "</div>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Filter the incidents displayed below.")

if timeline_df.empty:
    st.warning(
        "No incidents have dates between July 2024 and July 2026. "
        "Check the date column in your CSV."
    )

def make_filter(label, column):
    values = sorted(
        value
        for value in timeline_df[column].dropna().unique().tolist()
        if str(value).strip() and str(value) != "Unknown"
    )

    options = ["All"] + values

    return st.sidebar.selectbox(
        label,
        options=options,
        index=0,
    )


selected_sector = make_filter("Sector", "sector")
selected_attack = make_filter("Attack Type", "attack_type")
selected_status = make_filter("Verification Status", "status")
selected_country = make_filter("Country", "country")

filtered_df = timeline_df.copy()

if selected_sector != "All":
    filtered_df = filtered_df[
        filtered_df["sector"] == selected_sector
    ]

if selected_attack != "All":
    filtered_df = filtered_df[
        filtered_df["attack_type"] == selected_attack
    ]

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ]

st.sidebar.divider()
st.sidebar.caption(
    "Timeline: July 2024 – July 2026"
)

# --------------------------------------------------
# INDIA INCIDENT MAP — TOP OF DASHBOARD
# --------------------------------------------------
st.markdown(
    '<div class="section-title">🗺️ India Cyber Incident Map</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Highlighted points represent incidents with usable coordinates. "
    "Map locations may be approximate."
)

map_df = filtered_df.dropna(
    subset=["latitude", "longitude"]
).copy()

# Rough geographic bounds for India. This is a visual filter,
# not proof that an incident occurred within India's borders.
map_df = map_df[
    map_df["latitude"].between(6, 38)
    & map_df["longitude"].between(68, 98)
]

if map_df.empty:
    st.info(
        "No incidents with valid India-region coordinates match these "
        "filters. Check the CSV latitude and longitude fields, or change "
        "the filters."
    )
else:
    map_df["map_label"] = (
        map_df["victim"].astype(str)
        + " · "
        + map_df["attack_type"].astype(str)
    )

    fig_map = px.scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        color="attack_type",
        hover_name="victim",
        hover_data={
            "date": True,
            "location": True,
            "sector": True,
            "status": True,
            "latitude": False,
            "longitude": False,
        },
        zoom=3.4,
        center={"lat": 22.5, "lon": 79.0},
        height=570,
        map_style="carto-darkmatter",
        color_discrete_sequence=[
            "#00e5ff",
            "#ff3b6b",
            "#ffb020",
            "#a78bfa",
            "#36d399",
            "#f97316",
            "#e879f9",
        ],
    )

    fig_map.update_traces(
        marker={
            "size": 15,
            "opacity": 0.95,
        }
    )

    fig_map.update_layout(
        paper_bgcolor="#080b10",
        plot_bgcolor="#080b10",
        font_color="#e5e7eb",
        margin=dict(l=0, r=0, t=10, b=0),
        legend_title_text="Attack Type",
        legend=dict(
            bgcolor="rgba(8,11,16,0.85)",
            bordercolor="#273449",
            borderwidth=1,
        ),
        map_style="carto-darkmatter",
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        config={
            "displaylogo": False,
            "scrollZoom": True,
        },
    )

st.caption(
    "Note: map points depend on the coordinates supplied in the dataset. "
    "A plotted point does not independently verify an incident."
)

# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------
st.markdown("## 📊 Threat Overview")

total_incidents = len(filtered_df)
unique_targets = (
    filtered_df["victim"].replace("Unknown", pd.NA).nunique()
)
attack_types_count = (
    filtered_df["attack_type"].replace("Unknown", pd.NA).nunique()
)
sectors_count = (
    filtered_df["sector"].replace("Unknown", pd.NA).nunique()
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Incidents", f"{total_incidents:,}")
m2.metric("Unique Targets", f"{unique_targets:,}")
m3.metric("Attack Types", f"{attack_types_count:,}")
m4.metric("Sectors Affected", f"{sectors_count:,}")

st.markdown("")

# --------------------------------------------------
# ATTACK TYPE AND SECTOR CHARTS
# --------------------------------------------------
st.markdown("## 📈 Threat Analysis")

left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown("### Incidents by Attack Type")

    attack_counts = (
        filtered_df["attack_type"]
        .value_counts()
        .rename_axis("Attack Type")
        .reset_index(name="Incidents")
    )

    if attack_counts.empty:
        st.info("No attack-type data available.")
    else:
        fig_attack = px.bar(
            attack_counts,
            x="Incidents",
            y="Attack Type",
            orientation="h",
            text="Incidents",
            color="Incidents",
            color_continuous_scale=["#164e63", "#00e5ff"],
        )

        fig_attack.update_layout(
            template="plotly_dark",
            paper_bgcolor="#080b10",
            plot_bgcolor="#080b10",
            font_color="#e5e7eb",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=15, b=10),
        )

        st.plotly_chart(
            fig_attack,
            use_container_width=True,
        )

with right_chart:
    st.markdown("### Incidents by Sector")

    sector_counts = (
        filtered_df["sector"]
        .value_counts()
        .rename_axis("Sector")
        .reset_index(name="Incidents")
    )

    if sector_counts.empty:
        st.info("No sector data available.")
    else:
        fig_sector = px.bar(
            sector_counts,
            x="Incidents",
            y="Sector",
            orientation="h",
            text="Incidents",
            color="Incidents",
            color_continuous_scale=["#312e81", "#a78bfa"],
        )

        fig_sector.update_layout(
            template="plotly_dark",
            paper_bgcolor="#080b10",
            plot_bgcolor="#080b10",
            font_color="#e5e7eb",
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=15, b=10),
        )

        st.plotly_chart(
            fig_sector,
            use_container_width=True,
        )

# --------------------------------------------------
# MONTHLY TIMELINE: JULY 2024 – JULY 2026
# --------------------------------------------------
st.markdown("## 📅 Incident Timeline")
st.caption("Monthly incident counts from July 2024 through July 2026.")

if filtered_df["date"].notna().any():
    monthly_counts = (
        filtered_df.dropna(subset=["date"])
        .set_index("date")
        .resample("MS")
        .size()
    )

    all_months = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="MS",
    )

    monthly_counts = monthly_counts.reindex(
        all_months,
        fill_value=0,
    )

    timeline_chart_df = pd.DataFrame(
        {
            "Month": all_months,
            "Incidents": monthly_counts.values,
        }
    )

    fig_timeline = px.line(
        timeline_chart_df,
        x="Month",
        y="Incidents",
        markers=True,
    )

    fig_timeline.update_traces(
        line=dict(color="#00e5ff", width=3),
        marker=dict(size=7, color="#00e5ff"),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.10)",
    )

    fig_timeline.update_layout(
        template="plotly_dark",
        paper_bgcolor="#080b10",
        plot_bgcolor="#080b10",
        font_color="#e5e7eb",
        xaxis_title="Month",
        yaxis_title="Number of Incidents",
        xaxis=dict(
            range=["2024-07-01", "2026-08-01"],
            dtick="M2",
            tickformat="%b %Y",
        ),
        margin=dict(l=10, r=10, t=15, b=10),
    )

    st.plotly_chart(
        fig_timeline,
        use_container_width=True,
    )
else:
    st.info("No valid incident dates are available for the timeline.")

# --------------------------------------------------
# INCIDENT EXPLORER
# --------------------------------------------------
st.markdown("## 🔎 Incident Explorer")

search_text = st.text_input(
    "Search incidents",
    placeholder="Search by target, location, sector, or attack type...",
)

search_df = filtered_df.copy()

if search_text.strip():
    searchable = (
        search_df["victim"].astype(str)
        + " "
        + search_df["location"].astype(str)
        + " "
        + search_df["sector"].astype(str)
        + " "
        + search_df["attack_type"].astype(str)
        + " "
        + search_df["summary"].astype(str)
        + " "
        + search_df["country"].astype(str)
    )

    search_df = search_df[
        searchable.str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

display_df = search_df.copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df["date"] = display_df["date"].fillna("Unknown")

display_columns = [
    "date",
    "victim",
    "country",
    "location",
    "sector",
    "attack_type",
    "status",
]

st.dataframe(
    display_df[display_columns].rename(
        columns={
            "date": "Date",
            "victim": "Victim / Target",
            "country": "Country",
            "location": "Location",
            "sector": "Sector",
            "attack_type": "Attack Type",
            "status": "Verification Status",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Showing {len(search_df)} matching incident(s).")

# --------------------------------------------------
# INCIDENT DETAILS
# --------------------------------------------------
st.markdown("## 📝 Incident Details")

if not search_df.empty:
    options = search_df.index.tolist()

    def format_incident(index):
        row = search_df.loc[index]
        date_label = (
            row["date"].strftime("%Y-%m-%d")
            if pd.notna(row["date"])
            else "Unknown date"
        )
        return f"{date_label} | {row['victim']} | {row['attack_type']}"

    selected_index = st.selectbox(
        "Select an incident",
        options=options,
        format_func=format_incident,
    )

    incident = search_df.loc[selected_index]

    st.markdown(f"### {incident['victim']}")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write(f"**Date:** {format_incident(selected_index).split(' | ')[0]}")
        st.write(f"**Country:** {incident['country']}")
        st.write(f"**Location:** {incident['location']}")
        st.write(f"**Sector:** {incident['sector']}")

    with detail_col2:
        st.write(f"**Attack Type:** {incident['attack_type']}")
        st.write(f"**Verification Status:** {incident['status']}")

    st.markdown("**Incident Summary**")

    summary = incident["summary"]
    if summary and summary != "Unknown":
        st.write(summary)
    else:
        st.write("No summary is available for this incident.")

else:
    st.info("No incidents match your search and filters.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
    NewsIntel India · Cyber Threat Intelligence Dashboard<br>
    Research and visualization project. Incident claims may be unverified.
    Dates, target details, and geographic coordinates depend on the source
    dataset and should not be treated as independently confirmed facts.
    </div>
    """,
    unsafe_allow_html=True,
)
