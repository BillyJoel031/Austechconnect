jQuery(document).ready(function ($) {
  let projects = null;
  let $result = $('#result');
  let $searchForm = $('#search_form');

  function renderPersons(persons, clear = true) {
    if (clear) {
      $result.empty();
    }
    if (Array.isArray(persons) && persons.length) {
      for (let person of persons) {
        console.log(person.about.length);
        if (person.about.length > 500) {
          var about = person.about;
          var short_about = about.substring(0, 500);
          person.about = `${short_about} ...`;
        }
        $result.append($(`
          <div class="person" id="${person.id}">
            <a href="/profile/${person.pk}"><h2>${person.name}</h2></a>
            <h3>${person.category}</h3>
            <p>${person.location}</p>
            <span class="summary">${person.about}</span>
          </div><p>___________________________________________________________________</p><br/>`));
      }
    } else {
      $result.append('<div><h2>No result found</h2></div>')
    }
  }

  function renderProjects(projects, clear = true) {
    if (clear) {
      $result.empty();
    }
    if (Array.isArray(projects) && projects.length) {
      for (let project of projects) {
        $result.append($(`
          <div class="company" id="${project.id}">
            <h2>${project.name}</h2>
            <h3><i>By ${project.creator}</i></h3>
            <h3>${project.category}</h3>
            <p>${project.location}</p>
            <span class="summary">${project.short_description}</span>
          </div><br/>`));
      }
    } else {
      $result.append('<div><h2>No result found</h2></div>')
    }
  }

  // click event when click a job
  $('div').on('click', '.company', function () {
    let _id = $(this).attr('id');
    let p = projects.find(p => p.id === _id
      )
    ;
    $("#detail").empty()
      .append($(p.description))
      .append($('<input type="button" id="apply-btn" value="Apply" class="apply-btn">').on("click", function () {
        $("input[name='position_id']").val(_id);
        $(".background-container").show();
      }));
    $("#close").show();
  });
  // click event on close button
  $("#close").on("click", function () {
    $("#detail").empty();
    $("input[name='position_id']").val("");
    $(this).hide();
  });
  // click event on apply form close button
  $("#apply-close").on("click", function () {
    $(".background-container").hide();
  });
  // events on apply form
  $("#apply_form").on("submit", function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "/apply",
      data: $("#apply_form").serialize()
    }).done(function (result) {
      document.getElementById("apply_form").reset();
      alert(`Count: ${result.count}\nMessage: ${result.message}`);
      $("#apply-close").trigger("click");
    });
  });

  // search by words ( title,etc.)
  $searchForm.on("submit", function (event) {
    event.preventDefault();
    var category = $searchForm.find('#categorySelect').find(':selected').attr('value');
    var url = $searchForm.attr('target');
    $.ajax({
      type: "GET",
      url: url,
      data: {
        q: $searchForm.find('input[name="keywords"]').val(),
        location: $searchForm.find('input[name="location"]').val(),
        category: category ? category : ''
      }
    }).done(function (result) {
      console.log(result);
      var projects = result['projects'];
      var persons = result['persons'];
      // renderProjects(projects);
      renderPersons(persons)
    });
  });

  // // get 10 latest position
  // $.ajax({
  //     url: "/search",
  //     data: {
  //         q: "",
  //     }
  // }).done(function (result) {
  //     positions = result;
  //     console.log(positions[0]);
  //     console.log(positions);
  //     renderPosition(positions);
  // });

  $(function () {
    // Time function to get the date/time
    function time() {
      // Create new date var and init other vars
      var date = new Date(),
        hours = date.getHours(), // Get the hours
        minutes = date.getMinutes().toString(), // Get minutes, convert to string
        ante, // Will be used for AM and PM later
        greeting, // Set the appropriate greeting for the time of day
        dd = date.getDate().toString(), // Get the current day
        userName = "User"; // Can be used to insert a unique name
      /* Set the AM or PM according to the time, it is important to note that up
          to this point in the code this is a 24 clock */
      if (hours < 12) {
        ante = "AM";
        greeting = "Morning";
      } else if (hours === 12 && hours >= 3) {
        ante = "PM";
        greeting = "Afternoon"
      } else {
        ante = "PM";
        greeting = "Evening";
      }
      /* Since it is a 24 hour clock, 0 represents 12am, if that is the case
      then convert that to 12 */
      if (hours === 0) {
        hours = 12;/* For any other case where hours is not equal to twelve, let's use modulus
			             to get the corresponding time equivilant */
      } else if (hours !== 12) {
        hours = hours % 12;
      }
      // Minutes can be in single digits, hence let's add a 0 when the length is less than two
      if (minutes.length < 2) {
        minutes = "0" + minutes;
      }
      // Do the same thing above for the day
      if (dd.length < 2) {
        dd = "0" + dd;
      }
      // Months
      Date.prototype.monthNames = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
      ];
      // Days
      Date.prototype.weekNames = [
        "Sunday", "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"
      ];
      // Return the month name according to its number value
      Date.prototype.getMonthName = function () {
        return this.monthNames[this.getMonth()];
      };
      // Return the day's name according to its number value
      Date.prototype.getWeekName = function () {
        return this.weekNames[this.getDay()];
      };
      // Display the following in html
      $("#time").html(hours + ":" + minutes + " " + ante);
      $("#day").html(date.getWeekName() + ", " + date.getMonthName() + " " + dd);
      $("#greeting").html("Good " + greeting + "!!! ");
      // The interval is necessary for proper time syncing
      setInterval(time, 1000);
    }

    time();
  });
});

