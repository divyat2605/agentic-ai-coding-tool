// Function to send a reminder notification
function sendNotification(task, dueDate) {
  console.log(`Reminder: Task '${task}' is due on ${dueDate}`);
}

// Function to schedule a reminder notification
function scheduleNotification(task, dueDate) {
  const scheduledDate = new Date(dueDate);
  const currentTime = new Date();
  if (scheduledDate >= currentTime) {
    sendNotification(task, dueDate);
  }
}
