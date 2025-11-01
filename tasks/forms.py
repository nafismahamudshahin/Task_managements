from django import forms
from tasks.models import Project , Task ,Employee , TaskDetails

class StyledFormMixin:
    """Mixin to apply Tailwind CSS styles to form fields"""

    default_classes = (
        "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.PasswordInput)):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    # 'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 p-3 rounded-lg shadow-sm "
                             "focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })

class CreateProject(StyledFormMixin, forms.ModelForm):
    # name = forms.CharField()
    # start_date = forms.DateTimeField(widget=forms.SelectDateWidget)
    class Meta:
        model = Project
        fields = "__all__"

class CreateTask(StyledFormMixin , forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets ={
            'due_date': forms.SelectDateWidget,
            'assigne_to' : forms.CheckboxSelectMultiple
        }

class CreateEmployee(StyledFormMixin , forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class CreateTaskDetails(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetails
        fields = ['asset','priority','note']