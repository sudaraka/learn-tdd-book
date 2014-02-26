""" list app forms """

from django import forms

from lists.models import Item


EMPTY_LIST_ERROR = 'You can\'t have an empty list item'


class ItemForm(forms.models.ModelForm):
    """ item form """

    class Meta:
        """ item fomr meta """

        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            })}

    def __init__(self, *args, **kwargs):
        """ Init form object """

        super().__init__(*args, **kwargs)

        self.fields['text'].error_messages['required'] = EMPTY_LIST_ERROR

    def save(self, for_list):
        """ set current list instance """

        self.instance.list = for_list

        return super().save()
