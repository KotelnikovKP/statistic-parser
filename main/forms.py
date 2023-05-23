from django import forms


class LoadDataForm(forms.Form):
    data_file = forms.FileField(label='Файл с данными',
                                widget=forms.FileInput(attrs={'class': 'form-input', 'accept': '.xlsx'}))
    what_is_with_data = forms.ChoiceField(label='Что делать с уже существующими данными в системе',
                                          widget=forms.Select(attrs={'class': 'form-input'}),
                                          choices=[('delete', 'Удалить'), ('do_nothing', 'Оставить')],
                                          initial='delete')
    date_quantity = forms.ChoiceField(label='Сколько дат добавить',
                                      widget=forms.Select(attrs={'class': 'form-input'}),
                                      choices=[(1, 'Одну (1-е число)'), (2, 'Две (1-е и 16-е числа)'),
                                               (3, 'Три (1-е, 11-е и 21-е числа)')],
                                      initial=2)
