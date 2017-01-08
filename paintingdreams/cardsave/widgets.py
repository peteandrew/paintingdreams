from django import forms


class CardsaveBooleanHiddenInput(forms.HiddenInput):

    def render(self, name, value, attrs=None):
        value = str(value).lower()
        return super(CardsaveBooleanHiddenInput, self).render(name, value, attrs)
