import streamlit as st
import pandas as pd
from database import init_database, save_record, find_record, get_all_records

# Initialize database
init_database()

# Page configuration
st.set_page_config(
    page_title="Vicepresidencia Empresas Cotizador de Transportes Allianz",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for white background with dark blue and black accents
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .main-header-line1 {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-bottom: 0;
        font-weight: bold;
    }
    .main-header-line2 {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        margin-top: 0;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #000000;
        margin-bottom: 1rem;
        font-weight: bold;
        border-bottom: 2px solid #003366;
        padding-bottom: 0.5rem;
    }
    .field-label {
        color: #000000;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stApp {
        background-color: white;
    }
    .stButton button {
        background-color: #003366;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #002244;
        color: white;
    }
    /* Make all text black */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
        color: #000000 !important;
        font-weight: bold;
    }
    /* Make expander text black */
    .streamlit-expander p {
        color: #000000 !important;
        font-weight: bold;
    }
    .streamlit-expander {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main header with two lines
st.markdown('<div class="main-header-line1">Vicepresidencia Empresas</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header-line2">Cotizador de Transportes Allianz</div>', unsafe_allow_html=True)

# Initialize session state for form fields
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'nombre_cliente': '',
        'id_cliente': '',
        'ano': '',
        'comision_seguro': '',
        'reaseguro_proporcional': '',
        'comision_reaseguro': ''
    }

# Create two main columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">Campos de Cotización</div>', unsafe_allow_html=True)
    
    # Pricing fields with labels to the left
    col1_1, col1_2 = st.columns([1, 2])
    with col1_1:
        st.markdown('<div class="field-label">Nombre Cliente *</div>', unsafe_allow_html=True)
    with col1_2:
        nombre_cliente = st.text_input(
            "Nombre Cliente", 
            value=st.session_state.form_data['nombre_cliente'],
            placeholder="Ingrese el nombre del cliente",
            label_visibility="collapsed"
        )
    
    col2_1, col2_2 = st.columns([1, 2])
    with col2_1:
        st.markdown('<div class="field-label">ID Cliente *</div>', unsafe_allow_html=True)
    with col2_2:
        id_cliente = st.text_input(
            "ID Cliente", 
            value=st.session_state.form_data['id_cliente'],
            placeholder="Ingrese el ID del cliente",
            label_visibility="collapsed"
        )
    
    col2_3, col2_4 = st.columns([1, 2])
    with col2_3:
        st.markdown('<div class="field-label">Año *</div>', unsafe_allow_html=True)
    with col2_4:
        ano = st.text_input(
            "Año", 
            value=st.session_state.form_data['ano'],
            placeholder="Ej: 2024",
            label_visibility="collapsed"
        )
    
    col3_1, col3_2 = st.columns([1, 2])
    with col3_1:
        st.markdown('<div class="field-label">% Comisión Seguro *</div>', unsafe_allow_html=True)
    with col3_2:
        comision_seguro = st.text_input(
            "% Comisión Seguro", 
            value=st.session_state.form_data['comision_seguro'],
            placeholder="Ej: 15.5",
            label_visibility="collapsed"
        )
    
    col4_1, col4_2 = st.columns([1, 2])
    with col4_1:
        st.markdown('<div class="field-label">% Reaseguro Proporcional *</div>', unsafe_allow_html=True)
    with col4_2:
        reaseguro_proporcional = st.text_input(
            "% Reaseguro Proporcional", 
            value=st.session_state.form_data['reaseguro_proporcional'],
            placeholder="Ej: 25.0",
            label_visibility="collapsed"
        )
    
    col5_1, col5_2 = st.columns([1, 2])
    with col5_1:
        st.markdown('<div class="field-label">% Comisión Reaseguro Proporcional *</div>', unsafe_allow_html=True)
    with col5_2:
        comision_reaseguro = st.text_input(
            "% Comisión Reaseguro Proporcional", 
            value=st.session_state.form_data['comision_reaseguro'],
            placeholder="Ej: 10.0",
            label_visibility="collapsed"
        )
    
    # Buttons
    st.markdown("---")
    col1_1, col1_2, col1_3 = st.columns(3)
    
    with col1_1:
        guardar_registro = st.button("Guardar Registro", use_container_width=True)
    
    with col1_2:
        buscar_registro = st.button("Buscar Registro", use_container_width=True)
    
    with col1_3:
        limpiar_celdas = st.button("Limpiar Celdas", use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Búsqueda de Registros</div>', unsafe_allow_html=True)
    
    # Search fields with labels to the left
    col6_1, col6_2 = st.columns([1, 2])
    with col6_1:
        st.markdown('<div class="field-label">ID</div>', unsafe_allow_html=True)
    with col6_2:
        search_id = st.text_input(
            "ID", 
            placeholder="Buscar por ID",
            key="search_id",
            label_visibility="collapsed"
        )
    
    col7_1, col7_2 = st.columns([1, 2])
    with col7_1:
        st.markdown('<div class="field-label">Nombre Completo</div>', unsafe_allow_html=True)
    with col7_2:
        search_nombre = st.text_input(
            "Nombre Completo", 
            placeholder="Buscar por nombre completo",
            key="search_nombre",
            label_visibility="collapsed"
        )
    
    col8_1, col8_2 = st.columns([1, 2])
    with col8_1:
        st.markdown('<div class="field-label">NIT/CC</div>', unsafe_allow_html=True)
    with col8_2:
        search_nit_cc = st.text_input(
            "NIT/CC", 
            placeholder="Buscar por NIT/CC",
            key="search_nit_cc",
            label_visibility="collapsed"
        )
    
    col9_1, col9_2 = st.columns([1, 2])
    with col9_1:
        st.markdown('<div class="field-label">Año</div>', unsafe_allow_html=True)
    with col9_2:
        search_ano = st.text_input(
            "Año", 
            placeholder="Buscar por año",
            key="search_ano",
            label_visibility="collapsed"
        )
    
    # Search button
    buscar_bd = st.button("🔎 Buscar en Base de Datos", use_container_width=True)

# Handle button actions
if guardar_registro:
    # Validate required fields
    if not all([nombre_cliente, id_cliente, ano, comision_seguro, reaseguro_proporcional, comision_reaseguro]):
        st.markdown('<div class="error-message">Por favor complete todos los campos obligatorios (*)</div>', unsafe_allow_html=True)
    else:
        try:
            # Prepare record data
            record_data = {
                'nombre_cliente': nombre_cliente,
                'id_cliente': id_cliente,
                'ano': int(ano),
                'comision_seguro': float(comision_seguro),
                'reaseguro_proporcional': float(reaseguro_proporcional),
                'comision_reaseguro': float(comision_reaseguro),
                'nit_cc': search_nit_cc  # Save the NIT/CC if provided
            }
            
            # Save to database
            record_id, estimated_price = save_record(record_data)
            
            st.markdown(f'<div class="success-message">✅ Registro guardado exitosamente! ID: {record_id}</div>', unsafe_allow_html=True)
            
        except ValueError:
            st.markdown('<div class="error-message">Error: Los porcentajes y año deben ser valores numéricos válidos</div>', unsafe_allow_html=True)

if buscar_bd:
    if not any([search_id, search_nombre, search_nit_cc, search_ano]):
        st.markdown('<div class="error-message">Por favor ingrese al menos un criterio de búsqueda</div>', unsafe_allow_html=True)
    else:
        # In a real implementation, you would search by these criteria
        # For now, we'll search by ID if provided
        if search_id:
            record = find_record(search_id)
            if record:
                # Update session state with found record
                st.session_state.form_data = {
                    'nombre_cliente': record.get('nombre_cliente', ''),
                    'id_cliente': record.get('id_cliente', ''),
                    'ano': str(record.get('ano', '')),
                    'comision_seguro': str(record.get('comision_seguro', '')),
                    'reaseguro_proporcional': str(record.get('reaseguro_proporcional', '')),
                    'comision_reaseguro': str(record.get('comision_reaseguro', ''))
                }
                st.markdown(f'<div class="success-message">✅ Registro encontrado! Cliente: {record.get("nombre_cliente", "")}</div>', unsafe_allow_html=True)
                st.rerun()
            else:
                st.markdown('<div class="error-message">❌ No se encontró ningún registro con ese ID</div>', unsafe_allow_html=True)

if limpiar_celdas:
    # Clear all fields
    st.session_state.form_data = {
        'nombre_cliente': '',
        'id_cliente': '',
        'ano': '',
        'comision_seguro': '',
        'reaseguro_proporcional': '',
        'comision_reaseguro': ''
    }
    st.rerun()

# Display all records in an expandable section
with st.expander("📋 Ver Todos los Registros"):
    records_df = get_all_records()
    
    if not records_df.empty:
        # Format the dataframe for better display
        display_df = records_df.copy()
        display_df['comision_seguro'] = display_df['comision_seguro'].apply(lambda x: f"{x}%")
        display_df['reaseguro_proporcional'] = display_df['reaseguro_proporcional'].apply(lambda x: f"{x}%")
        display_df['comision_reaseguro'] = display_df['comision_reaseguro'].apply(lambda x: f"{x}%")
        display_df['created_date'] = pd.to_datetime(display_df['created_date']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Safe column selection - only use columns that exist
        available_columns = []
        desired_columns = ['id', 'nombre_cliente', 'id_cliente', 'ano', 'comision_seguro', 'reaseguro_proporcional', 'comision_reaseguro', 'created_date']
        
        for col in desired_columns:
            if col in display_df.columns:
                available_columns.append(col)
            else:
                st.warning(f"⚠️ Columna '{col}' no encontrada en la base de datos")
        
        st.dataframe(
            display_df[available_columns],
            use_container_width=True
        )
        
        # Export option
        csv = records_df.to_csv(index=False)
        st.download_button(
            label="📥 Exportar a CSV",
            data=csv,
            file_name="registros_cotizaciones.csv",
            mime="text/csv",
        )
    else:
        st.info("No hay registros en la base de datos. Guarde el primer registro para comenzar.")
