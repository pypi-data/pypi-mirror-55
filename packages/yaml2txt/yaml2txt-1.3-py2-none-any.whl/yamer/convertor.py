import yaml


class Yaml_convertor(object):
    """This class is used to create a .txt file out of a .yaml file"""
    def __init__(self, source_yaml_file, name_for_the_new_text_file="from_yaml_file"):
        """"""
        self._file = source_yaml_file
        self.name_for_the_new_text_file = name_for_the_new_text_file
        self._raw_data = self._read_file()
        self._get_full_string()
        self.filter = "true"


    def _read_file(self):
        """read the .yaml file and convert it to a python dictionary"""
        with open(self._file) as f:
            return yaml.safe_load(f)

    def _write_to_file(self, data):
        """create and write new .txt file"""
        with open(self.name_for_the_new_text_file, "a+") as file:
            file.write(data)
            file.write("\n")

    def _get_full_string(self):
        """produce a new .txt file out of the .yaml file
           only the values of the .yaml file will be appended to the .txt file
        """
        new_list = []
        for k, v in self._raw_data.items():
            temp_list = [i for i in v]

            for item in temp_list:
                new_list.append(item)

        for d in new_list:

            for key, value in d.items():
                new_temp_dict = value
                new_temp_list = list()
                new_temp_list.append(new_temp_dict.values())

                for i in new_temp_list:
                    temp_str = str()
                    temp_l = list(i)

                    for item in temp_l:
                        if "true" in str(item):
                            item = str(item).replace("true", "")

                            temp_str += "{0}".format(item)

                        temp_str += "{0}".format(item)

                    self._write_to_file(temp_str)
                    print(temp_str)


