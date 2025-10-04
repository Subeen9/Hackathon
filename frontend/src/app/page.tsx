"use client";
import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import {
  Container,
  Typography,
  Button,
  Paper,
  Box,
  LinearProgress,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

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

    try {
      setUploading(true);

      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();

      // Save the uploaded file URL for viewer
      localStorage.setItem("uploadedFileUrl", data.url);

      // Simulate delay so progress bar is visible
      setTimeout(() => {
        window.location.href = "/viewer";
      }, 1000);
    } catch (err) {
      console.error("Upload error:", err);
      setUploading(false);
    }
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
          backgroundColor: "background.paper",
          color: "text.secondary",
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

      {uploading ? (
        <Box display="flex" flexDirection="column" alignItems="center" mt={2}>
          <Typography variant="body2" sx={{ mb: 1 }}>
            Uploading your manuscript...
          </Typography>
          <LinearProgress sx={{ width: "100%" }} />
        </Box>
      ) : (
        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={handleUpload}
          disabled={!file}
        >
          Upload & Process
        </Button>
      )}
    </Container>
  );
}
