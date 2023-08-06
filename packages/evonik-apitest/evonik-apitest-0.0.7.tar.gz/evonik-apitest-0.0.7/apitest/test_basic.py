import random

from apitest import Property, Properties, Endpoints, Component, Instance, ComponentTest
from apitest.util import rand_str, rand_int, value_from_dict, dict_has_value


class CategoryApi:
    def __init__(self):
        self.categories = {}

    def create(self, values, parent):
        if "name" not in values:
            raise ValueError("must specify name")
        if values["name"] in [None, ""]:
            raise ValueError("name cannot be empty")
        id = random.randint(0, 1000)
        data = {**values, "id": id}
        self.categories[id] = data
        return data

    def update(self, values, instance):
        id = instance.data["id"]
        data = {**self.categories[id], **values}
        self.categories[instance.data["id"]] = data
        return data

    def delete(self, values, instance):
        id = instance.data["id"]
        data = self.categories[id]
        del self.categories[id]
        return data

    def list(self, values):
        return [v for v in self.categories.values()]

class EntryApi:
    def __init__(self):
        self.entries = {}

    def create(self, values, parent):
        if "name" not in values:
            raise ValueError("must specify name")
        if values["name"] in [None, ""]:
            raise ValueError("name cannot be empty")
        if "color" not in values:
            raise ValueError("must specify color")
        if values["color"] not in ["red", "green", "blue"]:
            raise ValueError("color is invalid: {}".format(values["color"]))
        id = random.randint(1, 1000)
        data = {**values, "category_id": parent.data["id"], "id": id}
        self.entries[id] = data
        return data

    def update(self, values, instance):
        id = instance.data["id"]
        data = {**self.entries[id], **values}
        self.entries[instance.data["id"]] = data
        return data

    def delete(self, values, instance):
        id = instance.data["id"]
        data = self.entries[id]
        del self.entries[id]
        return data

    def list(self, values):
        return [v for v in self.entries.values()]

class ComputeApi:
    def compute(self, data):
        return data["counter"] + 1



capi = CategoryApi()
category_api = Endpoints(
    create=capi.create,
    update=capi.update,
    delete=capi.delete,
    list=capi.list,
    prop_from_res=value_from_dict,
    res_has_prop=dict_has_value
)

eapi = EntryApi()
entry_api = Endpoints(
    create=eapi.create,
    update=eapi.update,
    delete=eapi.delete,
    list=eapi.list,
    prop_from_res=value_from_dict,
    res_has_prop=dict_has_value
)

compapi = ComputeApi()
compute_api = Endpoints(
    compute=compapi.compute
)

name = Property("name", rand_str, [""], [Endpoints.CREATE])
description = Property("description", rand_str, [])
color = Property("color", ["red", "green", "blue"], rand_str, [Endpoints.CREATE])
counter = Property("counter", rand_int, rand_str, ["compute"])

category = Component("Category", Properties(name, description), category_api)
entry = Component("Entry", Properties(name, description, color), entry_api, category)
computation = Component("Computation", Properties(counter), compute_api)

def test_create_category():
    ComponentTest(category).test_create()
def test_update_category():
    ComponentTest(category).test_update()
def test_list_category():
    ComponentTest(category).test_list(entries=5)

def test_create_entry():
    ComponentTest(entry).test_create()
def test_update_entry():
    ComponentTest(entry).test_update()
def test_list_entry():
    ComponentTest(entry).test_list(entries=5)

def test_compute():
    ComponentTest(computation).test("compute", 2, val_res=lambda values,x: type(x) == int)
