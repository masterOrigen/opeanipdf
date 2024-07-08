import os
import streamlit as st
import PyPDF2
import openai
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API de OpenAI desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para extraer texto de un archivo PDF
def extraer_texto_pdf(archivo):
    pdf_reader = PyPDF2.PdfFileReader(archivo)
    texto = ''
    for page_num in range(pdf_reader.numPages):
        texto += pdf_reader.getPage(page_num).extract_text()
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
            # Llamar a OpenAI para obtener la respuesta
            respuesta = openai.Answer.create(
                model="text-davinci-003",
                question=pregunta,
                documents=[texto_pdf],
                max_tokens=50
            )

            st.subheader("Respuesta de OpenAI:")
            st.write(respuesta['answers'][0])

if __name__ == '__main__':
    main()

