from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import os
import datetime
import re
from kivy.utils import platform

# ======================== 全局配置 ========================
VIDEO_DIR = "ShopVideos"
qr_data = ""
is_processing = False

try:
    os.makedirs(VIDEO_DIR, exist_ok=True)
except:
    pass

# ======================== 权限管理 ========================
class PermissionManager:
    granted = False

    @staticmethod
    def request_and_check():
        if platform != "android":
            PermissionManager.granted = True
            return True

        try:
            from android.permissions import request_permissions, Permission, check_permission
            perms = [
                Permission.CAMERA,
                Permission.RECORD_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ]
            request_permissions(perms)

            cam = check_permission(Permission.CAMERA)
            mic = check_permission(Permission.RECORD_AUDIO)
            sto = check_permission(Permission.WRITE_EXTERNAL_STORAGE)

            PermissionManager.granted = cam and mic and sto
            return PermissionManager.granted
        except:
            PermissionManager.granted = False
            return False

    @staticmethod
    def open_settings():
        if platform != "android":
            return
        try:
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            intent = Intent()
            intent.setAction("android.settings.APPLICATION_DETAILS_SETTINGS")
            intent.setData(Uri.fromParts("package", activity.getPackageName(), None))
            activity.startActivity(intent)
        except:
            pass

# ======================== 弹窗提示 ========================
class Dialog:
    current = None

    @staticmethod
    def show(title, msg):
        try:
            if Dialog.current:
                Dialog.current.dismiss()

            box = BoxLayout(orientation='vertical', padding=20, spacing=15)
            box.add_widget(Label(text=msg, font_size=18, halign='center'))
            btn = Button(text="我知道了", size_hint=(1, 0.25),
                         background_normal="", background_color=(0.2,0.6,0.86,1), color=(1,1,1,1))
            box.add_widget(btn)

            popup = Popup(title=title, content=box, size_hint=(0.85, 0.4), auto_dismiss=False)
            btn.bind(on_press=popup.dismiss)
            Dialog.current = popup
            popup.open()
        except:
            pass

    @staticmethod
    def show_permission():
        try:
            if Dialog.current:
                Dialog.current.dismiss()

            box = BoxLayout(orientation='vertical', padding=20, spacing=12)
            box.add_widget(Label(
                text="使用前必须开启三项权限：\n• 相机权限（扫码+拍摄）\n• 麦克风（视频录音）\n• 存储（保存视频）",
                font_size=16, halign='center'))

            btn_layout = BoxLayout(size_hint=(1, 0.25), spacing=10)
            btn_set = Button(text="去设置开启", background_normal="",
                             background_color=(0.2,0.6,0.86,1), color=(1,1,1,1))
            btn_cancel = Button(text="取消", background_normal="",
                                background_color=(0.5,0.5,0.5,1), color=(1,1,1,1))
            btn_layout.add_widget(btn_set)
            btn_layout.add_widget(btn_cancel)
            box.add_widget(btn_layout)

            popup = Popup(title="权限不足", content=box, size_hint=(0.9, 0.45), auto_dismiss=False)
            Dialog.current = popup

            btn_set.bind(on_press=lambda x: [PermissionManager.open_settings(), popup.dismiss()])
            btn_cancel.bind(on_press=popup.dismiss)
            popup.open()
        except:
            pass

# ======================== 文件工具 ========================
class FileUtil:
    @staticmethod
    def clean(name):
        try:
            name = re.sub(r'[\\/*?:"<>|]', "_", name)
            return name.strip() or "unknown"
        except:
            return "unknown"

    @staticmethod
    def new_path(qr):
        clean = FileUtil.clean(qr)
        time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.abspath(os.path.join(VIDEO_DIR, f"{clean}_{time_str}.mp4"))

# ======================== 界面 ========================
KV = '''
ScreenManager:
    MainScreen:
    ScanScreen:
    VideoListScreen:

<MainScreen>:
    name: "main"
    canvas:
        color: 1,1,1,1
        rect: pos: self.pos, size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20

        Label:
            text: "网店视频拍摄工具\\n扫码 → 拍摄 → 自动命名保存"
            font_size: 20
            halign: "center"
            size_hint_y: None
            height: 80
            color: 0.2,0.2,0.2,1

        Widget:
            size_hint_y: 0.4

        Button:
            text: "[b]扫码拍摄[/b]"
            markup: True
            font_size: 28
            size_hint_y: None
            height: 100
            background_normal: ""
            background_color: 0.2, 0.6, 0.86, 1
            color: 1,1,1,1
            on_press: app.start_scan()

        Button:
            text: "[b]查看已拍视频[/b]"
            markup: True
            font_size: 28
            size_hint_y: None
            height: 100
            background_normal: ""
            background_color: 0.2, 0.6, 0.86, 1
            color: 1,1,1,1
            on_press: app.open_video_list()

<ScanScreen>:
    name: "scan"
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "请将二维码对准扫描框"
            font_size: 24
            size_hint_y: None
            height: 70
            color: 0.1,0.1,0.1,1

        Label:
            text: "保持平稳，光线充足"
            font_size: 16
            size_hint_y: None
            height: 30
            color: 0.5,0.5,0.5,1

        ZBarCam:
            id: zbarcam
            on_code: app.on_qr_scanned(self.data)

        Button:
            text: "返回"
            font_size: 24
            size_hint_y: None
            height: 70
            background_normal: ""
            background_color: 0.4,0.4,0.4,1
            color: 1,1,1,1
            on_press: app.goto_main()

<VideoListScreen>:
    name: "list"
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "已拍摄视频列表"
            font_size: 22
            size_hint_y: None
            height: 60
            color: 0.2,0.2,0.2,1

        ScrollView:
            GridLayout:
                id: list_area
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 8

        Button:
            text: "返回主页"
            font_size: 24
            size_hint_y: None
            height: 70
            background_normal: ""
            background_color: 0.4,0.4,0.4,1
            color: 1,1,1,1
            on_press: app.goto_main()
'''

# ======================== 页面 ========================
class MainScreen(Screen): pass
class ScanScreen(Screen): pass
class VideoListScreen(Screen): pass

# ======================== 主程序 ========================
class ShopVideoApp(App):
    def build(self):
        self.sm = Builder.load_string(KV)
        PermissionManager.request_and_check()
        return self.sm

    def goto_main(self):
        try: self.sm.current = "main"
        except: pass

    def goto_scan(self):
        try: self.sm.current = "scan"
        except: pass

    def goto_list(self):
        try: self.sm.current = "list"
        except: pass

    def start_scan(self):
        global is_processing
        try:
            if is_processing: return
            is_processing = True

            if not PermissionManager.request_and_check():
                Dialog.show_permission()
                is_processing = False
                return

            self.goto_scan()
            is_processing = False
        except:
            is_processing = False
            Dialog.show("失败", "无法打开扫码界面")

    def on_qr_scanned(self, data):
        global qr_data, is_processing
        try:
            if is_processing: return
            is_processing = True

            if not data or not data.strip():
                Dialog.show("提示", "未识别到有效二维码，请重试")
                is_processing = False
                return

            qr_data = data.strip()
            Dialog.show("成功", f"已识别：{qr_data[:20]}\n即将打开相机拍摄")
            self.start_record_video()
            self.goto_main()
            is_processing = False
        except:
            is_processing = False
            Dialog.show("错误", "扫码处理失败")

    def start_record_video(self):
        try:
            if not PermissionManager.request_and_check():
                Dialog.show_permission()
                return

            FileUtil.new_path(qr_data)

            if platform == "android":
                from jnius import autoclass
                Intent = autoclass("android.content.Intent")
                MediaStore = autoclass("android.provider.MediaStore")
                activity = autoclass("org.kivy.android.PythonActivity").mActivity
                intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
                activity.startActivity(intent)
        except:
            Dialog.show("错误", "无法启动相机，请检查权限")

    def open_video_list(self):
        try:
            self.goto_list()
            self.load_videos()
        except:
            Dialog.show("错误", "无法打开视频列表")

    def load_videos(self):
        try:
            layout = self.sm.get_screen("list").ids.list_area
            layout.clear_widgets()

            if not os.path.exists(VIDEO_DIR):
                return

            files = []
            for f in os.listdir(VIDEO_DIR):
                try:
                    if f.lower().endswith(".mp4"):
                        files.append(f)
                except:
                    continue

            if not files:
                layout.add_widget(Label(
                    text="暂无视频\n请点击「扫码拍摄」",
                    font_size=18, color=0.5,0.5,0.5,1, size_hint_y=None, height=100))
                return

            files.sort(key=lambda x: os.path.getmtime(os.path.join(VIDEO_DIR, x)), reverse=True)

            for name in files:
                btn = Button(
                    text=name, font_size=20, size_hint_y=None, height=65,
                    background_normal="", background_color=(0.95,0.95,0.95,1), color=(0,0,0,1)
                )
                btn.bind(on_press=lambda _, n=name: self.play_video(n))
                layout.add_widget(btn)
        except:
            pass

    def play_video(self, name):
        try:
            path = os.path.join(VIDEO_DIR, name)
            if not os.path.exists(path):
                Dialog.show("提示", "视频文件不存在或已删除")
                return

            if platform == "android":
                from jnius import autoclass
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                uri = Uri.parse("file://" + path)
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "video/mp4")
                activity.startActivity(intent)
        except:
            Dialog.show("失败", "无法播放此视频")

if __name__ == "__main__":
    ShopVideoApp().run()