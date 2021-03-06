from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

WaterThreshold = 60
LuminosityThreshold = 900
TempertureMinRelax = 15
TempertureMaxRelax = 30


class Plant:
    def __init__(self,
                display_name,
                name,
                sensor_buffer,
                speech_center,
                water_threshold=WaterThreshold,
                luminosity_threshold=LuminosityThreshold,
                temperture_min_relax=TempertureMinRelax,
                temperture_max_relax=TempertureMaxRelax,
                listen_bieacon=(None, 0),):
        self.display_name = display_name
        self.name = name
        self.__sensor_buf = sensor_buffer
        self.__speech_center = speech_center
        self.water_threshold = water_threshold
        self.luminosity_threshold = luminosity_threshold
        self.temperture_min_relax = temperture_min_relax
        self.temperture_max_relax = temperture_max_relax
        self.listen_bieacon = listen_bieacon

        executor = ThreadPoolExecutor(2)
        self.__listening_thread = executor.submit(self.__sensor_buf.start)

    # ここでlisten_boecon(ビーコンが反応してから diff 現時刻, 設定がOn)なら1時間スパンにする(4時間の間)
    def update(self):
        if 14400 < (datetime.now() - self.listen_bieacon[0]).strftime('%s') and self.listen_bieacon[1] is 1:
            self.__sensor_buf.fetch_span = 12000
        else:
            self.__sensor_buf.fetch_span = 600

    # Lineに出力すべきテキストを生成します
    def chat(self, text):
        return self.__speech_center.make_response(self, user_text=text)

    # 

    
