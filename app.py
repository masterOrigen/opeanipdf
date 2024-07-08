import os
import streamlit as st
import io
import PyPDF2
import openai
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API de OpenAI desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para extraer texto de un archivo PDF
def extraer_texto_pdf(archivo):
    texto = ''
    with io.BytesIO(archivo.read()) as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto += page.extract_text()
    return texto

# Configurar la interfaz de usuario con Streamlit
def main():
    st.title('Consulta de PDF con OpenAI')

    # Subida de archivo PDF
    archivo_pdf = st.file_uploader("Subir archivo PDF", type=['pdf'])

    if archivo_pdf is not None:
        st.write("Archivo PDF cargado correctamente.")

        # Extraer texto del PDF
        texto_pdf = extraer_texto_pdf(archivo_pdf)

        # Mostrar el texto del PDF
        st.subheader("Texto del PDF")
        st.write(texto_pdf)

        # Área para hacer preguntas
        st.subheader("Realizar una consulta a OpenAI")
        pregunta = st.text_input("Escribe tu pregunta")

        if pregunta:
            try:
                # Llamar a OpenAI para obtener la respuesta
                respuesta = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=texto_pdf + "\n\nPregunta: " + pregunta + "\nRespuesta:",
                    max_tokens=50
                )

                st.subheader("Respuesta de OpenAI:")
                st.write(respuesta['choices'][0]['text'])

            except Exception as e:
                st.error(f"Error al procesar la consulta a OpenAI: {str(e)}")

if __name__ == '__main__':
    main()












