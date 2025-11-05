import vlc
import time
import serial
import ArduinoReader
import HacerFoto as ph
import HacerVideo as vd
import threading as th
# --- CONFIGURACIÓN ---
VIDEO_PATH = "carreteraLoop.mp4"
PORT = "COM5"
MIN_SPEED = 0.0
MAX_SPEED = 15.0

def map_range(x, in_min, in_max, out_min, out_max):
    """Mapea un valor desde un rango a otro."""
    return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)

def main():
    instance = vlc.Instance()
    # player = instance.media_player_new()
    # media = instance.media_new(VIDEO_PATH)
    # player.set_media(media)
    media = instance.media_new(VIDEO_PATH)

    media_list = instance.media_list_new()
    media_list.add_media(media)
    
    media_player = instance.media_player_new()
    list_player = instance.media_list_player_new()

    list_player.set_media_player(media_player)
    list_player.set_media_list(media_list)

    list_player.set_playback_mode(vlc.PlaybackMode.loop)
    list_player.play()
    
    # Espera a que comience la reproducción
    time.sleep(2)
    while list_player.get_state() != vlc.State.Playing:
        time.sleep(0.1)

    # arduino = ArduinoReader(PORT)
    valor = ArduinoReader.leer_arduino()
    ultima_velocidad = map_range(valor, 1, 100, MIN_SPEED, MAX_SPEED)

    print("🎥 Control de velocidad con potenciómetro (Ctrl+C para salir)")
    
    try:
        while True:
            valor = ArduinoReader.leer_arduino()
            if valor is not None:
                velocidad = map_range(valor, 1, 100, MIN_SPEED, MAX_SPEED)
                if (abs(velocidad - ultima_velocidad) > 0.05): #Solo cambia la velocidad del video
                    media_player.set_rate(velocidad)
                    print(f"🔧 Velocidad actual: {velocidad:.2f}x")
            # time.sleep(0.1)

            if ((velocidad <= 0) and ( velocidad != ultima_velocidad)): # Si la velocidad es 0 y venia de estar en marcha se pausa
                media_player.pause()
                foto = ph.hacer_foto(0)
                print("foto: ", foto)
            else:
                if ( velocidad != ultima_velocidad): #Si cambio pero la vel no es 0 lo pongo en marcha
                    media_player.play()
                    if (ultima_velocidad <= 0): #solo quiero grabar si venia de estar en reposo
                        #th.Thread(target=vd.hacer_video, args=(0), daemon=True).start()
                        video = vd.hacer_video(0)
                        print("video: ", video)


            ultima_velocidad = velocidad
            # state = player.get_state()
            # if state == vlc.State.Ended:
            #     player.set_media(media)
            #     player.play()

    except KeyboardInterrupt:
        print("\n🛑 Reproducción detenida por el usuario.")
    except serial.SerialException:
        print("\n⚠️ Error de conexión con Arduino.")
    finally:
        list_player.stop()

if __name__ == "__main__":
    main()