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

const RegisterPage = ({ onSwitchToLogin }) => {
  // Form state
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [formErrors, setFormErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Auth context
  const { register, isLoading, error } = useAuth();

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

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

    if (!formData.username.trim()) {
      errors.username = "Username is required";
    } else if (formData.username.length < 3) {
      errors.username = "Username must be at least 3 characters";
    }

    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = "Please enter a valid email address";
    }

    if (!formData.password) {
      errors.password = "Password is required";
    } else if (formData.password.length < 6) {
      errors.password = "Password must be at least 6 characters";
    }

    if (!formData.confirmPassword) {
      errors.confirmPassword = "Please confirm your password";
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = "Passwords do not match";
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const result = await register(formData);

    if (result.success) {
      // Switch to login page after successful registration
      onSwitchToLogin && onSwitchToLogin();
    }
  };

  return (
    <div className="login-page">
      <Container fluid className="h-100">
        <Row className="h-100 align-items-center justify-content-center">
          <Col xs={12} sm={8} md={6} lg={4} xl={3}>
            <div className="login-container fade-in">
              <div className="text-center mb-4">
                <div className="brand-logo">
                  <i className="bi bi-mortarboard-fill text-success fs-1"></i>
                </div>
                <h2 className="brand-title text-light mb-2">
                  BrightRoot Academy
                </h2>
                <p className="brand-subtitle  ">
                  Join Your AI-Powered Study Companion
                </p>
              </div>

              <Card className="login-card shadow-lg border-0">
                <Card.Body className="p-4">
                  <h4 className="text-center mb-4 text-light">
                    Create Account
                  </h4>

                  {error && (
                    <Alert variant="danger" className="mb-3">
                      <i className="bi bi-exclamation-triangle me-2"></i>
                      {error}
                    </Alert>
                  )}

                  <Form onSubmit={handleSubmit}>
                    {/* Username Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-person me-2"></i> Username
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        placeholder="Choose a username"
                        isInvalid={!!formErrors.username}
                        disabled={isLoading}
                        className="custom-input"
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.username}
                      </Form.Control.Feedback>
                    </Form.Group>

                    {/* Email Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-envelope me-2"></i> Email Address
                      </Form.Label>
                      <Form.Control
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Enter your email"
                        isInvalid={!!formErrors.email}
                        disabled={isLoading}
                        className="custom-input"
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.email}
                      </Form.Control.Feedback>
                    </Form.Group>

                    {/* Password Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-lock me-2"></i> Password
                      </Form.Label>
                      <div className="password-input-container">
                        <Form.Control
                          type={showPassword ? "text" : "password"}
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          placeholder="Create a password"
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

                    {/* Confirm Password Field */}
                    <Form.Group className="mb-3">
                      <Form.Label className="text-light">
                        <i className="bi bi-lock me-2"></i> Confirm Password
                      </Form.Label>
                      <div className="password-input-container">
                        <Form.Control
                          type={showConfirmPassword ? "text" : "password"}
                          name="confirmPassword"
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          placeholder="Confirm your password"
                          isInvalid={!!formErrors.confirmPassword}
                          disabled={isLoading}
                          className="custom-input"
                        />
                        <Button
                          variant="link"
                          className="password-toggle"
                          onClick={() =>
                            setShowConfirmPassword(!showConfirmPassword)
                          }
                          type="button"
                          disabled={isLoading}
                        >
                          <i
                            className={`bi ${
                              showConfirmPassword ? "bi-eye-slash" : "bi-eye"
                            }`}
                          ></i>
                        </Button>
                      </div>
                      <Form.Control.Feedback type="invalid">
                        {formErrors.confirmPassword}
                      </Form.Control.Feedback>
                    </Form.Group>

                    {/* Register Button */}
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
                            Creating Account...
                          </>
                        ) : (
                          <>
                            <i className="bi bi-person-plus me-2"></i>
                            Create Account
                          </>
                        )}
                      </Button>
                    </div>

                    {/* Switch to Login */}
                    <div className="text-center">
                      <small className="">
                        Already have an account?{" "}
                        <Button
                          variant="link"
                          className="p-0 text-success"
                          onClick={onSwitchToLogin}
                        >
                          Sign In
                        </Button>
                      </small>
                    </div>
                  </Form>
                </Card.Body>
              </Card>

              <div className="text-center mt-4">
                <small className=" ">
                    BrightRoot Team!
                </small>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default RegisterPage;
