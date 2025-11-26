import streamlit as st
import pandas as pd
from database import init_database, save_record, find_record, get_all_records, find_record_by_nombre, find_record_by_id_cliente, update_record

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
    .warning-message {
        padding: 1rem;
        background-color: #fff3cd;
        color: #856404;
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
        'comision_seguro': '',
        'reaseguro_proporcional': '',
        'comision_reaseguro': ''
    }

# Initialize session state for current record ID
if 'current_record_id' not in st.session_state:
    st.session_state.current_record_id = None

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
        actualizar_registro = st.button("Actualizar Registro", use_container_width=True)
    
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
    
    # Search button
    buscar_bd = st.button("Buscar Registro", use_container_width=True)

# Handle button actions
if guardar_registro:
    # Validate required fields
    if not all([nombre_cliente, id_cliente, comision_seguro, reaseguro_proporcional, comision_reaseguro]):
        st.markdown('<div class="error-message">Por favor complete todos los campos obligatorios (*)</div>', unsafe_allow_html=True)
    else:
        try:
            # Prepare record data
            record_data = {
                'nombre_cliente': nombre_cliente,
                'id_cliente': id_cliente,
                'comision_seguro': float(comision_seguro),
                'reaseguro_proporcional': float(reaseguro_proporcional),
                'comision_reaseguro': float(comision_reaseguro),
                'nit_cc': search_nit_cc  # Save the NIT/CC if provided
            }
            
            # Save to database
            record_id, estimated_price = save_record(record_data)
            
            st.markdown(f'<div class="success-message">✅ Registro guardado exitosamente! ID: {record_id}</div>', unsafe_allow_html=True)
            
        except ValueError:
            st.markdown('<div class="error-message">Error: Los porcentajes deben ser valores numéricos válidos</div>', unsafe_allow_html=True)

if actualizar_registro:
    # Check if we have a current record to update
    if st.session_state.current_record_id is None:
        st.markdown('<div class="error-message">❌ No hay un registro cargado para actualizar. Primero busque un registro existente.</div>', unsafe_allow_html=True)
    else:
        # Validate required fields
        if not all([nombre_cliente, id_cliente, comision_seguro, reaseguro_proporcional, comision_reaseguro]):
            st.markdown('<div class="error-message">Por favor complete todos los campos obligatorios (*)</div>', unsafe_allow_html=True)
        else:
            try:
                # Prepare record data for update
                record_data = {
                    'nombre_cliente': nombre_cliente,
                    'id_cliente': id_cliente,
                    'comision_seguro': float(comision_seguro),
                    'reaseguro_proporcional': float(reaseguro_proporcional),
                    'comision_reaseguro': float(comision_reaseguro),
                    'nit_cc': search_nit_cc
                }
                
                # Update the record in database
                success = update_record(st.session_state.current_record_id, record_data)
                
                if success:
                    st.markdown(f'<div class="success-message">✅ Registro actualizado exitosamente! ID: {st.session_state.current_record_id}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Error al actualizar el registro</div>', unsafe_allow_html=True)
                
            except ValueError:
                st.markdown('<div class="error-message">Error: Los porcentajes deben ser valores numéricos válidos</div>', unsafe_allow_html=True)

if buscar_bd:
    if not any([search_id, search_nombre, search_nit_cc]):
        st.markdown('<div class="error-message">Por favor ingrese al menos un criterio de búsqueda</div>', unsafe_allow_html=True)
    else:
        record = None
        search_type = ""
        multiple_records = None
        
        # Search by ID (primary key)
        if search_id:
            record = find_record(search_id)
            search_type = f"ID: {search_id}"
        
        # Search by Nombre Completo (Nombre Cliente)
        elif search_nombre:
            records = find_record_by_nombre(search_nombre)
            if records:
                if len(records) == 1:
                    record = records[0]
                    search_type = f"Nombre: {search_nombre}"
                else:
                    multiple_records = records
                    st.markdown(f'<div class="success-message">✅ Se encontraron {len(records)} registros con el nombre "{search_nombre}"</div>', unsafe_allow_html=True)
                    # Show multiple records and let user choose
                    for i, rec in enumerate(records, 1):
                        st.write(f"{i}. ID: {rec['id']} - {rec['nombre_cliente']} - {rec['id_cliente']}")
        
        # Search by NIT/CC (ID Cliente)
        elif search_nit_cc:
            records = find_record_by_id_cliente(search_nit_cc)
            if records:
                if len(records) == 1:
                    record = records[0]
                    search_type = f"NIT/CC: {search_nit_cc}"
                else:
                    multiple_records = records
                    st.markdown(f'<div class="success-message">✅ Se encontraron {len(records)} registros con el NIT/CC "{search_nit_cc}"</div>', unsafe_allow_html=True)
                    # Show multiple records and let user choose
                    for i, rec in enumerate(records, 1):
                        st.write(f"{i}. ID: {rec['id']} - {rec['nombre_cliente']} - {rec['id_cliente']}")
        
        # If we have a single record to display
        if record and not multiple_records:
            # Update session state with found record
            st.session_state.form_data = {
                'nombre_cliente': record.get('nombre_cliente', ''),
                'id_cliente': record.get('id_cliente', ''),
                'comision_seguro': str(record.get('comision_seguro', '')),
                'reaseguro_proporcional': str(record.get('reaseguro_proporcional', '')),
                'comision_reaseguro': str(record.get('comision_reaseguro', ''))
            }
            # Store the current record ID for potential updates
            st.session_state.current_record_id = record.get('id')
            
            st.markdown(f'<div class="success-message">✅ Registro encontrado por {search_type}! Cliente: {record.get("nombre_cliente", "")}</div>', unsafe_allow_html=True)
            st.markdown('<div class="warning-message">⚠️ Ahora puede modificar los datos y hacer clic en "Actualizar Registro" para guardar los cambios.</div>', unsafe_allow_html=True)
            st.rerun()
        elif not record and not multiple_records:
            st.markdown('<div class="error-message">❌ No se encontró ningún registro con los criterios especificados</div>', unsafe_allow_html=True)

if limpiar_celdas:
    # Clear all fields
    st.session_state.form_data = {
        'nombre_cliente': '',
        'id_cliente': '',
        'comision_seguro': '',
        'reaseguro_proporcional': '',
        'comision_reaseguro': ''
    }
    # Clear current record ID
    st.session_state.current_record_id = None
    st.rerun()

# Display current record info if any
if st.session_state.current_record_id:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Registro Actual")
    st.sidebar.info(f"**ID:** {st.session_state.current_record_id}\n\n**Modo:** Edición")

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
        
        st.dataframe(
            display_df[['id', 'nombre_cliente', 'id_cliente', 'comision_seguro', 'reaseguro_proporcional', 'comision_reaseguro', 'created_date']],
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
        st.info("No hay registros en la base de datos.")

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.subheader("Información")
st.sidebar.info(
    "Sistema de cotización para transportes Allianz. "
    "Guarde registros, busque por diferentes criterios o consulte todos los registros existentes."
)

