# -*- coding: utf-8 -*-
import query_extractar as query
from worldmap_visualiser import MapVisualiser

def run_query_operations(q):
    query_results = query.getQueryResults(q, num_results=1, pause=2)
    extracted_data = query.extractWebData(query_results)
    preprocessed_data = query.preprocessRawText(extracted_data)
    located_named_entity = query.locate_named_entities(preprocessed_data)
    
    mv = MapVisualiser()
    mv.showCountries()
    checked_countries = mv.checkCountries(located_named_entity)
    created_dataframe = mv.createCountriesDataframe(checked_countries)
    retrieved_continents = mv.getContinent(created_dataframe)
    geographical_loc = mv.geolocate(retrieved_continents)
    mv.generate_worldmap(geographical_loc)

def main():
    run_query_operations("best countries to move to 2021")

if __name__ == "__main__":
    main()