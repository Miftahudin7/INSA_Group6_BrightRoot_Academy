import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./components/auth/LoginPage";
import RegisterPage from "./components/auth/RegisterPage";
import WelcomePage from "./components/pages/WelcomePage";
import Dashboard from "./components/pages/Dashboard";
import ChatInterface from "./components/pages/ChatInterface";
import UploadDocuments from "./components/pages/UploadDocuments";
import SmartQuizzes from "./components/pages/SmartQuizzes";
import LandingPage from "./components/pages/LandingPage";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./App.css";

const AppContent = () => {
  const { user, isLoading, logout } = useAuth();
  const [currentView, setCurrentView] = useState("welcome");
  const [selectedSubjectGrade, setSelectedSubjectGrade] = useState(null);
  const [showRegistration, setShowRegistration] = useState(false);
  const [showLanding, setShowLanding] = useState(true);

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="text-center">
          <div className="spinner-border text-success mb-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <h4 className="text-light">Loading BrightRoot Academy...</h4>
          <p>Preparing your learning experience</p>
        </div>
      </div>
    );
  }

  if (!user && showLanding) {
    return (
      <LandingPage
        onGetStarted={(choice) => {
          setShowLanding(false);
          setShowRegistration(choice === "register");
        }}
      />
    );
  }

  if (!user && showRegistration) {
    return (
      <RegisterPage
        onRegisterSuccess={() => {
          setCurrentView("welcome");
          setShowRegistration(false);
        }}
        onSwitchToLogin={() => setShowRegistration(false)}
      />
    );
  }

  if (!user && !showRegistration) {
    return (
      <LoginPage
        onLoginSuccess={() => setCurrentView("welcome")}
        onSwitchToRegister={() => setShowRegistration(true)}
      />
    );
  }

  const handleSubjectSelected = (selection) => {
    setSelectedSubjectGrade(selection);
    setCurrentView("dashboard");
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case "welcome":
        return (
          <WelcomePage
            onSubjectSelected={handleSubjectSelected}
            onGoToChat={() => setCurrentView("chat")}
            onGoToUpload={() => setCurrentView("upload")}
            onGoToQuiz={() => setCurrentView("quiz")}
          />
        );
      case "dashboard":
        return (
          <Dashboard
            selectedSubjectGrade={selectedSubjectGrade}
            onBackToSubjects={() => setCurrentView("welcome")}
          />
        );
      case "chat":
        return <ChatInterface onBack={() => setCurrentView("welcome")} />;
      case "upload":
        return <UploadDocuments onBack={() => setCurrentView("welcome")} />;
      case "quiz":
        return <SmartQuizzes onBack={() => setCurrentView("welcome")} />;
      default:
        return (
          <WelcomePage
            onSubjectSelected={handleSubjectSelected}
            onGoToChat={() => setCurrentView("chat")}
            onGoToUpload={() => setCurrentView("upload")}
            onGoToQuiz={() => setCurrentView("quiz")}
          />
        );
    }
  };

  return (
    <div className="app">
      {user && (
        <nav className="app-header">
          <div className="container-fluid">
            <div className="d-flex justify-content-between align-items-center py-3">
              <div className="d-flex align-items-center">
                <i className="bi bi-mortarboard-fill text-success fs-4 me-2"></i>
                <span className="text-light fw-bold fs-5">
                  BrightRoot Academy
                </span>
              </div>
              <div className="d-flex align-items-center">
                <span className="me-3">
                  <i className="bi bi-person me-1"></i>
                  {user.username ||
                    `${user.first_name || ""} ${user.last_name || ""}`}
                </span>
                <button
                  className="btn btn-outline-light btn-sm"
                  onClick={() => {
                    if (window.confirm("Are you sure you want to logout?")) {
                      logout();
                      setShowLanding(true);
                    }
                  }}
                >
                  <i className="bi bi-box-arrow-right me-1"></i> Logout
                </button>
              </div>
            </div>
          </div>
        </nav>
      )}

      <main className="app-main">{renderCurrentView()}</main>

      {user && (
        <footer className="app-footer">
          <div className="container">
            <div className="row py-4">
              <div className="col-md-6">
                <p className="mb-0">
                  <strong>BrightRoot Academy</strong> - AI-Powered Study
                  Companion
                </p>
              </div>
              <div className="col-md-6 text-md-end">
                <p className="mb-0">
                  &copy; {new Date().getFullYear()} BrightRoot Academy. All
                  rights reserved.
                </p>
              </div>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
};

const App = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);

export default App;
