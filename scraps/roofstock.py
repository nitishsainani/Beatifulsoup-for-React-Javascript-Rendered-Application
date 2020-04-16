from scraps.scrapper import Scrapper


class RoofStock:
    def __init__(self):
        self.url = "https://www.roofstock.com/investment-property-marketplace"
        self.property_block_class = "MuiGrid-root fivecolumns CardViewstyle__GridCardStyled-sc-1wti8ll-6 cNLVyp " \
                                    "MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 " \
                                    "MuiGrid-grid-lg-3"
        self.banner_block_class = "MuiTypography-root MuiLink-root MuiLink-underlineHover MuiTypography-colorPrimary"

        self.scrapper_object = Scrapper(self.url)
        self.scrapper_object.initialize()
        self.properties = []

    def scrap_properties(self):
        self.properties = self.scrapper_object.find_all_tag_matches_by_class(
            class_name=self.property_block_class
        )

        self.clear_banners_from_properties()

        for listing in self.properties:
            print(listing)

    def clear_banners_from_properties(self):
        new_properties = []
        for listing in self.properties:
            if not self.scrapper_object.find_all_tag_matches_by_class_from_soup(
                    soup=listing, tag="a", class_name=self.banner_block_class):
                new_properties.append(listing)
        self.properties = new_properties
