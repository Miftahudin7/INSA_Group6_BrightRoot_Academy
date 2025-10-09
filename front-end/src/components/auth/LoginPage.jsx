import React, { useState } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
  Spinner,
} from "react-bootstrap";
import { useAuth } from "../../context/AuthContext";
import "./LoginPage.css";

const LoginPage = ({ onLoginSuccess, onSwitchToRegister }) => {
  // Form state
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [formErrors, setFormErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);

  // Auth context
  const { login, isLoading, error } = useAuth();

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    // Clear field error when user starts typing
    if (formErrors[name]) {
      setFormErrors((prev) => ({
        ...prev,
        [name]: null,
      }));
    }
  };

  // Validate form
  const validateForm = () => {
    const errors = {};

    // Username validation
    if (!formData.username) {
      errors.username = "Username is required";
    }

    // Password validation
    if (!formData.password) {
      errors.password = "Password is required";
    } else if (formData.password.length < 6) {
      errors.password = "Password must be at least 6 characters";
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const result = await login(formData.username, formData.password);

    if (result.success) {
      // Login successful, parent component will handle navigation
      onLoginSuccess && onLoginSuccess();
    }
    // Error handling is managed by AuthContext
  };

  return (
    <div className="login-page">
      <Container fluid className="h-100">
        <Row className="h-100 align-items-center justify-content-center">
          <Col xs={12} sm={8} md={6} lg={4} xl={3}>
            <div className="login-container fade-in">
              {/* Brand Header */}
              <div className="text-center mb-4">
                <div className="brand-logo">
                  <i className="bi bi-mortarboard-fill text-success fs-1"></i>
                </div>
                <h2 className="brand-title text-light mb-2">
                  BrightRoot Academy
                </h2>
                <p className="brand-subtitle ">
                  Your AI-Powered Study Companion
                </p>
              </div>

              {/* Login Card */}
              <Card className="login-card shadow-lg border-0">
                <Card.Body className="p-4">
                  <h4 className="text-center mb-4 text-light">Welcome Back</h4>

                  {/* Error Alert */}
                  {error && (
                    <Alert variant="danger" className="mb-3">
                      <i className="bi bi-exclamation-triangle me-2"></i>
                      {error}
                    </Alert>
                  )}

                  {/* Login Form */}
                  <Form onSubmit={handleSubmit}>
                    {/* Username Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-person me-2"></i>
                        Username
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Enter your username"
                        isInvalid={!!formErrors.username}
                        disabled={isLoading}
                        className="custom-input"
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.username}
                      </Form.Control.Feedback>
                    </Form.Group>

                    {/* Password Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-lock me-2"></i>
                        Password
                      </Form.Label>
                      <div className="password-input-container">
                        <Form.Control
                          type={showPassword ? "text" : "password"}
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          placeholder="Enter your password"
                          isInvalid={!!formErrors.password}
                          disabled={isLoading}
                          className="custom-input"
                        />
                        <Button
                          variant="link"
                          className="password-toggle"
                          onClick={() => setShowPassword(!showPassword)}
                          type="button"
                          disabled={isLoading}
                        >
                          <i
                            className={`bi ${
                              showPassword ? "bi-eye-slash" : "bi-eye"
                            }`}
                          ></i>
                        </Button>
                      </div>
                      <Form.Control.Feedback type="invalid">
                        {formErrors.password}
                      </Form.Control.Feedback>
                    </Form.Group>

                    {/* Login Button */}
                    <div className="d-grid mb-3">
                      <Button
                        type="submit"
                        variant="success"
                        size="lg"
                        disabled={isLoading}
                        className="login-btn"
                      >
                        {isLoading ? (
                          <>
                            <Spinner size="sm" className="me-2" />
                            Signing In...
                          </>
                        ) : (
                          <>
                            <i className="bi bi-box-arrow-in-right me-2"></i>
                            Sign In
                          </>
                        )}
                      </Button>
                    </div>

                 
                    {/* Switch to Registration */}
                    <div className="text-center mt-3">
                      <small className=" ">
                        Don't have an account?{" "}
                        <Button
                          variant="link"
                          className="p-0 text-success"
                          onClick={onSwitchToRegister}
                        >
                          Sign Up
                        </Button>
                      </small>
                    </div>
                  </Form>
                </Card.Body>
              </Card>

              {/* Footer */}
             
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default LoginPage;
