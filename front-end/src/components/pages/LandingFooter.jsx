import React from "react";
import "./LandingFooter.css";

const LandingFooter = ({ onGetStarted }) => {
  return (
    <footer className="landing-footer">
      <div className="footer-content">
        {/* Left Section */}
        <div className="footer-left">
          <h3>BrightRoot Academy</h3>
          <p>Empowering students to achieve academic excellence worldwide.</p>
          <div className="footer-cta">
            <button
              className="btn-footer-primary"
              onClick={() => onGetStarted("register")}
            >
              Sign Up
            </button>
            <button
              className="btn-footer-secondary"
              onClick={() => onGetStarted("login")}
            >
              Sign In
            </button>
          </div>
        </div>

        {/* Center Section: Contact Info */}
        <div className="footer-center">
          <h4>Contact Us</h4>
          <ul className="contact-info">
            <li>
              <i className="bi bi-envelope-fill"></i>
              <span>support@brightroot.com</span>
            </li>
            <li>
              <i className="bi bi-telephone-fill"></i>
              <span>+251982310974</span>
            </li>
            <li>
              <i className="bi bi-geo-alt-fill"></i>
              <span>Addis Ababa, Ethiopia</span>
            </li>
          </ul>
        </div>

        {/* Right Section: Links */}
        <div className="footer-right">
          <h4>About</h4>
          <ul className="footer-links">
            <li>
              <a href="#">About Us</a>
            </li>
            <li>
              <a href="#">Privacy Policy</a>
            </li>
            <li>
              <a href="#">Terms of Services</a>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="footer-bottom">
        <p>© 2025 BrightRoot Academy. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default LandingFooter;
