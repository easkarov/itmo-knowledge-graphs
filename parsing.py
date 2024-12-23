import json
import os
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS

EX = Namespace("http://example.org/")

g = Graph()

g.add((EX.TypeOfProduct, RDF.type, RDFS.Class))
g.add((EX.Product, RDF.type, RDFS.Class))
g.add((EX.Vitamin, RDF.type, RDFS.Class))

# Add object properties to the graph
g.add((EX.containsVitamin, RDF.type, RDF.Property))
g.add((EX.containsVitamin, RDFS.domain, EX.Product))
g.add((EX.containsVitamin, RDFS.range, EX.Vitamin))

g.add((EX.hasIngredient, RDF.type, RDF.Property))
g.add((EX.hasIngredient, RDFS.domain, EX.Product))
g.add((EX.hasIngredient, RDFS.range, EX.Product))

g.add((EX.typeOfProduct, RDF.type, RDF.Property))
g.add((EX.typeOfProduct, RDFS.domain, EX.Product))
g.add((EX.typeOfProduct, RDFS.range, EX.TypeOfProduct))

g.add((EX.Ingredient, RDF.type, EX.TypeOfProduct))
g.add((EX.Recipe, RDF.type, EX.TypeOfProduct))

def format(text):
    return text.replace(' ', '_').replace('A', 'А').replace('B', 'В').replace('C', 'С').replace('D', 'Д').replace('E', 'Е').replace('F', 'Ф').replace('K', 'К').lower()
    
def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_cuisine.json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                print(f)
                cuisines = json.load(f)
                for dish in cuisines:
                    dish_uri = URIRef(f"http://example.org/{format(dish['name'])}")
                    g.add((dish_uri, RDF.type, EX.Product))
                    g.add((dish_uri, EX.typeOfProduct, EX.Recipe))
                    
                    for ingredient in dish['ingredients']:
                        ingredient_uri = URIRef(f"http://example.org/{format(ingredient)}")
                        g.add((ingredient_uri, EX.typeOfProduct, EX.Ingredient))
                        g.add((ingredient_uri, RDF.type, EX.Product))
                        g.add((dish_uri, EX.hasIngredient, ingredient_uri))

        elif filename.endswith("_vitamins.json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                print(f)
                vitamins = json.load(f)
                for food in vitamins:
                    food_uri = URIRef(f"http://example.org/{format(food['name'])}")
                    g.add((food_uri, EX.typeOfProduct, EX.Ingredient))
                    for vitamin in food['vitamins']:
                        vitamin_uri = URIRef(f"http://example.org/{format(vitamin)}")
                        g.add((vitamin_uri, RDF.type, EX.Vitamin))
                        g.add((food_uri, EX.containsVitamin, vitamin_uri))

process_files("./data")

g.serialize(destination='output.rdf', format="pretty-xml")

print("RDF graph created successfully!")
