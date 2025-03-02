async function loadStudents() {
    const response = await fetch("/students");
    const students = await response.json();
    const tbody = document.getElementById("students-list");
    tbody.innerHTML = "";

    students.forEach(student => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${student.name}</td>
            <td><input type="number" id="mark-${student.id}" min="1" max="5"></td>
            <td><button onclick="submitMark(${student.id})">Отправить</button></td>
        `;
        tbody.appendChild(row);
    });
}

async function submitMark(studentId) {
    const input = document.getElementById(`mark-${studentId}`);
    const mark = input.value;
    if (!mark) return alert("Введите оценку!");

    const response = await fetch(`/students/${studentId}/mark`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mark: parseInt(mark) })
    });

    if (response.ok) {
        alert("Оценка сохранена!");
        input.value = "";
    } else {
        alert("Ошибка при сохранении оценки.");
    }
}

loadStudents();
