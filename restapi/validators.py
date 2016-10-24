from django.core.exceptions import ValidationError

ROBOT_FIELD_TYPES = ['option', 'badgood', 'number']

def robot_field_validator(value):
    if not isinstance(value, list):
        raise ValidationError("Array of values required")
    names = []
    for i in value:
        if not i.get("name"):
            raise ValidationError("{} requires a name field".format(i))
        if not i.get("type"):
            raise ValidationError("{} requires a type field".format(i))
        if i.get("type") not in ROBOT_FIELD_TYPES:
            raise ValidationError("{} type must be one of {}".format(i, ', '.join(ROBOT_FIELD_TYPES)))
        if i.get("type") == "option" and not isinstance(i.get("options"), list):
            raise ValidationError("{} requires an array of options".format(i))
        names.append(i.get("name"))
    if len(set(names)) != len(names):
        raise ValidationError("{} are not all unique".format(names))

# TODO: validator for robot properties
