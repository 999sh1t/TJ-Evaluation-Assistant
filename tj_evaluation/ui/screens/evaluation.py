from kivy.uix.screenmanager import Screen
from tj_evaluation.ui.widgets.comprehensive_evaluation_content import ComprehensiveEvaluationContent

class EvaluationScreen(Screen):
    def __init__(self, main_layout, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ComprehensiveEvaluationContent(main_layout))