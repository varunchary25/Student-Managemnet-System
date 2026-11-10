// Django API URLs



const API_BASE_URL = "https://student-managemnet-system-eehf.onrender.com";

const API_URL = "http://127.0.0.1:8000/api/students/";

const CREATE_URL = "http://127.0.0.1:8000/api/students/create/";


// Get HTML elements

const studentForm = document.getElementById("studentForm");

const studentList = document.getElementById("studentList");

const message = document.getElementById("message");

const refreshButton = document.getElementById("refreshButton");


// GET: Load all students from Django

async function getStudents() {

    studentList.textContent = "Loading students...";

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Unable to fetch student records");
        }

        const students = await response.json();

        displayStudents(students);

    }

    catch (error) {

        studentList.textContent = error.message;

        console.error(error);

    }

}


// Display student records

function displayStudents(students) {

    studentList.replaceChildren();

    if (students.length === 0) {

        studentList.textContent = "No students registered yet.";

        return;

    }

    students.forEach(student => {

        const card = document.createElement("div");

        card.className = "student-card";

        const name = document.createElement("h3");
        name.textContent = student.name;

        const roll = document.createElement("p");
        roll.textContent = "Roll Number: " + student.roll_number;

        const email = document.createElement("p");
        email.textContent = "Email: " + student.email;

        const department = document.createElement("p");
        department.textContent = "Department: " + student.department;

        const age = document.createElement("p");
        age.textContent = "Age: " + student.age;

        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", function () {

            deleteStudent(student.id);

        });

        card.append(
            name,
            roll,
            email,
            department,
            age,
            deleteButton
        );

        studentList.appendChild(card);

    });

}


// POST: Register a student

studentForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const student = {

        name: document.getElementById("name").value.trim(),

        roll_number: document.getElementById("roll_number").value.trim(),

        email: document.getElementById("email").value.trim(),

        course: document.getElementById("course").value.trim(),

        age: Number(document.getElementById("age").value)

    };

    try {

        const response = await fetch(CREATE_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(student)

        });

        const data = await response.json();

        if (!response.ok) {

            throw new Error(JSON.stringify(data));

        }

        message.textContent = "Student registered successfully!";

        message.style.color = "green";

        studentForm.reset();

        getStudents();

    }

    catch (error) {

        message.textContent = "Registration failed: " + error.message;

        message.style.color = "red";

        console.error(error);

    }

});


// DELETE: Remove a student

async function deleteStudent(studentId) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this student?"
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const response = await fetch(
            API_URL + studentId + "/delete/",
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(data.error || "Unable to delete student");

        }

        message.textContent = "Student deleted successfully!";

        message.style.color = "green";

        getStudents();

    }

    catch (error) {

        message.textContent = error.message;

        message.style.color = "red";

        console.error(error);

    }

}


// Refresh button

refreshButton.addEventListener("click", getStudents);


// Load students when the webpage opens

getStudents();