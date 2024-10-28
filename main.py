import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from datetime import datetime
from googletrans import Translator
import os
import time

class AsistenteVirtual:
    def __init__(self, nombre="Asistente"):
        self.nombre = nombre
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        
    def escuchar(self):
        """Escucha el micrófono y retorna el texto reconocido"""
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            texto = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {texto}")
            return texto.lower()
        except sr.UnknownValueError:
            print("No he entendido lo que has dicho")
            return ""
        except sr.RequestError:
            print("Error en el servicio de reconocimiento de voz")
            return ""

    def hablar(self, texto):
        """Convierte texto a voz y lo reproduce"""
        try:
            tts = gTTS(text=texto, lang='es')
            archivo = "respuesta.mp3"
            tts.save(archivo)
            playsound(archivo)
            os.remove(archivo)
        except Exception as e:
            print(f"Error al generar voz: {str(e)}")

    def procesar_comando(self, comando):
        """Procesa el comando recibido y retorna una respuesta"""
        if not comando:
            return "No he podido entender el comando"

        # Comandos básicos
        if "hola" in comando:
            return f"¡Hola! Soy {self.nombre}, ¿en qué puedo ayudarte?"
        
        elif "hora" in comando:
            hora = datetime.now().strftime('%H:%M')
            return f"Son las {hora}"
        
        elif "fecha" in comando:
            fecha = datetime.now().strftime('%d de %B del %Y')
            return f"Hoy es {fecha}"
        
        elif "traduce" in comando:
            # Extraer el texto a traducir (asumiendo formato: "traduce [texto] al [idioma]")
            try:
                partes = comando.split("traduce ")[1].split(" al ")
                texto = partes[0]
                idioma_destino = partes[1]
                
                # Mapeo de idiomas comunes
                idiomas = {
                    "inglés": "en",
                    "francés": "fr",
                    "alemán": "de",
                    "italiano": "it"
                }
                
                codigo_idioma = idiomas.get(idioma_destino, "en")
                traduccion = self.translator.translate(texto, dest=codigo_idioma)
                return f"La traducción es: {traduccion.text}"
            except:
                return "No he podido realizar la traducción"
        
        elif "adiós" in comando or "hasta luego" in comando:
            return "¡Hasta luego! Que tengas un buen día"
        
        return "No he entendido el comando. ¿Puedes repetirlo?"

    def ejecutar(self):
        """Inicia el asistente virtual"""
        self.hablar(f"¡Hola! Soy {self.nombre}, tu asistente virtual. ¿En qué puedo ayudarte?")
        
        while True:
            comando = self.escuchar()
            
            if "terminar" in comando or "apagar" in comando:
                self.hablar("Apagando asistente virtual. ¡Hasta pronto!")
                break
                
            respuesta = self.procesar_comando(comando)
            self.hablar(respuesta)

# Ejemplo de uso
if __name__ == "__main__":
    asistente = AsistenteVirtual("Luna")
    asistente.ejecutar()



