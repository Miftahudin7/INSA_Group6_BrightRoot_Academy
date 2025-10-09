import React, { useEffect } from "react";
import "./LandingPage.css";
import LandingHighlights from "./LandingHighlights";
import LandingFooter from "./LandingFooter"; 


const LandingPage = ({ onGetStarted }) => {
  // Add scroll animation
  useEffect(() => {
    const revealElements = document.querySelectorAll(".reveal");

    const revealOnScroll = () => {
      const windowHeight = window.innerHeight;
      revealElements.forEach((el) => {
        const elementTop = el.getBoundingClientRect().top;
        if (elementTop < windowHeight - 100) {
          el.classList.add("active");
        }
      });
    };

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll();

    return () => window.removeEventListener("scroll", revealOnScroll);
  }, []);

  return (
    <div className="landing-container">
      {/* Floating shapes */}
      <div className="floating-shapes">
        <span className="shape circle"></span>
        <span className="shape triangle"></span>
        <span className="shape square"></span>
        <span className="shape circle small"></span>
      </div>
      {/* Hero Section */}
      <section className="hero-section reveal">
        <div className="hero-overlay" /> {/* overlay should not block clicks */}
        <div className="hero-content">
          <h1 className="hero-title">
            Welcome to <span>BrightRoot Academy</span>
          </h1>
          <p className="hero-subtitle">
            Unlock your full potential with AI-powered personalized learning,
            interactive exercises, and progress tracking.
          </p>
          <div className="cta-buttons">
            <button
              className="btn-primary"
              onClick={() => onGetStarted && onGetStarted("register")}
            >
              Get Started
            </button>
            <button
              className="btn-secondary"
              onClick={() => onGetStarted && onGetStarted("login")}
            >
              Sign In
            </button>
          </div>
        </div>
      </section>

      {/* Highlights Section */}
      <div className="reveal">
        <LandingHighlights />
      </div>

      {/* Footer */}
      <LandingFooter onGetStarted={onGetStarted} />
    </div>
  );
};

export default LandingPage;
