db.define_table(
    'lesson',
    Field('codelanguage', 'text', label='Language', requires=IS_IN_SET(["C/C++", "C#", "Python"])),
    Field('topic', 'string', requires=IS_NOT_EMPTY()),
    Field('description', 'text', requires=IS_NOT_EMPTY()),
    auth.signature
)


db.define_table(
    'practice',
    Field('codelanguage', 'text', label='Language', requires=IS_IN_SET(["C/C++", "C#", "Python"])),
    Field('difficulty', 'integer', requires=IS_IN_SET([1, 2, 3, 4, 5])),
    Field('topic', 'string', requires=IS_NOT_EMPTY()),
    Field('title', 'string', requires=IS_NOT_EMPTY()),
    Field('prerequisites', 'text'),
    Field('description', 'text', requires=IS_NOT_EMPTY()),
    Field('answer', 'text', requires=IS_NOT_EMPTY()),
    auth.signature
)

db.define_table(
    'bookmark',
    Field('thingid', 'integer'),
    Field('thingtype', 'boolean'),
    auth.signature
)

db.lesson.description.widget = advanced_editor

db.practice.prerequisites.widget = advanced_editor
db.practice.description.widget = advanced_editor
db.practice.answer.widget = advanced_editor