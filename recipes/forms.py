from django import forms

from recipes.models import Recipe, Tag, Product


class RecipeForm(forms.ModelForm):
    """Форма для создания и редактирования рецепта."""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tags__checkbox'}),
        to_field_name='slug',
        required=False
    )

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'cook_time', 'ingredients', 'description', 'image',)#, 'ingredients'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'cook_time': forms.NumberInput(
                attrs={'class': 'form__input', 'id': 'id_time',
                       'name': 'time'}),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': '8'}),
        }
        labels = {
            'image': 'Загрузить фото'
        }

    # def __init__(self, request, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.request = request

    # def clean_ingredients(self):
    #     data = self.cleaned_data['ingredients']
    #     ingedient_names = self.request.getlist('nameIngredient')
    #     if len(ingedient_names) == 0:
    #         raise forms.ValidationError('Добавте ингридиент')
    #     for ingedient in ingedient_names:
    #         if not Product.objects.filter(title=ingedient).exists():
    #             raise forms.ValidationError(f'Ингредиент {ingedient} не корректный.')
    #     return data

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) == 0:
            raise forms.ValidationError("Name!")
    #
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
        return data

    def clean_cook_time(self):
        data = self.cleaned_data['cook_time']
        if len(data) == '':
            raise forms.ValidationError("cook_time!")
    #
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        if len(data) == 0:
            raise forms.ValidationError("description!")
    #
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
        return data

    def clean(self):
        # общая функция валидации
        return self.cleaned_data