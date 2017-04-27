#
# Collective Knowledge ()
#
# 
# 
#
# Developer: Michel Steuwer <michel.steuwer@ed.ac.uk>
#

cfg = {}  # Will be updated by CK (meta description of this module)
work = {}  # Will be updated by CK (temporal data)
ck = None  # Will be updated by CK (initialized CK kernel)


# Local settings

##############################################################################
# Initialize module


def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return': 0}


def get_settings_file(i):
    import os
    output_path = ck.access(
        {'action': 'find',
         'module_uoa': i['module_uoa'],
         'data_uoa': i['data_uoa']})['path']

    return os.path.join(output_path, "cachedSettings.json")

##############################################################################
# run a lift benchmark

def run(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    import json
    import os
    import subprocess
    import re
    import datetime

    ck.out(json.dumps(i))

    ck.out('Run the ' + i["data_uoa"] + ' lift benchmark at '
           + str(datetime.datetime.now()) + '\n')

    settings_file = get_settings_file(i)

    if not os.path.isfile(settings_file):
        prepare(i)

    if not os.path.isfile(settings_file):
        ck.out("benchmark preparation failed")
        return {'return': -1}

    with open(settings_file) as file:
        settings = json.load(file)

    java_options = settings.get("java_options", "")
    classpath = settings.get("classpath", "")
    lift_home = settings['lift_home']

    ck.out("Using Lift home: " + lift_home + '\n')

    os.chdir(lift_home)

    meta = ck.access({
            'action': 'load',
            'module_uoa': i["module_uoa"],
            'data_uoa': i["data_uoa"]})

    command = "java "
    command += meta["dict"].get("java_options", "")
    command += java_options
    command += " -cp " + classpath
    command += " " + meta["dict"]["main_class"]
    command += " " + i.get("args", "")

    output = subprocess.check_output(command, shell=True).decode()

    ck.out("\n" + output)

    if i.get("record", "no") == "yes":
        return record_output(i, meta, output)

    return {'return': 0}


def record_output(i, meta, output):
    record_repo = i.get("record_repo", "local")
    record_uoa = i.get("record_uoa", "")
    if record_uoa == "":
        ck.out("record_uoa required but not provided")
        return {'return': 1}

    post_processing_script = i.get("post_processing_script", "")
    if post_processing_script != "":
        ck.out("TODO: Call custom post processing script")
        d = {}
    else:
        d = parse_output(output)

    # TODO: make tags work, because currently they totally don't ...
    # Maybe have to ask Grigori about this.
    tags = meta["dict"]["tags"]
    t = i.get('tags', '')
    if t != '':
        tags += ',' + t

    r = ck.access({
        'action': 'add',
        'module_uoa': 'experiment',
        'experiment_uoa': record_uoa,
        'experiment_repo_uoa': record_repo,
        'dict': d,
        'tags': tags})
    if r['return'] > 0:
        return r

    point = r['point']
    sub_point = str(r['sub_point']).zfill(4)

    r = ck.access({
        'action': 'find',
        'module_uoa': 'experiment',
        'data_uoa': r['recorded_uid']})
    if r['return'] > 0:
        return r

    file_name = 'ckp-' + point + '.' + sub_point

    import os
    json_file_name = os.path.join(r['path'], file_name + '.json')
    log_file_name = os.path.join(r['path'], file_name + '.log')

    with open(log_file_name, 'w') as file:
        file.write(output)

    ck.out("Saved parsed json file at " + json_file_name)
    ck.out("Saved log file at " + log_file_name)

    return {'return': 0}


def parse_output(output):
    import re
    import json

    c = {}
    cs = []
    for line in output.splitlines():

        match = re.search("Benchmark: (.*)", line)
        if match:
            c = {"benchmark": match.group(1)}
            cs.append(c)

        match = re.search("MEDIAN: (.*) ms", line)
        if match:
            c["median"] = match.group(1)

    return {"characteristics_list": cs}

##############################################################################
# Prepare a lift benchmark

def prepare(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    import json
    import os
    import subprocess
    import re

    ck.out('Prepare the ' + i["data_uoa"] + ' lift benchmark')

    settings_file = get_settings_file(i)

    if os.path.isfile(settings_file):
        ck.out("Cached settings file already exist at " + settings_file)
        return {'return': 0}

    lift_home = os.environ.get('LIFT_HOME', "")
    if lift_home == "":
        lift_home = ck.access({
            'action': 'find',
            'module_uoa': 'repo',
            'data_uoa': 'ck-lift'})['path']

    ck.out("Using Lift home: " + lift_home)

    os.chdir(lift_home)

    def remove_colour_codes(string):
        rgx = re.compile('\\x1b\[[0-9;]*m')
        return rgx.sub('', string)

    ck.out('')
    ck.out("Obtaining class path via sbt")
    output = remove_colour_codes(subprocess.check_output(["sbt", "show runtime:fullClasspath"]).decode())
    classpath = ':'.join(re.compile("Attributed\(([^\)]*)\)").findall(output))
    ck.out(classpath)

    ck.out('')
    ck.out("Obtain java options via sbt")
    output = remove_colour_codes(subprocess.check_output(["sbt", "show javaOptions"]).decode())
    java_options = ' '.join(re.compile("\[info\] \* (.*)").findall(output))
    ck.out(java_options)

    ck.out('')
    ck.out("Writing cached setting to settings file at " + settings_file)
    json_output = {
        'classpath': classpath,
        'java_options': java_options,
        'lift_home': lift_home
    }
    with open(settings_file, 'w') as file:
        json.dump(json_output, file)

    return {'return': 0}
