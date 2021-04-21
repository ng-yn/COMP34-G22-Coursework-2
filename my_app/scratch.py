from flask import render_template



exists = Profile.query.filter(Profile.username == 'a').first
if exists:
    print('exist')
else:
    print('exist not')
