import re

base_form_part_with_pos_tag_regex = '[a-z0-9A-Z\/]+(:[a-z0-9]+)*$'
nkjp_pos_allowed_base_forms_regex = r"[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ\"\'!?.,;\-\s„”–()&*…—§’/ü\[\]+­“°%é=ôòéëä•ţ@‘ö×·$" \
                                    r"_{}«»~èàášíúČ#¨˝ý><ÉŢő−č|`řñç^âêōěßû]+(:[a-z0-9]+)*"
nkjp_base_form_first_emoji_regex = "^:[-]?[DOP\/]:"
nkjp_base_form_second_emoji_regex = "^[:(][-oP]?[\/()\\|\]:]?"
nkjp_websites_base_forms_first_regex = "\s*http://"
nkjp_websites_base_forms_second_regex = "news:"


def correct_nkjp_base_form_and_tag_format(base_form_with_tag):
    """
    Handles proper base_form and tag parsing from ann_morphosyntax.xml NKJP corpora files

    :param base_form_with_tag: str
        base_form and tag of NKJP corpora token divided with ':'
    :return: tuple (str, str)
        A tuple of two strings: (base_form, tag)
    """
    # if base_form_with_tag == ':D:subst:sg:nom:n':
    #     return ':D', 'subst:sg:nom:n'
    if re.findall(':$', base_form_with_tag):
        base_form_with_tag = base_form_with_tag[0:-1]
    if re.fullmatch(nkjp_pos_allowed_base_forms_regex, base_form_with_tag) is None:
        if base_form_with_tag == '::interp':
            return ':', 'interp'
        if re.findall(nkjp_base_form_first_emoji_regex, base_form_with_tag):
            tag = ":".join(re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group().split(':')[1:])
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if re.findall(nkjp_base_form_second_emoji_regex, base_form_with_tag):
            tag = re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group()
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if re.findall(nkjp_websites_base_forms_first_regex, base_form_with_tag) \
                or re.findall(nkjp_websites_base_forms_second_regex, base_form_with_tag):
            tag = ":".join(re.search(base_form_part_with_pos_tag_regex, base_form_with_tag).group().split(':')[1:])
            base_form = base_form_with_tag[0:len(base_form_with_tag) - len(tag) - 1]
            return base_form, tag
        if base_form_with_tag.startswith("E:") or base_form_with_tag.startswith("D:"):
            base_form = base_form_with_tag[0:2]
            tag = base_form_with_tag[3:]
            return base_form, tag
        if base_form_with_tag == '\\:interp':
            return '\\', 'interp'
        if base_form_with_tag == '´:interp':
            return '´', 'interp'
    else:
        base_form = base_form_with_tag.split(':')[0]
        tag = ":".join(base_form_with_tag.split(':')[1:])
        return base_form, tag

