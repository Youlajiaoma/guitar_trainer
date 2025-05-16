from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Line, Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty

import random

class GuitarFretboard(Widget):
    mode = StringProperty("自由模式")
    target_note = StringProperty("")
    natural_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    open_string_notes = [40, 45, 50, 55, 59, 64]  # E A D G B E
    fret_count = 13
    fret_spacing = NumericProperty(30)
    string_spacing = NumericProperty(20)
    left_margin = NumericProperty(15)
    top_margin = NumericProperty(20)
    
    string_sequence = ListProperty([])
    current_string_index = NumericProperty(0)
    
    markers = ListProperty([])  # list of dicts: {'string': int, 'fret': int, 'color': str, 'note': str}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_note = random.choice(self.natural_notes)
        self.string_sequence = []
        self.current_string_index = 0
        self.mode = "自由模式"
        self.markers = []
        Window.bind(on_resize=self.on_window_resize)
        self.bind(size=self.on_size)
        self.update_string_sequence()
    
    def on_window_resize(self, window, width, height):
        self.calculate_sizes()
        self.canvas.ask_update()

    def on_size(self, *args):
        self.calculate_sizes()
        self.canvas.ask_update()

    def calculate_sizes(self):
        width, height = self.size
        self.left_margin = max(15, width * 0.04)
        self.top_margin = max(20, height * 0.1)
        usable_width = width - 2 * self.left_margin
        usable_height = height - 2 * self.top_margin
        self.fret_spacing = usable_width / self.fret_count
        self.string_spacing = usable_height / 5

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        x, y = touch.pos
        string_clicked = int(round((y - self.top_margin) / self.string_spacing))
        fret = int((x - self.left_margin) // self.fret_spacing)
        if 0 <= string_clicked < 6 and 0 <= fret <= 12:
            string = 5 - string_clicked
            if self.mode == "自由模式":
                self.toggle_marker(string, fret)
            elif self.mode == "限制模式":
                if self.string_sequence and string == self.string_sequence[self.current_string_index]:
                    self.toggle_marker(string, fret)
                    if self.check_string_finished(string):
                        self.current_string_index += 1
                        if self.current_string_index >= len(self.string_sequence):
                            self.parent.ids.status_label.text = f"🎉 完成！已找到所有 {self.target_note} 音！"
                        else:
                            self.parent.ids.status_label.text = f"🎯 {self.target_note}音，点击第 {6 - self.string_sequence[self.current_string_index]} 弦"
        return True

    def toggle_marker(self, string, fret):
        # Check if marker exists
        for m in self.markers:
            if m['string'] == string and m['fret'] == fret:
                return  # already marked
        open_note = self.open_string_notes[string]
        note_number = (open_note + fret) % 12
        note_name = self.note_names[note_number]
        is_correct = (note_name == self.target_note)
        color = (0, 1, 0, 1) if is_correct else (1, 0, 0, 1)
        self.markers.append({'string': string, 'fret': fret, 'color': color, 'note': note_name})
        self.canvas.ask_update()

    def check_string_finished(self, string):
        open_note = self.open_string_notes[string]
        needed_frets = [f for f in range(13)
                        if self.note_names[(open_note + f) % 12] == self.target_note]
        for fret in needed_frets:
            found = False
            for m in self.markers:
                if m['string'] == string and m['fret'] == fret:
                    found = True
                    break
            if not found:
                return False
        return True

    def clear_markers(self):
        self.markers = []
        self.current_string_index = 0
        self.canvas.ask_update()

    def set_random_target_note(self):
        self.target_note = random.choice(self.natural_notes)
        self.clear_markers()
        self.update_string_sequence()
        self.parent.ids.status_label.text = f"🎯 请点击所有的 {self.target_note} 音"

    def update_string_sequence(self):
        if self.mode == "限制模式":
            self.string_sequence = random.sample(range(6), 6)
            self.current_string_index = 0
            self.parent.ids.status_label.text = f"🎯 {self.target_note}音，点击第 {6 - self.string_sequence[0]} 弦"
        else:
            self.string_sequence = []
            self.current_string_index = 0
            self.parent.ids.status_label.text = f"🎯 请点击所有的 {self.target_note} 音"

    def switch_mode(self, mode):
        self.mode = mode
        self.clear_markers()
        self.update_string_sequence()

    def switch_target(self, target):
        if target == "随机":
            self.set_random_target_note()
        else:
            self.target_note = target
            self.clear_markers()
            self.update_string_sequence()
            self.parent.ids.status_label.text = f"🎯 练习目标音：{self.target_note}"

    def on_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw fretboard background
            Color(0.94, 0.87, 0.73, 1)  # light wood color
            Rectangle(pos=self.pos, size=self.size)

            # Draw frets
            fret_height = self.top_margin + self.string_spacing * 5
            Color(0, 0, 0, 1)
            for i in range(1, self.fret_count + 1):
                x = self.left_margin + i * self.fret_spacing
                Line(points=[x, self.top_margin, x, fret_height], width=1)

            # Draw strings
            for i in range(6):
                y = self.top_margin + i * self.string_spacing
                # Highlight string in limit mode
                if self.mode == "限制模式" and self.string_sequence:
                    if i == (5 - self.string_sequence[self.current_string_index]):
                        Color(0, 0, 0, 1)
                        width = 3
                    else:
                        Color(0.8, 0.8, 0.8, 1)
                        width = 1
                else:
                    Color(0, 0, 0, 1)
                    width = 1
                Line(points=[self.left_margin + self.fret_spacing, y,
                             self.left_margin + self.fret_spacing * self.fret_count, y], width=width)

            # Draw nut
            x = self.left_margin + self.fret_spacing
            Line(points=[x - 5, self.top_margin - 5, x - 5, fret_height + 5], width=2)

            # Fret markers (dots)
            fret_markers = [3, 5, 7, 9]
            Color(0.53, 0.53, 0.53, 1)
            for fret in fret_markers:
                x = self.left_margin + fret * self.fret_spacing + self.fret_spacing / 2
                y = self.top_margin + (fret_height - self.top_margin) / 2
                Ellipse(pos=(x - 5, y - 5), size=(10, 10))

            # 12th fret double dots
            x = self.left_margin + 12 * self.fret_spacing + self.fret_spacing / 2
            y1 = self.top_margin + self.string_spacing * (5 - 1.5)
            y2 = self.top_margin + self.string_spacing * (5 - 3.5)
            Ellipse(pos=(x - 5, y1 - 5), size=(10, 10))
            Ellipse(pos=(x - 5, y2 - 5), size=(10, 10))

            # Draw markers
            for m in self.markers:
                x = self.left_margin + m['fret'] * self.fret_spacing + self.fret_spacing / 2
                y = self.top_margin + (5 - m['string']) * self.string_spacing
                Color(*m['color'])
                radius = 12
                Ellipse(pos=(x - radius, y - radius), size=(radius*2, radius*2))
                # Draw note text
                Color(1, 1, 1, 1)
                from kivy.core.text import Label as CoreLabel
                label = CoreLabel(text=m['note'] if m['note'] in self.natural_notes else '', font_size=16, bold=True)
                label.refresh()
                texture = label.texture
                texture_size = list(texture.size)
                self.canvas.blit(texture, (x - texture_size[0]/2, y - texture_size[1]/2))

class RootWidget(BoxLayout):
    pass

class GuitarApp(App):
    def build(self):
        root = RootWidget()
        fretboard = root.ids.fretboard
        fretboard.switch_target("随机")
        fretboard.on_canvas()
        fretboard.bind(markers=lambda *a: fretboard.on_canvas())
        fretboard.bind(size=lambda *a: fretboard.on_canvas())
        fretboard.bind(pos=lambda *a: fretboard.on_canvas())
        fretboard.bind(mode=lambda *a: fretboard.on_canvas())
        return root

if __name__ == '__main__':
    GuitarApp().run()
