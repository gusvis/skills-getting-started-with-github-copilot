document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const cancelActivitySelect = document.getElementById("cancel-activity");
  const signupForm = document.getElementById("signup-form");
  const cancelForm = document.getElementById("cancel-form");
  const messageDiv = document.getElementById("message");
  const cancelMessageDiv = document.getElementById("cancel-message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left (${details.participants.length}/${details.max_participants})</p>
          <button class="view-participants-btn" data-activity="${name}">View Participants</button>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdowns
        const signupOption = document.createElement("option");
        signupOption.value = name;
        signupOption.textContent = name;
        activitySelect.appendChild(signupOption);

        const cancelOption = document.createElement("option");
        cancelOption.value = name;
        cancelOption.textContent = name;
        cancelActivitySelect.appendChild(cancelOption);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Handle cancel form submission
  cancelForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("cancel-email").value;
    const activity = document.getElementById("cancel-activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/cancel?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        cancelMessageDiv.textContent = result.message;
        cancelMessageDiv.className = "success";
        cancelForm.reset();
        fetchActivities(); // Refresh the activities list
      } else {
        cancelMessageDiv.textContent = result.detail || "An error occurred";
        cancelMessageDiv.className = "error";
      }

      cancelMessageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        cancelMessageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      cancelMessageDiv.textContent = "Failed to cancel registration. Please try again.";
      cancelMessageDiv.className = "error";
      cancelMessageDiv.classList.remove("hidden");
      console.error("Error cancelling registration:", error);
    }
  });

  // Handle view participants button clicks
  document.addEventListener("click", async (event) => {
    if (event.target.classList.contains("view-participants-btn")) {
      const activityName = event.target.getAttribute("data-activity");
      
      try {
        const response = await fetch(`/activities/${encodeURIComponent(activityName)}/participants`);
        const result = await response.json();
        
        if (response.ok) {
          const participantsList = result.participants.length > 0 
            ? result.participants.join(", ") 
            : "No participants yet";
            
          alert(`${activityName} Participants:\n\n${participantsList}\n\nTotal: ${result.total_participants}/${result.total_participants + result.available_spots}`);
        } else {
          alert("Failed to load participants");
        }
      } catch (error) {
        alert("Error loading participants");
        console.error("Error fetching participants:", error);
      }
    }
  });

  // Initialize app
  fetchActivities();
});
