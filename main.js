// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Initialize Binary Background
  initBinaryBackground()

  // Initialize Custom Cursor
  initCustomCursor()

  // Initialize Scroll Animations
  initScrollAnimations()

  // Initialize Theme Toggle
  initThemeToggle()

  // Initialize Mobile Menu
  initMobileMenu()

  // Initialize Handwritten Text Animation
  initHandwrittenText()

  // Initialize FAQ Accordion
  initFaqAccordion()

  // Initialize Testimonial Slider
  initTestimonialSlider()

  // Initialize Form Validation
  initFormValidation()
})

// Binary Background Animation
function initBinaryBackground() {
  const binaryBackground = document.querySelector(".binary-background")
  const characters = "01"
  const binaryCount = 100

  for (let i = 0; i < binaryCount; i++) {
    const binary = document.createElement("div")
    binary.classList.add("binary")

    // Random binary string
    let binaryString = ""
    const stringLength = Math.floor(Math.random() * 8) + 3

    for (let j = 0; j < stringLength; j++) {
      binaryString += characters.charAt(Math.floor(Math.random() * characters.length))
    }

    binary.textContent = binaryString

    // Random position and animation duration
    const left = Math.floor(Math.random() * 100)
    const size = Math.floor(Math.random() * 16) + 10
    const duration = Math.floor(Math.random() * 15) + 5
    const delay = Math.floor(Math.random() * 10)
    const opacity = Math.random() * 0.5 + 0.1

    binary.style.left = `${left}%`
    binary.style.fontSize = `${size}px`
    binary.style.animationDuration = `${duration}s`
    binary.style.animationDelay = `${delay}s`
    binary.style.opacity = opacity

    binaryBackground.appendChild(binary)
  }
}

// Custom Cursor
function initCustomCursor() {
  const cursor = document.querySelector(".cursor")

  document.addEventListener("mousemove", (e) => {
    cursor.style.left = e.clientX + "px"
    cursor.style.top = e.clientY + "px"
  })

  // Cursor effects on different elements
  const links = document.querySelectorAll("a, button, .faq-question, .course-card, .instructor-card")

  links.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      cursor.style.width = "40px"
      cursor.style.height = "40px"
      cursor.style.backgroundColor = "var(--accent-secondary)"
    })

    link.addEventListener("mouseleave", () => {
      cursor.style.width = "20px"
      cursor.style.height = "20px"
      cursor.style.backgroundColor = "var(--accent-primary)"
    })
  })

  // Hide cursor when it leaves the window
  document.addEventListener("mouseout", (e) => {
    if (e.relatedTarget === null) {
      cursor.style.opacity = "0"
    }
  })

  document.addEventListener("mouseover", () => {
    cursor.style.opacity = "0.7"
  })
}

// Scroll Animations
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll(
    ".about-card, .course-card, .feature, .instructor-card, .section-header, .about-text p, .contact-info, .contact-form",
  )

  // Add animation classes
  animatedElements.forEach((element, index) => {
    if (element.classList.contains("section-header")) {
      element.classList.add("fade-in-up")
    } else if (element.classList.contains("about-card") || element.classList.contains("feature")) {
      element.classList.add("scale-in")
      element.classList.add(`delay-${(index % 5) + 1}`)
    } else if (element.classList.contains("course-card") || element.classList.contains("instructor-card")) {
      element.classList.add("fade-in-up")
      element.classList.add(`delay-${(index % 5) + 1}`)
    } else if (element.classList.contains("about-text")) {
      element.classList.add("fade-in-up")
    } else if (element.classList.contains("contact-info")) {
      element.classList.add("fade-in-left")
    } else if (element.classList.contains("contact-form")) {
      element.classList.add("fade-in-right")
    }
  })

  // Intersection Observer for scroll animations
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate")
          observer.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.1,
    },
  )

  animatedElements.forEach((element) => {
    observer.observe(element)
  })
}

// Update the initThemeToggle function
function initThemeToggle() {
  const themeSwitch = document.getElementById("theme-switch")
  const body = document.body
  const toggleLabel = document.querySelector(".toggle-label")

  // Check for saved theme preference
  const savedTheme = localStorage.getItem("theme")

  if (savedTheme === "light") {
    body.classList.add("light-mode")
    themeSwitch.checked = true
  }

  themeSwitch.addEventListener("change", () => {
    if (themeSwitch.checked) {
      body.classList.add("light-mode")
      localStorage.setItem("theme", "light")

      // Add transition animation
      body.style.transition = "background-color 1s ease, color 1s ease"

      // Create a sun burst animation
      const burst = document.createElement("div")
      burst.classList.add("theme-burst")
      toggleLabel.appendChild(burst)

      setTimeout(() => {
        toggleLabel.removeChild(burst)
      }, 1000)
    } else {
      body.classList.remove("light-mode")
      localStorage.setItem("theme", "dark")

      // Add transition animation
      body.style.transition = "background-color 1s ease, color 1s ease"

      // Create a moon phase animation
      const phase = document.createElement("div")
      phase.classList.add("theme-phase")
      toggleLabel.appendChild(phase)

      setTimeout(() => {
        toggleLabel.removeChild(phase)
      }, 1000)
    }
  })
}

// Mobile Menu
function initMobileMenu() {
  const menuBtn = document.querySelector(".mobile-menu-btn")
  const mobileMenu = document.querySelector(".mobile-menu")
  const mobileLinks = document.querySelectorAll(".mobile-menu-link")
  const closeBtn = document.querySelector(".mobile-menu-close")

  menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("active")

    // Animate menu button
    const spans = menuBtn.querySelectorAll("span")

    if (mobileMenu.classList.contains("active")) {
      spans[0].style.transform = "rotate(45deg) translateY(6px)"
      spans[1].style.opacity = "0"
      spans[2].style.transform = "rotate(-45deg) translateY(-6px)"
      document.body.style.overflow = "hidden" // Prevent scrolling
    } else {
      spans[0].style.transform = "none"
      spans[1].style.opacity = "1"
      spans[2].style.transform = "none"
      document.body.style.overflow = "" // Allow scrolling
    }
  })

  // Close menu when clicking on the X button
  closeBtn.addEventListener("click", () => {
    mobileMenu.classList.remove("active")
    const spans = menuBtn.querySelectorAll("span")
    spans[0].style.transform = "none"
    spans[1].style.opacity = "1"
    spans[2].style.transform = "none"
    document.body.style.overflow = "" // Allow scrolling
  })

  // Close menu when clicking on a link
  mobileLinks.forEach((link) => {
    link.addEventListener("click", () => {
      mobileMenu.classList.remove("active")

      const spans = menuBtn.querySelectorAll("span")
      spans[0].style.transform = "none"
      spans[1].style.opacity = "1"
      spans[2].style.transform = "none"
      document.body.style.overflow = "" // Allow scrolling
    })
  })

  // Animate mobile menu circles
  const circles = document.querySelectorAll(".mobile-menu-circle")
  circles.forEach((circle, index) => {
    circle.style.animationDelay = `${index * 2}s`
  })
}

// Add a new function for the handwritten text animation
function initHandwrittenText() {
  const handwrittenRows = document.querySelectorAll(".handwritten-row")

  // Create letter spans for each row
  handwrittenRows.forEach((row) => {
    const text = row.textContent
    row.textContent = ""

    for (let i = 0; i < text.length; i++) {
      const letterSpan = document.createElement("span")
      letterSpan.classList.add("letter")
      letterSpan.textContent = text[i]
      row.appendChild(letterSpan)
    }
  })

  // Animate letters in sequence
  function animateLetters() {
    const allLetters = document.querySelectorAll(".letter")
    let currentIndex = 0

    function highlightNext() {
      // Remove highlight from all letters
      allLetters.forEach((letter) => letter.classList.remove("highlight"))

      // Add highlight to current letter
      if (currentIndex < allLetters.length) {
        allLetters[currentIndex].classList.add("highlight")
        currentIndex = (currentIndex + 1) % allLetters.length
      }

      setTimeout(highlightNext, 100)
    }

    highlightNext()
  }

  // Start animation after a short delay
  setTimeout(animateLetters, 1000)
}

// FAQ Accordion
function initFaqAccordion() {
  const faqItems = document.querySelectorAll(".faq-item")

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question")
    const toggle = item.querySelector(".faq-toggle")

    question.addEventListener("click", () => {
      // Close all other items
      faqItems.forEach((otherItem) => {
        if (otherItem !== item && otherItem.classList.contains("active")) {
          otherItem.classList.remove("active")
          otherItem.querySelector(".faq-toggle i").className = "fas fa-plus"
        }
      })

      // Toggle current item
      item.classList.toggle("active")

      if (item.classList.contains("active")) {
        toggle.innerHTML = '<i class="fas fa-minus"></i>'
      } else {
        toggle.innerHTML = '<i class="fas fa-plus"></i>'
      }
    })
  })
}

// Testimonial Slider
function initTestimonialSlider() {
  const testimonials = document.querySelectorAll(".testimonial")
  const dots = document.querySelectorAll(".dot")
  const prevBtn = document.querySelector(".prev-btn")
  const nextBtn = document.querySelector(".next-btn")
  let currentIndex = 0

  // Function to show testimonial by index
  function showTestimonial(index) {
    testimonials.forEach((testimonial) => {
      testimonial.classList.remove("active")
    })

    dots.forEach((dot) => {
      dot.classList.remove("active")
    })

    testimonials[index].classList.add("active")
    dots[index].classList.add("active")
    currentIndex = index
  }

  // Event listeners for dots
  dots.forEach((dot) => {
    dot.addEventListener("click", () => {
      const index = Number.parseInt(dot.getAttribute("data-index"))
      showTestimonial(index)
    })
  })

  // Event listeners for prev/next buttons
  prevBtn.addEventListener("click", () => {
    currentIndex = currentIndex === 0 ? testimonials.length - 1 : currentIndex - 1
    showTestimonial(currentIndex)
  })

  nextBtn.addEventListener("click", () => {
    currentIndex = currentIndex === testimonials.length - 1 ? 0 : currentIndex + 1
    showTestimonial(currentIndex)
  })

  // Auto slide
  let interval = setInterval(() => {
    currentIndex = currentIndex === testimonials.length - 1 ? 0 : currentIndex + 1
    showTestimonial(currentIndex)
  }, 5000)

  // Pause auto slide on hover
  const testimonialSlider = document.querySelector(".testimonial-slider")

  testimonialSlider.addEventListener("mouseenter", () => {
    clearInterval(interval)
  })

  testimonialSlider.addEventListener("mouseleave", () => {
    interval = setInterval(() => {
      currentIndex = currentIndex === testimonials.length - 1 ? 0 : currentIndex + 1
      showTestimonial(currentIndex)
    }, 5000)
  })
}

// Form Validation
function initFormValidation() {
  const form = document.getElementById("signup-form")

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault()

      // Get form inputs
      const name = document.getElementById("name")
      const email = document.getElementById("email")
      const phone = document.getElementById("phone")
      const course = document.getElementById("course")
      const message = document.getElementById("message")

      // Simple validation
      let isValid = true

      if (name.value.trim() === "") {
        showError(name, "Name is required")
        isValid = false
      } else {
        showSuccess(name)
      }

      if (email.value.trim() === "") {
        showError(email, "Email is required")
        isValid = false
      } else if (!isValidEmail(email.value)) {
        showError(email, "Email is not valid")
        isValid = false
      } else {
        showSuccess(email)
      }

      if (phone.value.trim() === "") {
        showError(phone, "Phone number is required")
        isValid = false
      } else {
        showSuccess(phone)
      }

      if (course.value === "") {
        showError(course, "Please select a course")
        isValid = false
      } else {
        showSuccess(course)
      }

      if (message.value.trim() === "") {
        showError(message, "Message is required")
        isValid = false
      } else {
        showSuccess(message)
      }

      // If form is valid, show success message
      if (isValid) {
        // Simulate form submission
        const submitBtn = form.querySelector(".submit-btn")
        const originalText = submitBtn.innerHTML

        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...'
        submitBtn.disabled = true

        setTimeout(() => {
          form.reset()
          submitBtn.innerHTML = originalText
          submitBtn.disabled = false

          // Show success message
          alert("Form submitted successfully! We will contact you soon.")
        }, 2000)
      }
    })
  }

  // Helper functions for form validation
  function showError(input, message) {
    const formGroup = input.parentElement.parentElement
    formGroup.classList.add("error")

    // Create error message if it doesn't exist
    let errorMessage = formGroup.querySelector(".error-message")

    if (!errorMessage) {
      errorMessage = document.createElement("div")
      errorMessage.className = "error-message"
      formGroup.appendChild(errorMessage)
    }

    errorMessage.textContent = message

    // Add shake animation to input
    input.style.animation = "shake 0.5s ease"
    setTimeout(() => {
      input.style.animation = ""
    }, 500)
  }

  function showSuccess(input) {
    const formGroup = input.parentElement.parentElement
    formGroup.classList.remove("error")

    // Remove error message if it exists
    const errorMessage = formGroup.querySelector(".error-message")
    if (errorMessage) {
      formGroup.removeChild(errorMessage)
    }
  }

  function isValidEmail(email) {
    const re =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return re.test(String(email).toLowerCase())
  }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()

    const target = document.querySelector(this.getAttribute("href"))

    if (target) {
      window.scrollTo({
        top: target.offsetTop - 80,
        behavior: "smooth",
      })
    }
  })
})

// Header scroll effect
window.addEventListener("scroll", () => {
  const header = document.querySelector("header")

  if (window.scrollY > 50) {
    header.style.padding = "10px 5%"
    header.style.boxShadow = "0 5px 20px rgba(0, 0, 0, 0.1)"
  } else {
    header.style.padding = "20px 5%"
    header.style.boxShadow = "none"
  }
})

// Add floating animation to some elements
const floatingElements = document.querySelectorAll(".about-card, .course-card")
floatingElements.forEach((element, index) => {
  element.classList.add("floating")
  element.style.animationDelay = `${index * 0.2}s`
})
