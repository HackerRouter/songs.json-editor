import json
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.label_song_name = self.__tk_label_song_name(self)
        self.output_json = self.__tk_output_json(self)
        self.input_datapack_id = self.__tk_input_datapack_id(self)
        self.input_song = self.__tk_input_song(self)
        self.label_preview_datapack_id = self.__tk_label_preview_datapack_id(self)
        self.label_preview_json = self.__tk_label_preview_json(self)
        self.button_import_song = self.__tk_button_import_song(self)
        self.button_import_datapack = self.__tk_button_import_datapack(self)
        self.button_export_json = self.__tk_button_export_json(self)
        self.button_import_json = self.__tk_button_import_json(self)

        self.input_song.bind("<Return>", self.refresh_json_preview)
        self.input_datapack_id.bind("<Return>", self.refresh_json_preview)

    def __win(self):
        self.title("songs.json导入助手")
        width = 788
        height = 458
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.minsize(width=width, height=height)

    def __tk_label_song_name(self, parent):
        label = Label(parent, text="歌手 - 歌名（按回车触发预览）", anchor="w")
        label.place(relx=0.0266, rely=0.0218, relwidth=2, relheight=0.0655)
        return label

    def __tk_output_json(self, parent):
        ipt = Text(parent, wrap="word", height=5, width=20) 
        ipt.place(relx=0.6789, rely=0.0983, relwidth=0.2970, relheight=0.7358)
        ipt.config(padx=5, pady=5)
        return ipt

    def __tk_input_datapack_id(self, parent):
        ipt = Text(parent, wrap="word", height=5, width=20)
        ipt.place(relx=0.3528, rely=0.0983, relwidth=0.2970, relheight=0.7358)
        ipt.config(padx=5, pady=5)
        return ipt

    def __tk_input_song(self, parent):
        ipt = Text(parent, wrap="word", height=5, width=20)
        ipt.place(relx=0.0266, rely=0.0983, relwidth=0.2970, relheight=0.7358)
        ipt.config(padx=5, pady=5)
        return ipt

    def __tk_label_preview_datapack_id(self, parent):
        label = Label(parent, text="数据包ID预览", anchor="w")
        label.place(relx=0.3528, rely=0.0218, relwidth=0.1015, relheight=0.0655)
        return label

    def __tk_label_preview_json(self, parent):
        label = Label(parent, text="JSON文件预览", anchor="w")
        label.place(relx=0.6789, rely=0.0218, relwidth=0.1091, relheight=0.0655)
        return label

    def __tk_button_import_song(self, parent):
        btn = Button(parent, text="导入歌名-歌手文本文件", takefocus=False, command=self.import_song_file)
        btn.place(relx=0.0266, rely=0.8755, relwidth=0.2970, relheight=0.0721)
        return btn

    def __tk_button_import_datapack(self, parent):
        btn = Button(parent, text="导入数据包", takefocus=False, command=self.import_datapack_file)
        btn.place(relx=0.3528, rely=0.8755, relwidth=0.2970, relheight=0.0721)
        return btn

    def __tk_button_export_json(self, parent):
        btn = Button(parent, text="导出JSON文件", takefocus=False, command=self.export_json_file)
        #btn.place(relx=0.6789, rely=0.8755, relwidth=0.2970, relheight=0.0721)
        btn.place(relx=0.8452, rely=0.0172, relwidth=0.1294, relheight=0.0711)
        return btn
    
    def __tk_button_import_json(self, parent):
        btn = Button(parent, text="导入JSON文件", takefocus=False, command=self.import_json_file)
        #btn.place(relx=0.8452, rely=0.0172, relwidth=0.1294, relheight=0.0711)
        btn.place(relx=0.6789, rely=0.8755, relwidth=0.2970, relheight=0.0721)

        return btn










    def import_song_file(self):
        file_path = filedialog.askopenfilename(title="选择 歌名-歌手文本文件", filetypes=[("Text Files", "*.txt")])
        
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.input_song.insert(END, content)
                self.refresh_json_preview()

    def import_datapack_file(self):
        file_paths = filedialog.askopenfilenames(title="选择 数据包 文件", filetypes=[("Text Files", "*.zip")])
        
        if file_paths:
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                file_name_without_extension = os.path.splitext(file_name)[0]
                formatted_name = file_name_without_extension.replace(" ", "_")
                self.input_datapack_id.insert(END, formatted_name + "\n")
            self.refresh_json_preview()

    def parse_text(self, event=None):
        song_text = self.input_song.get(1.0, END).strip().split("\n")
        
        parsed_data = []
        
        datapack_text = self.input_datapack_id.get(1.0, END).strip().split("\n")
        
        for i, song_line in enumerate(song_text):
            song_parts = song_line.split("-")
            if len(song_parts) == 1:
                song_name = song_parts[0].strip()
                artist = ["anonymous"]
            else:
                song_name = song_parts[0].strip()
                artist = [artist.strip() for artist in song_parts[1].split(",")]

            # 获取对应的datapack名
            datapack_name = datapack_text[i] if i < len(datapack_text) else ""

            parsed_data.append({
                "name": song_name,
                "link": datapack_name,
                "artist": artist
            })
        
        return parsed_data
    


    def export_json_file(self):
        parsed_data = self.parse_text()
        
        if parsed_data:
            file_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="songs.json", filetypes=[("JSON Files", "*.json")])
            if file_path:
                with open(file_path, 'w', encoding="utf-8") as json_file:
                    json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)


    def export_json(self, parsed_data):
        if parsed_data:
            json_content = json.dumps(parsed_data, ensure_ascii=False, indent=4)
            self.output_json.delete(1.0, END)
            self.output_json.insert(END, json_content)

    # 刷新JSON预览
    def refresh_json_preview(self, event=None):
        parsed_data = self.parse_text()
        self.export_json(parsed_data)

    def import_json_file(self):
        file_path = filedialog.askopenfilename(title="选择 JSON 文件", filetypes=[("JSON Files", "*.json")])

        if file_path:
            with open(file_path, "r", encoding="utf-8") as json_file:
                parsed_data = json.load(json_file)

                self.input_song.delete(1.0, END)
                self.input_datapack_id.delete(1.0, END)
                self.output_json.delete(1.0, END)

                for entry in parsed_data:
                    song_name = entry["name"]
                    artist = ", ".join(entry["artist"])
                    self.input_song.insert(END, f"{song_name} - {artist}\n")

                    datapack_name = entry["link"]
                    self.input_datapack_id.insert(END, f"{datapack_name}\n")

                self.export_json(parsed_data)





class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()