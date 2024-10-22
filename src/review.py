import json
import subprocess

import automatic_code_review_commons as commons


def review(config):
    path_source = config['path_source']
    changes = config['merge']['changes']

    comments = []
    message_no_constructor = config['messageNoConstructor']
    message_constructor_no_delete = config['messageConstructorNoDelete']
    message_constructor_no_public = config['messageConstructorNoPublic']

    for change in changes:
        new_path = change['new_path']
        path = path_source + "/" + new_path

        if not path.endswith('.h'):
            continue

        comments.extend(__review_by_file(
            path=path,
            message_no_constructor=message_no_constructor,
            message_constructor_no_delete=message_constructor_no_delete,
            message_constructor_no_public=message_constructor_no_public,
            new_path=new_path
        ))

    return comments


def __review_by_file(
        path,
        message_no_constructor,
        message_constructor_no_delete,
        message_constructor_no_public,
        new_path
):
    data = subprocess.run(
        'ctags -R --output-format=json --languages=c++ --fields=+an --c++-kinds=+p ' + path,
        shell=True,
        capture_output=True,
        text=True,
    ).stdout

    has_method = False
    only_static_method = True
    constructor_method = None

    for data_obj in data.split('\n'):
        if data_obj == '':
            continue

        obj = json.loads(data_obj)

        if obj['kind'] != 'prototype':
            continue

        if obj.get('scope', "") == obj['name']:
            constructor_method = obj
            continue

        has_method = True

        if "static" not in obj['pattern']:
            only_static_method = False
            break

    if not has_method or not only_static_method:
        return []

    if constructor_method is None:
        description_comment = message_no_constructor
        description_comment = description_comment.replace("${FILE_PATH}", new_path)

        return [
            commons.comment_create(
                comment_id=commons.comment_generate_id(description_comment),
                comment_path=new_path,
                comment_description=description_comment,
            )
        ]

    if '= delete' not in constructor_method['pattern']:
        line_number = constructor_method['line']

        description_comment = message_constructor_no_delete
        description_comment = description_comment.replace("${FILE_PATH}", new_path)
        description_comment = description_comment.replace("${LINE_NUMBER}", str(line_number))

        return [
            commons.comment_create(
                comment_id=commons.comment_generate_id(description_comment),
                comment_path=new_path,
                comment_description=description_comment,
                comment_snipset=True,
                comment_end_line=line_number,
                comment_start_line=line_number,
                comment_language='c++',
            )
        ]

    if constructor_method['access'] != 'public':
        line_number = constructor_method['line']

        description_comment = message_constructor_no_public
        description_comment = description_comment.replace("${FILE_PATH}", new_path)
        description_comment = description_comment.replace("${LINE_NUMBER}", str(line_number))

        return [
            commons.comment_create(
                comment_id=commons.comment_generate_id(description_comment),
                comment_path=new_path,
                comment_description=description_comment,
                comment_snipset=True,
                comment_end_line=line_number,
                comment_start_line=line_number,
                comment_language='c++',
            )
        ]

    return []
