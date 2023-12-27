const wrapper = document.querySelector(".wrapper");
const loginLink = document.querySelector(".loginLink");
const registerLink = document.querySelector(".registerLink");
const toDoBox = document.querySelector(".toDoBox")
const editBox = document.querySelector(".edit")

function formatDate(dateString) {
    var date = new Date(dateString);
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
}

registerLink.addEventListener("click", () => {
    wrapper.classList.add("active");
    //const isActive = wrapper.classList.contains('active');
});

loginLink.addEventListener("click", () => {
    wrapper.classList.remove("active");
});

function show() {
    toDoBox.classList.add("show");
};

function hide() {
    toDoBox.classList.remove("show");
};

function showEdit(itemId, title, content, end_date) {
    var allEditBoxes = document.querySelectorAll('.todoBox.edit');
    allEditBoxes.forEach(function(box) {
        box.classList.remove('show');
    });

    var editBox = document.querySelector('.toDoBox.edit[data-todo-id="' + itemId + '"]');
    if (editBox) {
        editBox.classList.add('show'); 
        
        var formattedEndDate = formatDate(end_date);

        editBox.querySelector('input[name="title"]').value = title;
        editBox.querySelector('textarea[name="description"]').value = content;
        editBox.querySelector('input[name="end_date"]').value = formattedEndDate;
    }
};

function hideEdit(itemId) {
    var editBox = document.querySelector('.toDoBox.edit[data-todo-id="' + itemId + '"]');
    editBox.classList.remove("show");
};

const togglePasswordBtn = document.getElementById('togglePasswordBtn');
togglePasswordBtn.addEventListener('click', function(event) {
    const eyeIcon = togglePasswordBtn.querySelector('.eyeIcon');
    const passwordField = document.querySelector('.passwordField');

        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            eyeIcon.setAttribute('name', 'eye-off');
        } else {
            passwordField.type = 'password';
            eyeIcon.setAttribute('name', 'eye');
        }
});
