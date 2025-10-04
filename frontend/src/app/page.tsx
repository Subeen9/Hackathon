"use client";
import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Container, Typography, Button, Paper } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
    },
  });

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    alert("Uploaded: " + data.filename);
  };

  return (
    <Container maxWidth="md" sx={{ textAlign: "center", mt: 6 }}>
      <Typography variant="h4" gutterBottom>
        Upload Your Manuscript
      </Typography>
      <Typography variant="body1" sx={{ mb: 4, color: "text.secondary" }}>
        Preserve ancient texts by uploading PDFs or images. We’ll digitize and translate them for modern readers.
      </Typography>

      <Paper
  {...getRootProps()}
  sx={{
    border: "2px dashed",
    borderColor: isDragActive ? "primary.main" : "grey.700",
    backgroundColor: "background.paper",   // Dark background
    color: "text.secondary",               // Makes placeholder visible
    borderRadius: "12px",
    p: 6,
    mb: 3,
    cursor: "pointer",
    textAlign: "center",
    "&:hover": {
      borderColor: "primary.main",
      backgroundColor: "grey.900",
    },
  }}
  elevation={3}
>
  <input {...getInputProps()} />
  <CloudUploadIcon sx={{ fontSize: 50, color: "primary.main", mb: 2 }} />
  {file ? (
    <Typography variant="subtitle1">{file.name}</Typography>
  ) : isDragActive ? (
    <Typography variant="subtitle1" color="primary">
      Drop the file here…
    </Typography>
  ) : (
    <Typography variant="subtitle1">
      Drag & drop a file here, or click to select
    </Typography>
  )}
</Paper>

      <Button
        variant="contained"
        color="primary"
        size="large"
        onClick={handleUpload}
        disabled={!file}
      >
        Upload & Process
      </Button>
    </Container>
  );
}
