import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
import os
try:
    from asistente_virtual import AsistenteVirtual
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from asistente_virtual import AsistenteVirtual

class TestAsistenteVirtual(unittest.TestCase):
    def setUp(self):
        self.asistente = AsistenteVirtual("Test Bot")
        # Capturar salida de consola
        self.output = StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = self.old_stdout
        if os.path.exists("respuesta.mp3"):
            os.remove("respuesta.mp3")

    def test_procesar_comandos_basicos(self):
        """Prueba los comandos básicos del asistente"""
        print("\nProbando comandos básicos...")
        
        # Test saludo
        respuesta = self.asistente.procesar_comando("hola")
        print(f"Comando 'hola' -> Respuesta: {respuesta}")
        self.assertIn("¡Hola!", respuesta)
        
        # Test hora
        respuesta = self.asistente.procesar_comando("que hora es")
        print(f"Comando 'que hora es' -> Respuesta: {respuesta}")
        self.assertIn("Son las", respuesta)
        
        # Test fecha
        respuesta = self.asistente.procesar_comando("que fecha es")
        print(f"Comando 'que fecha es' -> Respuesta: {respuesta}")
        self.assertIn("Hoy es", respuesta)

    @patch('gtts.gTTS')
    @patch('playsound.playsound')
    def test_funcion_hablar(self, mock_playsound, mock_gtts):
        """Prueba la función de hablar"""
        print("\nProbando función de hablar...")
        
        texto_prueba = "Esto es una prueba de voz"
        self.asistente.hablar(texto_prueba)
        
        mock_gtts.assert_called()
        mock_playsound.assert_called()
        print(f"Texto reproducido: '{texto_prueba}'")

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_funcion_escuchar(self, mock_micro, mock_recog):
        """Prueba la función de escuchar"""
        print("\nProbando función de escuchar...")
        
        # Simular reconocimiento de voz
        mock_recog.return_value.recognize_google.return_value = "hola asistente"
        
        resultado = self.asistente.escuchar()
        print(f"Texto reconocido: '{resultado}'")
        self.assertEqual(resultado, "hola asistente")

def ejecutar_demo():
    """Ejecuta una demo interactiva del asistente"""
    print("\n=== DEMO INTERACTIVA DEL ASISTENTE VIRTUAL ===")
    asistente = AsistenteVirtual("Demo Bot")
    
    comandos_demo = [
        "hola",
        "que hora es",
        "que fecha es",
        "quien eres",
        "traduce hola al inglés",
        "adiós"
    ]
    
    print("\nProcesando comandos de demostración:")
    for comando in comandos_demo:
        print("\n" + "-"*50)
        print(f"📝 Comando: '{comando}'")
        respuesta = asistente.procesar_comando(comando)
        print(f"🤖 Respuesta: '{respuesta}'")
        print(f"🔊 Simulando voz: '{respuesta}'")

if __name__ == '__main__':
    # Ejecutar tests
    print("=== INICIANDO TESTS UNITARIOS ===")
    unittest.main(argv=[''], exit=False)
    
    # Preguntar si se quiere ejecutar la demo
    print("\n¿Deseas ejecutar la demo interactiva? (s/n)")
    if input().lower() == 's':
        ejecutar_demo()