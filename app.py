
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import streamlit as st


# -- Set page config
apptitle = 'VictorIA Trekkers'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  color: #07173F !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.image("assets/image2.png", width='stretch')
st.sidebar.markdown("# Exoplanet Data Explorer")

uploaded_df = None
with st.sidebar:
    tab_input, tab_view = st.tabs(["Input", "View"])
    
    with tab_input:
        # -- upload data file
        tab_input.markdown('## Data load')
        uploaded_file = tab_input.file_uploader("Choose an Excel or CSV file", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            # Check file type and load accordingly
            if uploaded_file.name.endswith('.csv'):
                uploaded_df = pd.read_csv(uploaded_file, sep=',', quotechar='"', escapechar='\\',
                         skiprows=144, on_bad_lines='skip', header=0)
            elif uploaded_file.name.endswith('.xlsx'):
                uploaded_df = pd.read_excel(uploaded_file,skiprows=144, header=0)
            else:
                st.error("Unsupported file type.")
                uploaded_df = None

        tab_input.markdown('## AI configuration')
        tab_input.markdown('### Model')
        select_model = tab_input.selectbox('Select Model', ['CNN', 'CNN + Explainability Layer (Do not work)', 'SNN (Do not work)', 'GAN (Do not work)',
                                                            'KNN (Do not work)', 'RF (Do not work)', 'DT (Do not work)', 'CatBoost (Do not work)', 'Logistic Regression (Do not work)'])

        tab_input.markdown('### Set hyperparameters')

        test_size = tab_input.slider('Test size (%)', 0, 100, 30)  # min, max, default
        max_iter = tab_input.slider('Max iterations', 100, 5000, 1000)  # min, max, default
        random_state = tab_input.slider('Random state', 10, 100, 42)  # min, max, default
        validation_fraction = tab_input.slider('Validation fraction', 0, 20, 15)  # min, max, default

        data_origin = tab_input.multiselect('Select Data Origin', ['Kepler', 'K2 (Do not work)', 'TESS (Do not work)'])

        # Display the uploaded data for preview in main area
        if uploaded_df is not None:
            # Append button
            if st.button("Append to Main DataFrame"):
                # Append uploaded data to main dataframe
                st.session_state["main_df"] = pd.concat(
                    [st.session_state["main_df"], uploaded_df], ignore_index=True
                )
                st.success("Data appended!")

    with tab_view:
        st.write("Data Preview")
        if uploaded_file is not None and uploaded_df is not None:
            st.dataframe(uploaded_df)
        else:
            st.write("No data uploaded yet.")

mapeamento_koi = {
    # Identification and Catalog
    'rowid': 'Row ID',
    'kepid': 'KepID',
    'kepoi_name': 'KOI Name',
    'kepler_name': 'Kepler Name',

    # Disposition and Status
    'koi_disposition': 'Exoplanet Archive Disposition',
    'koi_vet_stat': 'Vetting Status',
    'koi_vet_date': 'Date of Last Parameter Update',
    'koi_pdisposition': 'Disposition Using Kepler Data',
    'koi_score': 'Disposition Score',

    # False Positive Flags
    'koi_fpflag_nt': 'Not Transit-Like False Positive Flag',
    'koi_fpflag_ss': 'Stellar Eclipse False Positive Flag',
    'koi_fpflag_co': 'Centroid Offset False Positive Flag',
    'koi_fpflag_ec': 'Ephemeris Match Indicates Contamination False Positive Flag',
    'koi_disp_prov': 'Disposition Provenance',
    'koi_comment': 'Comment',

    # Orbital Parameters
    'koi_period': 'Orbital Period [days]',
    'koi_period_err1': 'Orbital Period Upper Unc. [days]',
    'koi_period_err2': 'Orbital Period Lower Unc. [days]',
    'koi_time0bk': 'Transit Epoch [BKJD]',
    'koi_time0bk_err1': 'Transit Epoch Upper Unc. [BKJD]',
    'koi_time0bk_err2': 'Transit Epoch Lower Unc. [BKJD]',
    'koi_time0': 'Transit Epoch [BJD]',
    'koi_time0_err1': 'Transit Epoch Upper Unc. [BJD]',
    'koi_time0_err2': 'Transit Epoch Lower Unc. [BJD]',
    'koi_eccen': 'Eccentricity',
    'koi_eccen_err1': 'Eccentricity Upper Unc.',
    'koi_eccen_err2': 'Eccentricity Lower Unc.',
    'koi_longp': 'Longitude of Periastron [deg]',
    'koi_longp_err1': 'Longitude of Periastron Upper Unc. [deg]',
    'koi_longp_err2': 'Longitude of Periastron Lower Unc. [deg]',

    # Transit Parameters
    'koi_impact': 'Impact Parameter',
    'koi_impact_err1': 'Impact Parameter Upper Unc.',
    'koi_impact_err2': 'Impact Parameter Lower Unc.',
    'koi_duration': 'Transit Duration [hrs]',
    'koi_duration_err1': 'Transit Duration Upper Unc. [hrs]',
    'koi_duration_err2': 'Transit Duration Lower Unc. [hrs]',
    'koi_ingress': 'Ingress Duration [hrs]',
    'koi_ingress_err1': 'Ingress Duration Upper Unc. [hrs]',
    'koi_ingress_err2': 'Ingress Duration Lower Unc. [hrs]',
    'koi_depth': 'Transit Depth [ppm]',
    'koi_depth_err1': 'Transit Depth Upper Unc. [ppm]',
    'koi_depth_err2': 'Transit Depth Lower Unc. [ppm]',
    'koi_ror': 'Planet-Star Radius Ratio',
    'koi_ror_err1': 'Planet-Star Radius Ratio Upper Unc.',
    'koi_ror_err2': 'Planet-Star Radius Ratio Lower Unc.',

    # Fitted Stellar Properties
    'koi_srho': 'Fitted Stellar Density [g/cm**3]',
    'koi_srho_err1': 'Fitted Stellar Density Upper Unc. [g/cm**3]',
    'koi_srho_err2': 'Fitted Stellar Density Lower Unc. [g/cm**3]',
    'koi_fittype': 'Planetary Fit Type',

    # Planet Characteristics
    'koi_prad': 'Planetary Radius [Earth radii]',
    'koi_prad_err1': 'Planetary Radius Upper Unc. [Earth radii]',
    'koi_prad_err2': 'Planetary Radius Lower Unc. [Earth radii]',
    'koi_sma': 'Orbit Semi-Major Axis [au]',
    'koi_sma_err1': 'Orbit Semi-Major Axis Upper Unc. [au]',
    'koi_sma_err2': 'Orbit Semi-Major Axis Lower Unc. [au]',
    'koi_incl': 'Inclination [deg]',
    'koi_incl_err1': 'Inclination Upper Unc. [deg]',
    'koi_incl_err2': 'Inclination Lower Unc. [deg]',
    'koi_teq': 'Equilibrium Temperature [K]',
    'koi_teq_err1': 'Equilibrium Temperature Upper Unc. [K]',
    'koi_teq_err2': 'Equilibrium Temperature Lower Unc. [K]',
    'koi_insol': 'Insolation Flux [Earth flux]',
    'koi_insol_err1': 'Insolation Flux Upper Unc. [Earth flux]',
    'koi_insol_err2': 'Insolation Flux Lower Unc. [Earth flux]',
    'koi_dor': 'Planet-Star Distance over Star Radius',
    'koi_dor_err1': 'Planet-Star Distance over Star Radius Upper Unc.',
    'koi_dor_err2': 'Planet-Star Distance over Star Radius Lower Unc.',

    # Limb Darkening Model
    'koi_limbdark_mod': 'Limb Darkening Model',
    'koi_ldm_coeff4': 'Limb Darkening Coeff. 4',
    'koi_ldm_coeff3': 'Limb Darkening Coeff. 3',
    'koi_ldm_coeff2': 'Limb Darkening Coeff. 2',
    'koi_ldm_coeff1': 'Limb Darkening Coeff. 1',
    'koi_parm_prov': 'Parameters Provenance',

    # Detection Statistics
    'koi_max_sngle_ev': 'Maximum Single Event Statistic',
    'koi_max_mult_ev': 'Maximum Multiple Event Statistic',
    'koi_model_snr': 'Transit Signal-to-Noise',
    'koi_count': 'Number of Planets',
    'koi_num_transits': 'Number of Transits',
    'koi_tce_plnt_num': 'TCE Planet Number',
    'koi_tce_delivname': 'TCE Delivery',
    'koi_quarters': 'Quarters',
    'koi_bin_oedp_sig': 'Odd-Even Depth Comparison Statistic',
    'koi_trans_mod': 'Transit Model',
    'koi_model_dof': 'Degrees of Freedom',
    'koi_model_chisq': 'Chi-Square',

    # Data Links
    'koi_datalink_dvr': 'Link to DV Report',
    'koi_datalink_dvs': 'Link to DV Summary',

    # Stellar Properties
    'koi_steff': 'Stellar Effective Temperature [K]',
    'koi_steff_err1': 'Stellar Effective Temperature Upper Unc. [K]',
    'koi_steff_err2': 'Stellar Effective Temperature Lower Unc. [K]',
    'koi_slogg': 'Stellar Surface Gravity [log10(cm/s**2)]',
    'koi_slogg_err1': 'Stellar Surface Gravity Upper Unc. [log10(cm/s**2)]',
    'koi_slogg_err2': 'Stellar Surface Gravity Lower Unc. [log10(cm/s**2)]',
    'koi_smet': 'Stellar Metallicity [dex]',
    'koi_smet_err1': 'Stellar Metallicity Upper Unc. [dex]',
    'koi_smet_err2': 'Stellar Metallicity Lower Unc. [dex]',
    'koi_srad': 'Stellar Radius [Solar radii]',
    'koi_srad_err1': 'Stellar Radius Upper Unc. [Solar radii]',
    'koi_srad_err2': 'Stellar Radius Lower Unc. [Solar radii]',
    'koi_smass': 'Stellar Mass [Solar mass]',
    'koi_smass_err1': 'Stellar Mass Upper Unc. [Solar mass]',
    'koi_smass_err2': 'Stellar Mass Lower Unc. [Solar mass]',
    'koi_sage': 'Stellar Age [Gyr]',
    'koi_sage_err1': 'Stellar Age Upper Unc. [Gyr]',
    'koi_sage_err2': 'Stellar Age Lower Unc. [Gyr]',
    'koi_sparprov': 'Stellar Parameter Provenance',

    # Coordinates and Position
    'ra': 'RA [decimal degrees]',
    'dec': 'Dec [decimal degrees]',

    # Magnitudes
    'koi_kepmag': 'Kepler-band [mag]',
    'koi_gmag': "g'-band [mag]",
    'koi_rmag': "r'-band [mag]",
    'koi_imag': "i'-band [mag]",
    'koi_zmag': "z'-band [mag]",
    'koi_jmag': 'J-band [mag]',
    'koi_hmag': 'H-band [mag]',
    'koi_kmag': 'K-band [mag]',

    # Flux Weighted Centroid Analysis
    'koi_fwm_stat_sig': 'FW Offset Significance [percent]',
    'koi_fwm_sra': 'FW Source α(OOT) [hrs]',
    'koi_fwm_sra_err': 'FW Source α(OOT) Unc. [hrs]',
    'koi_fwm_sdec': 'FW Source δ(OOT) [deg]',
    'koi_fwm_sdec_err': 'FW Source δ(OOT) Unc. [deg]',
    'koi_fwm_srao': 'FW Source Δα(OOT) [sec]',
    'koi_fwm_srao_err': 'FW Source Δα(OOT) Unc. [sec]',
    'koi_fwm_sdeco': 'FW Source Δδ(OOT) [arcsec]',
    'koi_fwm_sdeco_err': 'FW Source Δδ(OOT) Unc. [arcsec]',
    'koi_fwm_prao': 'FW Δα(OOT) [sec]',
    'koi_fwm_prao_err': 'FW Δα(OOT) Unc. [sec]',
    'koi_fwm_pdeco': 'FW Δδ(OOT) [arcsec]',
    'koi_fwm_pdeco_err': 'FW Δδ(OOT) Unc. [arcsec]',

    # PRF (Pixel Response Function) Analysis
    'koi_dicco_mra': 'PRF Δα_SQ(OOT) [arcsec]',
    'koi_dicco_mra_err': 'PRF Δα_SQ(OOT) Unc. [arcsec]',
    'koi_dicco_mdec': 'PRF Δδ_SQ(OOT) [arcsec]',
    'koi_dicco_mdec_err': 'PRF Δδ_SQ(OOT) Unc. [arcsec]',
    'koi_dicco_msky': 'PRF Δθ_SQ(OOT) [arcsec]',
    'koi_dicco_msky_err': 'PRF Δθ_SQ(OOT) Unc. [arcsec]',
    'koi_dikco_mra': 'PRF Δα_SQ(KIC) [arcsec]',
    'koi_dikco_mra_err': 'PRF Δα_SQ(KIC) Unc. [arcsec]',
    'koi_dikco_mdec': 'PRF Δδ_SQ(KIC) [arcsec]',
    'koi_dikco_mdec_err': 'PRF Δδ_SQ(KIC) Unc. [arcsec]',
    'koi_dikco_msky': 'PRF Δθ_SQ(KIC) [arcsec]',
    'koi_dikco_msky_err': 'PRF Δθ_SQ(KIC) Unc. [arcsec]',
}

uploaded_df = uploaded_df.rename(columns=mapeamento_koi).drop('Row ID', axis=1)

columns_to_keep = [
    'Orbital Period [days]',
    'Planet-Star Radius Ratio',
    'Planetary Radius [Earth radii]',
    'Orbit Semi-Major Axis [au]',
    'Inclination [deg]',
    'Equilibrium Temperature [K]',
    'Insolation Flux [Earth flux]',
    'Stellar Effective Temperature [K]',
    'Stellar Surface Gravity [log10(cm/s**2)]',
    'Stellar Metallicity [dex]',
    'Stellar Radius [Solar radii]',
    'Stellar Mass [Solar mass]',
    'Eccentricity',
    'Transit Depth [ppm]',
    'Transit Duration [hrs]',
    'Transit Signal-to-Noise',
    'Number of Transits',
    'Not Transit-Like False Positive Flag',
    'Stellar Eclipse False Positive Flag',
    'Centroid Offset False Positive Flag',
    'Ephemeris Match Indicates Contamination False Positive Flag'
]

uploaded_df = uploaded_df[columns_to_keep]


st.title("Main Content Area")
if uploaded_df is not None:
    st.write("Preview of uploaded data:")


# --- Statistical Summary ---
st.subheader("Statistical Summary of the Data")

# Show descriptive statistics
st.write("Main statistics of the numerical variables:")
st.dataframe(uploaded_df.describe().T, width=1000)

# --- Quick Visualizations ---
st.subheader("Quick Visualizations")

# Distribution of orbital periods
fig, ax = plt.subplots()
sns.histplot(uploaded_df["Orbital Period [days]"], bins=50, kde=True, ax=ax)
ax.set_title("Distribution of Orbital Periods (days)")
st.pyplot(fig)

# Planet radius vs Equilibrium temperature
fig, ax = plt.subplots()
sns.scatterplot(
    data=uploaded_df,
    x="Planetary Radius [Earth radii]",
    y="Equilibrium Temperature [K]",
    hue="Stellar Effective Temperature [K]",
    palette="viridis",
    alpha=0.7,
    ax=ax
)
ax.set_title("Planetary Radius vs Equilibrium Temperature")
st.pyplot(fig)

# Correlation between main variables
st.subheader("Correlation Between Variables")
fig, ax = plt.subplots(figsize=(10,6))
corr = uploaded_df.corr(numeric_only=True)
sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, ax=ax)
st.pyplot(fig)

# --- False Positive Flags ---
st.subheader("False Positive Indicators")

flags = [
    "Not Transit-Like False Positive Flag",
    "Stellar Eclipse False Positive Flag",
    "Centroid Offset False Positive Flag",
    "Ephemeris Match Indicates Contamination False Positive Flag"
]

false_positive_summary = uploaded_df[flags].sum().reset_index()
false_positive_summary.columns = ["Flag", "Number of Cases"]

st.bar_chart(false_positive_summary.set_index("Flag"))

