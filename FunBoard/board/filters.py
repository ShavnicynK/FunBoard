from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Advertisement, Reaction


class ReactionFilter(FilterSet):

    class Meta:
        model = Reaction
        fields = ['content', 'advertisement', 'status']

    def __init__(self, *args, **kwargs):
        super(ReactionFilter, self).__init__(*args, **kwargs)
        self.filters['advertisement'].queryset = Advertisement.objects.filter(author_id=kwargs['request'])
