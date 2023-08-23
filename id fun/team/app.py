from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user and admin credentials (for demonstration purposes)
credentials = {
    "user": "0880",
    "admin": "adminpassword"
}
students_data = []
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in credentials and credentials[username] == password:
            if username == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("student"))
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin_students.html", students=students_data)
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        student_name = request.form.get("student_name")
        student_age = request.form.get("student_age")
        gender=request.form.get("gender")
        mail=request.form.get("mail")
        phone_number=request.form.get("phone_number")
        student_course = request.form.get("student_course")
        student ={
            "name": student_name,
            "age": student_age,
            "gender": gender,
            "mail": mail,
            "phone_number": phone_number,
            "course": student_course,
            "avatar_filename": "male_avatar.png" if gender == "male" else "female_avatar.png"
        }
        students_data.append(student)
        return redirect(url_for("student_details"))

    return render_template("student.html",)
@app.route("/student_details")
def student_details():
    student = students_data[-1]
    avatar_filename = "male_avatar.png" if student.get("gender", "") == "male" else "female_avatar.png"
    return render_template("student_details.html", student=student, avatar_filename=avatar_filename)
# ... (your existing imports)

@app.route("/edit_student/<int:index>", methods=["GET", "POST"])
def edit_student(index):
    if request.method == "POST":
        # Update the student details based on the form data
        student = students_data[index]
        student["name"] = request.form.get("edited_name")
        student["age"] = request.form.get("edited_age")
        student["gender"] = request.form.get("edited_gender")
        student["mail"] = request.form.get("edited_mail")
        student["phone_number"] = request.form.get("edited_phone_number")
        student["course"] = request.form.get("edited_course")

        return redirect(url_for("admin"))

    student = students_data[index]
    return render_template("edit_student.html", student=student, index=index)

@app.route("/delete_student/<int:index>", methods=["POST"])
def delete_student(index):
    del students_data[index]
    return redirect(url_for("admin"))

# ... (your existing routes)

if __name__ == "__main__":
    app.run(debug=True)
