#!/usr/bin/env python3
from transform import identity


class Node:
    """ Scene graph transform and parameter broadcast node """

    def __init__(self, name='', children=(), transform=identity(), **param):
        self.transform, self.param, self.name = transform, param, name
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model, **param):
        """ Recursive draw, passing down named parameters & model matrix. """
        # merge named parameters given at initialization with those given here
        param = dict(param, **self.param)
        # model = ...   # what to insert here for hierarchical update?
        model = model @ self.transform
        for child in self.children:
            # model = model @ self.transform
            child.draw(projection, view, model, **param)
