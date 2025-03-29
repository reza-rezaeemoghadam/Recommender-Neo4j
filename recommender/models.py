from neomodel import StructuredNode, StructuredRel,StringProperty, FloatProperty, RelationshipTo

class Rating(StructuredRel):
    score = FloatProperty()

class User(StructuredNode):
    username = StringProperty(unique_index=True)
    rated = RelationshipTo('Product', 'RATED', model=Rating)

class Product(StructuredNode):
    name = StringProperty()
    category = StringProperty()