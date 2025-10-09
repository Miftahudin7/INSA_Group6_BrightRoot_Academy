import React, { useState } from "react";
import { Container, Button, Card, Form } from "react-bootstrap";

const SmartQuizzes = ({ onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  // Simulate generating quiz questions
  const generateQuiz = () => {
    const sampleQuestions = [
      {
        id: 1,
        question: "What is the capital of Ethiopia?",
        options: ["Addis Ababa", "Gondar", "Mekele", "Bahir Dar"],
        correct: "Addis Ababa",
      },
      {
        id: 2,
        question: "What is 5 + 7?",
        options: ["10", "11", "12", "13"],
        correct: "12",
      },
      {
        id: 3,
        question: "Which element has the chemical symbol O?",
        options: ["Oxygen", "Gold", "Silver", "Iron"],
        correct: "Oxygen",
      },
    ];
    setQuestions(sampleQuestions);
    setShowResults(false);
    setAnswers({});
  };

  const handleAnswerChange = (qId, value) => {
    setAnswers({ ...answers, [qId]: value });
  };

  const calculateResults = () => {
    let score = 0;
    questions.forEach((q) => {
      if (answers[q.id] === q.correct) score++;
    });
    alert(`You scored ${score} out of ${questions.length}`);
    setShowResults(true);
  };

  return (
    <Container className="py-4">
      <Button variant="secondary" onClick={onBack} className="mb-3">
        &larr; Back
      </Button>
      <h4 className="text-light mb-3">Smart Quizzes</h4>

      <Button variant="success" onClick={generateQuiz} className="mb-3">
        Generate Quiz
      </Button>

      {questions.map((q) => (
        <Card key={q.id} className="mb-3">
          <Card.Body>
            <Card.Title>{q.question}</Card.Title>
            <Form>
              {q.options.map((opt, idx) => (
                <Form.Check
                  key={idx}
                  type="radio"
                  label={opt}
                  name={`question-${q.id}`}
                  value={opt}
                  checked={answers[q.id] === opt}
                  onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                  disabled={showResults}
                />
              ))}
            </Form>
            {showResults && (
              <p className="mt-2">
                Correct Answer: <strong>{q.correct}</strong>
              </p>
            )}
          </Card.Body>
        </Card>
      ))}

      {questions.length > 0 && !showResults && (
        <Button variant="primary" onClick={calculateResults}>
          Submit Answers
        </Button>
      )}
    </Container>
  );
};

export default SmartQuizzes;
