import streamlit as st
import os
import subprocess
from PIL import Image


def execute_r_script():
    """Executes the R script using subprocess."""
    try:
        result = subprocess.run(
            ["Rscript", "scr/analysis.r"], capture_output=True, text=True
        )
        if result.returncode == 0:
            st.success("Script R executado com sucesso!")
        else:
            st.error(f"Erro ao executar o script R: {result.stderr}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao executar o script R: {e}")


def display_images():
    """Displays images from the 'outputs' folder."""
    output_dir = "scr/outputs"
    if not os.path.exists(output_dir):
        st.warning(
            "A pasta 'outputs' ainda não foi criada. Execute o script R para gerar os gráficos."
        )
        return

    image_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]

    if not image_files:
        st.warning(
            "Nenhuma imagem foi encontrada na pasta 'scr/outputs'. Execute o script R para gerar os gráficos."
        )
        return

    for i, image_file in enumerate(image_files):
        st.image(
            os.path.join(output_dir, image_file),
            caption=image_file,
            use_container_width=True,
        )
        if i < len(image_files) - 1:  # Add separator except after the last image
            st.markdown("---")


def dashboard():
    """Main dashboard layout."""
    st.title("SCR")
    st.write(
        "Este dashboard exibe gráficos gerados pelo script R para análise de eficiência energética."
    )

    # Button to execute the R script
    if st.button("Executar Script R"):
        with st.spinner("Executando script R..."):
            execute_r_script()

    # Display generated charts
    st.subheader("Gráficos Gerados")
    display_images()
