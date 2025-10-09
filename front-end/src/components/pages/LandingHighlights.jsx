import React from "react";
import "./LandingHighlights.css";

const LandingHighlights = () => {
  const highlights = [
    {
      icon: "bi bi-lightning-charge-fill",
      title: "Unlock Your Academic Potential",
      description:
        "BrightRoot Academy empowers students with personalized lessons and AI-driven insights to build confidence and mastery in learning.",
    },
    {
      icon: "bi bi-journal-bookmark-fill",
      title: "Build Strong Foundations",
      description:
        "Interactive lessons ensure students grasp core concepts before advancing, strengthening both knowledge and confidence.",
    },
    {
      icon: "bi bi-bricks",
      title: "Develop Problem-Solving Skills",
      description:
        "Engage in challenges and hands-on exercises that stimulate creativity, critical thinking, and innovative problem-solving.",
    },
    {
      icon: "bi bi-person-badge-fill",
      title: "Personalized Learning Pathways",
      description:
        "AI adapts lessons to each student’s pace, ensuring progress is tailored to individual strengths and improvement areas.",
    },
    {
      icon: "bi bi-bar-chart-fill",
      title: "Track Progress & Stay Motivated",
      description:
        "Visual dashboards show growth, celebrate achievements, and keep students motivated to reach their learning goals.",
    },
    {
      icon: "bi bi-people-fill",
      title: "Learn Together & Access Resources",
      description:
        "Connect with peers, join group challenges, and explore curated resources to deepen understanding and collaboration.",
    },
  ];

  return (
    <section className="highlights-section">
      <h2 className="highlights-title">Why Students Love BrightRoot Academy</h2>
      <div className="highlights-grid">
        {highlights.map((item, index) => (
          <div key={index} className="highlight-card">
            <i className={`${item.icon} highlight-icon`}></i>
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default LandingHighlights;
