"""
Prototype code for the plugin loader
More design on how plugin code should be handled in shim needs to be done
"""

from optparse import OptionParser
import os

parser = OptionParser()


# option parsing logic, adds options for names and group information
def opt_init():
    parser.add_option('-d', '--dir_name', dest='dir_name',
                      type='string', help='Name of plugin folder to process')


def load_content_data(dir_name):
    lines = [line for line in open(os.path.join(dir_name, 'package'), 'r')]
    for line in lines:
        # this is hardcoded for now, this can change in the future.
        # Right now there isn't much to save in the package file
        if line.startswith('package_name'):
            return line.split(':')[-1].strip()


def remove_plugin_code(lines, start_dlist, end_dlist):
    dall = False
    for i in range(len(lines) - 1, -1, -1):
        if lines[i] in end_dlist:
            dall = False
        elif lines[i] in start_dlist:
            dall = True
        elif dall:
            lines.pop(i)


def add_plugin_code(lines, add_map, stop_list):
    add_s = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i] in add_map:
            add_s = add_map[lines[i]]
        elif lines[i] in stop_list:
            add_s = None
        if add_s is not None:
            lines.insert(i, add_s)


# this is not how it should look like in the end
# But for demonstration purposes I think it works just fine
def fill_metadata_loader(dir_name, package_name):
    fn = package_name + '_meta.py'

    with open(os.path.join(dir_name, 'metadata.py'), 'r') as c:
        contents = c.read()
        with open(os.path.join('plugins', fn), 'w') as f:
            f.write(contents)

    lines = [line for line in open('metadata.py', 'r')]
    start_dlist = set([
        '# END code-generated list of module imports\n',
        '        # END code-generated list of modules to call write_data\n'])
    end_dlist = set([
        '# BEGIN code-generated list of module imports\n',
        '        # BEGIN code-generated list of modules to call write_data\n'])

    remove_plugin_code(lines, start_dlist, end_dlist)
    ipn = package_name + '_meta'

    add_map = {
        '# END code-generated list of module imports\n': 'from plugins import %s\n' % (ipn),
        '        # END code-generated list of modules to call write_data\n': '        MODULES = [%s]\n' % (ipn),
    }
    stop_list = set(['# BEGIN code-generated list of module imports\n', '        # BEGIN code-generated list of modules to call write_data\n'])

    add_plugin_code(lines, add_map, stop_list)

    with open('metadata.py', 'w') as f:
        f.write(''.join(lines))


def fill_interaction_manager(dir_name, package_name):
    lines = [line for line in open('Backend/interaction_manager.py', 'r')]
    start_dlist = set([
        '# END PLUGIN DEFINED FUNCTIONS HERE\n',
        '    # END PLUGIN DEFINED REFERENCES HERE\n'])
    end_dlist = set([
        '# BEGIN PLUGIN DEFINED FUNCTIONS HERE\n',
        '    # BEGIN PLUGIN DEFINED REFERENCES HERE\n'])

    remove_plugin_code(lines, start_dlist, end_dlist)

    add_map = {
        '# END PLUGIN DEFINED FUNCTIONS HERE\n': open(os.path.join(dir_name, 'interaction.py'), 'r').read(),
        '    # END PLUGIN DEFINED REFERENCES HERE\n': open(os.path.join(dir_name, 'interaction_routes.py'), 'r').read(),
    }

    stop_list = set(['# BEGIN PLUGIN DEFINED FUNCTIONS HERE\n', '    # BEGIN PLUGIN DEFINED REFERENCES HERE\n'])

    add_plugin_code(lines, add_map, stop_list)

    with open('Backend/interaction_manager.py', 'w') as f:
        f.write(''.join(lines))


def fill_user_input(dir_name, package_name):
    lines = [line for line in open('Backend/user_input.py', 'r')]
    start_dlist = set([
        '    # END BEGIN PLUGIN DEFINED ROUTING FUNCITONS HERE\n',
        '        # END MODE CHANGE MAPPINGS HERE\n'])
    end_dlist = set([
        '    # BEGIN PLUGIN DEFINED ROUTING FUNCITONS HERE\n',
        '        # BEGIN MODE CHANGE MAPPINGS HERE\n'])

    remove_plugin_code(lines, start_dlist, end_dlist)

    dictstr =  "        mode_dict = { 'i': self.init_insert_mode, 'v': self.init_visual_mode, ':': self.init_ex_mode, %s }\n" % \
        (open(os.path.join(dir_name, 'user_input_routes.py')).read().strip())
    add_map = {
        '    # END BEGIN PLUGIN DEFINED ROUTING FUNCITONS HERE\n': open(os.path.join(dir_name, 'user_input.py'), 'r').read(),
        '        # END MODE CHANGE MAPPINGS HERE\n': dictstr
    }

    stop_list = set([
        '    # BEGIN PLUGIN DEFINED ROUTING FUNCITONS HERE\n',
        '        # BEGIN MODE CHANGE MAPPINGS HERE\n'])

    add_plugin_code(lines, add_map, stop_list)

    with open('Backend/user_input.py', 'w') as f:
        f.write(''.join(lines))


def load_plugin(dir_name):
    package_name = load_content_data(dir_name)
    fill_metadata_loader(dir_name, package_name)
    fill_interaction_manager(dir_name, package_name)
    fill_user_input(dir_name, package_name)
