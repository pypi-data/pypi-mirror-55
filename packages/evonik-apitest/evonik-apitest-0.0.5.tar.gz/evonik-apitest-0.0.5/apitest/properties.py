import json

def expand_dicts(dicts, key, values):
    """Expand and return the dicts with all values for the key.

    For each dict in dicts and each value in values, a new dict is generated.
    This new dict contains all entries from the original one as well
    as a mapping from key to value.
    If a value is None, a copy of the original dict is added.
    Overall, len(dicts)*len(values) dicts are generated and returned.

    Parameters
    ----------
    dicts: list
        List of dictionaries to expand
    key: str
        Key of the entry to be added to each dict
    values: list
        List of values to be added to each dict
    """
    expanded = []
    for old in dicts:
        for value in values:
            if value is not None:
                expanded.append({**old, key:value})
            else:
                expanded.append({**old})
    return expanded

def update_dicts(dicts, key, values):
    """Update and return the dicts with all values for the key.

    For each dict in dicts and each value in values, a new dict is generated.
    It contains all entries from the original one except for key.
    If a value is not None, key is mapped to value.
    Otherwise, key is not added to the dict as key.
    Overall, len(dicts)*len(values) dicts are generated and returned.

    Parameters
    ----------
    dicts: list
        List of dictionaries to update
    key: str
        Key of the entry to be updated in each dict
    values: list
        List of values to be added to each dict
    """
    updated = []
    for old in dicts:
        for value in values:
            old_ = {k:v for k,v in old.items() if k != key}
            if value is not None:
                old_.update({key: value})
            updated.append(old_)
    return updated

def dicts_without_key(dicts, key):
    """Return a list of new dicts without the key."""
    updated = []
    for old in dicts:
        updated.append({k:v for k,v in old.items() if k != key})
    return updated

def _dict_as_str(dict_):
    """Return as string representation of the dict."""
    return json.dumps(dict_, sort_keys=True)

def unique_dicts(dicts):
    """Return a list of all unique dicts."""
    return list({
        _dict_as_str(d):d
        for d in dicts
    }.values())

def exclude_dicts(dicts, exclude):
    """Return a list of all dicts that are not in exclude."""
    buts = [_dict_as_str(d) for d in exclude]
    return [
        d for d in dicts
        if _dict_as_str(d) not in buts
    ]

def non_empty_dicts(dicts):
    """Return a list all dicts with at least one entry."""
    return [x for x in dicts if len(x) > 0]

class Properties:
    """Wrapper for generating valid / invalid combinations of properties.

    Parameters
    ----------
    *props: list of Property
        List of the properties to wrap

    Examples
    --------
    prop1 = Property("prop1", rand_str, rand_int)
    prop2 = Property("prop2", rand_int, rand_str)
    props = Properties(prop1, prop2)
    """
    def __init__(self, *props):
        names = []
        spec_names = []
        res_names = []
        for prop in props:
            if prop.name in names:
                raise ValueError("Two properties with name '{}' specified.".format(prop.name))
            if prop.spec_name in spec_names:
                raise ValueError("Two properties with spec_name '{}' specified.".format(prop.spec_name))
            if prop.res_name in res_names:
                raise ValueError("Two properties with res_name '{}' specified.".format(prop.res_name))
            names.append(prop.name)
            spec_names.append(prop.spec_name)
            res_names.append(prop.res_name)
        self.props = props

    def get_valids(self, method, count=1):
        """Return a list of valid value dicts from all properties.

        For each property, a list of valid values is generated.
        Then, all valid combinations of these values are generated
        and stored in dicts.
        As a key, the name of a property is used.

        Parameters
        ----------
        endpoint: str
            Key of the endpoint to get values for
        count: int
            Number of values to generate per property
        """
        all_valids = [{}]
        for prop in self.props:
            valids = prop.get_valids(method, count)
            if len(valids) > 0:
                all_valids = expand_dicts(all_valids, prop.spec_name, valids)
        return all_valids

    def get_invalids(self, method, count=1):
        """Return a list of invalid value dicts from all properties.

        Parameters
        ----------
        endpoint: str
            Key of the endpoint to get values for
        count: int
            Number of values to generate per property
        """
        all_valids = self.get_valids(method, count)
        all_invalids = []
        # create invalids from valids
        for prop in self.props:
            invalids = prop.get_invalids(method, count)
            if len(invalids) > 0:
                updated = [{k:v for k,v in x.items()} for x in all_valids]
                updated = update_dicts(updated, prop.spec_name, invalids)
                all_invalids += updated
        # remove duplicated
        all_invalids = unique_dicts(all_invalids)
        # remove empty dict
        all_invalids = non_empty_dicts(all_invalids)
        # add empty dict if this would be invalid
        for prop in self.props:
            if prop.is_required(method):
                all_invalids.append({})
                break
        # remove still valid dicts
        all_invalids = exclude_dicts(all_invalids, all_valids)
        return all_invalids


import pytest
from .property import Property
from .endpoints import Endpoints
from .util import rand_str

def test_names():
    p1 = Property(rand_str(), [], [], spec_name=rand_str(), res_name=rand_str())
    p2 = Property(rand_str(), [], [], spec_name=rand_str(), res_name=rand_str())
    p1_1 = Property(p1.name, [], [], spec_name=rand_str(), res_name=rand_str())
    p1_2 = Property(rand_str(), [], [], spec_name=p1.spec_name, res_name=rand_str())
    p1_3 = Property(rand_str(), [], [], spec_name=rand_str(), res_name=p1.res_name)
    Properties(p1, p2)
    Properties(p2, p1_1)
    Properties(p2, p1_2)
    Properties(p2, p1_3)
    with pytest.raises(Exception):
        Properties(p1, p1_1)
    with pytest.raises(Exception):
        Properties(p1, p1_2)
    with pytest.raises(Exception):
        Properties(p1, p1_3)

def test_valids():
    c, u = Endpoints.CREATE, Endpoints.UPDATE
    p1 = Property("p1", [1, 2, 3, 4, 5], [], [c])
    p2 = Property("p2", [11, 12, 13], [])
    props = Properties(p1, p2)
    assert len(props.get_valids(c, count=1)) == len(p1.get_valids(c)) * len(p2.get_valids(c))
    assert len(props.get_valids(u, count=1)) == len(p1.get_valids(u)) * len(p2.get_valids(u))
