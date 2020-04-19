from scraps.scrapper import Scrapper
import os


class RoofStock:
    def __init__(self):
        self.properties_listing_page = "https://www.roofstock.com/investment-property-marketplace"
        self.name = "roofstock"
        self.scrapper_object = Scrapper(self.name)
        self.properties_data_json = []

    def scrap_properties(self):
        properties_soups = self.get_properties_soup_from_listing_page()

        for listing in properties_soups:
            image = self.get_property_image(listing)
            address, city, state, zipcode = self.get_property_address_info(listing)
            beds, bath = self.get_bed_bath(listing)
            year_built = self.get_build_year(listing)
            neighbourhood_rating = self.get_property_rating(listing)
            sqft = self.get_property_space(listing)
            open_house_price = self.get_property_value(listing)
            remarks = self.get_property_remarks(listing)
            is_duplex = self.is_duplex(listing)

            listing_json = {
                "address": address,
                "city": city,
                "state": state,
                "zipcode": zipcode,
                "property_image": image,
                "num-bedroom": beds,
                "num-bathroom": bath,
                "year-built": year_built,
                "open-house-price": open_house_price,
                "neighbourhood": neighbourhood_rating,
                "sqft": sqft,
                "property_remarks": remarks,
                "is_property_duplex": is_duplex
            }

            listing_json.update(self.get_additional_info_from_property_page(listing))

            self.properties_data_json.append(listing_json)

        self.scrapper_object.export_to_json(self.properties_data_json)
        self.scrapper_object.export_to_csv(self.properties_data_json)
        print("\r\n\n...............................\nScrapper ran successfully, Outputs in folder:",
              os.path.join(os.path.abspath(os.getcwd()), "outputs", self.name), sep='\n')

    def get_properties_soup_from_listing_page(self):
        property_block_class = "MuiGrid-root fivecolumns CardViewstyle__GridCardStyled-sc-1wti8ll-6 cNLVyp " \
                               "MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 " \
                               "MuiGrid-grid-lg-3"
        css_selector_for_page = "div.fivecolumns:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1)"
        properties_soups = self.scrapper_object.get_page_soup(self.properties_listing_page, css_selector_for_page)
        properties_soups = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            properties_soups,
            attribute_value=property_block_class
        )
        properties_soups = self.__clear_banners_from_properties(properties_soups)
        return properties_soups

    def __clear_banners_from_properties(self, properties_soups):
        banner_block_class = "MuiTypography-root MuiLink-root MuiLink-underlineHover MuiTypography-colorPrimary"
        new_properties = []
        for listing in properties_soups:
            if not self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
                    soup=listing,
                    tag="a",
                    attribute="class",
                    attribute_value=banner_block_class):
                new_properties.append(listing)
        return new_properties

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

    def get_property_address_info(self, listing):
        # 712 Saint Monica Dr, Cahokia, IL 62206
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
        address_line_1 = address_lines[0]
        address_line_2 = address_lines[2]

        address_line_1 = " ".join(map(str, address_line_1.split()))
        address_line_2 = " ".join(map(str, address_line_2.split()))

        line_2_list = address_line_2.split()
        zipcode = line_2_list[-1]
        state = line_2_list[-2]
        city = " ".join(map(str, line_2_list[:len(line_2_list)-2]))

        # Removing the comma from city
        city = city[:len(city)-1]

        full_address = address_line_1 + ", " + address_line_2

        return full_address, city, state, zipcode

    def get_bed_bath(self, listing):
        property_bed_bath_class = "RoofCard__BottomBarStyled-niegej-3 eMaDcd"

        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=property_bed_bath_class
        )
        bed_bath_string = element[0].contents[1]
        bed_bath_string = bed_bath_string.replace(',', '').replace('|', '')
        bed, bath = bed_bath_string.split()

        return float(bed[:len(bed) - 2]), float(bath[:len(bath) - 2])

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

    def get_additional_info_from_property_page(self, listing):
        property_page_link = "https://www.roofstock.com" + listing.find("a").attrs['href']
        return self.get_items_set_from_property_page(property_page_link)

    def get_items_set_from_property_page(self, property_page_link):

        css_selector_for_page = "div.ListingMediaViewer__MediaBlockStyled-sc-16guiwa-7:nth-child(2) > div:nth-child(" \
                                "1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > " \
                                "div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > " \
                                "img:nth-child(1) "
        class_name = "inline-block md NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        listing = self.scrapper_object.get_page_soup(property_page_link, css_selector_for_page)

        items = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            listing,
            "span",
            attribute_value=class_name
        )

        annualized_return = self.extract_float_from_percentage(str(items[5].contents[0]))
        cap_rate = self.extract_float_from_percentage(str(items[6].contents[0]))
        gross_yield = self.extract_float_from_percentage(str(items[7].contents[0]))
        cash_flow = self.extract_int_from_price(str(items[8].contents[0]))
        appreciation = self.extract_float_from_percentage(str(items[9].contents[0]))
        expected_rent = self.extract_int_from_price(str(items[10].contents[0]))
        expenses = self.extract_int_from_price(str(items[11].contents[0]))
        property_taxes = self.extract_int_from_price(str(items[12].contents[0]))
        loan_payments = self.extract_int_from_price(str(items[13].contents[0]))

        # Feature items
        hoa, lease_end, lease_start, lot_size, occupancy = self.get_feature_items_from_property_page(listing)

        initial_investment = self.get_initial_investment_from_property_page(listing)
        net_cash_flow = self.get_net_cash_flow_from_property_page(listing)
        flood_risk = self.get_flood_risk_from_property_page(listing)
        school = self.get_school_from_property_page(listing)

        return {
            "annualized-return": annualized_return,
            "cap-rate": cap_rate,
            "gross-yield": gross_yield,
            "appreciation": appreciation,
            "cash-flow": cash_flow,
            "expected-rent": expected_rent,
            "expenses": expenses,
            "property-taxes": property_taxes,
            "loan-payments": loan_payments,
            "initial_investment": initial_investment,
            "net-cash-flow": net_cash_flow,
            "occupancy": occupancy,
            "lease-start": lease_start,
            "lease-end": lease_end,
            "lot-size": lot_size,
            "hoa": hoa,
            "flood-risk": flood_risk,
            "school": school
        }

    def get_feature_items_from_property_page(self, listing):
        feature_class_name = "Featurestyle__LabelWithoutInfoStyled-zhjho0-9 iPcqHt"
        feature_items = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            listing,
            attribute_value=feature_class_name
        )

        feature_items_map = {}
        for item in feature_items:
            item_name = item.parent.contents[0].contents[0].contents[0]
            if str(item_name) == "Lot Size":
                feature_items_map[str(item_name)] = str(item.contents[0].contents[0])
            else:
                feature_items_map[str(item_name)] = str(item.contents[0])

        if "Occupancy" in feature_items_map:
            occupancy = feature_items_map["Occupancy"].lower() != "occupied"
        else:
            occupancy = None

        if "Lease Start" in feature_items_map:
            lease_start = feature_items_map["Lease Start"]
        else:
            lease_start = None

        if "Lease End" in feature_items_map:
            lease_end = feature_items_map["Lease End"]
        else:
            lease_end = None

        if "Lot Size" in feature_items_map:
            lot_size = self.extract_int_from_price(feature_items_map["Lot Size"])
        else:
            lot_size = None

        if "HOA" in feature_items_map:
            hoa = feature_items_map["HOA"] != "None"
        else:
            hoa = None

        return hoa, lease_end, lease_start, lot_size, occupancy

    def get_school_from_property_page(self, listing):
        school_class = "Featurestyle__IconInfoSecondLineStyled-zhjho0-17 kKSOfU"
        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            attribute_value=school_class
        )
        return str(element[1].contents[0])

    def get_flood_risk_from_property_page(self, listing):
        flood_risk_style = "margin: 0px; color: rgb(118, 118, 118); display: block;"
        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="p",
            attribute="style",
            attribute_value=flood_risk_style
        )
        return str(element[0].contents[0].contents[0])

    def get_initial_investment_from_property_page(self, listing):
        initial_investment_class = "block xl NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="span",
            attribute_value=initial_investment_class
        )

        initial_investment = element[0].contents[0]
        initial_investment = self.extract_int_from_price(initial_investment)

        return initial_investment

    def get_net_cash_flow_from_property_page(self, listing):
        net_cash_flow_class = "inline-block lg NumberFormatWithStyle__NumberFormatStyled-sc-1yvv7lw-0 cGlbYB"

        element = self.scrapper_object.find_all_tag_matches_by_attribute_from_soup(
            soup=listing,
            tag="span",
            attribute_value=net_cash_flow_class
        )

        net_cash_flow = element[0].contents[0]
        net_cash_flow = self.extract_int_from_price(net_cash_flow)

        return net_cash_flow

    @staticmethod
    def extract_float_from_percentage(str_per: str) -> float:
        str_per = str_per.replace('%', '')
        return round(float(str_per)/10, 2)

    @staticmethod
    def extract_int_from_price(str_price: str) -> int:
        str_price = str_price.replace('$', '').replace(',', '').replace('-', '')
        return int(str_price)
