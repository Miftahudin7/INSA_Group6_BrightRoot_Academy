import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./components/auth/LoginPage";
import RegisterPage from "./components/auth/RegisterPage";
import WelcomePage from "./components/pages/WelcomePage";
import Dashboard from "./components/pages/Dashboard";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./App.css";

// Main App Content Component (inside AuthProvider)
const AppContent = () => {
  const { user, isLoading, logout } = useAuth(); // <-- changed logoutUser → logout
  const [currentView, setCurrentView] = useState("welcome");
  const [selectedSubjectGrade, setSelectedSubjectGrade] = useState(null);
  const [showRegistration, setShowRegistration] = useState(false);

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="text-center">
          <div className="spinner-border text-success mb-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <h4 className="text-light">Loading BrightRoot Academy...</h4>
          <p className="text-muted">Preparing your learning experience</p>
        </div>
      </div>
    );
  }

  // If not authenticated → show login/register
  if (!user) {
    if (showRegistration) {
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

    return (
      <LoginPage
        onLoginSuccess={() => {
          setCurrentView("welcome");
        }}
        onSwitchToRegister={() => setShowRegistration(true)}
      />
    );
  }

  // Handle subject and grade selection from WelcomePage
  const handleSubjectSelected = (selection) => {
    setSelectedSubjectGrade(selection);
    setCurrentView("dashboard");
    console.log("Selected:", selection);
  };

  // Render based on currentView
  const renderCurrentView = () => {
    switch (currentView) {
      case "welcome":
        return <WelcomePage onSubjectSelected={handleSubjectSelected} />;
      case "dashboard":
        return (
          <Dashboard
            selectedSubjectGrade={selectedSubjectGrade}
            onBackToSubjects={() => setCurrentView("welcome")}
          />
        );
      default:
        return <WelcomePage onSubjectSelected={handleSubjectSelected} />;
    }
  };

  return (
    <div className="app">
      {/* Header (when logged in) */}
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
                <span className="text-muted me-3">
                  <i className="bi bi-person me-1"></i>
                  {user.username ||
                    `${user.first_name || ""} ${user.last_name || ""}`}
                </span>
                <button
                  className="btn btn-outline-light btn-sm"
                  onClick={() => {
                    if (window.confirm("Are you sure you want to logout?")) {
                      logout(); // ✅ use correct logout
                    }
                  }}
                >
                  <i className="bi bi-box-arrow-right me-1"></i>
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>
      )}

      {/* Main Content */}
      <main className="app-main">{renderCurrentView()}</main>

      {/* Footer (when logged in) */}
      {user && (
        <footer className="app-footer">
          <div className="container">
            <div className="row py-4">
              <div className="col-md-6">
                <p className="text-muted mb-0">
                  <strong>BrightRoot Academy</strong> - AI-Powered Study
                  Companion
                </p>
              </div>
              <div className="col-md-6 text-md-end">
                <p className="text-muted mb-0">
                  Built by Team BrightRoot • Frontend: Abdurehman • Backend:
                  Mihretab • AI: Miftah
                </p>
              </div>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
};

// Wrap with AuthProvider
const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
