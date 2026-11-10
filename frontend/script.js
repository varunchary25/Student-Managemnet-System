// Django API URLs
const API_BASE_URL = "https://student-managemnet-system-eehf.onrender.com";

const API_URL = `${API_BASE_URL}/api/students/`;
const CREATE_URL = `${API_BASE_URL}/api/students/create/`;

// HTML Elements
const studentForm = document.getElementById("studentForm");
const studentList = document.getElementById("studentList");
const message = document.getElementById("message");
const refreshButton = document.getElementById("refreshButton");


// Common response handler
async function handleResponse(response) {
    const text = await response.text();

    let data = {};

    try {
        data = text ? JSON.parse(text) : {};
    } catch {
        data = { detail: text };
    }

    if (!response.ok) {
        throw new Error(
            data.detail ||
            data.error ||
            JSON.stringify(data) ||
            `HTTP Error: ${response.status}`
        );
    }

    return data;
}


// GET: Fetch all students
async function getStudents() {

    studentList.textContent = "Loading students...";

    try {
        const response = await fetch(API_URL);

        const students = await handleResponse(response);

        displayStudents(students);

    } catch (error) {

        studentList.textContent = "Unable to load students: " + error.message;

        console.error("GET Error:", error);
    }
}


// Display students
function displayStudents(students) {

    studentList.replaceChildren();

    if (!Array.isArray(students) || students.length === 0) {
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

        const course = document.createElement("p");
        course.textContent = "Course: " + student.course;

        const age = document.createElement("p");
        age.textContent = "Age: " + student.age;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", () => {
            deleteStudent(student.id);
        });

        card.append(
            name,
            roll,
            email,
            course,
            age,
            deleteButton
        );

        studentList.appendChild(card);
    });
}


// POST: Register student
studentForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    message.textContent = "Registering student...";
    message.style.color = "blue";

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

        const data = await handleResponse(response);

        message.textContent = "Student registered successfully!";
        message.style.color = "green";

        studentForm.reset();

        await getStudents();

    } catch(error) {

        message.textContent = "Registration failed: " + error.message;

        message.style.color = "red";

        console.error("POST Error:", error);
    }

});


// DELETE: Delete student
async function deleteStudent(studentId) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}${studentId}/delete/`,
            {
                method: "DELETE"
            }
        );

        await handleResponse(response);

        message.textContent = "Student deleted successfully!";
        message.style.color = "green";

        await getStudents();

    } catch(error) {

        message.textContent = "Delete failed: " + error.message;

        message.style.color = "red";

        console.error("DELETE Error:", error);
    }
}


// Refresh button
refreshButton.addEventListener("click", getStudents);


// Load students on page opening
getStudents();