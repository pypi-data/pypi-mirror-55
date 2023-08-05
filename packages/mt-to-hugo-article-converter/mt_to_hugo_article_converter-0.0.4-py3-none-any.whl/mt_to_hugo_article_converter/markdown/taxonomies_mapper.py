class TaxonomiesMapper:
    def map_each_value(self, acceptable_values_map, src_attr_values):
        values = []
        for key in acceptable_values_map:
            acceptable_values = [key]
            acceptable_values += acceptable_values_map[key]
            for v in src_attr_values:
                if v.lower() in acceptable_values:
                    values.append(key)
        result = sorted(list(set(values)))
        return result

    def map_each_attr(self, attr_map, src_attr_name, src_attr_values):
        acceptable_attr_names = list(
            map(lambda attr_name: attr_name.lower(), attr_map["from"]))
        if not src_attr_name.lower() in acceptable_attr_names:
            return []

        acceptable_values = attr_map["values"]
        values = self.map_each_value(acceptable_values, src_attr_values)
        return values

    def map(self, config, src_attr_name, src_attr_values):
        mapped_taxonomies = {}
        attribute_map = config.get_attribute_map()
        for attr in attribute_map:
            mapped_taxonomies[attr] = self.map_each_attr(
                attribute_map[attr], src_attr_name, src_attr_values)
        return mapped_taxonomies
