import React, { useState } from "react";
import { Container, Row, Col, Badge, Button, Card } from "react-bootstrap";
import { useAuth } from "../../context/AuthContext";
import "./WelcomePage.css";

const WelcomePage = ({
  onSubjectSelected,
  onGoToChat,
  onGoToUpload,
  onGoToQuiz,
}) => {
  const { user, updateUserProfile } = useAuth();
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [selectedGrade, setSelectedGrade] = useState(null);

  const subjects = [
    {
      id: "maths",
      name: "Maths",
      icon: "bi-calculator",
      color: "#3498db",
      description: "Algebra, Geometry, and Problem Solving",
      topics: ["Algebra", "Geometry", "Statistics", "Calculus"],
    },
    {
      id: "physics",
      name: "Physics",
      icon: "bi-lightning",
      color: "#9b59b6",
      description: "Mechanics, Electricity, and Modern Physics",
      topics: ["Mechanics", "Thermodynamics", "Electricity", "Optics"],
    },
    {
      id: "chemistry",
      name: "Chemistry",
      icon: "bi-droplet",
      color: "#2ecc71",
      description: "Organic, Inorganic, and Physical Chemistry",
      topics: [
        "Organic Chemistry",
        "Inorganic Chemistry",
        "Physical Chemistry",
        "Biochemistry",
      ],
    },
    {
      id: "biology",
      name: "Biology",
      icon: "bi-tree",
      color: "#f39c12",
      description: "Life Sciences and Human Biology",
      topics: ["Cell Biology", "Genetics", "Ecology", "Human Biology"],
    },
    {
      id: "english",
      name: "English",
      icon: "bi-book",
      color: "#e74c3c",
      description: "Literature, Grammar, and Writing Skills",
      topics: [
        "Grammar",
        "Literature",
        "Essay Writing",
        "Reading Comprehension",
      ],
    },
  ];

  const grades = [
    { value: "Grade9", label: "Grade 9", level: "Preparatory" },
    { value: "Grade10", label: "Grade 10", level: "Preparatory" },
    { value: "Grade11", label: "Grade 11", level: "Preparatory" },
    { value: "Grade12", label: "Grade 12", level: "Preparatory" },
  ];

  const handleSubjectClick = (subject) => {
    setSelectedSubject(subject);
    setSelectedGrade(null);
  };

  const handleGradeClick = (grade) => {
    setSelectedGrade(grade);
  };

  const handleContinue = () => {
    if (selectedSubject && selectedGrade) {
      updateUserProfile({
        currentSubject: selectedSubject.id,
        currentGrade: selectedGrade.value,
        lastActivity: new Date().toISOString(),
      });
      onSubjectSelected &&
        onSubjectSelected({ subject: selectedSubject, grade: selectedGrade });
    }
  };

  return (
    <div className="welcome-page">
      <Container fluid className="py-5">
        {/* Hero Section */}
        <Row className="hero-section mb-5">
          <Col xs={12} className="text-center">
            <div className="hero-content fade-in">
              <div className="hero-icon mb-3">
                <i className="bi bi-mortarboard-fill"></i>
              </div>
              <h1 className="hero-title">
                Welcome to{" "}
                <span className="brand-gradient">BrightRoot Academy</span>
              </h1>
              <p className="hero-subtitle mb-4">
                Your AI-powered study companion for Ethiopian students. Upload
                documents, chat with AI, and master your subjects with
                personalized learning.
              </p>
              {user && (
                <div className="user-welcome mb-4">
                  <Badge bg="success" className="user-badge">
                    <i className="bi bi-person-check me-2"></i>
                    Welcome back, {user.firstName}!
                  </Badge>
                </div>
              )}
            </div>
          </Col>
        </Row>

        {/* Features Section */}
        <Row className="features-section mb-5">
          <Col xs={12} className="text-center mb-4">
            <h3 className="section-title text-light">What You Can Do</h3>
            <p>Powerful AI tools designed for Ethiopian curriculum</p>
          </Col>

          <Col md={4} className="mb-3">
            <div
              className="feature-card"
              style={{ cursor: "pointer" }}
              onClick={onGoToUpload}
            >
              <i className="bi bi-upload feature-icon text-primary"></i>
              <h5 className="text-light">Upload Documents</h5>
              <p>PDF, Word docs, textbooks - upload any study material</p>
            </div>
          </Col>

          <Col md={4} className="mb-3">
            <div
              className="feature-card"
              style={{ cursor: "pointer" }}
              onClick={onGoToChat}
            >
              <i className="bi bi-chat-dots feature-icon text-success"></i>
              <h5 className="text-light">AI Chat Assistant</h5>
              <p>
                Ask questions and get instant explanations from your documents
              </p>
            </div>
          </Col>

          <Col md={4} className="mb-3">
            <div
              className="feature-card"
              style={{ cursor: "pointer" }}
              onClick={onGoToQuiz}
            >
              <i className="bi bi-patch-question feature-icon text-warning"></i>
              <h5 className="text-light">Smart Quizzes</h5>
              <p>Generate custom quizzes and get bullet-point summaries</p>
            </div>
          </Col>
        </Row>

        {/* Subject Selection Section */}
        <Row className="subject-section mt-5">
          <Col xs={12} className="text-center mb-4">
            <h3 className="section-title text-light">Choose Your Subject</h3>
            <p>Select a subject to start learning</p>
          </Col>

          {subjects.map((subject) => (
            <Col key={subject.id} md={4} lg={3} className="mb-4">
              <Card
                className={`subject-card text-center ${
                  selectedSubject?.id === subject.id ? "selected" : ""
                }`}
                style={{
                  backgroundColor:
                    selectedSubject?.id === subject.id ? subject.color : "#222",
                  cursor: "pointer",
                }}
                onClick={() => handleSubjectClick(subject)}
              >
                <Card.Body>
                  <i
                    className={`bi ${subject.icon} fs-1 mb-3`}
                    style={{ color: subject.color }}
                  ></i>
                  <Card.Title className="text-light">{subject.name}</Card.Title>
                  <Card.Text className="text-secondary small">
                    {subject.description}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        {selectedSubject && (
          <Row className="grade-section mt-4">
            <Col xs={12} className="text-center mb-3">
              <h5 className="text-light">
                Select Grade for {selectedSubject.name}
              </h5>
            </Col>
            {grades.map((grade) => (
              <Col key={grade.value} md={3} className="mb-3 text-center">
                <Button
                  variant={
                    selectedGrade?.value === grade.value
                      ? "success"
                      : "outline-light"
                  }
                  onClick={() => handleGradeClick(grade)}
                >
                  {grade.label}
                </Button>
              </Col>
            ))}
          </Row>
        )}

        {selectedSubject && selectedGrade && (
          <Row className="text-center mt-4">
            <Col>
              <Button variant="success" onClick={handleContinue}>
                Continue to Study
              </Button>
            </Col>
          </Row>
        )}
      </Container>
    </div>
  );
};

export default WelcomePage;
