""" list app forms """

from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item


EMPTY_LIST_ERROR = 'You can\'t have an empty list item'
DUPLICATE_ITEM_ERROR = 'You\'ve already got this in your list'


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
        """ Init item form object """

        super().__init__(*args, **kwargs)

        self.fields['text'].error_messages['required'] = EMPTY_LIST_ERROR

    def save(self, for_list):
        """ set current list instance """

        self.instance.list = for_list

        return super().save()


class ExistingListItemForm(ItemForm):
    """ existing list item form """

    def __init__(self, for_list, *args, **kwargs):
        """Init existing list item from object """

        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """ do form uniqueness validation """

        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
