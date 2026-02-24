import os
import random
import sys
import pygame
from datetime import datetime


def get_base_dir() -> str:
    """PyInstaller (--onefile) と通常実行の両方に対応したベースディレクトリを返す"""
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_app_dir() -> str:
    """ログなど永続ファイルの保存先ディレクトリを返す（exe隣 or スクリプト隣）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def play_random_sound() -> str:
    """soundフォルダからsound01〜sound05.mp3をランダムで再生する。再生中なら前のサウンドをキャンセルする。再生したファイル名を返す。"""
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
    return chosen


def write_log(play_count: int, start_time: datetime, count_by_file: dict) -> None:
    """再生回数（合計・ファイル別）をログファイルに追記する"""
    log_path = os.path.join(get_app_dir(), "jingle_bells.log")
    end_time = datetime.now()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("--- セッション ---\n")
        f.write(f"開始時刻  : {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"終了時刻  : {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"再生回数  : {play_count} 回\n")
        f.write("[ ファイル別 ]\n")
        for name in sorted(count_by_file):
            f.write(f"  {name} : {count_by_file[name]} 回\n")
        f.write("\n")
    print(f"ログを保存しました: {log_path}")


def main():
    pygame.mixer.init()
    play_count = 0
    count_by_file: dict[str, int] = {}
    start_time = datetime.now()
    print("Enterを押すとランダムにサウンドを再生します。Ctrl+C で終了。")
    try:
        while True:
            input(">>> Enterを押してください: ")
            chosen = play_random_sound()
            play_count += 1
            count_by_file[chosen] = count_by_file.get(chosen, 0) + 1
    except KeyboardInterrupt:
        print("\n終了します。")
    finally:
        pygame.mixer.quit()
        write_log(play_count, start_time, count_by_file)


if __name__ == "__main__":
    main()
