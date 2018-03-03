from django.db import models

from bs4 import BeautifulSoup

import requests

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255)

    code = models.CharField(max_length=10)

    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def crawl_worlds():
        r = requests.get("https://developers.google.com/public-data/docs/canonical/countries_csv")

        data = r.text

        soup = BeautifulSoup(data, 'html.parser')

        countries = list(soup.find("table").findChildren("tr"))

        row_length = len(countries)

        for country in range(0, row_length):
            country_info = countries[country].findChildren("td")

            if len(country_info) == 4:

                code = country_info[0].getText()
                latitude = country_info[1].getText()
                longitude = country_info[2].getText()
                name = country_info[3].getText()

                Country.objects.create(code=code, latitude=latitude, longitude=longitude, name=name)

                print(f"{name} saved successfully")

        # row_length = len(list(all_rows))
        #
        # for x in range(0, row_length):
        #     if len(list(all_rows[x].findChildren("td"))) > 1:  # If the row has two td's
        #
        #         sci_block = list(all_rows[x].findChildren("td"))[0].findChildren("a")
        #         if len(sci_block) > 0:  # If the scientific name has an anchor tag in it
        #             sci_name = sci_block[0].get_text()  # Get the entire scientific name, em's and all
        #
        #         common_name = all_rows[x].findChildren("td")[1].get_text()
        #         usda_code = all_rows[x].findChildren("th")
        #         if len(usda_code) > 0:
        #             code = usda_code[0].get_text()
        #
        #         # If there is a scientific name, and a common name
        #         if common_name != '' and len(sci_name) > 0:
        #             try:
        #                 Plant.objects.create(scientific_name=sci_name, botanical_name=common_name, usda_code=code)
        #             except Exception as e:
        #                 pass

        return True