import React, { useState, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Form,
  Alert,
  Spinner,
  ListGroup,
  Badge,
  Modal,
  Tab,
  Tabs,
} from "react-bootstrap";
import axios from "axios";
import "./Dashboard.css";

const Dashboard = ({ selectedSubjectGrade, onBackToSubjects }) => {
  const [activeTab, setActiveTab] = useState("upload");
  const [files, setFiles] = useState([]);
  const [summaries, setSummaries] = useState([]);
  const [quizzes, setQuizzes] = useState([]);
  const [commonBooks, setCommonBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // File upload state
  const [uploadForm, setUploadForm] = useState({
    title: "",
    description: "",
    subject: selectedSubjectGrade?.subject?.id
      ? selectedSubjectGrade.subject.name
      : selectedSubjectGrade?.subject?.value || "Maths",
    grade: selectedSubjectGrade?.grade?.value || "Grade9",
  });
  const [selectedFile, setSelectedFile] = useState(null);

  // AI generation state
  const [selectedFileForAI, setSelectedFileForAI] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Quiz state
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [showQuizResults, setShowQuizResults] = useState(false);

  // Modal states
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const [showQuizModal, setShowQuizModal] = useState(false);
  const [currentSummary, setCurrentSummary] = useState("");
  const [currentQuiz, setCurrentQuiz] = useState(null);

  const API_BASE_URL = "http://localhost:8000/api";
  const token = localStorage.getItem("brightroot_token");

  const apiClient = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
    },
  });

  useEffect(() => {
    if (selectedSubjectGrade) {
      loadUserFiles();
      loadCommonBooks();
      loadUserSummaries();
      loadUserQuizzes();
    }
  }, [selectedSubjectGrade]);

  const loadUserFiles = async () => {
    try {
      const response = await apiClient.get("/notes/files/");
      setFiles(response.data);
    } catch (error) {
      console.error("Failed to load files:", error);
    }
  };

  const loadCommonBooks = async () => {
    try {
      const response = await apiClient.get(
        `/notes/common-books/?subject=${uploadForm.subject}&grade=${uploadForm.grade}`
      );
      setCommonBooks(response.data);
    } catch (error) {
      console.error("Failed to load common books:", error);
    }
  };

  const loadUserSummaries = async () => {
    try {
      const response = await apiClient.get("/ai/summaries/");
      setSummaries(response.data);
    } catch (error) {
      console.error("Failed to load summaries:", error);
    }
  };

  const loadUserQuizzes = async () => {
    try {
      const response = await apiClient.get("/ai/quizzes/");
      setQuizzes(response.data);
    } catch (error) {
      console.error("Failed to load quizzes:", error);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError("Please select a file to upload");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("title", uploadForm.title);
      formData.append("description", uploadForm.description);
      formData.append("subject", uploadForm.subject);
      formData.append("grade", uploadForm.grade);

      await apiClient.post("/notes/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setSuccess("File uploaded successfully!");
      setUploadForm({
        title: "",
        description: "",
        subject: selectedSubjectGrade?.subject?.value || "Math",
        grade: selectedSubjectGrade?.grade?.value || "Grade9",
      });
      setSelectedFile(null);
      loadUserFiles();
    } catch (error) {
      setError(error.response?.data?.error || "Failed to upload file");
    } finally {
      setIsLoading(false);
    }
  };

  const generateSummary = async (fileId) => {
    setAiLoading(true);
    try {
      const response = await apiClient.post("/ai/summary/generate/", {
        file_id: fileId,
      });

      setCurrentSummary(response.data.summary);
      setShowSummaryModal(true);
      loadUserSummaries();
    } catch (error) {
      setError(error.response?.data?.error || "Failed to generate summary");
    } finally {
      setAiLoading(false);
    }
  };

  const generateQuiz = async (fileId) => {
    setAiLoading(true);
    try {
      const response = await apiClient.post("/ai/quiz/generate/", {
        file_id: fileId,
        num_questions: 5,
      });

      setCurrentQuiz(response.data.quiz);
      setQuizQuestions(response.data.quiz.questions);
      setUserAnswers({});
      setCurrentQuestionIndex(0);
      setShowQuizResults(false);
      setShowQuizModal(true);
      loadUserQuizzes();
    } catch (error) {
      setError(error.response?.data?.error || "Failed to generate quiz");
    } finally {
      setAiLoading(false);
    }
  };

  const handleQuizAnswer = (answer) => {
    setUserAnswers((prev) => ({
      ...prev,
      [currentQuestionIndex]: answer,
    }));
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      setShowQuizResults(true);
    }
  };

  const previousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const getQuizScore = () => {
    let correct = 0;
    quizQuestions.forEach((question, index) => {
      if (userAnswers[index] === question.correct_answer) {
        correct++;
      }
    });
    return {
      correct,
      total: quizQuestions.length,
      percentage: Math.round((correct / quizQuestions.length) * 100),
    };
  };

  const renderUploadTab = () => (
    <div>
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">
            <i className="bi bi-cloud-upload me-2"></i>
            Upload Study Material
          </h5>
        </Card.Header>
        <Card.Body>
          <Form onSubmit={handleFileUpload}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Title</Form.Label>
                  <Form.Control
                    type="text"
                    value={uploadForm.title}
                    onChange={(e) =>
                      setUploadForm((prev) => ({
                        ...prev,
                        title: e.target.value,
                      }))
                    }
                    placeholder="Enter document title"
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Subject</Form.Label>
                  <Form.Select
                    value={uploadForm.subject}
                    onChange={(e) =>
                      setUploadForm((prev) => ({
                        ...prev,
                        subject: e.target.value,
                      }))
                    }
                  >
                    <option value="Maths">Maths</option>
                    <option value="Physics">Physics</option>
                    <option value="Chemistry">Chemistry</option>
                    <option value="Biology">Biology</option>
                    <option value="English">English</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Grade</Form.Label>
                  <Form.Select
                    value={uploadForm.grade}
                    onChange={(e) =>
                      setUploadForm((prev) => ({
                        ...prev,
                        grade: e.target.value,
                      }))
                    }
                  >
                    <option value="Grade9">Grade 9</option>
                    <option value="Grade10">Grade 10</option>
                    <option value="Grade11">Grade 11</option>
                    <option value="Grade12">Grade 12</option>
                  </Form.Select>
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>File</Form.Label>
                  <Form.Control
                    type="file"
                    onChange={(e) => setSelectedFile(e.target.files[0])}
                    accept=".pdf,.docx,.txt"
                    required
                  />
                </Form.Group>
              </Col>
            </Row>
            <Form.Group className="mb-3">
              <Form.Label>Description (Optional)</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={uploadForm.description}
                onChange={(e) =>
                  setUploadForm((prev) => ({
                    ...prev,
                    description: e.target.value,
                  }))
                }
                placeholder="Brief description of the document"
              />
            </Form.Group>
            <Button type="submit" variant="success" disabled={isLoading}>
              {isLoading ? (
                <>
                  <Spinner size="sm" className="me-2" />
                  Uploading...
                </>
              ) : (
                <>
                  <i className="bi bi-cloud-upload me-2"></i>
                  Upload Document
                </>
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {/* User Files */}
      <Card>
        <Card.Header>
          <h5 className="mb-0">
            <i className="bi bi-folder me-2"></i>
            Your Uploaded Files
          </h5>
        </Card.Header>
        <Card.Body>
          {files.length === 0 ? (
            <p className=" ">
              No files uploaded yet. Upload your first study material above!
            </p>
          ) : (
            <ListGroup>
              {files.map((file) => (
                <ListGroup.Item
                  key={file.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <h6 className="mb-1">{file.title}</h6>
                    <p className="mb-1">{file.description}</p>
                    <small className=" ">
                      {file.subject} • {file.grade} •{" "}
                      {new Date(file.uploaded_at).toLocaleDateString()}
                    </small>
                  </div>

                  <div className="d-flex gap-2">
                    {/* Download button */}
                    <a
                      href={`http://localhost:8000/api/notes/download/${file.id}/`}
                      className="btn btn-outline-success btn-sm d-flex align-items-center"
                      target="_blank"
                      download
                    >
                      <i className="bi bi-download me-1"></i>
                      Download
                    </a>

                    {/* Summary Button */}
                    <Button
                      size="sm"
                      variant="outline-primary"
                      onClick={() => generateSummary(file.id)}
                      disabled={aiLoading}
                    >
                      <i className="bi bi-lightbulb me-1"></i>
                      Summary
                    </Button>

                    {/* Quiz Button */}
                    <Button
                      size="sm"
                      variant="outline-success"
                      onClick={() => generateQuiz(file.id)}
                      disabled={aiLoading}
                    >
                      <i className="bi bi-question-circle me-1"></i>
                      Quiz
                    </Button>
                  </div>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Card.Body>
      </Card>
    </div>
  );

  const renderStudyTab = () => (
    <div>
      {/* Common Books */}
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">
            <i className="bi bi-book me-2"></i>
            Curriculum Materials
          </h5>
        </Card.Header>
        <Card.Body>
          {commonBooks.length === 0 ? (
            <p className=" ">
              No curriculum materials available for this subject and grade.
            </p>
          ) : (
            <ListGroup>
              {commonBooks.map((book) => (
                <ListGroup.Item
                  key={book.id}
                  className="d-flex justify-content-between align-items-center"
                >
                  <div>
                    <h6 className="mb-1">{book.title}</h6>
                    <small className=" ">
                      {book.subject} • {book.grade} •{" "}
                      {new Date(book.uploaded_at).toLocaleDateString()}
                    </small>
                  </div>
                  <Button size="sm" variant="outline-primary">
                    <i className="bi bi-eye me-1"></i>
                    View
                  </Button>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Card.Body>
      </Card>

      {/* AI Summaries */}
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">
            <i className="bi bi-lightbulb me-2"></i>
            AI-Generated Summaries
          </h5>
        </Card.Header>
        <Card.Body>
          {summaries.length === 0 ? (
            <p className=" ">
              No summaries generated yet. Upload a document and generate a
              summary!
            </p>
          ) : (
            <ListGroup>
              {summaries.map((summary) => (
                <ListGroup.Item key={summary.id}>
                  <h6 className="mb-1">{summary.file_title}</h6>
                  <p className="mb-2">{summary.content.substring(0, 150)}...</p>
                  <small className=" ">
                    {summary.subject} • {summary.grade} •{" "}
                    {new Date(summary.created_at).toLocaleDateString()}
                  </small>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Card.Body>
      </Card>

      {/* AI Quizzes */}
      <Card>
        <Card.Header>
          <h5 className="mb-0">
            <i className="bi bi-question-circle me-2"></i>
            AI-Generated Quizzes
          </h5>
        </Card.Header>
        <Card.Body>
          {quizzes.length === 0 ? (
            <p className=" ">
              No quizzes generated yet. Upload a document and generate a quiz!
            </p>
          ) : (
            <ListGroup>
              {quizzes.map((quiz) => (
                <ListGroup.Item key={quiz.id}>
                  <h6 className="mb-1">{quiz.file_title}</h6>
                  <p className="mb-2">
                    {quiz.questions.questions?.length || 0} questions •{" "}
                    {quiz.subject} • {quiz.grade}
                  </p>
                  <small className=" ">
                    {new Date(quiz.created_at).toLocaleDateString()}
                  </small>
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Card.Body>
      </Card>
    </div>
  );

  return (
    <div className="dashboard">
      <Container fluid className="py-4">
        {/* Header */}
        <Row className="mb-4">
          <Col>
            <div className="d-flex justify-content-between align-items-center">
              <div>
                <h2 className="text-light mb-2">
                  <i className="bi bi-mortarboard-fill text-success me-2"></i>
                  Study Dashboard
                </h2>
                <p className="  mb-0">
                  {selectedSubjectGrade?.subject?.name} •{" "}
                  {selectedSubjectGrade?.grade?.label}
                </p>
              </div>
              <Button variant="outline-light" onClick={onBackToSubjects}>
                <i className="bi bi-arrow-left me-2"></i>
                Change Subject
              </Button>
            </div>
          </Col>
        </Row>

        {/* Alerts */}
        {error && (
          <Alert variant="danger" dismissible onClose={() => setError(null)}>
            <i className="bi bi-exclamation-triangle me-2"></i>
            {error}
          </Alert>
        )}
        {success && (
          <Alert variant="success" dismissible onClose={() => setSuccess(null)}>
            <i className="bi bi-check-circle me-2"></i>
            {success}
          </Alert>
        )}

        {/* Main Content */}
        <Row>
          <Col>
            <Card className="border-0 shadow">
              <Card.Body className="p-0">
                <Tabs
                  activeKey={activeTab}
                  onSelect={(k) => setActiveTab(k)}
                  className="dashboard-tabs"
                >
                  <Tab eventKey="upload" title="Upload & AI Tools">
                    {renderUploadTab()}
                  </Tab>
                  <Tab eventKey="study" title="Study Materials">
                    {renderStudyTab()}
                  </Tab>
                </Tabs>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Summary Modal */}
      <Modal
        show={showSummaryModal}
        onHide={() => setShowSummaryModal(false)}
        size="lg"
      >
        <Modal.Header closeButton>
          <Modal.Title>AI-Generated Summary</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="summary-content">
            {currentSummary.split("\n").map((paragraph, index) => (
              <p key={index} className="mb-3">
                {paragraph}
              </p>
            ))}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => setShowSummaryModal(false)}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Quiz Modal */}
      <Modal
        show={showQuizModal}
        onHide={() => setShowQuizModal(false)}
        size="lg"
      >
        <Modal.Header closeButton>
          <Modal.Title>AI-Generated Quiz</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {!showQuizResults ? (
            <div className="quiz-content">
              {quizQuestions.length > 0 && (
                <div>
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h6>
                      Question {currentQuestionIndex + 1} of{" "}
                      {quizQuestions.length}
                    </h6>
                    <Badge bg="info">
                      {Math.round(
                        ((currentQuestionIndex + 1) / quizQuestions.length) *
                          100
                      )}
                      % Complete
                    </Badge>
                  </div>

                  <h5 className="mb-3">
                    {quizQuestions[currentQuestionIndex]?.question}
                  </h5>

                  <div className="quiz-options">
                    {Object.entries(
                      quizQuestions[currentQuestionIndex]?.options || {}
                    ).map(([key, value]) => (
                      <Button
                        key={key}
                        variant={
                          userAnswers[currentQuestionIndex] === key
                            ? "primary"
                            : "outline-primary"
                        }
                        className="w-100 mb-2 text-start"
                        onClick={() => handleQuizAnswer(key)}
                      >
                        <strong>{key}.</strong> {value}
                      </Button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="quiz-results text-center">
              <h4 className="mb-4">Quiz Results</h4>
              {(() => {
                const score = getQuizScore();
                return (
                  <div>
                    <div className="score-display mb-4">
                      <h2
                        className={`text-${
                          score.percentage >= 70
                            ? "success"
                            : score.percentage >= 50
                            ? "warning"
                            : "danger"
                        }`}
                      >
                        {score.percentage}%
                      </h2>
                      <p className=" ">
                        You got {score.correct} out of {score.total} questions
                        correct
                      </p>
                    </div>

                    <div className="question-review">
                      {quizQuestions.map((question, index) => (
                        <div key={index} className="mb-3 p-3 border rounded">
                          <h6>Question {index + 1}</h6>
                          <p>{question.question}</p>
                          <p className="mb-2">
                            <strong>Your Answer:</strong>{" "}
                            {userAnswers[index] || "Not answered"}
                          </p>
                          <p className="mb-2">
                            <strong>Correct Answer:</strong>{" "}
                            {question.correct_answer}
                          </p>
                          <p className="  small">{question.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          {!showQuizResults ? (
            <div className="d-flex justify-content-between w-100">
              <Button
                variant="secondary"
                onClick={previousQuestion}
                disabled={currentQuestionIndex === 0}
              >
                <i className="bi bi-arrow-left me-2"></i>
                Previous
              </Button>
              <Button
                variant="primary"
                onClick={nextQuestion}
                disabled={!userAnswers[currentQuestionIndex]}
              >
                {currentQuestionIndex === quizQuestions.length - 1 ? (
                  <>
                    <i className="bi bi-check-circle me-2"></i>
                    Finish Quiz
                  </>
                ) : (
                  <>
                    Next
                    <i className="bi bi-arrow-right ms-2"></i>
                  </>
                )}
              </Button>
            </div>
          ) : (
            <Button variant="secondary" onClick={() => setShowQuizModal(false)}>
              Close
            </Button>
          )}
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Dashboard;
