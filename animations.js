// Additional Animations
document.addEventListener("DOMContentLoaded", () => {
  // Add shimmer effect to headings
  const headings = document.querySelectorAll("h1, h2")
  headings.forEach((heading) => {
    if (!heading.classList.contains("glitch")) {
      heading.classList.add("shimmer")
    }
  })

  // Add hover animations to social links
  const socialLinks = document.querySelectorAll(".social-links a")
  socialLinks.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      link.style.transform = "translateY(-5px) rotate(10deg)"
    })

    link.addEventListener("mouseleave", () => {
      link.style.transform = "translateY(0) rotate(0)"
    })
  })

  // Add particle effect to hero section
  initParticles()

  // Add 3D tilt effect to cards
  init3DTilt()

  // Update handwritten text content
  updateHandwrittenText()
})

// Dummy function for initHandwrittenText to prevent errors.
// Replace this with the actual implementation if available.
function initHandwrittenText() {
  // Placeholder implementation
  console.warn("initHandwrittenText() is not fully implemented.")
}

// Update handwritten text content
function updateHandwrittenText() {
  const handwrittenRows = document.querySelectorAll(".handwritten-row")
  const newText = "IT Creative Code Academy"

  handwrittenRows.forEach((row) => {
    row.textContent = `${newText} ${newText}`
  })

  // Re-initialize the handwritten text animation
  initHandwrittenText()
}

// Particle Effect
function initParticles() {
  const heroSection = document.querySelector(".hero")

  // Create canvas for particles
  const canvas = document.createElement("canvas")
  canvas.classList.add("particles-canvas")
  canvas.style.position = "absolute"
  canvas.style.top = "0"
  canvas.style.left = "0"
  canvas.style.width = "100%"
  canvas.style.height = "100%"
  canvas.style.pointerEvents = "none"
  canvas.style.zIndex = "1"

  heroSection.appendChild(canvas)

  const ctx = canvas.getContext("2d")

  // Set canvas size
  function resizeCanvas() {
    canvas.width = heroSection.offsetWidth
    canvas.height = heroSection.offsetHeight
  }

  resizeCanvas()
  window.addEventListener("resize", resizeCanvas)

  // Particle class
  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width
      this.y = Math.random() * canvas.height
      this.size = Math.random() * 3 + 1
      this.speedX = Math.random() * 2 - 1
      this.speedY = Math.random() * 2 - 1
      this.color = getComputedStyle(document.documentElement).getPropertyValue("--accent-primary")
    }

    update() {
      this.x += this.speedX
      this.y += this.speedY

      if (this.size > 0.2) this.size -= 0.01

      // Bounce off edges
      if (this.x < 0 || this.x > canvas.width) this.speedX *= -1
      if (this.y < 0 || this.y > canvas.height) this.speedY *= -1
    }

    draw() {
      ctx.fillStyle = this.color
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
      ctx.fill()
    }
  }

  // Create particles
  const particles = []
  const particleCount = 50

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle())
  }

  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    for (let i = 0; i < particles.length; i++) {
      particles[i].update()
      particles[i].draw()

      // Connect particles with lines
      for (let j = i; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const distance = Math.sqrt(dx * dx + dy * dy)

        if (distance < 100) {
          ctx.beginPath()
          ctx.strokeStyle = `rgba(0, 204, 255, ${0.2 - distance / 500})`
          ctx.lineWidth = 0.5
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.stroke()
        }
      }

      // Replace particles that are too small
      if (particles[i].size <= 0.2) {
        particles[i] = new Particle()
      }
    }

    requestAnimationFrame(animate)
  }

  animate()
}

// 3D Tilt Effect
function init3DTilt() {
  const cards = document.querySelectorAll(".course-card, .instructor-card, .about-card, .feature")

  cards.forEach((card) => {
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      const centerX = rect.width / 2
      const centerY = rect.height / 2

      const angleX = (y - centerY) / 20
      const angleY = (centerX - x) / 20

      card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) scale3d(1.05, 1.05, 1.05)`
      card.style.boxShadow = `
                ${angleY * -1}px ${angleX}px 20px rgba(0, 0, 0, 0.2),
                0 10px 30px rgba(0, 0, 0, 0.3)
            `
    })

    card.addEventListener("mouseleave", () => {
      card.style.transform = "perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)"
      card.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.1)"
    })
  })
}
