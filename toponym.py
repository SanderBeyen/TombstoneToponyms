import geocoder
import mpu
import nltk
import os
import spacy
import sys
import webbrowser
from exif import Image
from geopy.geocoders import GeoNames


def dms_coordinates_to_dd_coordinates(coordinates, coordinates_ref):
    """Format the GPS metadata"""

    decimal_degrees = coordinates[0] + \
        coordinates[1] / 60 + \
        coordinates[2] / 3600

    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees

    return decimal_degrees


def main():

    # List of possible toponyms in GeoNames database
    toponyms_list = []
    with open("GeoNames_Toponyms_List.txt") as file:
        for line in file:
            line = line.replace('"', '').strip('\n').lower()
            toponyms_list.append(line)

    # Dictionary that maps old toponym spellings to their modern variant (Example: Zutfen -> Zutphen)
    ambiguous_dict = {}
    with open("Ambiguous_old_modern_spelling.txt") as file:
        for line in file:
            old, modern = line.strip('\n').lower().split(',')
            ambiguous_dict[old] = modern

    # Fills list with toponyms found in the Optical Character Recognition output
    found_toponyms = []
    print("Tesseract output: \n")
    with open(sys.argv[1]) as file:
        for line in file:
            print(line)
            words = line.lower().replace('(', ' ').replace(')', ' ').replace(',', ' ').replace('?', ' ').replace('.', ' ').replace('!', ' ').split()
            for word in words:
                if word in ambiguous_dict:
                    modern_word = ambiguous_dict[word]
                    if modern_word in toponyms_list:
                        found_toponyms.append(modern_word)
                elif word in toponyms_list:
                    found_toponyms.append(word)
                # Check for missing spacecharacter after Dutch place indicator "TE"
                elif word[2:] in toponyms_list:
                    found_toponyms.append(word[2:])

    print('Toponyms detected in output text: ', found_toponyms)
    print('-----------------------------------------------------------------')

    # Handles the Tombstone image file and the GPS coordinates
    txt_filename = sys.argv[1]
    jpg_filename = txt_filename.replace(".txt", ".jpg")
    print(jpg_filename)

    with open(jpg_filename, "rb") as file:
        gravestone = Image(file)

    print("\nGPS Data of image:")
    latitude_img = dms_coordinates_to_dd_coordinates(gravestone.gps_latitude, gravestone.gps_latitude_ref)
    print(latitude_img)
    longitude_img = dms_coordinates_to_dd_coordinates(gravestone.gps_longitude, gravestone.gps_longitude_ref)
    print(longitude_img)

    # Queries the GeoNames database and fills a list with the possible options
    # Calculates the minimum distance for disambiguation purposes
    toponym_details = []
    for toponym in found_toponyms:
        toponym = toponym.title()
        print('-----------------------------------------------------------------')
        print("\nToponym queried: ", toponym, "\n")
        g = geocoder.geonames(toponym, maxRows=25, featureClass='P', key='sebeyen')
        min_dist = 100000.0
        for result in g:
            print("Option in Geonames database: ", result.address, result.geonames_id)
            if result.address == toponym:
                id, lat, lng = result.geonames_id, float(result.lat), float(result.lng)
                dist = mpu.haversine_distance((latitude_img, longitude_img), (lat, lng))
                print("Exact match: ", "id: ", id, "distance: ", dist, "\n")
                if dist < min_dist:
                    min_dist = dist
                    min_dist_id = result.geonames_id
                    min_dist_add = result.address
                    min_dist_lat = result.lat
                    min_dist_lng = result.lng
                    min_dist_cou = result.country
        toponym_details.append([min_dist_id, min_dist_add, min_dist_cou, min_dist_lat, min_dist_lng])
    print("\nFound GeoNames identifiers: ")
    print(toponym_details)

    # Store the disambiguated GeoNames identifiers
    out_filename = txt_filename.replace(".txt", ".jpg")
    identifiers = [str(item[0]) for item in toponym_details]
    with open("Found_Toponyms.txt", "a") as file1:
        formatted_output = f"{out_filename} {identifiers}\n"
        file1.write(formatted_output)


if __name__ == "__main__":
    main()
