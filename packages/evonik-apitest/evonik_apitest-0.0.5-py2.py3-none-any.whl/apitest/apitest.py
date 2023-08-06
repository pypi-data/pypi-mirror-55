import random
import uuid
import exrex
import pytest
import json



def rand_str(min_length=5, max_length=20):
    """Return a random non-empty string."""
    if min_length <= 0:
        raise ValueError("min_length must be greater than 0.")
    if min_length > max_length:
        raise ValueError("min_length must by greater than or equal to max_length.")
    length = random.randint(min_length-1, max_length-1)
    cfg = "[a-z A-Z 0-9][a-z A-Z 0-9 ]{{{}}}".format(length)
    return exrex.getone(cfg)

def rand_int(min_value=1, max_value=1000):
    """Return a randon int."""
    if min_value > max_value:
        raise ValueError("max_length must be greater than or equal to min_length.")
    return random.randint(min_value, max_value)

def rand_uuid(as_string=True):
    """Return a random uuid."""
    return str(uuid.uuid4()) if as_string else uuid.uuid4()



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




class Property:
    """Model of a single property with different valid and invalid values.

    Parameters
    ----------
    name: str
        Name of the property
    valids: list or callable
        Specification of valid values
    invalids: list or callable
        Specification of invalid values
    required: list of str, default None
        List of endpoints this property is required for
    excluded: list of str, default ['GET', DELETE', 'LIST']
        List of endpoints this property should be excluded from

    Examples
    --------
    Property("name", rand_str, [""], [Endpoints.CREATE])
    Property("description", rand_str, [])
    Property("count", rand_int, [])
    """
    def __init__(self, name, valids, invalids, required=None, excluded=None):
        self.name = name
        self.valids = valids
        self.invalids = invalids
        self.required = required if required is not None else []
        self.excluded = excluded if excluded is not None else [Endpoints.GET, Endpoints.DELETE, Endpoints.LIST]
        for r in self.required:
            if r in self.excluded:
                raise ValueError("'{}' cannot be required AND excluded endpoint".format(r))

    def __str__(self):
        return self.name

    def is_required(self, endpoint):
        """Return True if this property is required for the endpoint."""
        return endpoint in self.required

    def is_excluded(self, endpoint):
        """Return True if this property should be excluded for the endpoint."""
        return endpoint in self.excluded

    def _get_values(self, endpoint, values, count):
        """Return a list of vlud for the endpoint.

        Returns an empty list if this property is excluded for
        the endpoint.
        If values is specified as a list, a copy of this list
        is returned (i.e. count is ignored).
        If values is specified as a callable, count values
        are generated and returned in a new list.

        Parameters
        ----------
        endpoint: str
            Key of the endpoint to get values for
        values: list or callable
            Specification of the values
        count: int
            Number of values to generate if values is callable
        """
        if self.is_excluded(endpoint):
            return []
        if callable(values):
            values = [values() for _ in range(count)]
        else:
            values = [v for v in values]
        return values

    def get_valids(self, endpoint, count=1):
        """Return a list of count valid values of this property for the endpoint.

        If valids is specified as a list, a copy of this list
        is returned (i.e. count is ignored).
        If valids is specified as a callable, count values
        are generated and returned in a new list.
        If this property is not required for the endpoint,
        None is added to the list.
        
        endpoint: str
            Key of the endpoint to get values for
        count: int
            Number of values to generate if valid values are specified as callable
        """
        values = self._get_values(endpoint, self.valids, count)
        if not self.is_required(endpoint):
            values.append(None)
        return values

    def get_invalids(self, endpoint, count=1):
        """Return a list of count invalid values of this property for the endpoint.

        If invalids is specified as a list, a copy of this list
        is returned (i.e. count is ignored).
        If invalids is specified as a callable, count values
        are generated and returned in a new list.
        If this property is required for the endpoint,
        None is added to the list.
        
        endpoint: str
            Key of the endpoint to get values for
        count: int
            Number of values to generate if valid values are specified as callable
        """
        values = self._get_values(endpoint, self.invalids, count)
        if self.is_required(endpoint):
            values.append(None)
        return values



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
        for prop in props:
            if prop.name in names:
                raise ValueError("Two properties with name '{}' specified.".format(prop.name))
            names.append(prop.name)
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
                all_valids = expand_dicts(all_valids, prop.name, valids)
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
                updated = update_dicts(updated, prop.name, invalids)
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



def value_from_dict(dict_, key):
    """Return the value for the key.
    
    Parameters
    ----------
    dict_: dict
        Dict containing the key
    key: str
        Key to lookup in the dict
    """
    return dict_[key]

def dict_has_value(dict_, key):
    """Return True if the key is contained in the dict.
    
    Parameters
    ----------
    dict_: dict
        Dict to check in
    key: str
        Key to check
    """
    return key in dict_

def attr_from_obj(obj, name):
    """Return the value of the attribute name.
    
    Parameters
    ----------
    obj: object
        Object with attribute name
    name: str
        Attribute name to return
    """
    return getattr(obj, name)

def obj_has_attr(obj, name):
    """Return True if the object has the attribute.
    
    Parameters
    ----------
    obj: object
        Object to check
    name: str
        Attribute name to check
    """
    return hasattr(obj, name)

class Endpoints:
    """Specification of endpoints of an API.

    The following endpoints with specific meaning can be specified:

    1. create, signature: create(values, parent)
    2. update, signature: update(values, instance)
    3. delete, signature: delete(values, instance)
    4. get, signature: get(values, instance)
    5. list, signature: list(values)

    These endpoints are identified with the following keys:

    1. create: Endpoints.CREATE
    2. update: Endpoints.UPDATE
    2. delete: Endpoints.DELETE
    2. get: Endpoints.GET
    2. list: Endpoints.LIST

    Other endpoints can be specified with arbitrary names.
    They must have the following signature:

    6. other, signature: other(values)

    Each of these endpoints is identified with its name as key,
    e.g., "other".
    
    Parameters
    ----------
    create: callable, default None
        Function for creating a new resource
    update: callable, default None
        Function for updating an existing resource
    delete: callable, default None
        Function for deleting an existing resource
    get: callable, default None
        Function for getting an existing resource
    list: callable, default None
        Function to list all existing resources
    prop_from_res: callable, default None
        Function to get a property from an API call result
    res_has_prop: callable, default None
        Function to determine if an API call result has a property
    **others: callable
        Other functions

    Examples
    --------
    component_api = Endpoints(
        create=lambda values,parent: {**values, "parent_id": parent.data.id},
        update=lambda values,instance: {**instance.data, **values},
        delete=lambda values,instance: {**instance.data},
        get=lambda values,instance: {**instance.data},
        list=lambda values: [],
        prop_from_res=value_from_dict,
        res_has_prop=dict_has_value
    )
    compute_api = Endppoints(
        square=lambda values: values["number"]**2
    )
    """

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    GET = "GET"
    LIST = "LIST"

    def __init__(self,
                 create=None,
                 update=None,
                 delete=None,
                 get=None,
                 list=None,
                 prop_from_res=attr_from_obj,
                 res_has_prop=obj_has_attr,
                 **others):
        self.create = create
        self.get = get
        self.update = update
        self.delete = delete
        self.list = list
        self.others = others
        self.prop_from_res = prop_from_res
        self.res_has_prop = res_has_prop



class Component:
    """Specification of a resource managed by an API.

    Parameters
    ----------
    name: str
        Name of the component
    props: Properties object
        Properties of the component
    endpoints: Endpoints object
        Endpoints of this component
    parent: Component object, default None
        Parent component

    Examples
    --------
    prop1 = Property("prop1", rand_str, rand_int)
    prop2 = Property("prop2", rand_int, rand_str)
    props = Properties(prop1, prop2)
    component_api = Endpoints(
        create=lambda values,parent: {**values},
        delete=lambda values,instance: {**instance.data}
    )
    comp = Component("Test", props, component_api)
    """
    def __init__(self, name, props, endpoints, parent=None):
        self.name = name
        self.props = props
        self.endpoints = endpoints
        self.parent = parent

    def get_valids(self, endpoint, count=1):
        """Generate and return list of valids from properties for endpoint."""
        return self.props.get_valids(endpoint, count)

    def get_invalids(self, endpoint, count=1):
        """Generate and return list of invalids from properties for endpoint."""
        return self.props.get_invalids(endpoint, count)



class Instance:
    """Wrapper for the creation and deletion of a component.

    An instance object provides __enter__ and __exit__ methods.
    They use the component's andpoints specification to
    create a resource and delete it.

    During enter, a component is created using the endpoint
    comp.endpoints.create.
    As payload data, it uses a random element from the
    generated list of valids for comp.endpoints.CREATE.

    During exit, the component is deleted using the endpoint
    comp.endpooints.delete.
    As payload data, it uses a random element from the
    generated list of valids for comp.endpoints.DELETE.

    The result of the create endpoint is stored in
    self.data for accessing it later.

    Parameters
    ----------
    comp: Component object
        Component to create an instance from
    parent: Instance object, default None
        Instance of a parent (as specified by the component's parent)
    **values: arbitrary
        Arbitrary values to overwrite values (from valids) for resource creation

    Examples
    --------
    comp = ...
    with Instance(comp) as instance:
        print(instance.data)
    """
    def __init__(self, comp, parent=None, **values):
        self.comp = comp
        self.parent = parent
        self.values = values

    def __enter__(self):
        if self.comp.parent is not None and self.parent is None:
            self.parent = Instance(self.comp.parent)
            self.parent.__enter__()
            self.parent_created = True
        else:
            self.parent_created = False

        valids = random.choice(self.comp.get_valids(Endpoints.CREATE))
        values_ = {**valids, **self.values}
        self.data = self.comp.endpoints.create(values_, self.parent)
        return self

    def __exit__(self, type, value, traceback):
        valids = random.choice(self.comp.get_valids(Endpoints.DELETE))
        self.comp.endpoints.delete(valids, self)
        if self.parent_created:
            self.parent.__exit__(None, None, None)



class ComponentTest:
    """Execution of common test patterns for a component.

    ComponentTest provides standardized tests for all
    CRUDL operations, specified as endpoints for the
    component.
    In addition, arbitrary endpoints can be tested
    with custom validation methods.

    Parameters
    ----------
    comp: Component object
        Component to execute tests for

    Examples
    --------
    comp = ...
    test = ComponentTest(comp)
    test.test_create(2)
    test.test_update_invalid()
    test.test_update_valid(3)
    """
    def __init__(self, comp):
        self.comp = comp

    def test_create_valid(self, count=1, exp_props=None):
        """Test the success and result of valid input to the create endpoint.

        This test creates instances of the component using
        valid input data, generated by the component.

        For each component instance, it checks if all properties,
        specified in valids, are also present in the endpoints
        result and their values match.
        You can limit the set of tested properties by specifying a list
        of expected property (exp_props).
        """
        print("# # # test create (valid)")
        for valids in self.comp.get_valids(Endpoints.CREATE, count):
            exp_props = list(valids.keys()) if exp_props is None else exp_props
            print("valids:", valids)
            with Instance(self.comp, **valids) as instance:
                for k in exp_props:
                    assert self.comp.endpoints.res_has_prop(instance.data, k)
                    assert valids[k] == self.comp.endpoints.prop_from_res(instance.data, k)

    def test_create_invalid(self, count=1):
        """Test the success of invalid input to the create endpoint.

        This test attempts to create instance of the component
        using invalid data, generated by the component.

        For each creation attempt, it checks if the invalid creation
        indeed caused raising an exception.
        """
        print("# # # test create (invalid)")
        for invalids in self.comp.get_invalids(Endpoints.CREATE, count):
            print("invalids:", invalids)
            with pytest.raises(Exception) as e_info:
                if self.comp.parent is None:
                    self.comp.endpoints.create(invalids, None)
                else:
                    with Instance(self.comp.parent) as parent:
                        self.comp.endpoints.create(invalids, parent)

    def test_create(self, count=1, exp_props=None):
        """Test the success and result of valid and invalid input to the create endpoint."""
        self.test_create_valid(count, exp_props)
        self.test_create_invalid(count)

    def test_update_valid(self, count=1, exp_props=None):
        """Test the success and result of valid input to the update endpoint.

        This test updates properties of an instance and validates
        that the updated and rerturned values are the same as the
        ones specified in valid payload data.
        You can limit the set of tested properties by specifying a list
        of expected property (exp_props).
        """
        print("# # # test update (valid)")
        for valids in self.comp.get_valids(Endpoints.UPDATE, count):
            exp_props = list(valids.keys()) if exp_props is None else exp_props
            print("valids:", valids)
            with Instance(self.comp) as instance:
                data = self.comp.endpoints.update(valids, instance)
                for k in exp_props:
                    assert self.comp.endpoints.res_has_prop(data, k)
                    assert valids[k] == self.comp.endpoints.prop_from_res(data, k)

    def test_update_invalid(self, count=1):
        """Test the success and result of invalid input to the update endpoint.

        This test checks if the update endpoint indeed raises an exception
        if the provided data is invalid.
        """
        print("# # # test update (invalid)")
        for invalids in self.comp.get_invalids(Endpoints.UPDATE, count):
            print("invalids:", invalids)
            with Instance(self.comp) as instance:
                with pytest.raises(Exception) as e_info:
                    data = self.comp.endpoints.update(valids, instance)

    def test_update(self, count=1, exp_props=None):
        """Test the success and result of valid and invalid input to the update endpoint."""
        self.test_update_valid(count, exp_props)
        self.test_update_invalid(count)

    def test_get(self, count=1, times=2):
        """Test the success and result of the get endpoint.

        This test checks if the data of a component, obtained using the
        get endpoint, is the same as the one used during its creation.
        """
        print("# # # test get")
        for _ in range(times):
            with Instance(self.comp) as instance:
                print(instance.data)
                for valids in self.comp.get_valids(Endpoints.GET, count):
                    data = self.comp.endpoints.get(valids, instance)
                    for prop in self.comp.props.props:
                        k = prop.name
                        v = self.comp.endpoints.prop_from_res(instance.data, k)
                        assert self.comp.endpoints.res_has_prop(data, k)
                        assert v == self.comp.endpoints.prop_from_res(data, k)

    def test_list(self, count=1, entries=5, len_from_res=len):
        """Test the success of the list endpoint.

        This tests checks the count of entries obtained using the
        list endpoints.
        This is done by creating entries components and checking
        if the number of entries in list is actually increased
        accordingly.

        Parameters
        ----------
        count: int, default 1
            Count passed down to the valid data generator
        entries: int, default 5
            Number of entries to create during the test
        len_from_res: callable, default len
            Function to obtain the current component count from
            the list endpoint's result
        """
        print("# # # test list")
        for valids in self.comp.get_valids(Endpoints.LIST, count):
            initial = len_from_res(self.comp.endpoints.list(valids))
            print("initial:", initial)
            elements = []
            for i in range(entries):
                elements.append(Instance(self.comp, None))
                elements[-1].__enter__()
                current = len_from_res(self.comp.endpoints.list(valids))
                print("->", current)
                assert current == initial + i + 1
            for i in range(entries):
                elements[i].__exit__(None, None, None)
                current = len_from_res(self.comp.endpoints.list(valids))
                print("->", current)
                assert current == initial + entries - i - 1

        assert len(self.comp.endpoints.list(valids)) == initial

    def test_valid(self, key, count=1, val_res=None):
        """Test valid input to a non-standard endpoint.

        The custom endpoint is executed for all valid data
        in comp.get_valids(count).
        The result of this request is then validated using
        the custom function.

        Parameters
        ----------
        key: str
            Key to identify the endpoint (as specified
            during initialization of the Endpoints object)
        count: int, default 1
            Count passed down to the valid data generator
        val_res: callable, default None
            Function to validate the result from the
            custom endpoint
            It should return True is the result data is
            valid and False otherwise.
        """
        print("# # # test {} (valid)".format(key))
        for valids in self.comp.get_valids(key, count):
            print("valids:", valids)
            res = self.comp.endpoints.others[key](valids)
            print("        ->", res)
            if val_res is not None:
                assert(val_res(valids, res))

    def test_invalid(self, key, count=1):
        """Test invalid input to a non-standard endpoint.

        The custom endpoint is executed for all invalid data
        in comp.get_invalids(count).
        Then, the test checks if the endpoint's execution
        indeed raises an exception.

        Parameters
        ----------
        key: str
            Key to identify the endpoint (as specified
            during initialization of the Endpoints object)
        count: int, default 1
            Count passed down to the valid data generator
        """
        print("# # # test {} (invalid)".format(key))
        for invalids in self.comp.get_invalids(key, count):
            print("invalids:", invalids)
            with pytest.raises(Exception) as e_info:
                res = self.comp.endpoints.others[key](invalids)

    def test(self, key, count=1, val_res=None):
        """Test valid and invalid input to a non-standard endpoint."""
        self.test_valid(key, count, val_res)
        self.test_invalid(key, count)
