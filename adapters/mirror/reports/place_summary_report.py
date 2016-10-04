def process_section(section, columns):
    columns.append({
        'type': 'section',
        'name': section['title'],
        'value': section['res']
    })
    for question in section['items']:
        columns.append({
            'type': question['inputType'] if question.get('inputType') else question['type'],
            'name': question['text'],
            'value': question.get('value'),
            'res': question.get('res'),
            'percent': str((question['res'] / question['weight']) * 100) + '%' if question.get('weight') else None
        })


def process_block(block, columns):
    columns.append({
        'type': 'block',
        'name': block['title'],
        'value': block['res']
    })
    for section in block['sections']:
        process_section(section, columns)


def process_examination(examination, questionnaire_dict, place_title, place_labels):
    questionnaire = questionnaire_dict[examination['id']]
    columns = []

    for block in questionnaire['content']['blocks']:
        process_block(block, columns)

    return {
        'id': examination['id'],
        'place': place_title,
        'place_labels': place_labels,
        'seller': questionnaire['seller'],
        'visit_date': questionnaire['visit_date'].isoformat() if questionnaire.get('visit_date') else '',
        'entry_time': questionnaire['entry_time'].isoformat() if questionnaire.get('entry_time') else '',
        'exit_time': questionnaire['exit_time'].isoformat() if questionnaire.get('exit_time') else '',
        'columns': columns,
        'res': questionnaire['content']['res']
    }


def build_place_report(project_examination_list, questionnaire_dict, place_title, place_labels):
    result = []

    for examination in project_examination_list:
        report = process_examination(examination, questionnaire_dict, place_title, place_labels)
        result.append(report)

    return result
