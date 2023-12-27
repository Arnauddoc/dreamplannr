const dates = document.querySelector(".dates");
const prevBtn = document.querySelector(".prevBtn");
const nextBtn = document.querySelector(".nextBtn");
const yearMonth = document.querySelector(".yearMonth");

let currentDate = new Date();
let calendar;

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 0);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay();
    const lastDayIndex = lastDay.getDay();

    const monthYearString = currentDate.toLocaleString("default",{month:"long", year:"numeric"});
    yearMonth.textContent = monthYearString;

    let datesHTML = '';
    for (let i = firstDayIndex; i > 0; i--) {
        const prevDate = new Date(currentYear, currentMonth, 0 - i + 1);
        datesHTML += `<div class="date inactive" data-date="${prevDate.toISOString()}">${prevDate.getDate()}</div>`;
    }

    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const activeClass = date.toDateString() === new Date().toDateString() ? 'active' : '';
        datesHTML += `<div class="date ${activeClass}" data-date="${date.toISOString()}">${i}</div>`;
    }

    for (let i = 1; i <= 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive" data-date="${nextDate.toISOString()}">${nextDate.getDate()}</div>`;
    }

    dates.innerHTML = datesHTML;
};

prevBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});

updateCalendar();

const addBox = document.querySelector(".addBox")

function show() {
    addBox.classList.add("show");
};

function hide() {
    addBox.classList.remove("show");
};

function hideEdit(itemId) {
    var editBox = document.querySelector('.editBox[data-task-id="' + itemId + '"]');
    editBox.classList.remove("show");
};

function showTooltip(title, description, jsEvent) {
    const tooltip = document.getElementById('event-tooltip');
    tooltip.innerHTML = `<strong>${title}</strong><br>${description}`;
    
    // Position the tooltip next to the mouse cursor
    tooltip.style.left = jsEvent.pageX + 'px';
    tooltip.style.top = jsEvent.pageY + 'px';

    tooltip.style.display = 'block';
}

function hideTooltip() {
    const tooltip = document.getElementById('event-tooltip');
    tooltip.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {

    function showEdit(itemId, title, description, start_date, end_date, start_time, end_time, showrepeat) {
        var allEditBoxes = document.querySelectorAll('.editBox');
        allEditBoxes.forEach(function(box) {
            box.classList.remove('show');
        });
    
        var editBox = document.querySelector('.editBox[data-task-id="' + itemId + '"]');
        if (editBox) {
            editBox.classList.add('show'); 
    
            editBox.querySelector('input[name="title"]').value = title;
            editBox.querySelector('input[name="start_date"]').value = start_date;
            editBox.querySelector('input[name="end_date"]').value = end_date;
            editBox.querySelector('input[name="start_time"]').value = start_time;
            editBox.querySelector('input[name="end_time"]').value = end_time;
            editBox.querySelector('textarea[name="description"]').value = description;
            editBox.querySelector('select[name="repeat"]').value = showrepeat;
            
        }
    };
            
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
    editable: false,
    initialView: 'timeGridWeek',
    initialDate: new Date(),
    headerToolbar: {
        left: 'prev',
        center: 'title',
        right: 'next'

    },
    events: 
    {
        url: '/get_events/',
        method: 'GET',
        success: function (data) {
            calendar.getEvents().forEach(function (event) {
                event.remove();
            });

            var events = data.map(function (event) {

                if (event.all_day){
                    return {
                        'title': event.title,
                        'start': new Date(event.start_date),
                        'allDay': true,
                        'actualId':event.id,
                        'description':event.description, 
                        'startdate1': event.start_date,
                        'enddate1': event.end_date,
                        'starttime1': event.start_time,
                        'endtime1': event.end_time,
                        'repeat1': event.repeat
                    };
                }
                else{
                    return{
                        'title': event.title,
                        'start': new Date(event.start_date + 'T' + event.start_time).toISOString(),
                        'end': new Date(event.end_date + 'T' + event.end_time).toISOString(),
                        'actualId':event.id,
                        'description':event.description, 
                        'startdate1': event.start_date,
                        'enddate1': event.end_date,
                        'starttime1': event.start_time,
                        'endtime1': event.end_time,
                        'repeat1': event.repeat
                    };
                }

            });
            calendar.addEventSource(events);
        },
    },
    eventMouseEnter: function(info) {
        const event_title = info.event._def.title;
        const event_description = info.event.extendedProps.description;
                
        if (event_description!=null) {
            showTooltip(event_title, event_description, info.jsEvent);
        }
    },

    eventMouseLeave: function() {
        // Hide tooltip on mouse leave
        hideTooltip();
    },
    
    eventClick: function(info) {
        const event_title = info.event._def.title;
        const itemId = info.event.extendedProps.actualId;
        const start = info.event.extendedProps.startdate1;
        const end = info.event.extendedProps.enddate1;
        const startt = info.event.extendedProps.starttime1;
        const endt = info.event.extendedProps.endtime1;
        const event_description = info.event.extendedProps.description;
        const erepeat = info.event.extendedProps.repeat1;

        showEdit(itemId, title=event_title, description=event_description, start_date=start, 
            end_date=end, start_time=startt, end_time=endt, showrepeat=erepeat)
      }
    });

    calendar.render();

    addEventListener("mouseenter", (event) => {
        alert("hey");
    });


    const todayBtn = document.querySelector(".todayButton");
    todayBtn.addEventListener("click", () => {
    const today = new Date(); // Get the current date
    currentDate.setMonth(today.getMonth()); // Set the month to the current month
    currentDate.setFullYear(today.getFullYear()); // Set the month to the current month
    currentDate.setDate(today.getDate()); // Set the date to the current date

    calendar.gotoDate( new Date() )
    updateCalendar();
    });

    dates.addEventListener("click", (event) => {
        const clickedDateElement = event.target.closest(".date");
        if (clickedDateElement) {
            const clickedDate = new Date(clickedDateElement.dataset.date);
            currentDate = new Date(clickedDate);
            calendar.gotoDate(clickedDate);
        }
    });
});

const checkbox = document.querySelector(".allDayBox");



