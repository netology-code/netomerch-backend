import pytest

from apps.products.management.functions.find_match import find_match

search_set = [
    ('test', 'object1'),
    ('not_test', 'object2'),
    ('good phrase', 'object3')
]

samples = ['test', 'fucking', 'goot phrase']
results = [
    ('test', 'object1'),
    False,
    ('good phrase', 'object3')
]

test_data = []
for i in range(len(samples)):
    print(i)
    test_data.append((samples[i], search_set, results[i]))


@pytest.mark.parametrize(
    "sample, search_sets, value",
    test_data
)
def test_example(sample, search_sets, value):
    response = find_match(sample, search_sets)
    assert response == value
