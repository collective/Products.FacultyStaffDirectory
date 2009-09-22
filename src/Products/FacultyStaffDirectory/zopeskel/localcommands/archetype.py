"""
Local templates for the archetype zopeskel project
"""
import os
from zopeskel.base import var
from zopeskel.localcommands.archetype import ArchetypeSubTemplate
from paste.script import pluginlib

class FSDExtender(ArchetypeSubTemplate):
    """
    A FacultyStaffDirectory Extender Skeleton
    """
    _template_dir = 'templates/archetype/fsdextender'
    summary = "An Extender for the Faculty/Staff Directory Product"
    
    ATFieldTypes = ('BooleanField',
                    'ComputedField',
                    'CMFObjectField',
                    'DateTimeField',
                    'FileField',
                    'FixedPointField',
                    'FloatField',
                    'ImageField',
                    'IntegerField',
                    'LinesField',
                    'ReferenceField',
                    'StringField',
                    'TextField')
    
    vars = [
        var('extendertype_name', 'Name of the Extender ', default='MobilePhone'),
        var('interface_to_extend', 'Interface to extend (person.IPerson, committee.ICommittee, etc.) ', default='person.IPerson'),
        ]
        
    def pre(self, command, output_dir, vars):
        
        extendertype_canonical_name = vars['extendertype_name'].replace(" ","")
        vars['extendertype_classname'] = extendertype_canonical_name + 'Extender'
        vars['extender_class_filename'] = extendertype_canonical_name.lower()
        vars['interface_name'] = 'I' + extendertype_canonical_name
        vars['adapter_classname'] = extendertype_canonical_name + 'Adapter'
        vars['at_field_types'] = self.ATFieldTypes
        
    def post(self, command, output_dir, vars):
        """ Do some post-processing to insert to multiple points in a single template
        """
        insert_string = "                        'archetypes.schemaextender < 2.0',\n" + \
            "                        'Products.FacultyStaffDirectory < 3.0',\n"
        command.insert_into_file(os.path.join(os.path.dirname(pluginlib.find_egg_info_dir(os.getcwd())), 'setup.py'),
                'Extra requirements:',
                insert_string)

        insert_string = "from %s.extenders.%s import %s\n" % (vars['package_dotted_name'], 
                                                              vars['extender_class_filename'], 
                                                              vars['extendertype_classname'])
        command.insert_into_file(os.path.join(command.dest_dir(), 'setuphandlers.py'), 
                                 'additional extender class imports here', 
                                 insert_string)
        
        extender_registration_name = vars['package_dotted_name'] + '.' + vars['extender_class_filename']
        install_string = "    installExtender(portal, %s, \"%s\")\n" % (vars['extendertype_classname'],
                                                                        extender_registration_name)
        command.insert_into_file(os.path.join(command.dest_dir(), 'setuphandlers.py'), 
                                 'install additional extender classes here', 
                                 install_string)
                                 
        uninstall_string = "    uninstallExtender(portal, %s, \"%s\")\n" % (vars['extendertype_classname'],
                                                                            extender_registration_name)
        command.insert_into_file(os.path.join(command.dest_dir(), 'setuphandlers.py'), 
                                 'uninstall additional extender classes here', 
                                 uninstall_string)


