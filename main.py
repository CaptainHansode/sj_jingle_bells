import os
import random
import sys
import pygame


def get_base_dir() -> str:
    """PyInstaller (--onefile) と通常実行の両方に対応したベースディレクトリを返す"""
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def play_random_sound():
    """soundフォルダからsound01〜sound05.mp3をランダムで再生する。再生中なら前のサウンドをキャンセルする。"""
    sound_dir = os.path.join(get_base_dir(), "sound")
    sound_files = [f"sound{i:02d}.mp3" for i in range(1, 6)]
    chosen = random.choice(sound_files)
    sound_path = os.path.join(sound_dir, chosen)

    # 再生中なら停止してから新しいサウンドを再生
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

    print(f"再生中: {chosen}")


def main():
    pygame.mixer.init()
    print("Enterを押すとランダムにサウンドを再生します。Ctrl+C で終了。")
    try:
        while True:
            input(">>> Enterを押してください: ")
            play_random_sound()
    except KeyboardInterrupt:
        print("\n終了します。")
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    main()
