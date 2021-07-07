from flask import render_template, current_app as app

"""
CREATE - POST
READ - GET
UPDATE - PUT
DELETE - DELETE
"""

@app.route("/profile")
def profile():
    logged_in_user = "Evan"
    return render_template('profile.html', u=logged_in_user)





