from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from custom_ui.customgradient import CustomGradient
import matplotlib.pyplot as plt
import numpy as np
import os
import logging
from kivy.logger import Logger

logging.getLogger('matplotlib').setLevel(logging.WARNING)

import os
import numpy as np
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class GraphWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        plt.figure(figsize=(10, 6))

        x_values = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        y_values = [0.82, 0.19, 0.48, 0.69, 0.89, 1.22, 0.98]

        bar_color = (0.82, 0.90, 0.99, 1)
        text_color = (0.82, 0.90, 0.99, 1)
        font_size = 20
        bar_width = 0.6

        plt.bar(x_values, y_values, color=bar_color, width=bar_width, zorder=3)
        plt.xlabel('', color=text_color, fontsize=font_size)
        plt.title('Energy Usage', color=text_color, fontsize=26, loc='right')

        plt.xticks(np.arange(len(x_values)), x_values, color=text_color, fontsize=font_size, rotation=0, ha='right')
        plt.yticks(color=text_color, fontsize=font_size)

        plt.grid(axis='y', color=text_color, linestyle='--', linewidth=0.2, zorder=0)

        plt.subplots_adjust(left=0.1, right=1, top=0.9, bottom=0.3)

        plt.gcf().patch.set_facecolor('none')

        ax = plt.gca()
        for spine in ax.spines.values():
            spine.set_visible(False)

        total_kwh = sum(y_values)
        total_cost = total_kwh * 0.12
        plt.text(-.1, 1.08, f'(kWh) Cost: ${total_cost:.2f}', 
                 horizontalalignment='left', verticalalignment='top', 
                 transform=ax.transAxes, fontsize=font_size+4, color=text_color, fontweight='bold')

        plt.tight_layout()

        plt.savefig('graph.png', transparent=True)
        plt.close()

        image = Image(source='graph.png')
        self.add_widget(image)

        os.remove('graph.png')


class LightEnergyGraph(FloatLayout):
    def __init__(self, pos_hint={'center_x': 0.5, 'center_y': 0.525}, size_hint=(0.5, 0.45), **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = pos_hint
        self.size_hint = size_hint

        CustomGradient.enable_gradient(self, (.85, .85, .9, .3), (0.43, 0.54, 0.68754, 0.2), radius=9)

        graph_widget = GraphWidget(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(graph_widget)