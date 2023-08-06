

def get_base_attrs(field_name):
    attrs = {
        'data-formfield-stash': "true",
        'data-original-field': field_name,
    }
    return attrs


def get_single_stash_attrs(field_name):
    attrs = get_base_attrs(field_name)
    return attrs


def get_advanced_stash_attrs(field_name, stash_config):
    attrs = get_base_attrs(field_name)
    for choice, show_fields in stash_config.items():
        attrs['data-formfield-stash-%s' % choice] = (
            ','.join(show_fields)
        )
    return attrs
