# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


@auth.requires_membership('editors')
def create():
    try:
        if request.args[0] == 'lesson':
            form = SQLFORM(db.lesson, request.args[1]).process()
        elif request.args[0] == 'practice':
            form = SQLFORM(db.practice, request.args[1]).process()
        else:
            redirect(URL('default', 'index'))
    except:
        if request.args[0] == 'lesson':
            form = SQLFORM(db.lesson).process()
        elif request.args[0] == 'practice':
            form = SQLFORM(db.practice).process()

    if form.accepted:
        response.flash = T("Published")
    elif form.errors:
        response.flash = T("Some errors were found.")

    return dict(form=form)


def learn():
    if request.args[0].lower() == 'c':
        message = 'C/C++'
    else:
        message = request.args[0].upper()

    # This line fills the left side table with the topics.
    rows = db(db.lesson.codelanguage == message).select(orderby=db.lesson.topic)

    # This gets the data from the lesson
    try:
        lesson = db(db.lesson.id == int(request.args[1])).select().first()
    except:
        lesson = False

    return dict(message=T('Learn ' + message), rows=rows, lesson=lesson)


def practice():
    if request.args[0].lower() == 'c':
        message = 'C/C++'
    else:
        message = request.args[0].upper()

    # This line fills the left side table with the topics.
    rows = db(db.practice.codelanguage == message).select(orderby=db.practice.topic)

    # This gets the data from the lesson
    try:
        practice = db(db.practice.id == int(request.args[1])).select().first()
    except:
        practice = False

    # print practice.answer
    return dict(message=T('Practice ' + message), rows=rows, practice=practice)


def savetobookmarks():
    if not auth.is_logged_in():
        m = T("You must be looged in to save.")
    else:
        try:
            if request.vars['type'] == 'learn':
                learn = db((db.bookmark.thingtype == '0') & (db.bookmark.thingid == int(request.vars['id'])) & (db.bookmark.created_by == auth.user.id)).select().first()
                if not learn:
                    db.bookmark.insert(thingtype="0", thingid=int(request.vars['id']))
            else:
                practice = db((db.bookmark.thingtype == '1') & (db.bookmark.thingid == int(request.vars['id'])) & (db.bookmark.created_by == auth.user.id)).select().first()
                if not practice:
                    db.bookmark.insert(thingtype="1", thingid=int(request.vars['id']))

            m = T('Saved to your bookmarks')
        except:
            m = T('Not saved.')

    response.flash = m
    return True

@auth.requires_login()
def deletebookmarks():
    db((db.bookmark.id == request.args[0]) & (db.bookmark.created_by == auth.user.id)).delete()
    redirect(URL('default', 'bookmarks'))
    return True


@auth.requires_login()
def bookmarks():
    try:
        learn = []
        rows = db((db.bookmark.thingtype == 0) & (db.bookmark.created_by == auth.user.id)).select(orderby=db.bookmark.id)

        for row in rows:
            x = db(db.lesson.id == int(row.thingid)).select().first()
            if x.codelanguage == 'C/C++':
                langlink = 'c'
            else:
                langlink = x.codelanguage

            learn.append([x.codelanguage, x.topic, langlink, str(x.id), str(row.id)])
    except:
        learn = False

    try:
        practice = []
        rows = db((db.bookmark.thingtype == 1) & (db.bookmark.created_by == auth.user.id)).select(orderby=db.bookmark.id)

        for row in rows:
            x = db(db.practice.id == row.thingid).select().first()

            if x.codelanguage == 'C/C++':
                langlink = 'c'
            else:
                langlink = x.codelanguage

            practice.append([x.codelanguage, x.title, langlink, str(x.id), str(row.id)])
    except:
        practice = False

    return dict(learn=learn, practice=practice)


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
