#!/usr/bin/env python
# coding:utf-8
# env python 3.4.5

# from __future__ import division  # 少数点以下表示のためのモジュール
from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
import datetime as dt

# PC用の設定
Config.set('graphics', 'width', '800')  # 画面:横の大きさ
Config.set('graphics', 'height', '800')  # 画面:縦の大きさ
Config.set('graphics', 'show_cursor', '1')  # マウスカーソルの有無


# アプリデザイン（kvファイルでレイアウト指定）
class logtime(Widget):
    pass


# アプリの挙動
class MyApp(App):
    title = 'Log_Time'  # ウィンドウのタイトル

#################################################
# ボタン名（イベント名）：ここの名前を変えることでevent名が変化
#################################################
    bt1 = "event1"  # 左から1番目
    bt2 = "event2"  # 左から2番目
    bt3 = "event3"  # 左から3番目
#################################################

    data = []       # データ置き場
    file_check = 0  # 現在開いているファイルがあるかどうかをスイッチする変数

    def open_log(self):
        # ボタンを押した時間
        self.app_time = "{0:%y-%m-%d_%H-%M-%S}".format(dt.datetime.now())  # formatを使うと一行で済んで便利
        self.fp = open("Log/" + "Log_" + self.app_time + ".csv", "w")  # csvファイルを起動時刻で作成

        # ラベルの書き込み
        index = ["Event", "Time"]
        for i in index:
            self.fp.write("%s," % i)
        self.fp.write("\n")
        self.file_check = 1  # ファイルが開いた状態
        print("Open!")

        # メッセージの書き出し
        self.root.timel3.text = self.root.timel2.text
        self.root.timel2.text = self.root.timel1.text
        self.root.timel1.text = "Start Log : " + self.app_time + ".csv"

    def save_log(self):
        if self.file_check:
            # リストにあるデータを書き込み
            # print (self.data)
            for x in self.data:
                self.fp.write("%s, %s\n" % tuple(x))
            self.fp.flush()
            self.file_check = 0  # ファイルが閉じた状態
            print("Save!")

            self.data = []  # データのリセット

            # メッセージの書き出し
            self.root.timel3.text = self.root.timel2.text
            self.root.timel2.text = self.root.timel1.text
            self.root.timel1.text = "Save Log : " + self.app_time + ".csv"
        else:
            # セーブすべきファイルがないとき　
            # メッセージの書き出し
            self.root.timel3.text = self.root.timel2.text
            self.root.timel2.text = self.root.timel1.text
            self.root.timel1.text = "!! No save file !!"


    # ボタンを離した時の処理：文字色を元に戻す
    def bt_release(self, bt):
        if bt == 1:
            self.root.hit1.color = [0.2, 0.70588, 0.56470, 1]
        elif bt == 2:
            self.root.hit2.color = [0.2, 0.70588, 0.56470, 1]
        else:
            self.root.hit3.color = [0.2, 0.70588, 0.56470, 1]

    # ボタンを押した時の処理：ボタンの文字色と背景色を変更、押した時点での時刻を獲得
    def time_get(self, bt):
        if bt == 1:
            self.root.hit1.color = [0.8, 0.8, 0.8, 1]
            bt = self.bt1
        elif bt == 2:
            self.root.hit2.color = [0.8, 0.8, 0.8, 1]
            bt = self.bt2
        else:
            self.root.hit3.color = [0.8, 0.8, 0.8, 1]
            bt = self.bt3

        now = "{0:%y/%m/%d %H:%M:%S}".format(dt.datetime.now())  # ボタンを押した時の時刻を獲得
        self.data.append([bt] + [now])  # ラベル名と合わせてリストにぶちこむ
        # ログを残しておく作業 : 1つ上のログを１つ下に下げる（単なる書き換え）
        self.root.timel3.text = self.root.timel2.text
        self.root.timel2.text = self.root.timel1.text
        self.root.timel1.text = "*  " + bt + " | " + now

        print(self.root.timel1.text)  # PCでのデバック用


    # Kivyアプリの構築（必須）
    def build(self):
        return logtime()

    # 起動時に読み込まれる関数
    def on_start(self):
        pass

    # 終了時に読み込まれる関数
    def on_stop(self):
        # 終了時にセーブされていない場合、セーブする
        if self.file_check:
            # print (self.data)
            for x in self.data:
                self.fp.write("%s, %s\n" % tuple(x))
            self.fp.flush()
            print("Save!")
            self.file_check = 0

            self.data = []  # データのリセット
        else:
            pass

    # スマートフォンのポーズ機能をON（アプリを起動したまま画面を変えたりとか）
    def on_pause(self):
        return True

    # ポーズモードからの再開
    def on_resume(self):
        pass

if __name__ == '__main__':
    MyApp().run()
