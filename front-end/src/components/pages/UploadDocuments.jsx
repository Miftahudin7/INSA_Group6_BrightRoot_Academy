import React, { useState } from "react";
import { Container, Button, ListGroup, Modal } from "react-bootstrap";

const UploadDocuments = ({ onBack }) => {
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);

  // Handle file upload
  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);

    // Convert files to object URLs for in-app preview
    const newDocs = files.map((file) => ({
      name: file.name,
      url: URL.createObjectURL(file),
      type: file.type,
    }));

    setDocuments((prev) => [...prev, ...newDocs]);
    e.target.value = null; // Reset input
  };

  return (
    <Container className="py-4">
      <Button variant="secondary" onClick={onBack} className="mb-3">
        &larr; Back
      </Button>
      <h4 className="text-light mb-3">Upload and Read Documents</h4>

      <div className="mb-3">
        <input
          type="file"
          multiple
          onChange={handleFileUpload}
          accept=".pdf,.doc,.docx,.txt"
        />
      </div>

      <h5 className="text-light mt-4">Uploaded Documents</h5>
      {documents.length === 0 && (
        <p className="text-light">No documents uploaded yet.</p>
      )}

      <ListGroup>
        {documents.map((doc, index) => (
          <ListGroup.Item
            key={index}
            action
            onClick={() => setSelectedDoc(doc)}
          >
            {doc.name}
          </ListGroup.Item>
        ))}
      </ListGroup>

      {/* Modal to display document */}
      <Modal
        show={!!selectedDoc}
        onHide={() => setSelectedDoc(null)}
        size="lg"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>{selectedDoc?.name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedDoc?.type === "application/pdf" ? (
            <iframe
              src={selectedDoc.url}
              title={selectedDoc.name}
              width="100%"
              height="600px"
            ></iframe>
          ) : (
            <p>
              Preview not available for this file type. Please download to view.
            </p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setSelectedDoc(null)}>
            Close
          </Button>
          <Button
            variant="success"
            href={selectedDoc?.url}
            download={selectedDoc?.name}
          >
            Download
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default UploadDocuments;
