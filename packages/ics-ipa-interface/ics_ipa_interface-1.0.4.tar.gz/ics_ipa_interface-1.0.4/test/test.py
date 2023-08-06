import ics_ipa_interface as ipa

if __name__ == '__main__':
    # setup the help dialog for the script
    ipa.ipa_init(script_name='my_script_name.py', version='1.0',
                 message='this dose cool things')

    # input data path
    data_file_paths = ipa.get_data_files()
    if data_file_paths != ['path/to/data_file1', 'path/to/data_file2']:
        raise 'data files did not match'

    vehicle = ipa.get_attribute_from_file(data_file_paths[0], 'vehicleId')
    if not ipa.using_ipa_file() and vehicle is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and vehicle != 1234:
        raise 'did not read value properly'

    vehicle = ipa.get_attribute_from_file(data_file_paths[1], 'vehicleId')
    if not ipa.using_ipa_file() and vehicle is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and vehicle is not None:
        raise 'did not read value properly'


    # config are user defined and are uses as arguments to
    # the script
    config_file_paths = ipa.get_config_files()
    if config_file_paths != ['path/to/config1', 'path/to/config2']:
        raise 'config files did not match'

    name = ipa.get_attribute_from_file(config_file_paths[0], 'name')
    if not ipa.using_ipa_file() and name is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and name != "config1":
        raise 'did not read value properly'

    name = ipa.get_attribute_from_file(data_file_paths[1], 'name')
    if not ipa.using_ipa_file() and name is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and name is not None:
        raise 'did not read value properly'

    should_none = ipa.get_attribute_from_file(data_file_paths[1], 'none')
    if not ipa.using_ipa_file() and should_none is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and should_none is not None:
        raise 'did not read value properly'

    name = ipa.get_attribute_from_file("none", 'name')
    if not ipa.using_ipa_file() and name is not None:
        raise 'attributes only exist in a ipa file'

    if ipa.using_ipa_file() and name is not None:
        raise 'did not read value properly'

    # path to store data
    output_path = ipa.get_output_dir()
    if output_path != 'path/to/output_dir':
        raise 'output dir did not match'

    #path to store data
    previous_path = ipa.get_previous_dir()
    if previous_path != 'optional_path/to/previous_output_dir':
        raise 'previous dir did not match'
