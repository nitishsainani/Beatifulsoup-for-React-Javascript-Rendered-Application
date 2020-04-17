from scraps.scrapper import Scrapper
import os


class RoofStock:
    def __init__(self):
        self.url = "https://www.roofstock.com/investment-property-marketplace"
        self.property_block_class = "MuiGrid-root fivecolumns CardViewstyle__GridCardStyled-sc-1wti8ll-6 cNLVyp " \
                                    "MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 " \
                                    "MuiGrid-grid-lg-3"
        self.banner_block_class = "MuiTypography-root MuiLink-root MuiLink-underlineHover MuiTypography-colorPrimary"
        self.name = "roofstock"
        self.scrapper_object = Scrapper(self.url, self.name)
        self.scrapper_object.initialize()
        self.properties_soups = []
        self.properties_data_json = []

    def scrap_properties(self):
        self.properties_soups = self.scrapper_object.find_all_tag_matches_by_class(
            class_name=self.property_block_class
        )

        self.clear_banners_from_properties()

        for listing in self.properties_soups:
            image = self.get_property_image(listing)
            address = self.get_property_address(listing)
            beds, bath = self.get_bed_bath(listing)
            build_year = self.get_build_year(listing)
            neighbourhood_rating = self.get_property_rating(listing)
            space = self.get_property_space(listing)
            rent, cap_rate, total_return = self.get_rent_cap_return(listing)
            value = self.get_property_value(listing)
            remarks = self.get_property_remarks(listing)
            is_duplex = self.is_duplex(listing)

            listing_json = {
                "property_image": image,
                "property_address": address,
                "total_beds": beds,
                "total_bathrooms": bath,
                "property_build_year": build_year,
                "neighbourhood_rating": neighbourhood_rating,
                "property_area": space,
                "property_rent": rent,
                "cap_rate": cap_rate,
                "total_return_per_5_yr": total_return,
                "property_value": value,
                "property_remarks": remarks,
                "is_property_duplex": is_duplex
            }
            self.properties_data_json.append(listing_json)

        self.scrapper_object.export_to_json(self.properties_data_json)
        self.scrapper_object.export_to_csv(self.properties_data_json)
        print("Scrapper ran successfully, Outputs in folder:",
              os.path.join(os.path.abspath(os.getcwd()), "outputs", self.name), sep='\n')

    def clear_banners_from_properties(self):
        new_properties = []
        for listing in self.properties_soups:
            if not self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
                    soup=listing,
                    tag="a",
                    attribute="class",
                    attribute_value=self.banner_block_class):
                new_properties.append(listing)
        self.properties_soups = new_properties

    def is_duplex(self, listing):
        property_duplex_class = "RoofCard__TopBarStyled-niegej-2 iihfTu"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="span",
            attribute_value=property_duplex_class
        )
        if outside_element:
            return True
        else:
            return False

    def get_property_remarks(self, listing):
        property_remark_class = "MuiGridListTile-root CardViewstyle__GridListTileRightStyled-sc-1wti8ll-2 oURXk"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="li",
            attribute_value=property_remark_class
        )

        if not outside_element:
            return ""

        inside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[0],
            tag="span",
            attribute=None
        )

        if not inside_element:
            return ""

        return inside_element[0].contents[0]

    def get_property_address(self, listing):
        property_address_class = "MuiGridListTile-root CardViewstyle__GridListTileLeftStyled-sc-1wti8ll-1 ePjjbz"
        property_address_class_nested = "MuiTypography-root CardViewstyle__TypographyStyled-sc-1wti8ll-4 cZIqaQ " \
                                        "MuiTypography-subtitle1"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="li",
            attribute_value=property_address_class
        )

        if not outside_element:
            outside_element = [listing]

        inside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[0],
            tag="h6",
            attribute_value=property_address_class_nested
        )

        address_lines = inside_element[0].contents
        address_string = ""
        for line in address_lines:
            if str(line) != '<br/>':
                address_string += line + ", "

        return address_string[:len(address_string) - 1]

    def get_bed_bath(self, listing):
        property_bed_bath_class = "RoofCard__BottomBarStyled-niegej-3 eMaDcd"

        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=property_bed_bath_class
        )
        bed_bath_string = element[0].contents[1]
        bed_bath_string = bed_bath_string.replace(',', '').replace('|', '')
        bed, bath = bed_bath_string.split()

        return bed[:len(bed) - 2], bath[:len(bath) - 2]

    def get_build_year(self, listing):
        property_bed_bath_class = "RoofCard__BottomBarStyled-niegej-3 eMaDcd"

        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=property_bed_bath_class
        )

        return int(element[0].contents[-1].split("|")[1].split()[-1])

    def get_property_rating(self, listing):
        full_star_class = "dv-star-rating-star dv-star-rating-full-star"
        half_star_class = "svg-inline--fa fa-star-half fa-w-18 fa-sm"

        full_stars = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="label",
            attribute_value=full_star_class
        )

        half_star = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="svg",
            attribute_value=half_star_class
        )

        rating = len(full_stars)
        if half_star:
            rating += 0.5

        return rating

    def get_property_space(self, listing):
        property_space_class = "RoofCard__BottomBarStyled-niegej-3 eMaDcd"
        property_space_class_nested = "inline-block md NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=property_space_class
        )

        inside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[0],
            tag="span",
            attribute_value=property_space_class_nested
        )

        return inside_element[1].contents[0]

    def get_rent_cap_return(self, listing):
        property_info_class = "CardViewstyle__ValueStyled-sc-1wti8ll-3 cXixbv"
        property_info_class_nested = "inline-block md NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="span",
            attribute_value=property_info_class
        )

        rent_soup = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[0],
            tag="span",
            attribute_value=property_info_class_nested
        )

        cap_soup = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[1],
            tag="span",
            attribute_value=property_info_class_nested
        )

        return_soup = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[2],
            tag="span",
            attribute_value=property_info_class_nested
        )

        return rent_soup[0].contents[0], cap_soup[0].contents[0], return_soup[0].contents[0]

    def get_property_value(self, listing):
        property_price_class = "MuiTypography-root RoofCard__RoofCardNameStyled-niegej-7 fAYfRD MuiTypography-body1"
        property_price_class_nested = "inline-block md NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        outside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="p",
            attribute_value=property_price_class
        )

        inside_element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=outside_element[0],
            tag="span",
            attribute_value=property_price_class_nested
        )

        return inside_element[0].contents[0]

    def get_property_image(self, listing):
        property_image_class = "MuiCardMedia-root RoofCard__CardMediaStyled-niegej-1 cfpNCy"
        image = ""
        match = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=property_image_class
        )

        if len(match[0].attrs['style'].split('"')) > 1:
            return match[0].attrs['style'].split('"')[1]
        elif len(match[0].attrs['style'].split("'")) > 1:
            return match[0].attrs['style'].split("'")
        else:
            raise Exception("Could Not find the image in the soup")
