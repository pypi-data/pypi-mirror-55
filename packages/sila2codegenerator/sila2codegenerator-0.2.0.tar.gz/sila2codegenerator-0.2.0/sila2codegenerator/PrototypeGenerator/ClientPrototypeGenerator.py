"""
________________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 Code Generator for using Packages*

:details: Class to generate client prototypes of a SiLA2 Client/Server

:file:    ClientPrototypeGenerator.py
:authors: Timm Severin (timm.severin@tum.de)

:date: (creation)          2019-06-21
:date: (last modification) 2019-09-16

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

# import general modules
import os

# import modules from this package
from ..service_descriptor_parser import ServiceDescriptorParser
from .PrototypeGenerator import PrototypeGenerator

# import packages from the SiLA2 library
from sila2lib.fdl_parser.fdl_parser import FDLParser

# meta information packages
from typing import Union, Dict


class ClientPrototypeGenerator(PrototypeGenerator):
    """TODO: Document"""
    fdl_parsers: Dict[str, FDLParser]

    def __init__(self,
                 service_description: Union[ServiceDescriptorParser, None] = None,
                 output_dir: Union[str, None] = None,
                 template_dir: Union[str, None] = None,
                 fdl_path: str = '.',
                 ignore_overwrite_warning: bool = False):
        """
        Class initialiser

        :param fdl_path: Path to where **all** FDL input files are stored

        .. note:: For parameter descriptions compare initialiser :meth:`.PrototypeGenerator.__init__`
        """

        super().__init__(
            service_description=service_description,
            output_dir=output_dir,
            template_dir=template_dir,
            ignore_overwrite_warning=ignore_overwrite_warning
        )

        # Generate FDLParser objects for all sila features registered
        self.fdl_parsers = {}
        for feature_id in self.service_dict['SiLA_feature_list']:
            fdl_filename = os.path.join(fdl_path, feature_id) + '.sila.xml'
            self.fdl_parsers[feature_id] = FDLParser(fdl_filename=fdl_filename)

    def _generate_command_calls(self) -> str:
        """
        Generate the command calls to all features

        :return: The code to call all features
        """

        code_command_calls = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            for identifier, command in self.fdl_parsers[feature_id].commands.items():
                # distinguish between the different command variants
                if command.observable and command.intermediates:
                    # observable and defined intermediates
                    template_file = 'command_observable_intermediate_call'
                elif command.observable and not command.intermediates:
                    # observable without any intermediates defined
                    template_file = 'command_observable_no-intermediate_call'
                else:
                    # unobservable
                    template_file = 'command_unobservable_call'

                code_command_calls += self.generate_from_template({
                        'feature_identifier': feature_id,
                        'command_id': identifier,
                        'command_name': command.name,
                        'command_description': command.description
                    },
                    input_template=template_file
                ) + "\n"

        code_command_calls = code_command_calls[:-1]

        return code_command_calls

    def _generate_property_calls(self):
        """
        Generate the code to retrieve all properties

        :return: The code to send property requests to the server
        """

        code_property_calls = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            for identifier, property_object in self.fdl_parsers[feature_id].properties.items():
                # distinguish between the different command variants
                if property_object.observable:
                    # observable and defined intermediates
                    template_file = 'property_observable_call'
                else:
                    # unobservable
                    template_file = 'property_unobservable_call'

                code_property_calls += self.generate_from_template({
                        'feature_identifier': feature_id,
                        'property_id': identifier,
                        'property_name': property_object.name,
                        'property_description': property_object.description,
                    },
                    input_template=template_file
                )

        if not code_property_calls:
            code_property_calls = "#   No properties defined"

        return code_property_calls

    def _generate_stub_creation(self) -> str:
        """
        Creates the code to initialise the sub objects for the client

        :return: The stub code
        """

        code_stub_creation = ""

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_stub_creation += self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template="stub_creation"
            ) + "\n"

        code_stub_creation = code_stub_creation[:-1]

        return code_stub_creation

    def _generate_grpc_imports(self) -> str:
        """
        Generate the code to import the gRPC modules for each feature

        :return: The import code
        """

        code_import = "# Import gRPC libraries of features"

        for feature_id in self.service_dict['SiLA_feature_list']:
            code_import += "\n" + self.generate_from_template({
                    'feature_identifier': feature_id
                },
                input_template='import_grpc'
            )

        return code_import

    def write_client_code(self, output_filename: Union[str, None] = None):
        """
        This method builds a server class from a template.
            The resulting file can be run as SiLA server for the implemented features.

        :param output_filename: filename for server output file
        """

        # configuration options
        template_filename = "sila_client"
        if output_filename is None:
            output_filename = '{service_name}_client.py'.format(
                service_name=str(self.service_dict['service_name'])
            )

        # initialise variables
        template_vars = {
        }

        self.write_from_template(template_vars,
                                 command_calls=self._generate_command_calls(),
                                 property_calls=self._generate_property_calls(),
                                 stub_creation=self._generate_stub_creation(),
                                 import_grpc_modules=self._generate_grpc_imports(),
                                 output_filename=output_filename,
                                 input_template=template_filename)
