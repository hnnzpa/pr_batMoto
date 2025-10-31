import vlc
import time
import serial
import ArduinoReader

# --- CONFIGURACIÓN ---
VIDEO_PATH = "videosideconmoto.mp4"
PORT = "COM5"
MIN_SPEED = 1.0
MAX_SPEED = 15.0

def map_range(x, in_min, in_max, out_min, out_max):
    """Mapea un valor desde un rango a otro."""
    return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)

def main():
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(VIDEO_PATH)
    player.set_media(media)
    player.play()
    
    # Espera a que comience la reproducción
    time.sleep(2)
    while player.get_state() != vlc.State.Playing:
        time.sleep(0.1)

    # arduino = ArduinoReader(PORT)
    ultima_velocidad = None

    print("🎥 Control de velocidad con potenciómetro (Ctrl+C para salir)")

    try:
        while True:
            valor = ArduinoReader.leer_arduino()
            if valor is not None:
                velocidad = map_range(valor, 0, 100, MIN_SPEED, MAX_SPEED)
                if ultima_velocidad is None or abs(velocidad - ultima_velocidad) > 0.05:
                    player.set_rate(velocidad)
                    ultima_velocidad = velocidad
                    print(f"🔧 Velocidad actual: {velocidad:.2f}x")
            time.sleep(0.1)
            
            state = player.get_state()
            if state == vlc.State.Ended:
                # player.stop()
                player.set_media(media)
                player.play()

    except KeyboardInterrupt:
        print("\n🛑 Reproducción detenida por el usuario.")
    except serial.SerialException:
        print("\n⚠️ Error de conexión con Arduino.")
    finally:
        # arduino.cerrar()
        player.stop()

if __name__ == "__main__":
    main()
