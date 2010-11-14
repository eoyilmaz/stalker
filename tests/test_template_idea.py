
from jinja2 import Template

# old structure
template = Template('{{project.name}}/{{sequence.name}}/{{asset_base.type.name}}/{{shot.code}}/{{shot.code}}_{{shot.sub_name}}_{{shot.type.name}}_{{task.code}}_{{version.revision}}_{{version.version}}_{{user.code}}.extension')
template = Template('{{project.name}}/{{sequence.name}}/{{shot.type.name}}/{{shot.code}}/{{shot.code}}_{{shot.sub_name}}_{{shot.type.name}}_{{task.code}}_{{version.revision}}_{{version.version}}_{{user.code}}.extension')


# new structure
template = Template('{{project.name}}/SEQS/{{sequence.name}}/SHOTS/{{shot.code}}/{{shot.code}}_{{shot.sub_name}}_{{shot.type.name}}_{{task.code}}_{{version.revision}}_{{version.version}}_{{user.code}}.extension')
