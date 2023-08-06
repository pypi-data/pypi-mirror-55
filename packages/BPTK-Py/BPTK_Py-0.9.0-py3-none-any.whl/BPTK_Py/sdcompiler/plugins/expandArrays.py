#                                                       /`-
# _                                  _   _             /####`-
# | |                                | | (_)           /########`-
# | |_ _ __ __ _ _ __  ___  ___ _ __ | |_ _ ___       /###########`-
# | __| '__/ _` | '_ \/ __|/ _ \ '_ \| __| / __|   ____ -###########/
# | |_| | | (_| | | | \__ \  __/ | | | |_| \__ \  |    | `-#######/
# \__|_|  \__,_|_| |_|___/\___|_| |_|\__|_|___/  |____|    `- # /
#
# Copyright (c) 2019 transentis labs GmbH
# MIT License

from copy import deepcopy
import itertools


def cartesian_product(listoflists):
    """
    Helper for Cartesian product
    :param listoflists:
    :return:
    """
    if len(listoflists) == 1:
        return listoflists
    return list(itertools.product(*listoflists))

def extract_labels(arg,dimensions, index):
    """

    :param arg:
    :param dimensions:
    :param index:
    :return:
    """
    labels = dimensions[index]

    if arg["type"] == "asterisk":
        return labels

    elif arg["type"] == "range":
        range = [ar["name"] for ar in arg["args"]]
        start = labels.rfind(range[0])
        end = labels.rfind(range[1]) + 1
        return labels[start:end]

    elif arg["type"] == "label":
        return arg["name"]

    elif arg["type"] == "identifier":
        return arg

    else:
        class ExpressionNotSupportedException(Exception):
            pass
        raise(ExpressionNotSupportedException("Expressions in Array are not supported yet."))

def alter_identifier(IR, entity,expression,model_name):
    """
    Change idenfitifiers to elementName[Dimension]
    :param IR:
    :param entity:
    :param expression:
    :param model_name:
    :return:
    """
    if type(expression) is str or type(expression) is float:
        return entity

    if type(expression) is list:
        for elem in expression:
            alter_identifier(IR,entity,elem,model_name)

    if type(expression) is dict:
        name_ = expression["name"]
        type_ = expression["type"]

        if "args" in expression.keys():
            alter_identifier(IR,entity, expression["args"],model_name)

        if type_ == "identifier":

            labels_ = []

            for index, dim in enumerate(entity["dimensions"]):
                dimension = IR["dimensions"][dim]
                found = 0
                for var in dimension["variables"]:
                    if var["model"] == model_name and  var["name"] == name_:
                        found += 1

                if found > 0 :
                    labels_ += [entity["labels"][index]]

                if len(labels_) > 0:
                    expression["type"] = "array"

                    expression["args"] = toLabelObjects(labels_)

def spread_function_arguments(expression,model_name,IR):
    if type(expression) is str or type(expression) is float:
        return expression

    if type(expression) is list:
        for elem in expression:
            spread_function_arguments(elem,model_name,IR=IR)

    if type(expression) is dict:
        name_ = expression["name"]
        type_ = expression["type"]

        if type_ == "call":
            args = []

            for arg in expression["args"]:

                if type(arg) == list:
                    arg = arg[0]

                '''
                Asterisks for Identifiers
                '''
                if arg["type"] == 'identifier':

                        count = 0
                        for dim in IR["dimensions"]:
                            for variable in dim["variables"]:
                                if variable["model"] == model_name and variable["name"] == arg["name"]:
                                    count += 1

                        asterisks  = [{ "name": '*', "type": 'asterisk' } for _ in range(0,count)]

                        if len(asterisks) > 0:
                            arg["args"] = asterisks
                            arg["type"] = "array"

                '''
                Array Expressions
                '''
                if arg["type"] == "array":
                        dimensions = []
                        for dimension in IR["dimensions"]:
                            variables = dimension["variables"]
                            var_count = 0
                            for variable in variables:
                                if variable["model"] == model_name and variable["name"] == arg["name"] and len(
                                        dimension["labels"]) > 0:
                                    var_count += 1

                            if var_count > 0: dimensions += [dimension]

                        arg_args = arg["args"]

                        arg_args_labels = [extract_labels(dimensions=dimensions,index=index,arg=ar) for index, ar in enumerate(arg_args)]
                        products = cartesian_product(arg_args_labels)
                        args += [{"name": arg["name"], "type": "array", "args": toLabelObjects(product) } for product in products]

                else:
                    args += [arg]
                    #args += [spread_function_arguments(arg,model_name,IR)]
            expression["args"] = args

    return expression

def clone_entity(entity, idx,product=None):
    ent = deepcopy(entity)

    if product:
        ent["labels"] = product
    elif len(entity["labels"]) > 0:
            ent["labels"] = entity["labels"][idx]
            ent["equation"] = entity["equation"][idx]
            ent["equation_parsed"] = entity["equation_parsed"][idx]

    #if len(ent["labels"]) > 0 and type(ent["labels"]) is tuple:
        #ent["name"] = "{}".format(ent["name"]) + "[" + ", ".join(ent["labels"]) + "]"
    return ent


def toLabelObjects(labels):
    if type(labels) is list or type(labels) is tuple:
        return [{ "name": label, "type": 'label' } for label in labels]

    else:
        return [ { "name": labels, "type": 'label' } ]


def ExpandArrays(IR):
    """
    Actual plugin. Traverses the IR and finds all array expressions. Creates stocks such as stock1[Dimensions1,Dim1] for each dimension equation
    :param IR:
    :return:
    """
    for name, model in IR["models"].items():
        '''
        Traverse the IR
        '''
        for entity_type, entities in model["entities"].items():

            '''
            Build new entities
            '''
            for index, entity in enumerate(deepcopy(entities)):
                _entities = []

                if type(entity["equation_parsed"]) is list and len(entity["equation_parsed"]) > 1:

                    _entities = [deepcopy(clone_entity(entity, i)) for i in range(0, len(entity["equation_parsed"]))]
                    model["entities"][entity_type] += _entities


                elif ("dimensions" in entity.keys()) and len(entity["dimensions"]) > 0:

                    labels = [IR["dimensions"][name]["labels"] for name in entity["dimensions"]]
                    products = cartesian_product(labels)

                    _entities = [deepcopy(clone_entity(entity, i,products[i])) for i in range(0, len(products))]
                    model["entities"][entity_type] += _entities

                else:
                    continue

                '''
                Create new Expressions based on new entities
                '''
                for elem in _entities:
                    alter_identifier(IR,elem,elem["equation_parsed"],name)

                if len(_entities) == 1:
                    entities[index]["labels"] = []
                    entities[index]["equation_parsed"] = {
                        "name": _entities[0]["name"],
                        "type": 'array',
                        "args": toLabelObjects(_entities[0]["labels"])
                    }

                elif len(_entities) == 2:
                    entities[index]["labels"] = []
                    entities[index]["equation_parsed"] = {
                        "name": '+',
                        "type": 'operator',
                        "args": [
                            {"name": _entities[0]["name"], "type": 'array',
                             "args": toLabelObjects(_entities[0]["labels"])},
                            {"name": _entities[1]["name"], "type": 'array',
                             "args": toLabelObjects(_entities[1]["labels"])}
                        ]
                    }

                elif len(_entities) > 2:
                    tail = _entities[-2:]
                    rest = _entities[:-2]

                    already_reduced = initial = {
                        "name": "+",
                        "type": 'operator',
                        "args": [
                            {"name": tail[0]["name"], "type": 'array', "args":toLabelObjects( tail[0]["labels"])},
                            {"name": tail[1]["name"], "type": 'array',  "args":toLabelObjects( tail[1]["labels"]) }
                        ]
                    }

                    def reduce(already_reduced, rhs):
                        """
                        Reducer
                        :param already_reduced:
                        :param rhs:
                        :return:
                        """
                        return {
                            "name": "+",
                            "type": 'operator',
                            "args": [{"name": rhs["name"], "type": 'array', "args": toLabelObjects( rhs["labels"]) }, already_reduced]
                        }

                    for index, elem in enumerate(reversed(rest)):
                        already_reduced = reduce(already_reduced, elem)

                    model["entities"][entity_type][index]["equation_parsed"] = already_reduced
                    model["entities"][entity_type][index]["labels"] = []

                spread_function_arguments(expression=model["entities"][entity_type][index]["equation_parsed"],model_name=model["name"],IR=IR)
    return IR
