// Terminal Animation
document.addEventListener("DOMContentLoaded", () => {
  const terminalText = document.getElementById("terminal-text")
  const terminalOutput = document.getElementById("terminal-output")

  // Terminal commands and responses
  const commands = [
    {
      text: "whoami",
      response: "student@itcreative",
    },
    {
      text: "ls -la courses/",
      response: `
total 6
drwxr-xr-x  2 admin admin 4096 Apr 15 10:30 .
drwxr-xr-x 10 admin admin 4096 Apr 15 10:30 ..
-rw-r--r--  1 admin admin  512 Apr 15 10:30 html-css.md
-rw-r--r--  1 admin admin  768 Apr 15 10:30 javascript.md
-rw-r--r--  1 admin admin  640 Apr 15 10:30 python.md
-rw-r--r--  1 admin admin  704 Apr 15 10:30 react.md
-rw-r--r--  1 admin admin  592 Apr 15 10:30 sql.md
-rw-r--r--  1 admin admin  688 Apr 15 10:30 nodejs.md
`,
    },
    {
      text: "cat python_example.py",
      response: `<pre style="color: #00ff9d; margin: 0; font-family: 'Roboto Mono', monospace; font-size: 14px; line-height: 1.5;">
# Python Example: Simple Data Analysis
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate sample data
np.random.seed(42)
x = np.random.rand(100, 1)
y = 3 * x + np.random.randn(100, 1) * 0.2

# Create and train a model
model = LinearRegression()
model.fit(x, y)

# Make predictions
y_pred = model.predict(x)

# Calculate accuracy
r_squared = model.score(x, y)
print(f"Model accuracy (R²): {r_squared:.4f}")
</pre>`,
    },
    {
      text: "python -c \"print('Hello from IT Creative Code Academy!')\"",
      response: "Hello from IT Creative Code Academy!",
    },
    {
      text: './enroll.sh --course="python-data-science" --start="now"',
      response: `
Initializing enrollment process...
Checking available seats... OK
Reserving your spot... OK
Preparing welcome materials... OK

✅ Enrollment successful! Welcome to IT Creative Code Academy!
Your journey to becoming a developer starts now.
`,
    },
  ]

  let commandIndex = 0
  let charIndex = 0
  let currentCommand = commands[commandIndex]

  // Type command character by character
  function typeCommand() {
    if (charIndex < currentCommand.text.length) {
      terminalText.textContent += currentCommand.text.charAt(charIndex)
      charIndex++
      setTimeout(typeCommand, 100)
    } else {
      // Wait before showing response
      setTimeout(showResponse, 500)
    }
  }

  // Show command response
  function showResponse() {
    // Create response element
    const responseElement = document.createElement("div")
    responseElement.classList.add("response")
    responseElement.innerHTML = currentCommand.response
    terminalOutput.appendChild(responseElement)

    // Scroll to bottom of terminal
    const terminalBody = document.querySelector(".terminal-body")
    terminalBody.scrollTop = terminalBody.scrollHeight

    // Clear command and move to next
    setTimeout(() => {
      terminalText.textContent = ""
      charIndex = 0
      commandIndex = (commandIndex + 1) % commands.length
      currentCommand = commands[commandIndex]

      // Type next command
      setTimeout(typeCommand, 1000)
    }, 2000)
  }

  // Start typing first command
  setTimeout(typeCommand, 1000)
})
